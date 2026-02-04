# PLAN.md - DTF:FTL (Daily Tech Feed: From The Labs)

## Status: PLANNING
**Last Updated:** 2026-02-04

## Goals
- Scaffold DTF:FTL by cloning the dtfhn structure and adapting it for AI/Singularity sources.
- Preserve the pipeline pattern: fetch → LanceDB → script generation → TTS → stitch → R2 upload.
- Provide working local stubs so the pipeline can run in `--test` mode without external services.

## Scope (This Iteration)
- Mirror dtfhn directory structure with minimal, functional modules and scripts.
- Implement source fetcher stubs:
  - Reddit (r/singularity, r/LocalLLaMA, r/Accelerate)
  - AlphaXiv trending prefilter
  - Luminaries (Twitter/blogs) stub
- Implement pipeline skeleton that:
  - Loads stories from stubs
  - Stores to LanceDB when available (optional)
  - Generates simple scripts and interstitials
  - Writes an episode manifest + episode text
- Provide README + CLAUDE project conventions.
- Add basic tests to validate stubbed pipeline output.

## Non-Goals (This Iteration)
- Real Reddit/AlphaXiv API integrations
- Full TTS / R2 upload integration
- High-quality script generation

## Deliverables
1. `PLAN.md` (this file)
2. Directory structure mirroring dtfhn
3. Stubbed source fetchers (Reddit API, AlphaXiv, luminaries)
4. `CLAUDE.md` with rules/lessons
5. `README.md` with project overview and usage

## Implementation Plan
1. **Scaffold structure**
   - Create `src/`, `scripts/`, `templates/`, `docs/`, `test/`, `tests/`, `characters/`, `research/` to match dtfhn layout.
   - Add `.gitkeep` where needed.

2. **Core modules**
   - `src/models.py`: shared dataclasses (Story, SourceMeta).
   - `src/reddit.py`: stubbed reddit fetcher returning Story list.
   - `src/alphaxiv.py`: stubbed trending fetcher.
   - `src/luminaries.py`: stubbed twitter/blog fetcher.
   - `src/storage.py`: thin LanceDB wrapper with JSON fallback for test mode.
   - `src/generator.py`: simple script + interstitial generator.
   - `src/tts.py`: placeholder client with a no-op test mode.
   - `src/audio.py`: placeholder stitch/transcode stubs.
   - `src/pipeline.py`: orchestrates full pipeline with `--test` and `--no-store` options.

3. **Scripts**
   - `scripts/scrape_and_load.py`: fetch + store stories.
   - `scripts/generate_episode_audio.py`: stub TTS + stitch.
   - `scripts/run_episode.sh`: shell entrypoint mirroring dtfhn.
   - `scripts/upload_to_r2.py`: stub upload.

4. **Docs**
   - Update `README.md` for DTF:FTL.
   - Replace `CLAUDE.md` with new conventions and lessons.

5. **Verify**
   - Run a local test: `python -m src.pipeline --test --no-store`.
   - Run pytest for minimal test coverage.

## Risks / Unknowns
- LanceDB availability in the environment; will keep fallback storage.
- Actual API clients and auth for Reddit/AlphaXiv/Twitter will be added later.

