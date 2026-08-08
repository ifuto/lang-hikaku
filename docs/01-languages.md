# 世界の主要プログラミング言語（調査結果）

> 目的: 「計算速度比較」という自由研究にふさわしい、世界の主要言語を選定する。
> 調査日: 2026-08-08（最新: TIOBE 2026年2-3月 / Stack Overflow 2025 / GitHub Octoverse 2025）

## 1. 「主要」の定義 — 3つの世界規模データ

「主要な言語」は、人気の測り方によって順位が変わる。代表的な3つの指標を最新値で並べる。

| 指標 | 1位 | 2位 | 3位 | 4位 | 5位 | 6位 | 備考 |
|---|---|---|---|---|---|---|---|
| **TIOBE指数**（検索エンジン等, 2026年2月） | Python 21.81% | C 11.05% | C++ / Java 8-9% | Java | C# 7.39% | JavaScript 3% | Pythonが歴代最高26.98%を2025年7月に記録 [5](https://rockstardeveloperuniversity.com/programming-language-statistics/) [2](https://commandlinux.com/statistics/top-programming-languages/) |
| **TIOBE 2026年3月** | Python 21.25% | C 11.55%（2位に復帰） | C++ | Java (過去最低4位) | C# | JS | Cが2位に再浮上 [1](https://itdaily.com/news/software/python-remains-most-popular-programming-language/) |
| **Stack Overflow開発者調査**（49,000人以上, 2025年） | JavaScript 66% | HTML/CSS 61.9% | SQL 58.6% | Python 57.9% (+7pp YoY) | Bash 48.7% | TypeScript 43.6% | Pythonが前年比+7%で最大の伸び [2](https://aicodedetector.com/programming-language-statistics/) [1](https://enstacked.com/stack-overflow-developer-survey-insights/) |
| **GitHub Octoverse 2025**（月間コントリビューター数） | TypeScript 263万 (+66.6% YoY) | Python 約259万 (+48.7%) | JavaScript 213万 | Java | C# | C++ | 10年以上ぶりの首位交代。TypeScriptがPythonを約4.2万人差で抜いて初の1位 [3](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/) [4](https://jeffbruchado.com.br/en/blog/typescript-most-popular-language-github-2025-octoverse) |

- 開発者人口（SlashData, 2025）は世界で約4,720万人。言語別では JavaScript 約2,800万人、Java と Python が各約2,300万人、C++ 約1,630万人 [5](https://rockstardeveloperuniversity.com/programming-language-statistics/)。
- まとめ: **Python / JavaScript(とTypeScript) / C / C++ / Java / C#** はどの指標でも必ず上位に入る「世界の主要言語」。Rust は最も愛されている言語で72%が使い続けたいと回答 [2](https://aicodedetector.com/programming-language-statistics/)、Go もクラウド系で急成長で、速度比較の材料として面白い。

**出典**
- TIOBE Index Feb 2026: Python 21.81% [2](https://commandlinux.com/statistics/top-programming-languages/)
- TIOBE Index Mar 2026: [1](https://itdaily.com/news/software/python-remains-most-popular-programming-language/)
- TIOBE Peak 26.98% July 2025 歴代最高: [5](https://rockstardeveloperuniversity.com/programming-language-statistics/)
- Stack Overflow Developer Survey 2025 JavaScript 66% / Python 57.9%: [2](https://aicodedetector.com/programming-language-statistics/) / [1](https://enstacked.com/stack-overflow-developer-survey-insights/)
- GitHub Octoverse 2025 TypeScript 1位: [3](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/) / [4](https://jeffbruchado.com.br/en/blog/typescript-most-popular-language-github-2025-octoverse)
- SlashData 47.2M developers: [5](https://rockstardeveloperuniversity.com/programming-language-statistics/)

## 2. 選定基準

1. **世界規模で広く使われている**（上記のランキング上位）
2. **速度特性が多様** — 「なぜ速いのか」を学べるよう、コンパイル型・VM・JIT・インタプリタをバランスよく
3. **GitHub Actions（Ubuntu）で導入できる** — `apt-get`や公式Actionsで自動インストール可能
4. 高校生の自由研究でもコードが書きやすい — 文法が比較的読みやすく、サンプルが豊富

## 3. 本命12言語（今回のCIで自動計測する）

| # | 言語 | 処理系 (Actions) | 分類 | 世界での位置付け | 速度の特徴 | 備考 |
|---|---|---|---|---|---|---|
| 1 | C | GCC 13 | ネイティブコンパイル | TIOBE 2位(11-11.5%)。OS・組み込みの標準。Benchmarks Gameでも最速クラス [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) | 最速クラスの基準。-O2 | |
| 2 | C++ | G++ 13 | ネイティブコンパイル | TIOBE 3-4位。ゲーム・アプリ基盤 | Cとほぼ同等。標準ライブラリが充実 | |
| 3 | Rust | rustc 1.8x stable | ネイティブコンパイル | Stack Overflow 最も愛されている言語72% [2](https://aicodedetector.com/programming-language-statistics/)。TIOBE言語オブザイヤー候補 | C並みの速度+メモリ安全。Rust 1.05秒系で最速報告も [2](https://morsoftware.com/blog/fastest-programming-languages) | |
| 4 | Go | go 1.22 | ネイティブコンパイル(+GC) | GitHub伸び盛り。クラウド系標準 | Cに近い速度。GCの影響が出る項目も | |
| 5 | Java | OpenJDK Temurin 17 | VM (JIT) | TIOBE 4位(歴代最低)。企業システム定番。実行1.63秒系 [2](https://morsoftware.com/blog/fastest-programming-languages) | 起動は遅いがJITでネイティブ級 | |
| 6 | C# | .NET 8.0 | VM (JIT) | TIOBE 5位。TIOBE 2023/2025 Language of the Year | Javaと同系統。Linuxでも動作 | |
| 7 | Python | CPython 3.11/3.12 | インタプリタ | TIOBE 1位(21.81%) [2](https://commandlinux.com/statistics/top-programming-languages/)。AI・データサイエンス | 標準機能のみでは遅め。126秒系でCの100倍という計測も [2](https://morsoftware.com/blog/fastest-programming-languages) | C拡張の話が深掘りになる |
| 8 | JavaScript | Node.js 22 | JITスクリプト | 使用率世界1位66% [2](https://aicodedetector.com/programming-language-statistics/) | 起動が速く、実行中に最適化 | |
| 9 | TypeScript | tsc→Node.js 22 | コンパイル(実行はJS) | GitHub 1位(263万人) [3](https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/) | **実行時はJSなので速度はJSと同じ**になる。これは結果で確かめられる | 自由研究の考察ポイント |
| 10 | Ruby | CRuby 3.3 | インタプリタ | Webアプリ(Rails) | Pythonと似た特性 | |
| 11 | PHP | PHP 8.3 | インタプリタ | Webの定番(WordPress等) | 文字列処理は比較的速い | TIOBEでは微減傾向だが依然広く使われる |
| 12 | Julia | julia 1.10 | JIT (科学計算向け) | 数値計算言語として人気急上昇 | ループがネイティブ級に速い。JITのウォームアップあり。Fortran並みに速い用途も [2](https://morsoftware.com/blog/fastest-programming-languages) | |

### なぜこの12言語か？
- TIOBE Top6 (Python/C/C++/Java/C#/JavaScript) を全て含む
- GitHub #1 TypeScript を含むことで「TSとJSは同じ速さか？」を検証できる
- Rust/Go/Julia を入れることで「新しい言語はなぜ速いか」を語れる。RustはBenchmarks GameでC/C++と並ぶ最速常連 [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html)
- インタプリタ3種 (Python/Ruby/PHP) で「遅い理由」も比較できる

## 4. 追加候補（時間とCIの余裕があれば）

| 言語 | 処理系 | 分類 | 特徴 | 導入コスト |
|---|---|---|---|---|
| Swift | swiftc | ネイティブコンパイル | Appleの言語。Benchmarks GameでC++並みに速い報告 [4](https://hiredevelopers.com/fastest-computer-language/) | 数GB |
| Kotlin | kotlinc→JVM | VM (JIT) | Android標準。Javaと同じ土台 | 中 |
| Dart | dart compile exe | ネイティブコンパイル | Flutterの言語。AOTで実行 | 小 |
| R | Rscript | インタプリタ | 統計解析の定番(TIOBE 10位) | 小 |
| Perl | perl | インタプリタ | 歴史あるスクリプト言語。すでに一部実装あり | 小 |
| Lua | LuaJIT | JITスクリプト | 軽量・高速な組み込み言語。JSより速い場合も [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) | 小 |
| Zig | zig build-exe | ネイティブコンパイル | プライム数えで10,205 passes/secで1位の報告も [4](https://hiredevelopers.com/fastest-computer-language/) | 小 |
| Haskell | GHC | ネイティブコンパイル | 関数型言語。遅延評価の影響が見える | 中 |

実装は `harness/languages.json` に20言語分定義済み。Actions側で `matrix.lang` を増やせばすぐ追加できる。

## 5. 分類と速度の期待値（仮説）

Benchmarks Gameのまとめによると、C/Rust/C++/Swift/Go/Java系が最速グループ、JavaScript/Java系が中速、Python/Ruby/PHP/Perlが低速傾向にある [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) [2](https://morsoftware.com/blog/fastest-programming-languages)。

| 分類 | 言語 | 期待される速さ | 理由 |
|---|---|---|---|
| ネイティブコンパイル | C, C++, Rust, Go, Swift, Dart, Zig, Haskell | **最速クラス** (C 1.23秒, Rust 1.05秒など) [2](https://morsoftware.com/blog/fastest-programming-languages) | 実行前に機械語へ翻訳済み。オーバーヘッドが最小 |
| VM (JIT) | Java, C#, Kotlin | ネイティブに近い (Java 1.63秒) [2](https://morsoftware.com/blog/fastest-programming-languages) | 実行中にホットなコードを機械語へ変換(JIT) |
| JITスクリプト | JavaScript(Node), TypeScript, Julia, LuaJIT | 中〜高速 (JS 2.5秒) [2](https://morsoftware.com/blog/fastest-programming-languages) | 初回は遅いが繰り返し実行で最適化される |
| インタプリタ | Python, Ruby, PHP, Perl, R | 低速傾向 (Python 126.53秒) [2](https://morsoftware.com/blog/fastest-programming-languages) | 文を1つずつ解釈して実行。ただしライブラリ呼び出しはC実装で速い |

**自由研究ならではの注意ポイント**
- TypeScriptは実行時JavaScript → 速度はJavaScriptとほぼ同じになる「はず」。実際に同じになったら、それは正しい結果であり考察の種。
- PythonはNumPy等のC拡張を使うと行列計算が劇的に速くなる → 今回は**標準機能のみ**で比較し、「ライブラリを使うとどう変わるか」を追加実験にできる。
- 「起動時間を含めるかどうか」で順位が変わることがある（Java・Julia等は起動が遅い）→ 計測方法をはっきり決める（方法論ドキュメント参照）。
- 並行処理や文字列処理では「言語の標準ライブラリの実装差」が大きく出る。これは「言語の実力」の一部として考察できる。

## 6. 環境ダウンロード（GitHub Actions）での導入方法

`.github/workflows/benchmark.yml`（および `docs/github-actions/benchmark.yml`）が環境構築専用のActions定義。

- `actions/setup-python@v5` (Python 3.11)
- `dtolnay/rust-toolchain@stable` (Rust)
- `actions/setup-go@v5` (Go 1.22)
- `actions/setup-java@v4` Temurin 17 (Java)
- `actions/setup-dotnet@v4` .NET 8.0 (C#)
- `actions/setup-node@v4` Node.js 22 (JS/TS) + `npm install -g typescript`
- `ruby/setup-ruby@v1` Ruby 3.3
- `shivammathur/setup-php@v2` PHP 8.3
- `julia-actions/setup-julia@v2` Julia 1.10

各言語は matrix で別ジョブに分かれ、同時に4ジョブまで並列実行。失敗しても他の言語は止まらない (`fail-fast: false`)。
結果は `actions/upload-artifact@v4` で保存し、最後に `merge_results.py` と `report.py` で統合・HTML生成する。
