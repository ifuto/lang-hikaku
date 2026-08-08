# ベンチマーク項目一覧（50項目）

> 50項目を9カテゴリに分類。各項目は「同じアルゴリズム・同じ規模」を全言語で実装し、速度を比べる。
> 項目の定義データは `benchmarks/items.json` にも同じ内容で格納されている。
> 
> 多くの項目は世界で使われているベンチマーク集「The Computer Language Benchmarks Game」 [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) や、kostya/benchmarks [3](https://github.com/kostya/benchmarks) などのオープンなベンチマークを参考に、高校生の自由研究でも再現しやすい規模に調整したもの。

## 出典・参考にしたベンチマーク

- Benchmarks Game: binary-trees, fannkuch-redux, spectral-norm, nbody, fasta, pidigits, regex-redux, k-nucleotideなどが定番 [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html)
- kostya/benchmarks: base64, json, matmul, primes, brainfuckなど多数言語の実行時間比較 [3](https://github.com/kostya/benchmarks)
- 言語の速度差を語る記事: C 1.23秒 vs Java 1.63秒 vs Python 126.53秒といった桁違いの差が報告 [2](https://morsoftware.com/blog/fastest-programming-languages) / Zigが最速だったprime計測 [4](https://hiredevelopers.com/fastest-computer-language/)

## カテゴリ構成

| カテゴリ | 項目数 | 主に測れるもの | 代表的な元ネタ |
|---|---|---|---|
| A. 整数演算 | 8 | ループ・関数呼び出し・剰余・除算の速度 | primes, empty-loop |
| B. 浮動小数点 | 10 | 科学計算の速度 | spectral-norm, nbody, mandelbrot [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) |
| C. 文字列処理 | 7 | 文字列・正規表現・ハッシュの速度 | regex-redux, k-nucleotide [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) |
| D. データ構造 | 8 | 配列・ハッシュ・木・キュー操作の速度 | hash, sort |
| E. 再帰・アルゴリズム | 6 | 再帰・メモリ確保・探索の速度 | binary-trees, fannkuch-redux, n-queens [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) |
| F. 多倍長整数 | 3 | 大きな数(10進1000桁以上)の演算速度 | pidigits, gmp [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) |
| G. ファイル・I/O | 4 | 読み書き・パースの速度 | json-parse [3](https://github.com/kostya/benchmarks) |
| H. 並行処理 | 2 | スレッドの生成・通信の速度 | thread-ring [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) |
| I. その他 | 2 | 乱数生成・出力生成 | random, fasta [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) |
| **合計** | **50** | | |

## A. 整数演算（8項目）

| ID | 名称 | 内容（アルゴリズム） | 規模 | 主に測れるもの | expected |
|---|---|---|---|---|---|
| empty-loop | 空ループ | 1から10^9まで加算（最適化で消えないよう合計を出力） | 10^9回 | 純粋なループ・分岐の速度 | 499999999500000000 |
| fib-recursive | 再帰フィボナッチ | fib(35) を素朴な再帰で計算 | fib(35)=9227465 | 関数呼び出し・再帰のコスト | 9227465 |
| count-primes | 試し割り素数カウント | 2〜300,000 の素数を「割れるか試す」方法で数える | 300,000まで | 整数除算・剰余の速度 | 25997 |
| sieve | エラトステネスのふるい | ふるい法で 10^7 以下の素数を数える | 10^7（素数664,579個） | 配列アクセス・多重ループ | 664579 |
| gcd | ユークリッド互除法 | 乱数ペア5×10^6組の最大公約数を求める | 5×10^6ペア | 剰余演算の速度 | 33201628 |
| powmod | 冪剰余 | a^b mod m をバイナリ法で10^6回計算 | 10^6回 | 乗算・剰余・ループ | 16288765099 |
| collatz | コラッツ数列 | 1〜10^6 で「1になるまでのステップ数」の最大値を求める | 10^6個 | 整数分岐ループ | 837799 |
| factorize | 素因数分解 | 10^12付近の合成数2,000個を試し割りで分解 | 2,000個 | 除算・ループ（最悪ケースの差が出る） | 498265730 |

## B. 浮動小数点（10項目）

| ID | 名称 | 内容（アルゴリズム） | 規模 | 主に測れるもの | 由来 |
|---|---|---|---|---|---|
| monte-carlo-pi | モンテカルロ法でπ | 正方形に5×10^7個の点を打ち、円内に入る割合からπを推定 | 5×10^7点 | 乱数生成+浮動小数点演算 | 古典的数値計算 |
| pi-arctan | 級数でπ | π=4(1−1/3+1/5−…) を10^8項まで加算 | 10^8項 | 浮動小数点の加減算ループ | 古典的 |
| sqrt-newton | ニュートン法で平方根 | 10^7個の数について収束するまで反復 | 10^7個 | 浮動小数点演算・ループ | |
| matrix-mult | 行列積 | 300×300 の整数行列の積（int64, i-k-j順） | 300×300 | 多重ループ・メモリアクセス | matmul [3](https://github.com/kostya/benchmarks) |
| matrix-transpose | 行列転置 | 5,000×5,000 行列の転置 | 5,000×5,000 | メモリアクセス順序（キャッシュ） | |
| spectral-norm | スペクトルノルム | べき乗法で行列のスペクトルノルムを計算（ベンチマークゲーム定番） | n=2,000 | 浮動小数点・配列の総合性能 | spectral-norm [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) |
| nbody | n体シミュレーション | 太陽系5天体の軌道をシンプレクティック積分で500万ステップ | 500万ステップ | 浮動小数点の総合性能 | n-body [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) |
| mandelbrot | マンデルブロ集合 | 2,000×2,000画素で発散判定（最大1,000回反復） | 2,000×2,000 | 複素数演算・分岐ループ | mandelbrot [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) |
| gaussian-elim | ガウスの消去法 | 300元連立一次方程式を前進消去+後退代入で解く | 300元 | 浮動小数点・メモリ | 数値解析定番 |
| numerical-integral | 数値積分 | シンプソン則で ∫0^1 4/(1+x²)dx を10^8分割で計算（=πの近似） | 10^8分割 | 浮動小数点ループ | |

## C. 文字列処理（7項目）

| ID | 名称 | 内容（アルゴリズム） | 規模 | 主に測れるもの | 由来 |
|---|---|---|---|---|---|
| string-concat | 文字列連結 | 短い文字列を10^5回連結して1MBの文字列を作る | 10^5回 | 文字列メモリ管理（連結コストの伸び方の差） | |
| string-reverse | 文字列反転 | 10MBの文字列を反転する処理を10回 | 10MB×10回 | 文字列・配列の操作速度 | |
| char-count | 文字カウント | 10MBテキストを走査し、英字・数字・空白の個数を数える | 10MB | 文字列走査の速度 | |
| substring-search | 部分文字列検索 | 5MBテキストから500種のパターンを探して出現回数を数える | 5MB×500パターン | 文字列検索アルゴリズム | k-nucleotide [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) |
| regex-match | 正規表現マッチ | 5MBのDNA配列で8塩基パターン500種の出現数を正規表現で数える | 500パターン | 正規表現エンジンの速度 | regex-redux [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) |
| regex-replace | 正規表現置換 | 10MBテキストで5種の置換パターンを適用 | 10MB | 正規表現エンジンの速度 | |
| sha256 | SHA-256ハッシュ | 100KBデータのSHA-256を10^4回計算 | 10^4回 | 標準ライブラリのハッシュ速度 | |

## D. データ構造（8項目）

| ID | 名称 | 内容（アルゴリズム） | 規模 | 主に測れるもの |
|---|---|---|---|---|
| hash-insert | ハッシュマップ挿入 | "k0000001"形式のキー10^6件をマップに挿入 | 10^6件 | ハッシュ・メモリ管理 |
| hash-lookup | ハッシュマップ検索 | 挿入済み10^6件を全件検索して値の合計を出す | 10^6件 | ハッシュ・キー比較 |
| sort-ints | 整数配列ソート | 10^7個のランダムな32ビット整数をソート | 10^7個 | ソートアルゴリズム（ライブラリ含む） |
| sort-strings | 文字列ソート | 10^6個のランダム文字列をソート | 10^6個 | ソート+文字列比較 |
| bst | 二分探索木 | 10^6件を挿入し、続けて10^6件を検索 | 挿入10^6+検索10^6 | ポインタ追従・比較 |
| heap | 優先度キュー | 10^6件push→10^6件pop | 10^6+10^6 | データ構造の操作速度 |
| dedupe | 重複除去 | 10^6個（うち10^5種）の値を集合に入れて重複を数える | 10^6個 | 集合演算 |
| stack-queue | スタックとキュー | 10^7回のpush/popを交互に実行 | 10^7回 | データ構造の基本操作 |

## E. 再帰・アルゴリズム（6項目）

| ID | 名称 | 内容（アルゴリズム） | 規模 | 主に測れるもの | 由来 |
|---|---|---|---|---|---|
| binary-trees | 二分木の生成と解放 | 深さ19の二分木を作って破棄する操作を10回 | 深さ19×10回 | メモリ確保・解放（GC言語との差が出る） | binary-trees [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) |
| hanoi | ハノイの塔 | 23枚の円盤を移動（2^23−1回の移動を再帰で） | 23枚 | 再帰・関数呼び出し | 古典 |
| nqueens | n-クイーン | 13×13盤でクイーンを互いに効かせず置く配置の総数を数える | 13×13 | バックトラッキング探索 | n-queens的 |
| knapsack | ナップサック問題 | アイテム2,000個・容量2,000の動的計画法 | 2,000×2,000 | DP・配列アクセス | |
| fannkuch | fannkuch-redux | n=10の順列で「反転を繰り返して先頭を固定」する最大回数を求める（ベンチマークゲーム定番） | n=10 | 順列・配列操作 | fannkuch-redux [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) |
| levenshtein | レーベンシュタイン距離 | 500文字×500文字の編集距離をDPで計算 | 500×500 | DP・文字列 | |

## F. 多倍長整数（3項目）

| ID | 名称 | 内容（アルゴリズム） | 規模 | 主に測れるもの | 由来 |
|---|---|---|---|---|---|
| pidigits | πの桁計算 | spigotアルゴリズムでπを2,000桁計算 | 2,000桁 | 多倍長整数演算 | pi-digits [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) |
| factorial-bigint | 巨大階乗 | 50,000! を多倍長整数で計算（桁数は21万桁超） | 50,000! | 多倍長整数の乗算 | gmp |
| fib-bigint | 巨大フィボナッチ | fib(100,000) を多倍長整数で計算（2万桁超） | fib(100000) | 多倍長整数の加算 | |

## G. ファイル・I/O（4項目）

| ID | 名称 | 内容（アルゴリズム） | 規模 | 主に測れるもの |
|---|---|---|---|---|
| file-write | ファイル書き込み | 10^6行（約50MB）をテキストで書き込む | 50MB | ファイル書き込み速度 |
| file-read | ファイル読み込み | 上記のファイルを読み込んで行数を数える | 50MB | ファイル読み込み速度 |
| word-count | 単語カウント | 50MBテキストを読み、単語数を数える | 50MB | I/O+文字列処理 |
| json-parse | JSONパース | 10万件のレコード（約20MB）のJSONをパースして集計 | 20MB | パーサーの速度（json [3](https://github.com/kostya/benchmarks)） |

## H. 並行処理（2項目）

| ID | 名称 | 内容（アルゴリズム） | 規模 | 主に測れるもの | 由来 |
|---|---|---|---|---|---|
| thread-spawn | スレッド生成と参加 | 10^3個のスレッドを生成し、それぞれ小さな計算をさせてjoin | 10^3スレッド | スレッドの生成コスト | |
| thread-ring | スレッドリング | 1,000個のスレッドをリング状に繋ぎ、トークンを1,000周回す（ベンチマークゲーム定番） | 1,000スレッド×1,000周 | スレッド間通信 | thread-ring [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) |

## I. その他（2項目）

| ID | 名称 | 内容（アルゴリズム） | 規模 | 主に測れるもの | 由来 |
|---|---|---|---|---|---|
| random-gen | 乱数生成 | 線形合同法で5×10^7個の乱数を生成し、合計を出力 | 5×10^7個 | 乱数生成器（とループ）の速度 | |
| fasta-gen | DNA配列生成 | 擬似乱数で100万塩基のFASTA形式DNA配列を生成して出力（ベンチマークゲーム定番） | 100万塩基 | 乱数+文字列+書式整形 | fasta [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html) |

## 設計上の注意（自由研究の考察に使える）

- **規模の決め方**: 最速のCで約0.1〜3秒、最遅のインタプリタ言語でも1項目2分以内に終わる規模に調整してある。Benchmarks Gameでも同様に「全言語が完走できる規模」を選んでいる [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html)。規模は自由に変えられるので、「規模を2倍にしたら時間はどう伸びるか」という**計算量オーダーの観察**にも使える（追加研究テーマ）。
- **正しさの検証**: 各言語のプログラムは必ず「答え（チェックサム）」を1行出力し、全言語の出力が一致することを自動検証する。出力が違うプログラムは「結果不一致」として集計から外す。`benchmarks/items.json`に正解を格納。
- **最適化で消えない工夫**: 空ループや不要な計算はコンパイラが消してしまうため、必ず結果を合計に足して出力する。これは全ベンチマーク共通の常套手段 [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html)。
- **標準ライブラリを使う**: ハッシュマップやソートは言語標準のものを使う。独自実装するとアルゴリズムの差になってしまうため。
- **再現性**: GitHub Actionsの `ubuntu-latest` という同じスペックのマシンで直列実行し、ばらつきを抑える。

## 参考文献

1. Benchmarks Game: https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html [1](https://benchmarksgame-team.pages.debian.net/benchmarksgame/index.html)
2. Fastest Programming Languages article: C 1.23s, Rust 1.05s, Python 126.53s [2](https://morsoftware.com/blog/fastest-programming-languages)
3. kostya/benchmarks: multi-language benchmark collection [3](https://github.com/kostya/benchmarks)
4. Zig as fastest prime benchmark report [4](https://hiredevelopers.com/fastest-computer-language/)
