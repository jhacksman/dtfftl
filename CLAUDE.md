# CLAUDE.md — DTF:FTL (From The Labs)

## Project Overview

**DTF:FTL** — "From The Labs: Dispatches from the edge"

AI/Singularity news roundup from Reddit communities and tech luminaries. Part of the Daily Tech Feed podcast network.

## Status: PLANNING

Boris Method Phase 1 (PLAN) in progress. No code yet.

---

## Boris Method (MANDATORY)

Every task in this repo follows the Boris Cherny method:

### 1. PLAN
- Write out your approach before coding
- Document what you're going to build and why
- Identify risks and unknowns

### 2. APPROVE  
- Get sign-off from owner before execution
- Don't start coding without explicit approval
- Complex changes need discussion first

### 3. EXECUTE
- Implement the approved plan
- Commit early, commit often
- One logical change per commit

### 4. VERIFY
- Test that it works
- Listen to generated audio
- Validate data quality

### 5. DOCUMENT
- Update this file with lessons learned
- Document gotchas and edge cases
- Keep README.md current

**Full docs:** https://github.com/jhacksman/boris-method

---

## Git Discipline (MANDATORY)

- **Commit after each logical change**
- **Meaningful commit messages** — describe what and why
- **Never commit secrets** — no API keys, tokens, .env files
- **Git always** — even for experiments

---

## Source Configuration

### Subreddits (data/subreddits.json)
```json
{
  "high_priority": ["singularity", "LocalLLaMA", "Accelerate"],
  "medium_priority": ["MachineLearning", "artificial", "StableDiffusion"],
  "low_priority": ["ControlProblem", "mlscaling"]
}
```

### Luminaries (data/luminaries.json)
```json
{
  "twitter": ["kaborathy", "ylecun", "ESYudkowsky", ...],
  "blogs": ["gwern.net", "lesswrong.com", ...]
}
```

---

## Architecture Notes

See README.md for full architecture diagram.

Key components:
1. **Collectors** — Reddit, Twitter, RSS scrapers
2. **Scorer** — Normalize and rank stories
3. **Selector** — Pick top N, balance categories
4. **Generator** — Claude CLI for scripts
5. **Renderer** — TTS via quato
6. **Publisher** — R2 + RSS feed

---

## Integration with DTF Network

- **TTS Server:** quato (192.168.0.134:7849) — shared with DTFHN, DTFRF
- **Hosting:** Cloudflare R2 (dtf-podcasts bucket)
- **Website:** podcast.pdxh.org (add /dtfftl route)
- **Voice:** TBD — may reuse forbin or create new

---

## Lessons Learned

(None yet — project just started)

### From DTFHN
- Gold master rule: never overwrite published MP3s
- Website rebuild required after every feed update
- TTS server can hang — need retry logic

### From DTFRF
- Pause durations from actual data, not distributions
- Word count targets must match actual Lynch (~450 words, not 93)
- STT verification before merge catches errors

---

## Open Decisions

- [ ] Daily or weekly frequency?
- [ ] Voice/character?
- [ ] Story count per episode?
- [ ] Overlap handling with HN?

---

## File Locations (When Built)

| Component | Path |
|-----------|------|
| Reddit scraper | scripts/collect_reddit.py |
| Twitter scraper | scripts/collect_twitter.py |
| Blog aggregator | scripts/collect_blogs.py |
| Scorer | scripts/score_stories.py |
| Script generator | scripts/generate_script.py |
| TTS renderer | scripts/render_episode.py |
| Pipeline | scripts/run_episode.sh |
| Stories DB | data/stories.db |
| Episodes | episodes/ |
| Feed | feed.xml |
