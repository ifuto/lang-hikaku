#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lang-hikaku ベンチマーク実行ハーネス

全項目 x 全言語のベンチマークを実行し、結果を JSON / CSV で保存する。

使い方:
  python3 harness/run.py                       # 全項目 x 全言語
  python3 harness/run.py --lang c,python,java  # 言語を絞る
  python3 harness/run.py --item sieve,matrix-mult
  python3 harness/run.py --repeat 3 --max-repeat 7 --min-sec 0.2

ルール:
  - 各項目は benchmarks/<item_id>/run.<ext> というファイル名で実装する
  - プログラムは「答え(チェックサム)」を1行標準出力に出す
  - 期待値は benchmarks/<item_id>/expected.txt か items.json の expected で指定
  - コンパイル時間は計測しない(実行のみ計測)
  - 各項目: 最低 repeat 回、最大 max-repeat 回実行し、中央値を採用
  - 1回の実行が min-sec 秒以上になったら繰り返しを打ち切る
"""
import argparse
import csv
import json
import os
import platform
import shutil
import signal
import statistics
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BENCH = os.path.join(ROOT, "benchmarks")
BUILD = os.path.join(ROOT, "build")
RESULTS = os.path.join(ROOT, "results")
HARNESS = os.path.join(ROOT, "harness")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def read_expected(item_dir, item):
    """期待値を expected.txt > items.json の順で探す。なければ None。"""
    exp_file = os.path.join(item_dir, "expected.txt")
    if os.path.exists(exp_file):
        with open(exp_file, encoding="utf-8") as f:
            return f.read().strip()
    exp = item.get("expected")
    return str(exp).strip() if exp is not None else None


def measure(cmd, timeout, cwd):
    """コマンドを実行して (経過秒, status, stdout, stderr) を返す。"""
    t0 = time.perf_counter()
    try:
        proc = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, cwd=cwd, start_new_session=True,
        )
    except FileNotFoundError:
        return None, "missing", "", "実行ファイルが見つからない: %s" % cmd[0]
    try:
        out, err = proc.communicate(timeout=timeout)
        elapsed = time.perf_counter() - t0
        status = "ok" if proc.returncode == 0 else "error"
        return elapsed, status, out.strip(), err[-1000:] if err else ""
    except subprocess.TimeoutExpired:
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except ProcessLookupError:
            pass
        out, err = proc.communicate()
        return None, "timeout", out.strip() if out else "", (err or "")[-500:]


def build_lang(lang, cfg, item_id, src, bindir):
    """コンパイルが必要な言語はビルドする。成功なら (bin_path or None), err"""
    if "build" not in cfg:
        return None, ""
    bin_path = os.path.join(bindir, "run")
    placeholders = {"src": src, "bin": bin_path, "bindir": bindir}
    if lang == "csharp":
        # .NET はプロジェクトを生成してビルドする
        proj = os.path.join(bindir, "App.csproj")
        rel = os.path.relpath(src, bindir)
        csproj = (
            '<Project Sdk="Microsoft.NET.Sdk">\n'
            "  <PropertyGroup>\n"
            "    <OutputType>Exe</OutputType>\n"
            "    <TargetFramework>net8.0</TargetFramework>\n"
            "    <ImplicitUsings>disable</ImplicitUsings>\n"
            "    <Nullable>disable</Nullable>\n"
            "    <Optimize>true</Optimize>\n"
            "    <AssemblyName>App</AssemblyName>\n"
            "    <InvariantGlobalization>true</InvariantGlobalization>\n"
            "  </PropertyGroup>\n"
            f'  <ItemGroup><Compile Include="{rel}" Link="Program.cs" /></ItemGroup>\n'
            "</Project>\n"
        )
        with open(proj, "w", encoding="utf-8") as f:
            f.write(csproj)
        placeholders["proj"] = proj
    elif lang == "typescript":
        # tsc の出力は bindir/run.js
        pass
    cmd = [p.format(**placeholders) for p in cfg["build"]]
    print("    build: %s" % " ".join(cmd), flush=True)
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=bindir)
    if r.returncode != 0:
        return None, r.stderr[-2000:]
    return bin_path, ""


def run_one(item_id, lang, cfg, src, expected, args):
    bindir = os.path.join(BUILD, lang, item_id)
    os.makedirs(bindir, exist_ok=True)

    bin_path, err = build_lang(lang, cfg, item_id, src, bindir)
    if err:
        return {"status": "build-error", "error": err}

    placeholders = {"bin": bin_path, "bindir": bindir, "src": src}
    cmd = [p.format(**placeholders) for p in cfg["run"]]

    times, outputs, last_err = [], [], ""
    for attempt in range(1, args.max_repeat + 1):
        elapsed, status, out, err = measure(cmd, args.timeout, bindir)
        last_err = err
        if status != "ok":
            return {"status": status, "error": err, "times": times}
        if expected is not None and out != expected:
            return {"status": "mismatch",
                    "expected": expected, "got": out[:200], "times": times}
        times.append(elapsed)
        outputs.append(out)
        # 十分長い実行ならこれ以上繰り返さない
        if attempt >= args.repeat and elapsed >= args.min_sec:
            break

    return {
        "status": "ok",
        "median": statistics.median(times),
        "min": min(times),
        "max": max(times),
        "times": times,
        "output": outputs[-1],
    }


def main():
    ap = argparse.ArgumentParser(description="lang-hikaku benchmark harness")
    ap.add_argument("--lang", help="対象言語(カンマ区切り)。既定=全言語")
    ap.add_argument("--item", help="対象項目(カンマ区切り)。既定=全項目")
    ap.add_argument("--repeat", type=int, default=3, help="最低繰り返し回数(既定3)")
    ap.add_argument("--max-repeat", type=int, default=7, help="最大繰り返し回数(既定7)")
    ap.add_argument("--min-sec", type=float, default=0.2, help="1回の実行がこの秒数以上なら繰り返し打ち切り")
    ap.add_argument("--timeout", type=int, default=600, help="1回あたりのタイムアウト秒(既定600)")
    ap.add_argument("--output", default=os.path.join(RESULTS, "results.json"))
    args = ap.parse_args()

    langs_cfg = load_json(os.path.join(HARNESS, "languages.json"))
    items = load_json(os.path.join(BENCH, "items.json"))["items"]

    selected_langs = [l for l in langs_cfg if not args.lang or l in args.lang.split(",")]
    selected_items = [it for it in items if not args.item or it["id"] in args.item.split(",")]
    if not selected_items:
        print("項目が見つかりません: %s" % args.item, file=sys.stderr)
        sys.exit(1)

    results = {}
    for it in selected_items:
        iid = it["id"]
        item_dir = os.path.join(BENCH, iid)
        expected = read_expected(item_dir, it)
        print("== 項目: %s (%s)" % (iid, it.get("name_ja", "")), flush=True)
        for lang in selected_langs:
            cfg = langs_cfg[lang]
            src = os.path.join(item_dir, "run.%s" % cfg["ext"])
            if not os.path.exists(src):
                continue
            print("   %-10s %s" % (lang, cfg["label"]), flush=True)
            r = run_one(iid, lang, cfg, src, expected, args)
            results.setdefault(iid, {})[lang] = r
            if r["status"] == "ok":
                print("      -> OK  中央値 %.4f s (回数=%d)" % (r["median"], len(r["times"])), flush=True)
            else:
                detail = r.get("error", "")[:200].replace("\n", " ")
                print("      -> %s %s" % (r["status"], detail), flush=True)

    os.makedirs(RESULTS, exist_ok=True)
    data = {
        "meta": {
            "generated_at": time.strftime("%Y-%m-%d %H:%M:%S %Z"),
            "machine": platform.platform(),
            "python": platform.python_version(),
            "repeat_min": args.repeat,
            "repeat_max": args.max_repeat,
            "timeout_sec": args.timeout,
        },
        "results": results,
    }
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # CSV も出力
    csv_path = os.path.join(RESULTS, "results.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["item", "lang", "status", "median_sec", "min_sec", "max_sec", "repeats"])
        for iid, langs in results.items():
            for lang, r in langs.items():
                w.writerow([iid, lang, r["status"],
                            "%.6f" % r["median"] if r.get("median") is not None else "",
                            "%.6f" % r["min"] if r.get("min") is not None else "",
                            "%.6f" % r["max"] if r.get("max") is not None else "",
                            len(r.get("times", []))])
    print("\n保存しました: %s / %s" % (args.output, csv_path))


if __name__ == "__main__":
    main()
