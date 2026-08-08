# 計測方法論（公平に比べるためのルール）

速度比較が「言語のせい」ではなく「コードの書き方のせい」にならないよう、以下のルールで統一する。

## 1. フェアネスの基本ルール

1. **同じアルゴリズム・同じ規模**: 全言語で同じ手順・同じ入力サイズで計算する（項目定義書 `02-benchmark-items.md` に従う）。
2. **出力の自動検証**: 全プログラムは答え（チェックサム）を1行標準出力に出す。ハーネスが期待値と突き合わせ、不一致なら「結果不一致」として記録する。**答えが間違っているプログラムは速度を測っても無意味**なので、その回は無効にする。
3. **コンパイル時間は計測しない**: コンパイルは事前に1回だけ行い、実行時間のみを測る（C/Rust/Go/Java等）。「コンパイル+実行」の合計が知りたければ別途測れるよう、コンパイル時間もログに残す。
4. **コンパイル最適化**: C/C++ は `-O2`、Rust は `-O`（opt-level=3）、Go はデフォルト、Swift は `-O`、Java/.NET はリリースビルドで統一（開発者ツールの標準的な設定）。
5. **同じマシン・同じタイミング**: 全言語を同じCIランナー（同じ仮想マシン仕様）で実行し、同時実行はしない（他のジョブの負荷で結果が揺れるため直列実行）。
6. **最適化で計算が消えないように**: 空ループや未使用の計算結果はコンパイラに消されるため、必ず結果を合計に足して出力する。
7. **データ構造項目は標準ライブラリを使う**: ハッシュマップ・ソート・キューなどは「言語標準のライブラリ」を使う（独自実装するとライブラリの良し悪しが測れないため）。これは「言語の標準機能の実力」を比べるという意味で意図的な設計であり、考察の材料になる。

## 2. タイマーと統計

