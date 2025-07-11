# ragPromptBuilder.py
"""
RAG Prompt Builder — Step 2
===========================
Generates a ChatCompletion‑compatible messages array from a user question
plus retrieval context obtained via `search_embeddings.chunk_search`.

Public API
----------
build_prompt(question: str, top_k: int = 3) -> dict
    Returns {"messages": List[dict], "chunks": List[dict]} where:
      • messages: ready for openai.ChatCompletion.create(...)
      • chunks  : retrieval results (for debugging/logging)

Usage example
-------------
from ragPromptBuilder import build_prompt
pkg = build_prompt("根尖病変の治療は？")
openai.ChatCompletion.create(model="gpt-4o-mini", messages=pkg["messages"])
"""
from __future__ import annotations

import argparse
import importlib
import json
import re
import sys
from pathlib import Path
from typing import List, Dict, Any
from openai import OpenAI
from .qa_utils import get_answer

client = OpenAI()


def generate_query(question: str) -> str:
    sys_prompt = "あなたは検索クエリを生成するアシスタントです。ユーザーの質問から最適な検索クエリを日本語で1文で返してください。"
    messages = [
        {"role": "system", "content": sys_prompt},
        {"role": "user", "content": question},
    ]
    return (
        client.chat.completions.create(
            model="gpt-4.1-nano",
            messages=messages,
            temperature=0,
        )
        .choices[0]
        .message.content.strip()
    )

# --------------------------------------------------------------------------- #
# Try importing `chunk_search` (required)
# --------------------------------------------------------------------------- #
try:
    from search_embeddings import chunk_search  # type: ignore
except ImportError as import_err:
    # Attempt dynamic reload (helps when running from different CWDs)
    spec = importlib.util.find_spec("search_embeddings")
    if spec is None:
        msg = (
            "❌ `search_embeddings.py` が見つからないか、"
            "Python パスにありません。ファイルの配置か PYTHONPATH を確認してください。"
        )
        raise ImportError(msg) from import_err
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore
    if not hasattr(module, "chunk_search"):
        msg = (
            "❌ `search_embeddings.py` に `chunk_search` 関数が定義されていません。\n"
            "README のインターフェースに従って実装してください。"
        )
        raise ImportError(msg) from import_err
    chunk_search = getattr(module, "chunk_search")  # type: ignore

# --------------------------------------------------------------------------- #
# Helper
# --------------------------------------------------------------------------- #
DEFAULT_TOP_K = 2

_WS_RE = re.compile(r"[ \t\r\n]+")


def _collapse_ws(text: str) -> str:
    """Collapse consecutive whitespace to a single space for compact prompts."""
    return _WS_RE.sub(" ", text).strip()


# --------------------------------------------------------------------------- #
# Public API
# --------------------------------------------------------------------------- #
def build_prompt(question: str, top_k: int = DEFAULT_TOP_K) -> Dict[str, Any]:
    """
    Build a retrieval‑augmented prompt package.

    Parameters
    ----------
    question : str
        User's question in Japanese.
    top_k : int, optional
        Number of chunks to retrieve (default: 3).

    Returns
    -------
    dict
        {
          "messages": list[dict],  # for ChatCompletion
          "chunks":   list[dict],  # raw retrieval results
        }
    """
    # 1) retrieve
    q1 = generate_query(question)
    chunks: List[Dict[str, Any]] = chunk_search(q1, top_k=top_k)

    # 2) format retrieval context block
    context_lines: List[str] = []
    for ck in chunks:
        ans = get_answer(ck["id"])
        tag = ck["id"]
        body_q = _collapse_ws(ck["Q"])
        body_a = _collapse_ws(ans)
        context_lines.append(f"{tag}\nQ: {body_q}\nA: {body_a}")

    retrieval_block = "\n".join(context_lines)

    # 3) build messages
    sys_prompt = (
        "あなたはDentAssist-GPT、歯科に特化したプロフェッショナルアシスタントです。 "
        "ユーザーの質問には日本語で歯科に関する内容のみ厳密に答えてください。 "
        "回答は簡潔な箇条書き（•）で行い、合計200トークン以内にしてください。 "
        "質問が歯科以外の場合は、正確に以下のように応答してください\n"
        "「申し訳ありません。そのご質問にはお答えできません。」"
    )

    messages: List[Dict[str, str]] = [
        {"role": "system", "content": sys_prompt},
        {"role": "assistant", "name": "retrieval_context", "content": retrieval_block},
        {"role": "user", "content": question},
    ]

    return {"messages":messages, "chunks": chunks}


# --------------------------------------------------------------------------- #
# CLI entry point
# --------------------------------------------------------------------------- #
def _cli() -> None:
    parser = argparse.ArgumentParser(description="RAG Prompt Builder CLI")
    parser.add_argument("question", nargs="*", help="User question")
    parser.add_argument("--top_k", type=int, default=DEFAULT_TOP_K, help="retrieval k")
    args = parser.parse_args()

    if args.question:
        q = " ".join(args.question)
    else:
        q = input("質問を入力してください: ").strip()

    pkg = build_prompt(q, top_k=args.top_k)
    print(json.dumps(pkg, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _cli()