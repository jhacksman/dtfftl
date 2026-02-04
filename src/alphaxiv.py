"""AlphaXiv trending fetcher."""

from __future__ import annotations

import datetime as dt
import re
import time
from typing import Optional
import xml.etree.ElementTree as ET

from .models import Story, SourceMeta


def fetch_trending(limit: int = 5, use_stub: bool = True) -> list[Story]:
    """Fetch trending AlphaXiv threads (stub)."""
    if not use_stub:
        html = _fetch_explore_html()
        if not html:
            return []
        entries = _parse_trending_html(html, limit=limit)
        if not entries:
            return []

        arxiv_ids = [entry["arxiv_id"] for entry in entries if entry.get("arxiv_id")]
        abstracts = _fetch_arxiv_abstracts(arxiv_ids)

        stories: list[Story] = []
        for entry in entries:
            arxiv_id = entry.get("arxiv_id")
            abstract = abstracts.get(arxiv_id, "")
            abstract_snippet = abstract[:500].strip() if abstract else ""
            discussion = entry.get("discussion_highlights", "")
            summary = abstract_snippet or discussion or entry["title"]
            meta = SourceMeta(
                source="alphaxiv",
                score=entry.get("score"),
                comments=None,
                url=entry.get("url"),
                extra={
                    "arxiv_id": arxiv_id,
                    "abstract_snippet": abstract_snippet,
                    "discussion_highlights": discussion,
                },
            )
            stories.append(
                Story(
                    id=f"alphaxiv-{arxiv_id}" if arxiv_id else f"alphaxiv-{entry['title']}",
                    title=entry["title"],
                    summary=summary,
                    source_url=entry.get("url", ""),
                    source_meta=meta,
                    raw_text="\n\n".join([t for t in (abstract_snippet, discussion) if t]),
                    tags=["alphaxiv", "arxiv"],
                )
            )
        return stories

    now = dt.datetime.utcnow().strftime("%Y-%m-%d")
    stories: list[Story] = []
    for idx in range(limit):
        story_id = f"alphaxiv-{idx}"
        title = f"AlphaXiv trending paper {idx + 1}"
        summary = "Stub summary for AlphaXiv trending paper discussion."
        source_url = f"https://alphaxiv.org/abs/0000.{idx:05d}"
        meta = SourceMeta(
            source="alphaxiv",
            author="anon",
            score=50 - idx,
            comments=5 + idx,
            url=source_url,
            extra={"date": now, "arxiv_id": f"0000.{idx:05d}"},
        )
        stories.append(
            Story(
                id=story_id,
                title=title,
                summary=summary,
                source_url=source_url,
                source_meta=meta,
                raw_text=summary,
                tags=["stub", "alphaxiv"],
            )
        )

    return stories


def _fetch_explore_html(retries: int = 3) -> Optional[str]:
    import requests

    url = "https://www.alphaxiv.org/explore"
    headers = {"User-Agent": "dtfftl/0.1 (alphaxiv scraper)"}
    for attempt in range(retries):
        try:
            resp = requests.get(url, timeout=20, headers=headers)
            if resp.status_code == 200:
                return resp.text
            time.sleep(1 + attempt)
        except Exception:
            time.sleep(1 + attempt)
    return None


def _parse_trending_html(html: str, limit: int) -> list[dict]:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    results: list[dict] = []
    seen_ids: set[str] = set()

    anchors = soup.find_all("a", href=re.compile(r"^/abs/\\d{4}\\.\\d{4,5}"))
    for anchor in anchors:
        title_div = anchor.find("div", class_=lambda c: c and "tiptap" in c and "html-renderer" in c)
        if not title_div:
            continue
        title = title_div.get_text(" ", strip=True)
        href = anchor.get("href") or ""
        arxiv_match = re.search(r"/abs/(\\d{4}\\.\\d{4,5})", href)
        if not arxiv_match:
            continue
        arxiv_id = arxiv_match.group(1)
        if arxiv_id in seen_ids:
            continue

        card = anchor.find_parent("div", class_=lambda c: c and "rounded-xl" in c)
        discussion = ""
        score = None
        if card:
            summary_p = card.find("p", class_=lambda c: c and "line-clamp-4" in c)
            if summary_p:
                discussion = summary_p.get_text(" ", strip=True)
            score = _extract_vote_score(card)

        results.append(
            {
                "title": title,
                "arxiv_id": arxiv_id,
                "url": f"https://www.alphaxiv.org/abs/{arxiv_id}",
                "discussion_highlights": discussion,
                "score": score,
            }
        )
        seen_ids.add(arxiv_id)
        if len(results) >= limit:
            break

    return results


def _extract_vote_score(card) -> Optional[int]:
    for button in card.find_all("button"):
        text = button.get_text(" ", strip=True)
        match = re.search(r"\\b(\\d+)\\b", text)
        if match:
            try:
                return int(match.group(1))
            except ValueError:
                continue
    return None


def _fetch_arxiv_abstracts(arxiv_ids: list[str]) -> dict[str, str]:
    if not arxiv_ids:
        return {}
    import requests
    base = "https://export.arxiv.org/api/query?id_list="
    url = base + ",".join(arxiv_ids)
    try:
        resp = requests.get(url, timeout=20)
        resp.raise_for_status()
    except Exception:
        return {}

    try:
        root = ET.fromstring(resp.text)
    except Exception:
        return {}

    ns = {"atom": "http://www.w3.org/2005/Atom"}
    abstracts: dict[str, str] = {}
    for entry in root.findall("atom:entry", ns):
        id_elem = entry.find("atom:id", ns)
        summary_elem = entry.find("atom:summary", ns)
        if id_elem is None or summary_elem is None:
            continue
        arxiv_id = id_elem.text.rsplit("/", 1)[-1] if id_elem.text else None
        if not arxiv_id:
            continue
        summary = summary_elem.text.strip() if summary_elem.text else ""
        abstracts[arxiv_id] = " ".join(summary.split())
    return abstracts
