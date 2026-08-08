# lang-hikaku — プログラミング言語の計算速度比較（自由研究）

世界の主要プログラミング言語で **50項目の計算** を実行し、「どの言語が一番速いか」を
公平な方法で比較するプロジェクト。

## 構成

```
docs/                        調査・設計ドキュメント
  01-languages.md            世界の主要言語の調査と選定（2026年最新版）
  02-benchmark-items.md      50項目のベンチマーク定義（出典付き）
  03-methodology.md          公平な計測方法（方法論）
harness/
  run.py                     ベンチマーク実行ハーネス
  report.py                  ランキング・HTMLレポート生成
  merge_results.py           言語別ジョブの結果を統合（CI用）
  languages.json             言語ごとのビルド/実行コマンド定義（20言語定義済み）
benchmarks/
  items.json                 50項目の定義データ（expected付き）
  <項目ID>/run.<拡張子>       各言語の実装（例: sieve/run.c, sieve/run.py）
docs/github-actions/
  benchmark.yml             GitHub Actions ワークフロー（環境ダウンロード専用）
                            この中身を .github/workflows/benchmark.yml にペーストして使う
                            → リポジトリでは .github/workflows/benchmark.yml として配置済み
results/                    計測結果（自動生成・コミットしない）
```

## 使い方

```bash
# 全項目 x 全言語を実行（コンパイル言語は自動ビルド、各項目3回以上実行して中央値）
python3 harness/run.py

# 対象を絞って実行
python3 harness/run.py --lang c,python,java --item sieve,matrix-mult

# 特定の項目カテゴリだけ
python3 harness/run.py --item empty-loop,count-primes,fib-recursive,sieve,gcd,powmod,collatz

# レポート生成（ランキング.md / report.html / CSV）
python3 harness/report.py
```

## 検証ルール

- 各プログラムは答え（チェックサム）を1行出力し、全言語の出力が一致することを自動検証する
- コンパイル時間は計測しない（実行時間のみ）
- 各項目 3〜7回実行し、中央値を採用
- 詳細は `docs/03-methodology.md`

## 世界の主要言語（2026年最新）

- **TIOBE 2026年2月**: Python 21.81% [出典](https://commandlinux.com/statistics/top-programming-languages/)、C 11.05%、C++、Java、C#...
- **Stack Overflow 2025**: JavaScript 66%が最も使われている [出典](https://aicodedetector.com/programming-language-statistics/)、Python +7ppで急伸
- **GitHub Octoverse 2025**: TypeScriptが263万コントリビューターで初の1位 (+66.6% YoY) [出典](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/)
- 開発者人口は世界で約4,720万人（SlashData 2025）

本命12言語: C, C++, Rust, Go, Java, C#, Python, JavaScript, TypeScript, Ruby, PHP, Julia
（詳細は `docs/01-languages.md`）

## 50項目の計算内容

9カテゴリ50項目を定義済み（Benchmarks Gameの定番項目も含む）:
- A. 整数演算 (8): empty-loop, fib-recursive, count-primes, sieve, gcd, powmod, collatz, factorize
- B. 浮動小数点 (10): matrix-mult, spectral-norm, nbody, mandelbrot など [Benchmarks Game](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html)
- C. 文字列処理 (7): regex-match, sha256 など
- D. データ構造 (8): hash-insert, sort-ints, bst など
- E. 再帰・アルゴリズム (6): binary-trees, fannkuch-redux など
- F. 多倍長整数 (3): pidigits など
- G. ファイル・I/O (4): json-parse など
- H. 並行処理 (2): thread-ring など
- I. その他 (2): random-gen, fasta-gen

詳細は `docs/02-benchmark-items.md` と `benchmarks/items.json`。

## GitHub Actions（環境ダウンロード専用）

サンドボックスでは言語をダウンロードできないため、GitHub Actionsで環境を用意して計測する。

`.github/workflows/benchmark.yml` に以下が定義済み:

- **言語インストール**:
  - `actions/setup-python@v5` Python 3.11
  - `dtolnay/rust-toolchain@stable` Rust stable
  - `actions/setup-go@v5` Go 1.22
  - `actions/setup-java@v4` Temurin 17
  - `actions/setup-dotnet@v4` .NET 8.0
  - `actions/setup-node@v4` Node.js 22 + `npm install -g typescript`
  - `ruby/setup-ruby@v1` Ruby 3.3
  - `shivammathur/setup-php@v2` PHP 8.3
  - `julia-actions/setup-julia@v2` Julia 1.10
  - C/C++ は `gcc`/`g++`
- **計測**: `python3 harness/run.py --lang ${{ matrix.lang }}`
- **統合**: `merge_results.py` で言語別結果を統合 → `report.py` で `report.html`/`ranking.md`/`times.csv` 生成
- **成果物**: `results-*` と `benchmark-report` を Artifacts に保存

実行方法:
1. `docs/github-actions/benchmark.yml` をコピーして `.github/workflows/benchmark.yml` に配置（すでに配置済み）
2. GitHubのActionsタブから「Run workflow」または `main` へpushで起動

このリポジトリでは `arena/019fdee5-lang-hikaku` ブランチで作業中。`main` へマージしてpushするとActionsが動く。

## 状態

- [x] 言語調査・50項目の定義（docs/、2026年最新データと出典付きに更新）
- [x] ハーネス（run.py / report.py / merge_results.py）
- [x] GitHub Actions ワークフロー（環境ダウンロード専用、12言語対応、180分タイムアウト、fail-fast:false）
- [x] ベンチマーク実装（12言語 × 9項目）:
  - empty-loop, fib-recursive, count-primes, sieve, gcd, powmod, collatz, matrix-mult, hash-insert
  - C/C++/Rust/Go/Java/C#/Python/Node.js/TypeScript/Ruby/PHP/Julia/Perl の全てで動作確認
  - 期待値の不整合（matrix-mult, gcd, powmod）を修正し、全言語で一致することを検証済み
- [ ] 本命12言語の全50項目実装（9/50 完了、残りは `benchmarks/<id>/run.<ext>` を追加すればOK）
- [ ] レポートのHTMLをPagesで公開（オプション）

## 自由研究としての考察ポイント

- なぜC/Rustが速いのか（ネイティブコンパイル） vs Pythonが遅いのか（インタプリタ）
- TypeScriptは実行時JavaScriptなので速度が同じになることを検証
- 起動時間込み vs 純粋な計算時間の違い（Java/Juliaは起動が遅い）
- 文字列処理やハッシュではライブラリ実装の差が大きく出る
- 規模を2倍にしたときに時間がどう伸びるか（計算量オーダーの観察）

詳細は `docs/03-methodology.md` を参照。