- **測定する量**: ウォールタイム（実際に掛かった時間）を主指標にする。「人間が体感する速さ」はこれ。CPU時間・最大メモリ使用量も可能なら記録する。
- **1回だけの実行は信用しない**: 各項目 最低3回、最大7回実行し、**中央値（メディアン）**を採用する（外れ値に強い）。Benchmarks Gameでも最初の1回をウォームアップとして捨て、11回実行して中央値や信頼区間を取っている [1](https://grokipedia.com/page/The_Computer_Language_Benchmarks_Game)。
- **タイムアウト**: 1回あたり最大600秒。超えたら「timeout」として記録（遅すぎる言語のせいで全体が止まらないように）。
- **起動時間の扱い**: 実行プログラムの起動から終了までを測る＝**起動時間込み**（実際に使ったときの体感）。JIT言語（Java/Julia/Node）は「起動が遅いが実行中に速くなる」性質があるため、この差が結果に出る。追加実験として「ウォームアップ後だけを測る」方法も用意すると考察が深まる。

## 3. 順位のつけ方（レーティング方法の比較）

### 3.1 項目ごと

最速言語の時間を1.00として、他言語は「何倍遅いか」の相対倍率で表す（例: Python 42.3倍）。これはBenchmarks Gameでも採用されている正規化方法 [1](https://grokipedia.com/page/The_Computer_Language_Benchmarks_Game)。

### 3.2 総合順位 — 複数の指標を併用する

**単一の数字で全項目を要約する方法には正解がない**。代表的な方法を比較する:

| 方法 | 計算式 | 長所 | 短所 | 使われてる場所 |
|---|---|---|---|---|
| **幾何平均** (Geomean) | (Π rel_i)^(1/n) | 外れ値に強い。正規化された比の平均に適している。単位の違いに影響されない | 「速さ」の物理的意味が薄い。極端に遅い項目があると全体が悪化 | Benchmarks Gameのデフォルト [1](https://grokipedia.com/page/The_Computer_Language_Benchmarks_Game) [4](https://benchmarksgame-team.pages.debian.net/benchmarksgame/box-plot-summary-charts.html)、SPEC |
| **算術平均** | Σ rel_i / n | 直感的。合計時間に近い | 極端に遅い1項目に引っ張られる | 初心者向け |
| **調和平均 (Harmonic Mean) - Equal Work** | n / Σ (1/rel_i) | レート（速さ）の平均に適切。SPECの代替として提案されている [5](https://users.elis.ugent.be/~leeckhou/papers/CAL-2024-geomean.pdf) | 遅い項目の影響をさらに強く受ける | 最新論文で推奨 (EWS, ETS) [5](https://users.elis.ugent.be/~leeckhou/papers/CAL-2024-geomean.pdf) |
| **中央値 (Median)** | 中央値 | 外れ値に最も強い | 多くの情報を捨てる | 統計的に堅牢 |
| **加重幾何平均** | Π rel_i^w_i | カテゴリごとの項目数の偏りを補正できる。カテゴリ数の多い整数演算が支配的になるのを防げる [2](https://github.com/krausest/js-framework-benchmark/wiki/Computation-of-the-weighted-geometric-mean) | 重みの決め方が主観的 | js-framework-benchmark [2](https://github.com/krausest/js-framework-benchmark/wiki/Computation-of-the-weighted-geometric-mean) |
| **合計時間 (Total Time)** | Σ time_i | 最も物理的意味が明確。実際に全部実行したら何秒か | 実行時間の長い項目が支配的 | シンプルな比較 |
| **最速回数 (Gold Medal)** | 1位になった回数 | 分かりやすい。特定分野での強さが分かる | 安定性が評価されない。僅差で2位でも0カウント | オリンピック方式 |
| **ELOレーティング** | チェス式。項目ごとにペアワイズ勝敗でレートを更新 | 全項目での直接対決を反映。引き分けも考慮できる | 計算が複雑。順序に依存する可能性 | LLMベンチマークなどで使われる |
| **Paretoランキング** | エネルギーと時間などの多目的で優越関係を見る [1](https://haslab.github.io/SAFER/scp21.pdf) | 速さだけでなくメモリやエネルギーも考慮できる | 1次元ランキングにならない | エネルギー効率研究 [1](https://haslab.github.io/SAFER/scp21.pdf) |

**このプロジェクトでは以下を併用して表示する (report.py):**
- **主指標: 幾何平均** (Benchmarks Game準拠 [1](https://grokipedia.com/page/The_Computer_Language_Benchmarks_Game) [4](https://benchmarksgame-team.pages.debian.net/benchmarksgame/box-plot-summary-charts.html))
- 副指標: 算術平均、調和平均(EWS)、中央値、最大遅延、合計時間、最速回数
- カテゴリ別にも幾何平均と最速回数を出す
- グラフで視覚的に比較 (Chart.js)

### 3.3 なぜ最速回数が多くても総合1位にならないのか？

> **例**: Rustが10項目中8項目で1.05倍の僅差で最速、残り2項目で文字列処理が5倍遅いとします。
> Cが2項目で最速だが、残り8項目は1.5倍以内に収まるとします。
> - 金メダル: Rust 8個、C 2個 → Rustが優勢に見える
> - 幾何平均: Rust = (1.05^8 * 5^2)^(1/10) ≈ 1.82倍、C = (1^2 * 1.5^8)^(1/10) ≈ 1.38倍 → Cが総合で速い

つまり**極端に遅い項目があると幾何平均は大きく悪化**します。調和平均だとさらにペナルティが大きくなります [5](https://users.elis.ugent.be/~leeckhou/papers/CAL-2024-geomean.pdf)。

自由研究の考察では「金メダル数」と「総合スコア」の両方を見て、
- 金メダル数が多いが総合が悪い → 特定分野では最速だが苦手分野がある
- 総合が良いが金メダルが少ない → どの項目でも安定して速い
という風に語れると考察が深くなります。

### 3.4 信頼性の確保

- Benchmarks Gameでは各項目11回以上実行し、最初の1回をウォームアップとして捨て、信頼区間を報告している [1](https://grokipedia.com/page/The_Computer_Language_Benchmarks_Game)。
- 本プロジェクトでは最低3回、最大7回実行し、中央値を採用。0.2秒未満の短い項目は繰り返して誤差を減らす。
- ボックスプロットの考え方 [4](https://benchmarksgame-team.pages.debian.net/benchmarksgame/box-plot-summary-charts.html) を参考に、最小・最大・実行回数も記録する。

## 4. 落とし穴と対策（自由研究の考察材料にもなる）

| 落とし穴 | 対策 |
|---|---|
| コンパイラが計算を消す | 結果を出力して使う（検証つき） |
| GC（ごみ集め）の影響 | 同じ操作を繰り返し、中央値で評価。GC言語と手動メモリ言語の差は「考察」の種 |
| JITのウォームアップ | 繰り返し実行で安定化。初回だけ遅い現象も記録 |
| マシン負荷・温度 | CIの同じランナーで直列実行。結果のばらつきは繰り返しで吸収 |
| ライブラリ差 | 「標準機能のみ」で統一（PythonのNumPy等は使わない）。使う場合は別実験として明記 |
| 出力が大きい項目 | ファイルI/O・FASTA生成などは出力をファイルへ書き、チェックサムだけ標準出力へ出す |
| 言語の実装差（処理系バージョン） | 処理系バージョンを結果ファイルに記録（例: Python 3.11.2 / Node v22.22.3） |
| 平均の取り方の偏り | 幾何平均だけでなく、調和平均、中央値、最速回数も併記 [5](https://users.elis.ugent.be/~leeckhou/papers/CAL-2024-geomean.pdf) |

## 5. 実行手順（再現方法）

```bash
# 1) 全項目×全言語を実行（CIではここを Actions が実行）
python3 harness/run.py

# 2) 特定の言語・項目だけ実行
python3 harness/run.py --lang c,python,java --item sieve,matrix-mult

# 3) レポート生成（ランキング表・HTMLレポート）
python3 harness/report.py

# 4) レーティング方法を変えて比較（report.py内で複数指標を計算）
# ranking.md には幾何平均、算術平均、調和平均、中央値、最大遅延、最速回数が全て載る
```

結果は `results/results.json`（生データ）と `results/results.csv` に保存され、`report.py` が `results/report.html`・`results/ranking.md` を生成する。

レポートでは:
- 総合スコアの棒グラフ (幾何平均)
- 最速回数の棒グラフ
- カテゴリ別ランキングとグラフ
- 項目ごとの詳細 (相対倍率バー + 中央値・最小・最大・実行回数)
- なぜ最速回数と総合順位がずれるかの解説

が自動で生成される。

## 参考文献

- Benchmarks Game Methodology: elapsed time正規化と幾何平均 [1](https://grokipedia.com/page/The_Computer_Language_Benchmarks_Game) [4](https://benchmarksgame-team.pages.debian.net/benchmarksgame/box-plot-summary-charts.html)
- SPECと平均の選び方: 算術平均 vs 幾何平均 vs 調和平均 [3](https://www.quora.com/Why-is-geometric-mean-considered-a-good-metric-compared-to-average-AM-to-consider-improvements-in-performance-or-energy-in-the-field-of-computer-architecture) [4](https://www.researchgate.net/publication/220244867_The_harmonic_or_geometric_mean_does_it_really_matter) [5](https://users.elis.ugent.be/~leeckhou/papers/CAL-2024-geomean.pdf)
- 加重幾何平均の計算方法 [2](https://github.com/krausest/js-framework-benchmark/wiki/Computation-of-the-weighted-geometric-mean)
- エネルギー効率でのParetoランキング [1](https://haslab.github.io/SAFER/scp21.pdf)
- ベンチマークの信頼性と調和 (Harmony) [2](https://arxiv.org/html/2509.25671)
