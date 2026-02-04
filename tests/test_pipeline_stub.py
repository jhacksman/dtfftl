from __future__ import annotations

import datetime as dt

from src import pipeline


def test_pipeline_stub_creates_episode(tmp_path, monkeypatch):
    monkeypatch.setattr(pipeline, "EPISODES_DIR", tmp_path)
    episode_date = dt.date(2026, 2, 4)
    episode_dir = pipeline.run_pipeline(episode_date=episode_date, use_stub=True, store=False)

    assert episode_dir.exists()
    assert (episode_dir / "episode.txt").exists()
    assert (episode_dir / "manifest.json").exists()
    assert any(episode_dir.glob("*intro.txt"))
    assert any(episode_dir.glob("*outro.txt"))
