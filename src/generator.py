"""Script generation stubs for DTF:FTL."""

from __future__ import annotations

import datetime as dt
from typing import Iterable

from .models import Story

TAGLINE = "Dispatches from the edge"
VOICE = "forbin"


def format_date_for_tts(date: dt.date) -> str:
    return date.strftime("%A, %B %d, %Y")


def generate_intro(episode_date: dt.date) -> str:
    date_str = format_date_for_tts(episode_date)
    return (
        f"This is DTF:FTL — {TAGLINE}. It's {date_str}. "
        "Here's what's breaking at the edge of AI and singularity research."
    )


def generate_outro() -> str:
    return (
        "That wraps DTF:FTL for today. "
        "Stay sharp, stay curious, and we'll see you tomorrow at the edge."
    )


def generate_episode_scripts(stories: Iterable[Story]) -> list[str]:
    scripts: list[str] = []
    for idx, story in enumerate(stories, start=1):
        scripts.append(
            f"Story {idx}. {story.title}. {story.summary}"
        )
    return scripts


def generate_interstitial(prev_script: str, next_script: str) -> str:
    return "Next up, another signal from the frontier."

