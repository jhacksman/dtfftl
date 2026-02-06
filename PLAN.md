# PLAN.md - DTF:FTL (Daily Tech Feed: From The Labs)

## Status: INTEGRATION
**Last Updated:** 2026-02-04

## Goals
- Wire real integrations for Reddit, AlphaXiv, LanceDB embeddings, and TTS.
- Preserve dtfhn patterns for storage, script generation, and audio rendering.
- Deliver working `--live` mode with dedup + usage tracking.

## Scope (This Iteration)
- Real Reddit fetch via PRAW or httpx with 24h top/hot posts.
- Real AlphaXiv trending scraping or API integration.
- LanceDB schema + embedding generation + dedup + used-in-episode tracking.
- TTS client calling quato server and rendering WAV segments.
- Tests updated to reflect real integrations (with safe fallbacks/mocks).

## Format
**Two-host dialogue** between Stephen (mentor) and Philip (mentee):
- Stephen: stephen_fry voice — explains technical concepts, provides context
- Philip: philip_fry voice — asks clarifying questions, makes analogies

Scripts use `STEPHEN:` and `PHILIP:` prefixes. Each line is rendered separately with the appropriate voice, then stitched together.

## Non-Goals (This Iteration)
- Distribution changes (R2/publishing) beyond what already exists.

## Deliverables
1. Working `--live` mode with real data sources
2. LanceDB storage with embeddings + dedup + usage tracking
3. TTS client that renders WAV segments
4. Updated `CLAUDE.md` with patterns + lessons
5. All tests passing

## Implementation Plan
1. **Study dtfhn patterns**
   - Identify Reddit, LanceDB, embeddings, and TTS client implementations.

2. **Reddit integration**
   - Implement real fetch with rate limit handling and 24h filters.
   - Add config entries for `REDDIT_CLIENT_ID` and `REDDIT_CLIENT_SECRET`.

3. **AlphaXiv integration**
   - Implement trending scrape/API with required fields.

4. **LanceDB + embeddings**
   - Mirror dtfhn schema and embedding generation.
   - Add URL/arxiv_id dedup and used-in-episode tracking.

5. **TTS client**
   - Implement quato `/speak` client with multi-voice support
   - Parse scripts for STEPHEN:/PHILIP: prefixes
   - Route to stephen_fry or philip_fry voices accordingly
   - Stitch segments in order with brief pauses

6. **Verify**
   - Run tests and live-mode smoke test.

7. **Document**
   - Update `CLAUDE.md` with patterns and lessons.

## Risks / Unknowns
- AlphaXiv may lack an official API; scraping could change.
- Reddit auth limits or misconfigured credentials in env.
