#!/usr/bin/env python3
"""
日本語テキストを文境界ベースでチャンク化するスクリプト
- CLI対応（入力/出力/チャンク数指定/自動文字数計算機能）
- UTF-8日本語テキスト対応
"""
from __future__ import annotations
import argparse
from pathlib import Path
from typing import List

def split_into_chunks(
    text: str,
    chunk_size: int,
    overlap: int
) -> List[str]:
    """
    テキストを chunk_size 文字ごとにスライドウィンドウ分割。
    各チャンクは可能な限り文末(句点、疑問符、感嘆符)で切り、意味的連続性を確保。
    overlap は前チャンクとの重複文字数。
    """
    chunks: List[str] = []
    start = 0
    length = len(text)

    while start < length:
        end = start + chunk_size
        raw = text[start:end]
        # 文末で切り直し（句点“。”、疑問符“？”、感嘆符“！”優先）
        for delim in ["。", "？", "！"]:
            idx = raw.rfind(delim)
            if idx != -1 and idx > len(raw) * 0.5:
                raw = raw[:idx + 1]
                break
        chunks.append(raw)
        start = start + chunk_size - overlap

    return chunks


def main() -> None:
    parser = argparse.ArgumentParser(
        description="日本語テキストを文境界ベースでチャンク化するスクリプト"
    )
    parser.add_argument(
        "-i", "--input-file", type=Path,
        default=Path("raw/term_cleaned.txt"),
        help="前処理済みテキスト (default: raw/term_cleaned.txt)"
    )
    parser.add_argument(
        "-o", "--output-dir", type=Path,
        default=Path("raw/chunks"),
        help="チャンク出力ディレクトリ (default: raw/chunks)"
    )
    parser.add_argument(
        "-s", "--chunk-size", type=int,
        default=250,
        help="1チャンクあたりの文字数 (default: 250)。--num-chunks指定時は無視"
    )
    parser.add_argument(
        "-l", "--overlap", type=int,
        default=50,
        help="チャンク間重複文字数 (default: 50)"
    )
    parser.add_argument(
        "-n", "--num-chunks", type=int, default=None,
        help="分割後のチャンク数目標。指定すると chunk-size を自動計算"
    )
    args = parser.parse_args()

    text = args.input_file.read_text(encoding="utf-8")

    # --num-chunks 指定があれば chunk_size を自動計算
    if args.num_chunks:
        total_len = len(text)
        approx = (total_len + args.overlap) / args.num_chunks
        chunk_size = max(int(approx), 1)
        print(f"→ num_chunks={args.num_chunks} から自動計算した chunk_size={chunk_size}")
    else:
        chunk_size = args.chunk_size

    chunks = split_into_chunks(text, chunk_size, args.overlap)
    print(f"✅ 全部で {len(chunks)} チャンクに分割されました")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    # まとめファイル
    all_path = args.output_dir / "all_chunks.txt"
    with all_path.open("w", encoding="utf-8") as wf:
        for i, c in enumerate(chunks, 1):
            wf.write(f"--- CHUNK {i} ---\n{c}\n\n")

    # 個別ファイル
    for i, c in enumerate(chunks, 1):
        (args.output_dir / f"chunk_{i:04}.txt").write_text(c, encoding="utf-8")

    print(f"✅ チャンクを {args.output_dir} に保存しました")

if __name__ == "__main__":
    main()
