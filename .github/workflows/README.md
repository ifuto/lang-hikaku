# GitHub Actions ワークフロー置き場

ここに `benchmark.yml` などを置いてください（ユーザーがymlをペーストする想定）。

## ワークフローが用意すべきもの

1. **ツールチェーンのインストール**（`harness/languages.json` の全言語に対応）
2. **ベンチマーク実行**: `python3 harness/run.py`
3. **結果のアップロード**: `results/` を artifact として保存

## インストール例（ubuntu-latest）

```yaml
- name: Install toolchains
  run: |
    sudo apt-get update
    sudo apt-get install -y gcc g++ python3 nodejs ruby php perl openjdk-17-jdk-headless r-base lua5.4 luajit
    # Rust
    curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
    echo "$HOME/.cargo/bin" >> "$GITHUB_PATH"
    # Go
    curl -fsSL https://go.dev/dl/go1.22.12.linux-amd64.tar.gz | sudo tar -C /usr/local -xz
    echo "/usr/local/go/bin" >> "$GITHUB_PATH"
    # .NET (C#)
    curl -fsSL https://dot.net/v1/dotnet-install.sh | bash
    echo "$HOME/.dotnet" >> "$GITHUB_PATH"
    # Julia
    curl -fsSL https://install.julialang.org | sh -s -- --yes --default-channel release
    echo "$HOME/.juliaup/bin" >> "$GITHUB_PATH"
    # TypeScript
    npm install -g typescript
```

注意:
- **Swift / Kotlin / Dart / Zig / Haskell は追加インストールが重い**（Swiftは数GB）。本命12言語だけなら不要。
- 実行時間対策: 言語ごとにジョブを分ける（`matrix`）か、`--lang` で分割実行する。
- 計測結果は必ず `actions/upload-artifact` で保存する（`results/` ディレクトリ）。
