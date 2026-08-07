# Trigger

このファイルは GitHub Actions の `benchmark` ワークフローを起動するためのトリガーです。

ワークフローは `on: push: branches: [main]` で起動するため、
このファイルに何か1行追加して main に push するだけでベンチマークが再実行されます。

```bash
# 例
echo "run $(date)" >> Trigger.md
git add Trigger.md
git commit -m "run benchmark"
git push origin main
```

（Actionsタブの「Run workflow」ボタンを押す方法（workflow_dispatch）でも起動できます）
