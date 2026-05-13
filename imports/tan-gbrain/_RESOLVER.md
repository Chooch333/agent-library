# GBrain Skill Resolver

> **Imported from https://github.com/garrytan/gbrain (MIT License). Preserved for reference.**
> This is the routing dispatcher that points to gbrain's 34+ skills. Most require the gbrain Postgres + pgvector runtime to function — preserved here for the routing pattern, not direct use.

This is the dispatcher. Skills are the implementation. **Read the skill file before acting.** If two skills could match, read both. They are designed to chain (e.g., ingest then enrich for each entity).

## Always-on (every message)

| Trigger | Skill |
|---------|-------|
| Every inbound message (spawn parallel, don't block) | `skills/signal-detector/SKILL.md` |
| Any brain read/write/lookup/citation | `skills/brain-ops/SKILL.md` |

## Brain operations

| Trigger | Skill |
|---------|-------|
| "What do we know about", "tell me about", "search for", "who is", "background on", "notes on" | `skills/query/SKILL.md` |
| "Who knows who", "relationship between", "connections", "graph query" | `skills/query/SKILL.md` (use graph-query) |
| Creating/enriching a person or company page | `skills/enrich/SKILL.md` |
| Where does a new file go? Filing rules | `skills/repo-architecture/SKILL.md` |
| Fix broken citations in brain pages | `skills/citation-fixer/SKILL.md` |
| "citation audit", "check citations", "fix citations" | `skills/citation-fixer/SKILL.md` |
| "Research", "track", "extract from email", "investor updates", "donations" | `skills/data-research/SKILL.md` |
| Share a brain page as a link | `skills/publish/SKILL.md` |
| "validate frontmatter", "check frontmatter", "fix frontmatter", "frontmatter audit", "brain lint" | `skills/frontmatter-guard/SKILL.md` |

## Content & media ingestion

| Trigger | Skill |
|---------|-------|
| User shares a link, article, tweet, or idea | `skills/idea-ingest/SKILL.md` |
| Video/PDF/podcast/book/screenshot/repo | `skills/media-ingest/SKILL.md` |
| Meeting transcript received | `skills/meeting-ingestion/SKILL.md` |
| Generic "ingest this" | `skills/ingest/SKILL.md` |

## Thinking skills (from GStack)

| Trigger | Skill |
|---------|-------|
| "Brainstorm", "I have an idea", "office hours" | GStack: office-hours |
| "Review this plan", "CEO review", "poke holes" | GStack: ceo-review |
| "Debug", "fix", "broken", "investigate" | GStack: investigate |
| "Retro", "what shipped", "retrospective" | GStack: retro |

## Operational

| Trigger | Skill |
|---------|-------|
| Task add/remove/complete/defer/review | `skills/daily-task-manager/SKILL.md` |
| Morning prep, meeting context, day planning | `skills/daily-task-prep/SKILL.md` |
| Daily briefing, "what's happening today" | `skills/briefing/SKILL.md` |
| Cron scheduling, quiet hours, job staggering | `skills/cron-scheduler/SKILL.md` |
| Save or load reports | `skills/reports/SKILL.md` |
| "Create a skill", "improve this skill" | `skills/skill-creator/SKILL.md` |
| "Skillify this", "is this a skill?", "make this proper" | `skills/skillify/SKILL.md` |
| "Compress my resolver", routing-table shrink | `skills/functional-area-resolver/SKILL.md` |
| Brain health check, skillpack-check | `skills/skillpack-check/SKILL.md` |
| Post-restart smoke test | `skills/smoke-test/SKILL.md` |
| Cross-modal review, second opinion | `skills/cross-modal-review/SKILL.md` |
| "Validate skills", skill health check | `skills/testing/SKILL.md` |
| Webhook setup, external event processing | `skills/webhook-transforms/SKILL.md` |
| "Spawn agent", parallel tasks | `skills/minion-orchestrator/SKILL.md` |
| Choice gate, user decision | `skills/ask-user/SKILL.md` |

## Setup & migration

| Trigger | Skill |
|---------|-------|
| "Set up GBrain", first boot | `skills/setup/SKILL.md` |
| "Now what?", "fill my brain", "cold start" | `skills/cold-start/SKILL.md` |
| "Migrate from Obsidian/Notion/Logseq" | `skills/migrate/SKILL.md` |
| Brain health check, maintenance run | `skills/maintain/SKILL.md` |
| Agent identity, "who am I" | `skills/soul-audit/SKILL.md` |

## Specialty skills

| Trigger | Skill |
|---------|-------|
| Book mirroring, "apply this book to my life" | `skills/book-mirror/SKILL.md` |
| Enrich brain pages, batch enrich | `skills/article-enrichment/SKILL.md` |
| Strategic reading, "read through the lens of" | `skills/strategic-reading/SKILL.md` |
| Concept synthesis, find patterns across notes | `skills/concept-synthesis/SKILL.md` |
| Perplexity-style web research | `skills/perplexity-research/SKILL.md` |
| Crawl personal archive | `skills/archive-crawler/SKILL.md` |
| Verify academic claims | `skills/academic-verify/SKILL.md` |
| Brain page to PDF | `skills/brain-pdf/SKILL.md` |
| Voice note ingestion | `skills/voice-note-ingest/SKILL.md` |

## Disambiguation rules

1. Prefer the most specific skill (meeting-ingestion over ingest)
2. URL → route by content type (link → idea-ingest, video → media-ingest)
3. Person/company → check if enrich or query fits better
4. Chaining is explicit in each skill's Phases section
5. When in doubt, ask the user
