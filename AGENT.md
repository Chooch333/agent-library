# AGENT.md — Routing Schema

This file is the dispatcher. It points to skills; it does not contain domain knowledge.
Domain knowledge lives in individual SKILL.md files.

> Rule: not one line of domain knowledge belongs in this file.
> If you find yourself writing "how to do X" here, you're writing a skill, not routing.

## Active roles (Charles's own)

| Trigger | Skill |
|---------|-------|
| _(none yet — first roles will be added here as they're built)_ | — |

## Imported reference material

| Source | Path | Notes |
|--------|------|-------|
| Tan / gstack | `imports/tan-gstack/` | Specialist worker roles. Slash-command pattern. Many depend on Claude Code runtime. |
| Tan / gbrain | `imports/tan-gbrain/` | Brain operations + entity memory. Most skills need Postgres + pgvector runtime. |

## Disambiguation rules

When multiple skills could match, prefer the most specific. If unsure, ask before acting.

## Changelog

- 2026-05-13: Initial routing schema created. Imports populated.
