#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pprint import pprint

def main():
    parser = argparse.ArgumentParser(
        description="JSON埋め込みファイルをPythonモジュールに変換"
    )
    parser.add_argument(
        "input_json",
        nargs="?",
        default=os.path.join("raw", "embeddings_full.json"),
        help="読み込みたい JSON ファイル (default: raw/embeddings_full.json)"
    )
    parser.add_argument(
        "-o", "--output",
        default="embeddings_data.py",
        help="出力 Python モジュール名 (default: embeddings_data.py)"
    )
    args = parser.parse_args()

    if not os.path.exists(args.input_json):
        print(f"Error: 入力ファイルが見つかりません → {args.input_json}", file=sys.stderr)
        sys.exit(1)

    data = json.load(open(args.input_json, encoding="utf-8"))

    if os.path.exists(args.output):
        os.rename(args.output, args.output + ".bak")

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(f"# Auto-generated from {os.path.basename(args.input_json)}\n")
        f.write("embeddings = ")
        pprint(data, stream=f, width=120)
        f.write("\n")

    print(f"→ `{args.output}` を生成しました。")

if __name__ == "__main__":
    main()
