# lang-hikaku — プログラミング言語の計算速度比較（自由研究）

世界の主要プログラミング言語で **50項目の計算** を実行し、「どの言語が一番速いか」を
公平な方法で比較するプロジェクト。

## 構成

```
docs/                        調査・設計ドキュメント
  01-languages.md            世界の主要言語の調査と選定
  02-benchmark-items.md      50項目のベンチマーク定義
  03-methodology.md          公平な計測方法（方法論）
harness/
  run.py                     ベンチマーク実行ハーネス
  report.py                  ランキング・HTMLレポート生成
  merge_results.py           言語別ジョブの結果を統合（CI用）
  languages.json             言語ごとのビルド/実行コマンド定義
benchmarks/
  items.json                 50項目の定義データ
  <項目ID>/run.<拡張子>       各言語の実装（例: sieve/run.c, sieve/run.py）
docs/github-actions/
  benchmark.yml             GitHub Actions ワークフロー（この中身を
                            .github/workflows/benchmark.yml にペーストして使う）
results/                    計測結果（自動生成・コミットしない）
```

## 使い方

```bash
# 全項目 x 全言語を実行（コンパイル言語は自動ビルド、各項目3回以上実行して中央値）
python3 harness/run.py

# 対象を絞って実行
python3 harness/run.py --lang c,python,java --item sieve,matrix-mult

# レポート生成（ランキング.md / report.html / CSV）
python3 harness/report.py
```

## 検証ルール

- 各プログラムは答え（チェックサム）を1行出力し、全言語の出力が一致することを自動検証する
- コンパイル時間は計測しない（実行時間のみ）
- 各項目 3〜7回実行し、中央値を採用
- 詳細は `docs/03-methodology.md`

## 状態

- [x] 言語調査・50項目の定義（docs/、全項目の正解値も検証済み）
- [x] ハーネス（run.py / report.py / merge_results.py）
- [x] GitHub Actions ワークフロー（docs/github-actions/benchmark.yml 用意済み → .github/workflows/ にペースト）
- [x] スモークテスト実装（C / C++ / Python / Node.js / Perl）
- [ ] 本命12言語の全50項目実装（次フェーズ）
