"""
Vector embeddings for DTF:FTL.
Uses sentence-transformers by default, with an optional OpenAI fallback.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional, TYPE_CHECKING
import os

PROJECT_ROOT = Path(__file__).parent.parent
VECTORS_DIR = PROJECT_ROOT / "data" / "vectors"

EMBEDDING_MODEL = "BAAI/bge-large-en-v1.5"
EMBEDDING_DIM = 1024

_model = None
if TYPE_CHECKING:
    import lancedb

_db_connection: Optional["lancedb.DBConnection"] = None


def _get_device() -> str:
    try:
        import torch
    except Exception:
        return "cpu"

    if torch.backends.mps.is_available():
        return "mps"
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"


def _get_model():
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer

        device = _get_device()
        print(f"Loading embedding model on {device}...")
        _model = SentenceTransformer(EMBEDDING_MODEL, device=device)
        print(f"Model loaded: {EMBEDDING_MODEL}")
    return _model


def get_db() -> "lancedb.DBConnection":
    global _db_connection
    if _db_connection is None:
        import lancedb

        VECTORS_DIR.mkdir(parents=True, exist_ok=True)
        _db_connection = lancedb.connect(str(VECTORS_DIR))
    return _db_connection


def _embed_with_openai(texts: list[str]) -> list[list[float]]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set for OpenAI embeddings.")

    try:
        from openai import OpenAI
    except Exception as exc:
        raise RuntimeError("OpenAI client not installed. Install `openai` or use sentence-transformers.") from exc

    client = OpenAI(api_key=api_key)
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=texts,
    )
    return [item.embedding for item in response.data]


def embed_batch(texts: list[str], show_progress: bool = False) -> list[list[float]]:
    if not texts:
        return []

    prefer_openai = os.environ.get("DTFFTL_EMBEDDINGS", "").lower() == "openai"
    if prefer_openai:
        return _embed_with_openai(texts)

    model = _get_model()
    show_bar = show_progress or len(texts) > 50
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=show_bar)
    return [e.tolist() for e in embeddings]


def embed_text(text: str) -> list[float]:
    embeddings = embed_batch([text])
    return embeddings[0] if embeddings else []


def search(table: lancedb.table.Table, query: str, top_k: int = 10) -> list[dict]:
    vector = embed_text(query)
    results = table.search(vector).limit(top_k).to_list()
    return results
