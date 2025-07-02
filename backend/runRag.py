#!/usr/bin/env python3
"""
runRag.py — Dental RAG entry-point (OpenAI v0.x / v1.x 両対応版)
==============================================================
1. 受け取った質問を `ragPromptBuilder.build_prompt()` で RAG プロンプト化。
2. OpenAI API へ送信し回答を取得（v0.x・v1.x 自動判別）。
3. `--debug` でプロンプト & 検索チャンクを JSON 表示。

Usage
-----
```bash
$ python runRag.py "根尖病変の治療は？"
$ python runRag.py "睡眠時無呼吸症候群とは" --top_k 2 --debug
```
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import List, Dict, Any, Callable

# --------------------------------------------------------------------------- #
# OpenAI version-agnostic import helper
# --------------------------------------------------------------------------- #
try:
    # v1.x 系 (openai>=1.0.0)
    from openai import OpenAI  # type: ignore

    _client = OpenAI()

    def _chat_completion_v1(
        messages: List[Dict[str, str]], *, model: str, temperature: float, timeout: int
    ) -> str:
        resp = _client.chat.completions.create(
            model=model,
            messages=messages,
            temperature=temperature,
            timeout=timeout,
        )
        return resp.choices[0].message.content.strip()

    _call_chat: Callable[..., str] = _chat_completion_v1

except ImportError:
    try:
        # v0.x 系 (openai<=0.28)
        import openai  # type: ignore

        def _chat_completion_v0(
            messages: List[Dict[str, str]], *, model: str, temperature: float, timeout: int
        ) -> str:
            resp = openai.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                request_timeout=timeout,
            )
            return resp.choices[0].message["content"].strip()  # type: ignore[index]

        _call_chat = _chat_completion_v0  # type: ignore[assignment]

    except ImportError:
        sys.stderr.write(
            "❌ openai パッケージが見つかりません。\n    `pip install openai` を実行してください。\n"
        )
        sys.exit(1)

# --------------------------------------------------------------------------- #
from ragPromptBuilder import build_prompt  # 同ディレクトリ想定

# --------------------------------------------------------------------------- #
# 🔴下記からのコードを理解できない
# --------------------------------------------------------------------------- #
MODEL = "gpt-4.1-nano"
TEMPERATURE = 0.1
TIMEOUT = 30  # 秒
MAX_RETRIES = 1

# --------------------------------------------------------------------------- #
# Utility: RAG を呼び出す関数
# --------------------------------------------------------------------------- #
def ask_rag(question: str, top_k: int = 3) -> str:
    """
    質問文字列を受け取り、RAG の回答を返すユーティリティ関数。
    FastAPI からはこちらを呼び出します。
    """
    # 1) プロンプトとチャンクの取得
    pkg = build_prompt(question, top_k=top_k)
    messages = pkg["messages"]

    # 2) GPT 呼び出し（リトライなし）
    answer = _call_chat(
        messages,
        model=MODEL,
        temperature=TEMPERATURE,
        timeout=TIMEOUT,
    )
    return answer

# --------------------------------------------------------------------------- #
# CLI entry point
# --------------------------------------------------------------------------- #

def main() -> None:
    parser = argparse.ArgumentParser(description="Dental RAG — run with GPT-4o-nano")
    parser.add_argument(
        "question", nargs="*", help="質問文を直接指定 (複数語可)"
    )
    parser.add_argument(
        "--top_k", type=int, default=3, help="retrieval chunk 数 (default: 3)"
    )
    parser.add_argument(
        "--debug", action="store_true", help="プロンプトとチャンクを表示"
    )
    args = parser.parse_args()

    # 1) 質問取得
    if args.question:
        question = " ".join(args.question)
    else:
        question = input("質問を入力してください: ").strip()

    if not question:
        print("質問が空です。終了します。")
        sys.exit(0)

    # 2) プロンプト生成
    pkg: Dict[str, Any] = build_prompt(question, top_k=args.top_k)
    messages: List[Dict[str, str]] = pkg["messages"]

    if args.debug:
        print("\n----- Retrieval Chunks -----")
        print(json.dumps(pkg["chunks"], ensure_ascii=False, indent=2))
        print("\n----- Prompt (messages) -----")
        print(json.dumps(messages, ensure_ascii=False, indent=2))
        print("----------------------------\n")

    # 3) GPT 呼び出し（簡易リトライ）
    last_error: Exception | None = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            answer = _call_chat(
                messages,
                model=MODEL,
                temperature=TEMPERATURE,
                timeout=TIMEOUT,
            )
            break
        except Exception as e:  # pylint: disable=broad-except
            last_error = e
            sys.stderr.write(
                f"⚠️  API error, retrying ({attempt + 1}/{MAX_RETRIES})…\n    {e}\n"
            )
    else:
        sys.stderr.write(f"❌ OpenAI API 呼び出しに失敗しました:\n{last_error}\n")
        sys.exit(1)

    # 4) 出力
    print("\n=== 回答 ===")
    print(answer)


if __name__ == "__main__":
    if os.getenv("OPENAI_API_KEY") is None:
        sys.stderr.write(
            "❌ OPENAI_API_KEY 環境変数が設定されていません。\n"
        )
        sys.exit(1)
    main()
