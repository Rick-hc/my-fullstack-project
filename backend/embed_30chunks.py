"""
30チャンクのテキストを text-embedding-3-small でベクトル化し、
raw/embeddings_30.json に保存するスクリプト。
チャンク区切りは「--- CHUNK n ---」行で判定。
"""
import json
import re
import os
from pathlib import Path
from openai import OpenAI

# ------------------ 設定 ------------------
MODEL       = "text-embedding-3-small"
INPUT_FILE  = Path("raw/chunks/all_chunks.txt")
OUTPUT_FILE = Path("raw/embeddings_30.json")
BATCH_SIZE  = 30
# ------------------------------------------

client = OpenAI()  # OPENAI_API_KEY を環境変数から取得


def read_chunks(path: Path, max_chunks: int = BATCH_SIZE):
    """
    ファイルを読み込み、"--- CHUNK n ---" 区切りでブロックを抽出。
    max_chunks 件まで返す。
    """
    text = path.read_text(encoding="utf-8")
    # 区切り行で分割し、先頭の空文字を除去
    raw = re.split(r"^--- CHUNK \d+ ---$", text, flags=re.MULTILINE)
    # 最初の要素はヘッダ部分なので除去し、strip した上で空ブロックを除去
    chunks = [blk.strip() for blk in raw[1:] if blk.strip()]
    return chunks[:max_chunks]


def main() -> None:
    chunks = read_chunks(INPUT_FILE)
    print(f"Embedding {len(chunks)} chunks …")

    response = client.embeddings.create(
        model=MODEL,
        input=chunks
    )

    embeddings = [
        {"chunk_index": i, "embedding": item.embedding}
        for i, item in enumerate(response.data)
    ]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_FILE.open("w", encoding="utf-8") as fw:
        json.dump(embeddings, fw, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(embeddings)} embeddings → {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()
