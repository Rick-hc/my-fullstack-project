#!/usr/bin/env python3
"""
チャンクディレクトリを埋め込み → JSON出力するスクリプト
-------------------------------------------------------------------------------
- raw/chunks/*.txt を一括読み込み
- OpenAI SDK v0.x/v1.x 両対応
- CLI でモデル、入力ディレクトリ、出力ファイル、バッチサイズ指定
- batch‐size <= 0 で全チャンク一括処理
- デフォルトで 1 チャンク当たり 250 文字、オーバーラップ 50 文字のチャンクを
  別途 chunk.py で生成してからこのスクリプトを実行する想定
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import openai
from typing import List, Tuple

def _create_embedding_v1(texts: List[str], model: str) -> List[List[float]]:
    res = openai.embeddings.create(model=model, input=texts)
    return [d.embedding for d in res.data]

def _create_embedding_v0(texts: List[str], model: str) -> List[List[float]]:
    res = openai.Embedding.create(model=model, input=texts)
    return [d["embedding"] for d in res["data"]]

_create_embedding = (
    _create_embedding_v1 if hasattr(openai, "embeddings") else _create_embedding_v0
)

def read_chunks(dir_path: Path) -> List[Tuple[str, str]]:
    """
    raw/chunks 以下の chunk_*.txt を読み込んで
    [(chunk_id, text), ...] のリストを返す。
    """
    files = sorted(dir_path.glob("chunk_*.txt"))
    if not files:
        raise FileNotFoundError(f"No chunk files found in {dir_path}")
    return [(p.stem, p.read_text(encoding="utf-8")) for p in files]

def main() -> None:
    parser = argparse.ArgumentParser(
        description="チャンクディレクトリを埋め込み JSON に変換するスクリプト"
    )
    parser.add_argument(
        "-i", "--input-dir", type=Path,
        default=Path("raw/chunks"),
        help="チャンクファイルディレクトリ (default: raw/chunks)"
    )
    parser.add_argument(
        "-o", "--output-file", type=Path,
        default=Path("raw/embeddings_full.json"),
        help="出力 JSON ファイル (default: raw/embeddings_full.json)"
    )
    parser.add_argument(
        "-m", "--model", type=str,
        default="text-embedding-3-large",
        help="埋め込みモデル名 (default: text-embedding-3-large)"
    )
    parser.add_argument(
        "-b", "--batch-size", type=int,
        default=0,
        help="1 リクエストあたりのチャンク数 (0 以下で全チャンク一括, default: 0)"
    )
    args = parser.parse_args()

    # チャンク読み込み
    chunks = read_chunks(args.input_dir)
    print(f"▶ Found {len(chunks)} chunks in {args.input_dir}")

    # バッチサイズの解釈
    batch_size = len(chunks) if args.batch_size <= 0 else args.batch_size

    all_embeddings: List[dict] = []
    for offset in range(0, len(chunks), batch_size):
        batch = chunks[offset : offset + batch_size]
        ids, texts = zip(*batch)
        print(f"  ● Embedding chunks {offset + 1}–{offset + len(batch)} with model={args.model}")
        vecs = _create_embedding(list(texts), args.model)
        for cid, txt, vec in zip(ids, texts, vecs):
            all_embeddings.append({
                "id": cid,
                "text": txt,
                "embedding": vec,
            })

    # 出力
    args.output_file.parent.mkdir(parents=True, exist_ok=True)
    with args.output_file.open("w", encoding="utf-8") as fw:
        json.dump(all_embeddings, fw, ensure_ascii=False, indent=2)

    print(f"✅ Saved {len(all_embeddings)} embeddings to {args.output_file.resolve()}")

if __name__ == "__main__":
    main()
