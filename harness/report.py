#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lang-hikaku レポート生成 (グラフ強化版)

results/results.json を読んで、以下を生成する:
  - results/ranking.md      総合・カテゴリ別ランキング (Markdown)
  - results/report.html     グラフ付きHTMLレポート (Chart.js使用)
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
    # logが0になるのを防ぐために小さい値を足す必要はない、relは>=1なので
    return math.exp(sum(math.log(v) for v in values) / len(values))


def build_tables(items, results_raw):
    """項目ごとに {lang: median} と相対倍率を計算。詳細も保持。"""
    item_tables = {}
    for it in items:
        iid = it["id"]
        if iid not in results_raw:
            continue
        langs = {}
        rel = {}
        details = {}
        # medianで最速を求める
        medians = {}
        for lang, r in results_raw[iid].items():
            if r.get("status") == "ok" and r.get("median") is not None:
                medians[lang] = r["median"]
                details[lang] = r
        if not medians:
            continue
        fastest = min(medians.values())
        for lang, med in medians.items():
            langs[lang] = med
            rel[lang] = med / fastest if fastest > 0 else 1.0
        item_tables[iid] = {
            "item": it,
            "langs": langs,
            "rel": rel,
            "fastest": fastest,
            "details": details,  # full result with times, min, max
        }
    return item_tables


def rank_langs(item_tables, langs_cfg, lang_filter=None):
    """言語ごとの総合スコア(幾何平均の相対倍率)と統計を計算。"""
    stats = {}
    for lang in langs_cfg:
        if lang_filter and lang not in lang_filter:
            continue
        stats[lang] = {"n_ok": 0, "n_items": len(item_tables), "wins": 0}

    # 最速回数と完了数
    for tbl in item_tables.values():
        best = min(tbl["rel"].values()) if tbl["rel"] else None
        if best is None:
            continue
        for lang, rel in tbl["rel"].items():
            if lang in stats:
                stats[lang]["n_ok"] += 1
            if rel == best:
                if lang in stats:
                    stats[lang]["wins"] += 1

    # 幾何平均スコアと算術平均、中央値なども計算
    for lang in list(stats.keys()):
        rels = []
        for tbl in item_tables.values():
            if lang in tbl["rel"]:
                rels.append(tbl["rel"][lang])
        g = geomean(rels) if rels else None
        stats[lang]["score"] = g
        stats[lang]["completed"] = len(rels)
        if rels:
            stats[lang]["arith_mean"] = sum(rels) / len(rels)
            stats[lang]["median_rel"] = statistics.median(rels)
            stats[lang]["max_rel"] = max(rels)
            stats[lang]["min_rel"] = min(rels)
        else:
            stats[lang]["arith_mean"] = None

    ordered = sorted(stats.items(), key=lambda kv: (kv[1]["score"] is None, kv[1]["score"] or 1e18))
    return ordered


