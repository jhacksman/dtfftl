# DTF:FTL — From The Labs

> **Dispatches from the edge**

AI and singularity news roundup sourced from Reddit communities and tech luminaries. Part of the Daily Tech Feed network.

---

## Overview

| Field | Value |
|-------|-------|
| **Full Name** | Daily Tech Feed: FTL |
| **Acronym** | DTF:FTL |
| **FTL Meaning** | From The Labs |
| **Tagline** | Dispatches from the edge |
| **Focus** | AI, ML, Singularity, Acceleration |
| **Sources** | Reddit communities + Tech luminaries |
| **Format** | Daily roundup |
| **Voice** | TBD |

---

## Sources

### Reddit Communities

Primary signal sources from the frontier of AI/ML development:

| Subreddit | Focus | Priority |
|-----------|-------|----------|
| r/singularity | General singularity news, AGI discussion | HIGH |
| r/LocalLLaMA | Open source LLMs, local deployment | HIGH |
| r/Accelerate | e/acc content, acceleration philosophy | HIGH |
| r/MachineLearning | Academic/research ML | MEDIUM |
| r/artificial | General AI news | MEDIUM |
| r/StableDiffusion | Image generation, diffusion models | MEDIUM |
| r/OpenAI | OpenAI-specific news | MEDIUM |
| r/Anthropic | Anthropic/Claude news | MEDIUM |
| r/ControlProblem | AI safety/alignment | LOW |
| r/mlscaling | Scaling laws research | LOW |

### Luminaries

Key voices worth tracking (Twitter/X, blogs, papers):

| Category | Examples |
|----------|----------|
| **Researchers** | Andrej Karpathy, Yann LeCun, Ilya Sutskever, Jan Leike |
| **e/acc** | Guillaume Verdon (@BasedBeffJezos), Martin Shkreli |
| **Safety/Alignment** | Eliezer Yudkowsky, Connor Leahy, Paul Christiano |
| **Founders/Execs** | Sam Altman, Dario Amodei, Demis Hassabis |
| **Independent** | Gwern, Simon Willison, Swyx |
| **Blogs** | LessWrong, AI Alignment Forum, company blogs |

### Signal vs Noise

Most content is crap. Filtering criteria:
- **Include:** Breakthroughs, new models, significant papers, insider perspectives
- **Exclude:** Hype, speculation, repetitive takes, drama, memes
- **Weight:** Upvotes, engagement, author credibility, novelty

---

## Architecture (Proposed)

```
┌─────────────────────────────────────────────────────────────┐
│                      DTF:FTL Pipeline                        │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐   ┌─────────────┐   ┌─────────────┐       │
│  │   Reddit    │   │  Twitter/X  │   │    Blogs    │       │
│  │   Scraper   │   │   Scraper   │   │   RSS Feed  │       │
│  └──────┬──────┘   └──────┬──────┘   └──────┬──────┘       │
│         │                 │                 │               │
│         └────────────┬────┴────────────────┘               │
│                      ▼                                      │
│              ┌──────────────┐                               │
│              │   Scoring &  │                               │
│              │   Filtering  │                               │
│              └──────┬───────┘                               │
│                     ▼                                       │
│              ┌──────────────┐                               │
│              │    Story     │                               │
│              │   Selection  │                               │
│              │   (Top N)    │                               │
│              └──────┬───────┘                               │
│                     ▼                                       │
│              ┌──────────────┐                               │
│              │   Script     │                               │
│              │  Generation  │                               │
│              │  (Claude)    │                               │
│              └──────┬───────┘                               │
│                     ▼                                       │
│              ┌──────────────┐                               │
│              │     TTS      │                               │
│              │   (quato)    │                               │
│              └──────┬───────┘                               │
│                     ▼                                       │
│              ┌──────────────┐                               │
│              │  Assembly &  │                               │
│              │  Distribution│                               │
│              └──────────────┘                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Components

1. **Reddit Scraper**
   - Use Reddit API (PRAW) or pushshift
   - Track configured subreddits
   - Store posts with metadata (score, comments, author)

2. **Twitter/X Scraper**
   - Track luminary accounts
   - Capture tweets with engagement metrics
   - Handle threads

3. **Blog/RSS Aggregator**
   - LessWrong, AI Alignment Forum
   - Company blogs (OpenAI, Anthropic, DeepMind, Google AI)
   - ArXiv feeds for key categories

4. **Scoring & Filtering**
   - Normalize scores across sources
   - Dedup similar stories
   - Author credibility weighting
   - Recency decay
   - Novelty detection (vs rehashed takes)

5. **Story Selection**
   - Top N stories by score
   - Category balancing (research, product, philosophy)
   - Avoid clustering on single topic

6. **Script Generation**
   - Claude CLI for summarization
   - Consistent voice/tone
   - Source attribution

7. **TTS & Distribution**
   - Reuse DTFHN infrastructure
   - quato TTS server
   - R2 hosting, RSS feed

---

## Open Questions

1. ~~**Frequency:** Daily or weekly?~~ **DECIDED: Daily** (DTF = Daily Tech Feed)
2. **Length:** How many stories? 5? 10? Variable?
3. **Voice:** Same as DTFHN? Different character?
4. **Overlap:** How to handle stories that also appear on HN?
5. **Twitter API:** Cost? Alternatives? Nitter scraping?
6. **Luminary list:** Who makes the cut? How to maintain?

---

## Directory Structure (Planned)

```
dtfftl/
├── README.md
├── CLAUDE.md
├── scripts/
│   ├── collect_reddit.py
│   ├── collect_twitter.py
│   ├── collect_blogs.py
│   ├── score_stories.py
│   ├── generate_script.py
│   ├── render_episode.py
│   └── run_episode.sh
├── data/
│   ├── subreddits.json
│   ├── luminaries.json
│   ├── stories.db
│   └── episodes/
├── config/
│   └── sources.yaml
└── transcripts/
```

---

## Boris Method Status

### Phase 1: PLAN ← CURRENT
- [x] Define concept and name
- [x] Identify source categories
- [x] Draft architecture
- [ ] Finalize subreddit list
- [ ] Finalize luminary list
- [ ] Decide frequency (daily/weekly)
- [ ] Decide voice/character
- [ ] Get approval on architecture

### Phase 2: EXECUTE
- [ ] Build Reddit scraper
- [ ] Build Twitter/X scraper
- [ ] Build blog/RSS aggregator
- [ ] Build scoring system
- [ ] Build script generator
- [ ] Integrate TTS pipeline
- [ ] Build distribution (RSS, R2)

### Phase 3: VERIFY
- [ ] Test data collection
- [ ] Test scoring/filtering
- [ ] Test episode generation
- [ ] Review audio quality
- [ ] Validate source coverage

### Phase 4: DOCUMENT
- [ ] Finalize CLAUDE.md
- [ ] Document all scripts
- [ ] Add operational runbooks
- [ ] Update MEMORY.md

---

## Related Projects

- **DTFHN** — Daily Tech Feed: Hacker News (~/clawd/dtfhn)
- **DTFRF** — Daily Tech Feed: Raving Finch (~/clawd/dtfravingfinch)

---

## Next Steps

1. Approve this README
2. Finalize source lists (subreddits + luminaries)
3. Decide daily vs weekly
4. Begin Phase 2: EXECUTE
