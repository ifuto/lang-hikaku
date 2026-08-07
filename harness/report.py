#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lang-hikaku レポート生成

results/results.json を読んで、以下を生成する:
  - results/ranking.md      総合・カテゴリ別ランキング (Markdown)
  - results/report.html     並べ替え可能なHTMLレポート (依存ライブラリなし)
  - results/times.csv       項目 x 言語の中央値一覧

使い方: python3 harness/report.py [--results results/results.json]
"""
import argparse
import csv
import html
import json
import math
import os
import statistics

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RESULTS = os.path.join(ROOT, "results")
HARNESS = os.path.join(ROOT, "harness")


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def geomean(values):
    if not values:
        return None
    return math.exp(sum(math.log(v) for v in values) / len(values))


def build_tables(items, results):
    """項目ごとに {lang: median} と相対倍率を計算。"""
    item_tables = {}
    for it in items:
        iid = it["id"]
        if iid not in results:
            continue
        langs = {}
        for lang, r in results[iid].items():
            if r.get("status") == "ok" and r.get("median") is not None:
                langs[lang] = r["median"]
        if not langs:
            continue
        fastest = min(langs.values())
        rel = {lang: t / fastest for lang, t in langs.items()}
        item_tables[iid] = {"item": it, "langs": langs, "rel": rel, "fastest": fastest}
    return item_tables


def rank_langs(item_tables, langs_cfg, lang_filter=None):
    """言語ごとの総合スコア(幾何平均の相対倍率)と統計を計算。"""
    stats = {}
    for lang in langs_cfg:
        if lang_filter and lang not in lang_filter:
            continue
        rels, wins, n_ok = [], 0, 0
        for tbl in item_tables.values():
            if lang in tbl["rel"]:
                rels.append(tbl["rel"][lang])
                n_ok += 1
                if tbl["rel"][lang] == 1.0 and len(tbl["rel"]) > 1:
                    # 最速(同着含む: 1.0 は最速のみ)
                    pass
        stats[lang] = {"n_ok": n_ok, "n_items": len(item_tables)}
    # 最速回数
    for tbl in item_tables.values():
        best = min(tbl["rel"].values())
        for lang, rel in tbl["rel"].items():
            if rel == best:
                stats[lang]["wins"] = stats[lang].get("wins", 0) + 1
    # 幾何平均スコア
    for lang in list(stats):
        rels = []
        for tbl in item_tables.values():
            if lang in tbl["rel"]:
                rels.append(tbl["rel"][lang])
        g = geomean(rels) if rels else None
        stats[lang]["score"] = g
        stats[lang]["completed"] = len(rels)
    ordered = sorted(stats.items(), key=lambda kv: (kv[1]["score"] is None, kv[1]["score"] or 1e18))
    return ordered


def fmt_sec(t):
    if t is None:
        return "-"
    if t < 10:
        return "%.3f" % t
    if t < 100:
        return "%.2f" % t
    return "%.1f" % t


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--results", default=os.path.join(RESULTS, "results.json"))
    args = ap.parse_args()

    data = load_json(args.results)
    results = data["results"]
    items = load_json(os.path.join(ROOT, "benchmarks", "items.json"))["items"]
    langs_cfg = load_json(os.path.join(HARNESS, "languages.json"))

    used_langs = sorted({l for langs in results.values() for l in langs})
    used_langs = [l for l in used_langs if l in langs_cfg]

    item_tables = build_tables(items, results)
    ranking = rank_langs(item_tables, langs_cfg, used_langs)

    # ---- CSV: times.csv ----
    with open(os.path.join(RESULTS, "times.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["item", "category", "name_ja"] + used_langs)
        for it in items:
            iid = it["id"]
            if iid not in item_tables:
                continue
            tbl = item_tables[iid]
            w.writerow([iid, it["category"], it["name_ja"]] +
                       [fmt_sec(tbl["langs"].get(l)) for l in used_langs])

    # ---- ranking.md ----
    lines = ["# lang-hikaku ランキングレポート", "",
             "生成日時: %s" % data["meta"].get("generated_at", "?"), "",
             "## 総合ランキング（相対倍率の幾何平均、小さいほど速い・最速=1.00）", "",
             "| 順位 | 言語 | 総合スコア | 完了項目 | 最速回数 | 分類 |",
             "|---|---|---|---|---|---|"]
    for i, (lang, st) in enumerate(ranking, 1):
        score = "%.2f" % st["score"] if st["score"] is not None else "-"
        lines.append("| %d | %s | %s | %d/%d | %d | %s |" % (
            i, langs_cfg[lang]["label"], score, st["completed"],
            st["n_items"], st.get("wins", 0), langs_cfg[lang]["family"]))
    lines += ["", "## 項目ごとの最速言語", "", "| 項目 | 最速 | 秒数 |", "|---|---|---|"]
    for iid, tbl in item_tables.items():
        best = min(tbl["langs"], key=lambda l: tbl["langs"][l])
        lines.append("| %s (%s) | %s | %s |" % (iid, tbl["item"]["name_ja"],
                                                langs_cfg[best]["label"],
                                                fmt_sec(tbl["langs"][best])))
    with open(os.path.join(RESULTS, "ranking.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # ---- report.html ----
    def esc(s):
        return html.escape(str(s))

    h = ["<!DOCTYPE html><html lang='ja'><head><meta charset='utf-8'>",
         "<title>lang-hikaku ベンチマークレポート</title>",
         "<style>",
         "body{font-family:'Segoe UI',Meiryo,sans-serif;margin:24px;color:#222}",
         "table{border-collapse:collapse;margin:12px 0;font-size:14px}",
         "th,td{border:1px solid #ccc;padding:4px 10px;text-align:right}",
         "th{background:#f0f4f8} td.l,th.l{text-align:left}",
         ".bar{background:#4a90d9;height:14px;display:inline-block;border-radius:2px}",
         ".rank1{background:#ffd700}.rank2{background:#c0c0c0}.rank3{background:#cd7f32}",
         "h2{margin-top:36px;border-bottom:2px solid #4a90d9;padding-bottom:4px}",
         "summary{cursor:pointer;font-weight:bold}",
         "</style></head><body>",
         "<h1>lang-hikaku ベンチマークレポート</h1>",
         "<p>生成日時: %s<br>マシン: %s</p>" % (esc(data["meta"].get("generated_at", "?")),
                                              esc(data["meta"].get("machine", "?")))]

    # 総合ランキング表
    h.append("<h2>総合ランキング（相対倍率の幾何平均・小さいほど速い）</h2>")
    h.append("<table><tr class='l'><th class='l'>順位</th><th class='l'>言語</th>"
             "<th>総合スコア</th><th>完了項目</th><th>最速回数</th><th class='l'>分類</th></tr>")
    for i, (lang, st) in enumerate(ranking, 1):
        cls = "rank%d" % i if i <= 3 else ""
        score = "%.2f" % st["score"] if st["score"] is not None else "-"
        h.append("<tr><td class='%s'>%d</td><td class='l'>%s</td><td>%s</td>"
                 "<td>%d/%d</td><td>%d</td><td class='l'>%s</td></tr>" % (
                     cls, i, esc(langs_cfg[lang]["label"]), score,
                     st["completed"], st["n_items"], st.get("wins", 0),
                     esc(langs_cfg[lang]["family"])))
    h.append("</table>")

    # カテゴリ別
    cats = {}
    for iid, tbl in item_tables.items():
        cats.setdefault(tbl["item"]["category"], []).append(tbl)
    cat_names = {
        "integer": "A. 整数演算", "float": "B. 浮動小数点", "string": "C. 文字列処理",
        "data": "D. データ構造", "algorithm": "E. 再帰・アルゴリズム",
        "bigint": "F. 多倍長整数", "io": "G. ファイル・I/O",
        "concurrency": "H. 並行処理", "misc": "I. その他",
    }
    for cat in cat_names:
        if cat not in cats:
            continue
        h.append("<h2>カテゴリ別: %s</h2>" % esc(cat_names[cat]))
        r2 = rank_langs({t["item"]["id"]: t for t in cats[cat]}, langs_cfg, used_langs)
        h.append("<table><tr><th class='l'>順位</th><th class='l'>言語</th>"
                 "<th>スコア</th><th>完了</th><th>最速回数</th></tr>")
        for i, (lang, st) in enumerate(r2, 1):
            score = "%.2f" % st["score"] if st["score"] is not None else "-"
            h.append("<tr><td>%d</td><td class='l'>%s</td><td>%s</td><td>%d</td><td>%d</td></tr>" % (
                i, esc(langs_cfg[lang]["label"]), score, st["completed"], st.get("wins", 0)))
        h.append("</table>")

    # 項目ごとの詳細
    h.append("<h2>項目ごとの詳細</h2>")
    for iid, tbl in item_tables.items():
        it = tbl["item"]
        h.append("<details><summary>%s — %s（最速 %s: %s 秒）</summary>" % (
            esc(iid), esc(it["name_ja"]),
            esc(langs_cfg[min(tbl["langs"], key=lambda l: tbl["langs"][l])]["label"]),
            fmt_sec(tbl["fastest"])))
        h.append("<table><tr><th class='l'>言語</th><th>中央値(秒)</th>"
                 "<th>相対倍率</th><th style='text-align:left'>バー</th></tr>")
        max_rel = max(tbl["rel"].values())
        for lang in sorted(tbl["langs"], key=lambda l: tbl["langs"][l]):
            med, rel = tbl["langs"][lang], tbl["rel"][lang]
            width = max(1, int(300 / max(rel, 1e-9))) if max_rel > 1 else 300
            h.append("<tr><td class='l'>%s</td><td>%s</td><td>%.2f</td>"
                     "<td style='text-align:left'><span class='bar' style='width:%dpx'></span></td></tr>" % (
                         esc(langs_cfg[lang]["label"]), fmt_sec(med), rel, width))
        h.append("</table></details>")

    h.append("</body></html>")
    with open(os.path.join(RESULTS, "report.html"), "w", encoding="utf-8") as f:
        f.write("\n".join(h))

    print("生成しました:")
    print("  %s" % os.path.join(RESULTS, "ranking.md"))
    print("  %s" % os.path.join(RESULTS, "report.html"))
    print("  %s" % os.path.join(RESULTS, "times.csv"))


if __name__ == "__main__":
    main()
