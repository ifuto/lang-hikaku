#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""言語別ジョブの計測結果(results/results-*/results.json)を統合して results/results.json を作る。

GitHub Actions の「レポート生成」ジョブで使用する。
使い方: python3 harness/merge_results.py results
"""
import glob
import json
import os
import sys


def main():
    root = sys.argv[1] if len(sys.argv) > 1 else "results"
    merged = {"meta": {}, "results": {}}
    metas = []
    for f in sorted(glob.glob(os.path.join(root, "results-*", "results.json"))):
        with open(f, encoding="utf-8") as fh:
            d = json.load(fh)
        metas.append(d.get("meta", {}))
        for iid, langs in d.get("results", {}).items():
            merged["results"].setdefault(iid, {}).update(langs)
    if metas:
        merged["meta"] = metas[0]
        merged["meta"]["language_jobs"] = len(metas)
    out = os.path.join(root, "results.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(merged, fh, ensure_ascii=False, indent=2)
    n_items = len(merged["results"])
    n_ok = sum(1 for langs in merged["results"].values()
               for r in langs.values() if r.get("status") == "ok")
    print("統合: %d件のジョブ / %d項目 / %d件のOK結果 -> %s"
          % (len(metas), n_items, n_ok, out), flush=True)


if __name__ == "__main__":
    main()
