# 世界の主要プログラミング言語（調査結果）

> 目的: 「計算速度比較」という自由研究にふさわしい、世界の主要言語を選定する。
> 調査日: 2026-08-07

## 1. 「主要」の定義 — 3つの世界規模データ

「主要な言語」は、人気の測り方によって順位が変わる。代表的な3つの指標を並べる。

| 指標 | 1位 | 2位 | 3位 | 4位 | 5位 | 6位 |
|---|---|---|---|---|---|---|
| **TIOBE指数**（検索エンジンのヒット数ベース, 2026年7月） | Python | C | C++ | Java | C# | JavaScript |
| **Stack Overflow開発者調査**（実際に使っている人の割合, 2025年, 49,000人以上回答） | JavaScript 66% | HTML/CSS 61.9% | SQL 58.6% | Python 57.9% | Bash/Shell 48.7% | TypeScript 43.6% |
| **GitHub Octoverse**（リポジトリのコントリビューター数, 2025年） | TypeScript（月間264万人, 前年比+66.6%） | Python | Java | C++ | C# | Go・Rustなど |

- 開発者人口（SlashData, 2025）は世界で約4,720万人。言語別では JavaScript 約2,800万人、Java と Python が各約2,300万人、C++ 約1,630万人。
- まとめ: **Python / JavaScript(とTypeScript) / C / C++ / Java / C#** はどの指標でも必ず上位に入る「世界の主要言語」。Rust と Go は伸び盛りで開発者からの人気が高く、速度比較の材料として面白い。

**出典**
- TIOBE Index: https://www.tiobe.com/tiobe-index/
- Stack Overflow Developer Survey 2025: https://survey.stackoverflow.co/2025/
- GitHub Octoverse 2025: https://github.blog/news-insights/octoverse/octoverse-2025/
- SlashData: https://slashdata.org/

## 2. 選定基準

1. **世界規模で広く使われている**（上記のランキング上位）
2. **速度特性が多様** — 「なぜ速いのか」を学べるよう、コンパイル型・VM・JIT・インタプリタをバランスよく
3. **GitHub Actions（Ubuntu）で導入できる**
4. 高校生の自由研究でもコードが書きやすい

## 3. 本命12言語

| # | 言語 | 処理系 | 分類 | 世界での位置付け | 速度の特徴 |
|---|---|---|---|---|---|
| 1 | C | GCC 12 | ネイティブコンパイル | TIOBE 2位。OS・組み込みの標準 | 最速クラスの基準。最適化 -O2 |
| 2 | C++ | G++ | ネイティブコンパイル | TIOBE 3位。ゲーム・アプリ基盤 | Cとほぼ同等。標準ライブラリが充実 |
| 3 | Rust | rustc | ネイティブコンパイル | TIOBE 8位。開発者が最も「好き」な言語(72%) | C並みの速度+メモリ安全 |
| 4 | Go | go build | ネイティブコンパイル(+GC) | クラウド系で急成長 | Cに近い速度。GCの影響が出る項目も |
| 5 | Java | OpenJDK | VM (JIT) | TIOBE 4位。企業システムの定番 | 起動は遅いがJITでネイティブ級 |
| 6 | C# | .NET | VM (JIT) | TIOBE 5位。TIOBE 2025年の言語 | Javaと同系統。Linuxでも動作 |
| 7 | Python | CPython 3 | インタプリタ | TIOBE 1位。AI・データサイエンス | 標準機能のみでは遅め。C拡張(NumPy)の話が研究の深掘りになる |
| 8 | JavaScript | Node.js 22 | JITスクリプト | 使用率世界1位(66%) | 起動が速く、実行中に最適化(ウォームアップ) |
| 9 | TypeScript | tsc→Node.js | コンパイル(実行はJS) | GitHub 1位 | **実行時はJavaScriptなので速度はJSと同じ**になる。これは結果で確かめられる |
| 10 | Ruby | CRuby 3 | インタプリタ | TIOBE 15位。Webアプリ(Rails) | Pythonと似た特性。一部の処理は高速 |
| 11 | PHP | PHP 8 | インタプリタ | Webの定番(WordPress等) | 文字列処理は比較的速い |
| 12 | Julia | julia | JIT (科学計算向け) | 数値計算言語として人気急上昇 | ループがネイティブ級に速い。JITのウォームアップあり |

## 4. 追加候補（時間とCIの余裕があれば）

| 言語 | 処理系 | 分類 | 特徴 |
|---|---|---|---|
| Swift | swiftc | ネイティブコンパイル | Appleの言語。導入が重い(数GB) |
| Kotlin | kotlinc→JVM | VM (JIT) | Androidの標準言語。Javaと同じ土台 |
| Dart | dart compile exe | ネイティブコンパイル | Flutterの言語。AOTで実行 |
| R | Rscript | インタプリタ | 統計解析の定番(TIOBE 10位) |
| Perl | perl | インタプリタ | 歴史あるスクリプト言語 |
| Lua | LuaJIT | JITスクリプト | 軽量・高速な組み込み言語 |
| Zig | zig | ネイティブコンパイル | 話題の新進気鋭言語 |
| Haskell | GHC | ネイティブコンパイル | 関数型言語。遅延評価の影響が見える |

## 5. 分類と速度の期待値（仮説）

| 分類 | 言語 | 期待される速さ | 理由 |
|---|---|---|---|
| ネイティブコンパイル | C, C++, Rust, Go, Swift, Dart, Zig, Haskell | **最速クラス** | 実行前に機械語へ翻訳済み。オーバーヘッドが最小 |
| VM (JIT) | Java, C#, Kotlin | ネイティブに近い | 実行中にホットなコードを機械語へ変換(JIT) |
| JITスクリプト | JavaScript(Node), TypeScript, Julia | 中〜高速 | 初回は遅いが繰り返し実行で最適化される |
| インタプリタ | Python, Ruby, PHP, Perl, R, Lua | 低速傾向 | 文を1つずつ解釈して実行。ただしライブラリ呼び出しはC実装で速い |

**自由研究ならではの注意ポイント**
- TypeScriptは実行時JavaScript → 速度はJavaScriptとほぼ同じになる「はず」。実際に同じになったら、それは正しい結果であり考察の種。
- PythonはNumPy等のC拡張を使うと行列計算が劇的に速くなる → 今回は**標準機能のみ**で比較し、「ライブラリを使うとどう変わるか」を追加実験にできる。
- 「起動時間を含めるかどうか」で順位が変わることがある（Java・Julia等は起動が遅い）→ 計測方法をはっきり決める（後述の方法論ドキュメント参照）。
