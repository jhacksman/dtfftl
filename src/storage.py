"""Storage layer for DTF:FTL.

Uses LanceDB when available; falls back to JSON for stub/testing.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Optional

from .models import Story

PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
VECTORS_DIR = DATA_DIR / "vectors"
FALLBACK_STORIES = DATA_DIR / "stories.json"
FALLBACK_EPISODES = DATA_DIR / "episodes.json"


class StorageUnavailable(RuntimeError):
    pass


def _try_get_db():
    try:
        import lancedb  # type: ignore
    except Exception:
        return None

    VECTORS_DIR.mkdir(parents=True, exist_ok=True)
    return lancedb.connect(str(VECTORS_DIR))


def store_stories_batch(stories: Iterable[Story], episode_date: str, use_lancedb: bool = True) -> None:
    """Store stories in LanceDB or JSON fallback."""
    stories = list(stories)
    if use_lancedb:
        db = _try_get_db()
        if db is None:
            raise StorageUnavailable("LanceDB not available. Install dependencies or use fallback.")

        table = db.open_table("stories") if "stories" in db.table_names() else db.create_table(
            "stories",
            data=[],
            schema=None,
            mode="overwrite",
        )

        rows = []
        for idx, story in enumerate(stories, start=1):
            rows.append(
                {
                    "episode_date": episode_date,
                    "position": idx,
                    "story_id": story.id,
                    "title": story.title,
                    "source": story.source_meta.source,
                    "url": story.source_url,
                    "summary": story.summary,
                    "raw_text": story.raw_text,
                }
            )
        if rows:
            table.add(rows)
        return

    # Fallback JSON storage
    payload = {"episode_date": episode_date, "stories": [story.__dict__ for story in stories]}
    FALLBACK_STORIES.parent.mkdir(parents=True, exist_ok=True)
    FALLBACK_STORIES.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def store_episode(episode_date: str, episode_text: str, manifest: dict, use_lancedb: bool = True) -> None:
    """Store episode metadata in LanceDB or JSON fallback."""
    if use_lancedb:
        db = _try_get_db()
        if db is None:
            raise StorageUnavailable("LanceDB not available. Install dependencies or use fallback.")

        table = db.open_table("episodes") if "episodes" in db.table_names() else db.create_table(
            "episodes",
            data=[],
            schema=None,
            mode="overwrite",
        )
        table.add(
            [
                {
                    "episode_date": episode_date,
                    "episode_text": episode_text,
                    "manifest": json.dumps(manifest),
                }
            ]
        )
        return

    payload = {"episode_date": episode_date, "episode_text": episode_text, "manifest": manifest}
    FALLBACK_EPISODES.parent.mkdir(parents=True, exist_ok=True)
    FALLBACK_EPISODES.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def list_stories_json() -> Optional[dict]:
    if not FALLBACK_STORIES.exists():
        return None
    return json.loads(FALLBACK_STORIES.read_text(encoding="utf-8"))

