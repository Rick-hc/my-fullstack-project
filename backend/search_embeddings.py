#!/usr/bin/env python3
"""
RAG 検索モジュール & CLI
- `chunk_search()` を提供して他モジュールから呼び出せる
- 既存の CLI (`python search_embeddings.py`) も維持
"""
from __future__ import annotations
import json, sys, numpy as np, openai
from pathlib import Path
from typing import List, Dict

# --- 設定 ---
EMBEDDINGS_FILE = Path(__file__).with_suffix("").parent / "raw" / "embeddings_full.json"
MODEL = "text-embedding-3-large"

# --- 埋め込みコーパスをメモリにロード（初回のみ） ---
with EMBEDDINGS_FILE.open(encoding="utf-8") as f:
    _CORPUS: List[Dict] = json.load(f)                     # [{id, embedding}, …]
_IDS  = [item["id"] for item in _CORPUS]                   # e.g. "chunk_12"
_MAT  = np.vstack([item["embedding"] for item in _CORPUS]).astype(float)
_MAT /= np.linalg.norm(_MAT, axis=1, keepdims=True)        # 正規化

# --- 公開 API ---------------------------------------------------------------
def chunk_search(question: str, top_k: int = 3) -> List[Dict]:
    """
    質問文を受け取り、類似チャンク上位 *top_k* 件を返す。

    Returns
    -------
    list[dict]: [{"chunk_no": int, "content": str, "score": float}, …]
    """
    # 1) 質問をベクトル化 & 正規化
    res = openai.embeddings.create(model=MODEL, input=question)
    qvec = np.array(res.data[0].embedding, dtype=float)
    qvec /= np.linalg.norm(qvec)

    # 2) コサイン類似度（正規化済みなので dot）
    sims = _MAT @ qvec
    idxs = sims.argsort()[-top_k:][::-1]

    results = []
    for i in idxs:
        # id から番号を取得
        try:
            num = int(_IDS[i].split("_")[1])
        except Exception:
            num = i + 1
        results.append(
            {
                "chunk_no": num,
                "content": _CORPUS[i].get("text", ""),  # 埋め込み作成時に保存した本文キー
                "score": float(sims[i]),
            }
        )
    return results

# --- 既存 CLI ---------------------------------------------------------------
def main() -> None:
    print("質問を入力してください。")
    q = input().strip()
    if not q:
        print("クエリが空です。終了。"); sys.exit(0)

    try:
        res = chunk_search(q, top_k=1)
    except Exception as e:
        print(f"検索失敗: {e}"); sys.exit(1)

    print(res[0]["chunk_no"])

if __name__ == "__main__":
    main()
