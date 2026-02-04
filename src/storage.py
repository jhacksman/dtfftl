"""Storage layer for DTF:FTL.

Uses LanceDB when available; falls back to JSON for stub/testing.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional

import pyarrow as pa

from dataclasses import asdict

from .models import Story
from .embeddings import EMBEDDING_DIM, embed_batch, embed_text, get_db

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
FALLBACK_STORIES = DATA_DIR / "stories.json"
FALLBACK_EPISODES = DATA_DIR / "episodes.json"


SCHEMA_VERSION = 1


class StorageUnavailable(RuntimeError):
    pass


STORIES_SCHEMA = pa.schema([
    pa.field("id", pa.string()),
    pa.field("source", pa.string()),
    pa.field("title", pa.string()),
    pa.field("url", pa.string()),
    pa.field("arxiv_id", pa.string()),
    pa.field("summary", pa.string()),
    pa.field("raw_text", pa.string()),
    pa.field("score", pa.int32()),
    pa.field("comments", pa.int32()),
    pa.field("subreddit", pa.string()),
    pa.field("author", pa.string()),
    pa.field("created_utc", pa.string()),
    pa.field("fetched_at", pa.string()),
    pa.field("selftext", pa.string()),
    pa.field("comments_summary", pa.string()),
    pa.field("discussion_highlights", pa.string()),
    pa.field("used_in_episode", pa.bool_()),
    pa.field("used_episode_date", pa.string()),
    pa.field("schema_version", pa.int32()),
    pa.field("vector", pa.list_(pa.float32(), EMBEDDING_DIM)),
])

EPISODES_SCHEMA = pa.schema([
    pa.field("episode_date", pa.string()),
    pa.field("episode_text", pa.string()),
    pa.field("manifest", pa.string()),
    pa.field("generated_at", pa.string()),
    pa.field("schema_version", pa.int32()),
    pa.field("vector", pa.list_(pa.float32(), EMBEDDING_DIM)),
])


def _table_names(db) -> list[str]:
    result = db.list_tables()
    if hasattr(result, "tables"):
        return result.tables
    return list(result)


def _try_get_db():
    try:
        return get_db()
    except Exception:
        return None


def _safe_value(value: str) -> str:
    return value.replace("'", "''")


def _story_lookup_filter(story: Story) -> Optional[str]:
    clauses = []
    if story.id:
        clauses.append(f"id = '{_safe_value(story.id)}'")
    if story.source_url:
        clauses.append(f"url = '{_safe_value(story.source_url)}'")
    arxiv_id = story.source_meta.extra.get("arxiv_id")
    if arxiv_id:
        clauses.append(f"arxiv_id = '{_safe_value(arxiv_id)}'")
    return " OR ".join(clauses) if clauses else None


def _story_to_row(story: Story, vector: list[float], used_episode_date: str | None) -> dict:
    meta = story.source_meta
    created = meta.extra.get("created_utc")
    return {
        "id": story.id,
        "source": meta.source,
        "title": story.title,
        "url": story.source_url,
        "arxiv_id": meta.extra.get("arxiv_id"),
        "summary": story.summary,
        "raw_text": story.raw_text,
        "score": meta.score or 0,
        "comments": meta.comments or 0,
        "subreddit": meta.subreddit,
        "author": meta.author,
        "created_utc": created,
        "fetched_at": datetime.utcnow().isoformat(),
        "selftext": meta.extra.get("selftext"),
        "comments_summary": meta.extra.get("comments_summary"),
        "discussion_highlights": meta.extra.get("discussion_highlights"),
        "used_in_episode": used_episode_date is not None,
        "used_episode_date": used_episode_date,
        "schema_version": SCHEMA_VERSION,
        "vector": vector,
    }


def _update_story_usage(table, existing: dict, used_episode_date: str) -> None:
    existing["used_in_episode"] = True
    existing["used_episode_date"] = used_episode_date
    story_id = existing.get("id")
    if story_id:
        table.delete(f"id = '{_safe_value(story_id)}'")
    table.add([existing])


def store_stories_batch(
    stories: Iterable[Story],
    episode_date: str,
    use_lancedb: bool = True,
    mark_used: bool = True,
) -> None:
    """Store stories in LanceDB or JSON fallback."""
    stories = list(stories)
    if use_lancedb:
        db = _try_get_db()
        if db is None:
            raise StorageUnavailable("LanceDB not available. Install dependencies or use fallback.")

        table = db.open_table("stories") if "stories" in _table_names(db) else db.create_table(
            "stories",
            schema=STORIES_SCHEMA,
        )

        new_stories: list[Story] = []
        for story in stories:
            lookup = _story_lookup_filter(story)
            if lookup:
                existing = table.search().where(lookup, prefilter=True).limit(1).to_list()
            else:
                existing = []

            if existing:
                if mark_used and not existing[0].get("used_in_episode"):
                    _update_story_usage(table, existing[0], episode_date)
                continue
            new_stories.append(story)

        if new_stories:
            embed_texts = [
                (s.raw_text or s.summary or s.title or "").strip() for s in new_stories
            ]
            try:
                vectors = embed_batch(embed_texts)
            except Exception as exc:
                raise StorageUnavailable(f"Embedding generation failed: {exc}") from exc
            rows = [
                _story_to_row(story, vector, episode_date if mark_used else None)
                for story, vector in zip(new_stories, vectors)
            ]
            table.add(rows)
        return

    # Fallback JSON storage
    payload = {"episode_date": episode_date, "stories": [asdict(story) for story in stories]}
    FALLBACK_STORIES.parent.mkdir(parents=True, exist_ok=True)
    FALLBACK_STORIES.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def store_episode(episode_date: str, episode_text: str, manifest: dict, use_lancedb: bool = True) -> None:
    """Store episode metadata in LanceDB or JSON fallback."""
    if use_lancedb:
        db = _try_get_db()
        if db is None:
            raise StorageUnavailable("LanceDB not available. Install dependencies or use fallback.")

        table = db.open_table("episodes") if "episodes" in _table_names(db) else db.create_table(
            "episodes",
            schema=EPISODES_SCHEMA,
        )
        try:
            vector = embed_text(episode_text)
        except Exception as exc:
            raise StorageUnavailable(f"Embedding generation failed: {exc}") from exc
        table.add(
            [{
                "episode_date": episode_date,
                "episode_text": episode_text,
                "manifest": json.dumps(manifest),
                "generated_at": datetime.utcnow().isoformat(),
                "schema_version": SCHEMA_VERSION,
                "vector": vector,
            }]
        )
        return

    payload = {"episode_date": episode_date, "episode_text": episode_text, "manifest": manifest}
    FALLBACK_EPISODES.parent.mkdir(parents=True, exist_ok=True)
    FALLBACK_EPISODES.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def list_stories_json() -> Optional[dict]:
    if not FALLBACK_STORIES.exists():
        return None
    return json.loads(FALLBACK_STORIES.read_text(encoding="utf-8"))