def fmt_sec(t):
    if t is None:
        return "-"
    if t < 0.01:
        return "%.4f" % t
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
    results_raw = data["results"]
    items = load_json(os.path.join(ROOT, "benchmarks", "items.json"))["items"]
    langs_cfg = load_json(os.path.join(HARNESS, "languages.json"))

    used_langs = sorted({l for langs in results_raw.values() for l in langs})
    used_langs = [l for l in used_langs if l in langs_cfg]

    item_tables = build_tables(items, results_raw)
    ranking = rank_langs(item_tables, langs_cfg, used_langs)

    # ---- CSV: times.csv ----
    os.makedirs(RESULTS, exist_ok=True)
    with open(os.path.join(RESULTS, "times.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["item", "category", "name_ja", "name_en"] + used_langs)
        for it in items:
            iid = it["id"]
            if iid not in item_tables:
                continue
            tbl = item_tables[iid]
            w.writerow([iid, it["category"], it["name_ja"], it["name_en"]] +
                       [fmt_sec(tbl["langs"].get(l)) for l in used_langs])

    # ---- ranking.md (詳細版) ----
    lines = ["# lang-hikaku ランキングレポート", "",
             f"生成日時: {data['meta'].get('generated_at', '?')}",
             f"マシン: {data['meta'].get('machine', '?')}",
             "", "## 総合ランキング（相対倍率の幾何平均、小さいほど速い・最速=1.00）", "",
             "| 順位 | 言語 | 総合スコア(幾何平均) | 算術平均 | 中央値 | 最大遅延 | 完了項目 | 最速回数 | 分類 |",
             "|---|---|---|---|---|---|---|---|---|"]
    for i, (lang, st) in enumerate(ranking, 1):
        score = "%.2f" % st["score"] if st["score"] is not None else "-"
        arith = "%.2f" % st.get("arith_mean", 0) if st.get("arith_mean") is not None else "-"
        med_rel = "%.2f" % st.get("median_rel", 0) if st.get("median_rel") is not None else "-"
        max_rel = "%.2f" % st.get("max_rel", 0) if st.get("max_rel") is not None else "-"
        lines.append(f"| {i} | {langs_cfg[lang]['label']} | {score} | {arith} | {med_rel} | {max_rel} | {st['completed']}/{st['n_items']} | {st.get('wins', 0)} | {langs_cfg[lang]['family']} |")
    lines += ["", "## なぜ最速回数が多くても総合1位にならないのか？", "",
              "このレポートの総合スコアは**幾何平均**で計算されています。最速回数(金メダル数)とは違う指標です。",
              "", "> **例**: 言語Aが10項目中8項目で1.1倍の僅差で最速、残り2項目で10倍遅いとします。",
              "> 言語Bが2項目で最速だが、残り8項目は2倍遅いとします。",
              "> - 金メダル: A 8個、B 2個 → Aが優勢に見える",
              "> - 幾何平均: A = (1.1^8 * 10^2)^(1/10) ≈ 2.1倍、B = (1^2 * 2^8)^(1/10) ≈ 1.74倍 → Bが総合で速い",
              "> つまり**極端に遅い項目があると幾何平均は大きく悪化**します。算術平均だとさらに悪化しますが、幾何平均は外れ値に強いのでまだマシです。",
              "", "自由研究の考察では「金メダル数」と「総合スコア」の両方を見て、",
              "- 金メダル数が多いが総合が悪い → 特定分野では最速だが苦手分野がある",
              "- 総合が良いが金メダルが少ない → どの項目でも安定して速い",
              "という風に語れると考察が深くなります。",
              "", "詳細は `docs/03-methodology.md` を参照。", ""]
    lines += ["## 項目ごとの最速言語", "", "| 項目 | 最速 | 秒数 | 相対1位との差 |", "|---|---|---|---|"]
    for iid, tbl in item_tables.items():
        best = min(tbl["langs"], key=lambda l: tbl["langs"][l])
        second_best = sorted(tbl["langs"].values())[1] if len(tbl["langs"]) > 1 else tbl["fastest"]
        diff = second_best / tbl["fastest"] if tbl["fastest"] > 0 else 1.0
        lines.append(f"| {iid} ({tbl['item']['name_ja']}) | {langs_cfg[best]['label']} | {fmt_sec(tbl['langs'][best])} | {diff:.2f}倍 |")
    # カテゴリ別ランキングもmdに
    cats = {}
    for iid, tbl in item_tables.items():
        cats.setdefault(tbl["item"]["category"], []).append(tbl)
    cat_names = {
        "integer": "A. 整数演算", "float": "B. 浮動小数点", "string": "C. 文字列処理",
        "data": "D. データ構造", "algorithm": "E. 再帰・アルゴリズム",
        "bigint": "F. 多倍長整数", "io": "G. ファイル・I/O",
        "concurrency": "H. 並行処理", "misc": "I. その他",
    }
    for cat_key, cat_label in cat_names.items():
        if cat_key not in cats:
            continue
        lines += ["", f"## カテゴリ別: {cat_label}", "", "| 順位 | 言語 | スコア | 完了 | 最速 |", "|---|---|---|---|---|"]
        r2 = rank_langs({t["item"]["id"]: t for t in cats[cat_key]}, langs_cfg, used_langs)
        for i, (lang, st) in enumerate(r2, 1):
            score = "%.2f" % st["score"] if st["score"] is not None else "-"
            lines.append(f"| {i} | {langs_cfg[lang]['label']} | {score} | {st['completed']} | {st.get('wins', 0)} |")

    with open(os.path.join(RESULTS, "ranking.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    # ---- report.html (グラフ強化版) ----
    def esc(s):
        return html.escape(str(s))

    # データ準備 for Chart.js
    lang_labels = [langs_cfg[lang]["label"] for lang, _ in ranking]
    lang_keys = [lang for lang, _ in ranking]
    scores = [round(st["score"], 3) if st["score"] is not None else None for _, st in ranking]
    wins = [st.get("wins", 0) for _, st in ranking]
    # カテゴリ別データも
    cat_chart_data = {}
    for cat_key in cat_names:
        if cat_key not in cats:
            continue
        r2 = rank_langs({t["item"]["id"]: t for t in cats[cat_key]}, langs_cfg, used_langs)
        cat_chart_data[cat_key] = {
            "labels": [langs_cfg[lang]["label"] for lang, _ in r2],
            "scores": [round(st["score"], 3) if st["score"] else None for _, st in r2],
        }

    # HTML生成
    h = []
    h.append("<!DOCTYPE html><html lang='ja'><head><meta charset='utf-8'>")
    h.append("<meta name='viewport' content='width=device-width,initial-scale=1'>")
    h.append("<title>lang-hikaku ベンチマークレポート</title>")
    h.append("<script src='https://cdn.jsdelivr.net/npm/chart.js'></script>")
    h.append("<style>")
    h.append("body{font-family:'Segoe UI',Meiryo,sans-serif;margin:24px;color:#222;max-width:1200px}")
    h.append("table{border-collapse:collapse;margin:12px 0;font-size:14px;width:100%}")
    h.append("th,td{border:1px solid #ccc;padding:6px 10px;text-align:right}")
    h.append("th{background:#f0f4f8;position:sticky;top:0} td.l,th.l{text-align:left}")
    h.append(".bar{background:#4a90d9;height:14px;display:inline-block;border-radius:2px}")
    h.append(".rank1{background:#ffd700}.rank2{background:#c0c0c0}.rank3{background:#cd7f32}")
    h.append("h2{margin-top:40px;border-bottom:2px solid #4a90d9;padding-bottom:4px}")
    h.append("h3{margin-top:24px}")
    h.append("summary{cursor:pointer;font-weight:bold;padding:8px;background:#f7f7f7;border:1px solid #ddd;border-radius:4px}")
    h.append(".grid{display:grid;grid-template-columns:1fr 1fr;gap:24px}")
    h.append("@media(max-width:900px){.grid{grid-template-columns:1fr}}")
    h.append(".card{border:1px solid #ddd;border-radius:8px;padding:16px;background:#fff;box-shadow:0 2px 4px rgba(0,0,0,0.05)}")
    h.append(".explain{background:#fff8e1;border-left:4px solid #ffb300;padding:12px 16px;margin:16px 0}")
    h.append("canvas{max-width:100%}")
    h.append("</style></head><body>")
    h.append("<h1>lang-hikaku ベンチマークレポート</h1>")
    h.append(f"<p>生成日時: {esc(data['meta'].get('generated_at', '?'))}<br>マシン: {esc(data['meta'].get('machine', '?'))}<br>項目数: {len(item_tables)} / 言語数: {len(used_langs)}</p>")

    # 概要グラフ
    h.append("<div class='grid'>")
    h.append("<div class='card'><h3>総合スコア (幾何平均, 小さいほど速い)</h3><canvas id='chartOverall'></canvas></div>")
    h.append("<div class='card'><h3>最速回数 (金メダル数)</h3><canvas id='chartWins'></canvas></div>")
    h.append("</div>")

    # 説明
    h.append("<div class='explain'>")
    h.append("<strong>なぜ最速回数が多くても総合1位にならないのか？</strong><br>")
    h.append("総合スコアは全項目の相対倍率の<strong>幾何平均</strong>。1項目でも極端に遅いとスコアが大きく悪化します。<br>")
    h.append("例: Rustが8項目で1.05倍の僅差で最速だが、残り2項目で文字列処理が5倍遅いと、幾何平均は (1.05^8 * 5^2)^(1/10) ≈ 1.8倍。<br>")
    h.append("一方Cが全項目2倍以内に収まれば総合は2.0倍を切らず、Cが1位になります。金メダル数と総合スコアの違いは自由研究の考察ポイントです。")
    h.append("</div>")

    # 総合ランキング表
    h.append("<h2>総合ランキング</h2>")
    h.append("<table><tr><th class='l'>順位</th><th class='l'>言語</th><th>総合スコア</th><th>算術平均</th><th>中央値</th><th>最大遅延</th><th>完了</th><th>最速回数</th><th class='l'>分類</th></tr>")
    for i, (lang, st) in enumerate(ranking, 1):
        cls = f"rank{i}" if i <= 3 else ""
        score = f"{st['score']:.2f}" if st["score"] is not None else "-"
        arith = f"{st.get('arith_mean', 0):.2f}" if st.get("arith_mean") is not None else "-"
        med_rel = f"{st.get('median_rel', 0):.2f}" if st.get("median_rel") is not None else "-"
        max_rel = f"{st.get('max_rel', 0):.2f}" if st.get("max_rel") is not None else "-"
        h.append(f"<tr><td class='{cls}'>{i}</td><td class='l'>{esc(langs_cfg[lang]['label'])}</td><td>{score}</td><td>{arith}</td><td>{med_rel}</td><td>{max_rel}</td><td>{st['completed']}/{st['n_items']}</td><td>{st.get('wins', 0)}</td><td class='l'>{esc(langs_cfg[lang]['family'])}</td></tr>")
    h.append("</table>")

    # カテゴリ別
    h.append("<h2>カテゴリ別ランキング & グラフ</h2>")
    for cat_key, cat_label in cat_names.items():
        if cat_key not in cats:
            continue
        h.append(f"<div class='card'><h3>{esc(cat_label)}</h3><canvas id='chartCat_{cat_key}'></canvas>")
        r2 = rank_langs({t["item"]["id"]: t for t in cats[cat_key]}, langs_cfg, used_langs)
        h.append("<table><tr><th class='l'>順位</th><th class='l'>言語</th><th>スコア</th><th>完了</th><th>最速</th></tr>")
        for i, (lang, st) in enumerate(r2, 1):
            score = f"{st['score']:.2f}" if st["score"] is not None else "-"
            h.append(f"<tr><td>{i}</td><td class='l'>{esc(langs_cfg[lang]['label'])}</td><td>{score}</td><td>{st['completed']}</td><td>{st.get('wins', 0)}</td></tr>")
        h.append("</table></div>")

    # 項目ごとの詳細 (グラフ付き)
    h.append("<h2>項目ごとの詳細 (クリックで開く)</h2>")
    h.append("<p>各項目の相対倍率バーと、中央値・最小・最大・標準偏差を表示。バーは最速=100%として相対的に短く表示。</p>")
    for iid, tbl in item_tables.items():
        it = tbl["item"]
        best_lang = min(tbl["langs"], key=lambda l: tbl["langs"][l])
        h.append(f"<details class='card'><summary>{esc(iid)} — {esc(it['name_ja'])}（{esc(it['category'])} / 最速 {esc(langs_cfg[best_lang]['label'])}: {fmt_sec(tbl['fastest'])} 秒）</summary>")
        h.append(f"<p><b>アルゴリズム:</b> {esc(it['algorithm'])}<br><b>規模:</b> {esc(it['workload'])}<br><b>測ってるもの:</b> {esc(it['measures'])}</p>")
        h.append(f"<canvas id='chart_{esc(iid)}' style='max-height:300px'></canvas>")
        h.append("<table><tr><th class='l'>言語</th><th>中央値(秒)</th><th>最小</th><th>最大</th><th>実行回数</th><th>相対倍率</th><th style='text-align:left'>バー</th></tr>")
        # ソートは速い順
        for lang in sorted(tbl["langs"], key=lambda l: tbl["langs"][l]):
            det = tbl["details"].get(lang, {})
            med = tbl["langs"][lang]
            rel = tbl["rel"][lang]
            min_t = det.get("min", med)
            max_t = det.get("max", med)
            reps = len(det.get("times", []))
            # バー幅: 1/rel に比例 (最速が300px)
            width = max(2, int(300 / rel)) if rel >= 1 else 300
            h.append(f"<tr><td class='l'>{esc(langs_cfg[lang]['label'])}</td><td>{fmt_sec(med)}</td><td>{fmt_sec(min_t)}</td><td>{fmt_sec(max_t)}</td><td>{reps}</td><td>{rel:.2f}</td><td style='text-align:left'><span class='bar' style='width:{width}px'></span></td></tr>")
        h.append("</table>")
        # 失敗した言語も表示
        failed = []
        for lang, r in results_raw.get(iid, {}).items():
            if r.get("status") != "ok":
                failed.append(f"{langs_cfg.get(lang, {}).get('label', lang)}: {r.get('status')} {esc(str(r.get('error',''))[:200])}")
        if failed:
            h.append("<p><b>失敗・タイムアウト:</b><br>" + "<br>".join(failed) + "</p>")
        h.append("</details>")

    # Chart.js スクリプト生成
    h.append("<script>")
    # 全体スコア
    h.append(f"""
const overallLabels = {json.dumps(lang_labels, ensure_ascii=False)};
const overallScores = {json.dumps(scores)};
const overallWins = {json.dumps(wins)};

new Chart(document.getElementById('chartOverall'), {{
  type: 'bar',
  data: {{
    labels: overallLabels,
    datasets: [{{
      label: '総合スコア (低いほど速い)',
      data: overallScores,
      backgroundColor: 'rgba(74,144,217,0.7)',
      borderColor: 'rgba(74,144,217,1)',
      borderWidth: 1
    }}]
  }},
  options: {{
    indexAxis: 'y',
    responsive: true,
    plugins: {{ legend: {{display:false}} }},
    scales: {{ x: {{ beginAtZero:true, title:{{display:true,text:'幾何平均 相対倍率'}} }} }}
  }}
}});

new Chart(document.getElementById('chartWins'), {{
  type: 'bar',
  data: {{
    labels: overallLabels,
    datasets: [{{
      label: '最速回数',
      data: overallWins,
      backgroundColor: 'rgba(255,179,0,0.7)',
      borderColor: 'rgba(255,179,0,1)',
      borderWidth: 1
    }}]
  }},
  options: {{
    indexAxis: 'y',
    responsive: true,
    scales: {{ x: {{ beginAtZero:true, ticks:{{stepSize:1}} }} }}
  }}
}});
""")
    # カテゴリ別チャート
    for cat_key, ch in cat_chart_data.items():
        h.append(f"""
new Chart(document.getElementById('chartCat_{cat_key}'), {{
  type: 'bar',
  data: {{
    labels: {json.dumps(ch['labels'], ensure_ascii=False)},
    datasets: [{{
      label: '{cat_names[cat_key]} スコア',
      data: {json.dumps(ch['scores'])},
      backgroundColor: 'rgba(76,175,80,0.6)',
    }}]
  }},
  options: {{
    indexAxis: 'y',
    responsive: true,
    scales: {{ x: {{ beginAtZero:true }} }}
  }}
}});
""")
    # 項目別チャート
    for iid, tbl in item_tables.items():
        sorted_langs = sorted(tbl["langs"], key=lambda l: tbl["langs"][l])
        labels = [langs_cfg[l]["label"] for l in sorted_langs]
        data_vals = [round(tbl["rel"][l], 3) for l in sorted_langs]
        # Chart.js用にエスケープ
        h.append(f"""
new Chart(document.getElementById('chart_{iid}'), {{
  type: 'bar',
  data: {{
    labels: {json.dumps(labels, ensure_ascii=False)},
    datasets: [{{
      label: '{iid} 相対倍率',
      data: {json.dumps(data_vals)},
      backgroundColor: 'rgba(33,150,243,0.6)',
    }}]
  }},
  options: {{
    indexAxis: 'y',
    responsive: true,
    plugins: {{ legend: {{display:false}} }},
    scales: {{ x: {{ beginAtZero:true }} }}
  }}
}});
""")

    h.append("</script>")
    h.append("</body></html>")

    with open(os.path.join(RESULTS, "report.html"), "w", encoding="utf-8") as f:
        f.write("\n".join(h))

    print("生成しました:")
    print(f"  {os.path.join(RESULTS, 'ranking.md')}")
    print(f"  {os.path.join(RESULTS, 'report.html')}")
    print(f"  {os.path.join(RESULTS, 'times.csv')}")


if __name__ == "__main__":
    main()
