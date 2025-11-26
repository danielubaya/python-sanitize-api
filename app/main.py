import re
from pathlib import Path
from typing import Iterable, List

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="Sanitize API")

BANNED_PATH = Path(__file__).resolve().parent / "banned_words.txt"

def load_banned_words() -> List[str]:
    if not BANNED_PATH.exists():
        return []
    return [
        line.strip()
        for line in BANNED_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.strip().startswith("#")
    ]

DEFAULT_BANNED = load_banned_words()

def _mask_keep_first_last(matched_text: str) -> str:
    n = len(matched_text)
    if n <= 2:
        return "*" * n
    return matched_text[0] + ("*" * (n - 2)) + matched_text[-1]

def sanitize(text: str, banned_words: Iterable[str]) -> str:
    if text is None:
        raise ValueError("text must not be None")

    cleaned = text
    words = [w.strip() for w in banned_words if (w or "").strip()]

    for w in words:
        pattern = re.compile(re.escape(w), re.IGNORECASE)
        cleaned = pattern.sub(lambda m: _mask_keep_first_last(m.group(0)), cleaned)

    return cleaned

class SanitizeRequest(BaseModel):
    text: str = Field(..., min_length=1)

@app.post("/sanitize")
def sanitize_endpoint(req: SanitizeRequest):
    return {"cleaned": sanitize(req.text, DEFAULT_BANNED)}
