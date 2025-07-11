import json
from functools import lru_cache
from pathlib import Path
from typing import Dict

EMBEDDINGS_FILE = Path(__file__).with_suffix("").parent / "raw" / "embeddings_full.json"

@lru_cache(maxsize=1)
def load_qa_map() -> Dict[str, Dict[str, str]]:
    with EMBEDDINGS_FILE.open(encoding="utf-8") as f:
        data = json.load(f)
    return {item["id"]: {"Q": item["Q"], "A": item["A"]} for item in data}


def get_answer(chunk_id: str) -> str:
    return load_qa_map().get(chunk_id, {}).get("A", "")
