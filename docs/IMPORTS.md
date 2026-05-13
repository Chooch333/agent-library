# IMPORTS — Reference material from other stacks

This directory tracks material cloned from external agent stacks for study and reference. Imported files are **not active roles**. They live under `imports/` until and unless you reshape them into your own `roles/`.

## Why imports stay separate

1. Imported skills often depend on runtimes you don't have (Claude Code local file system, Playwright, Postgres + pgvector). Marking them as imports keeps the working `roles/` directory clean of non-functional files.
2. Attribution is clearer when the originals are preserved alongside your reshaped versions.
3. You can diff your reshaped role against the source to track what changed.

## What's been imported

### `imports/tan-gstack/` — Garry Tan's gstack

Source: https://github.com/garrytan/gstack (MIT License)

48 SKILL.md files covering specialist worker roles for software development.
Most depend on Claude Code's runtime. The portable subset is the judgment-frame
roles (plan-ceo-review, plan-eng-review, plan-design-review, plan-devex-review,
office-hours, autoplan) — these work without Claude Code as long as the
markdown body is loaded into the session as instructions.

See `imports/tan-gstack/_AGENTS.md` for Tan's full routing table.

### `imports/tan-gbrain/` — Garry Tan's gbrain

Source: https://github.com/garrytan/gbrain (MIT License)

43 SKILL.md files for brain operations + entity memory. All depend on Postgres + pgvector runtime and the gbrain CLI. Not currently portable to claude.ai chat without the gbrain backend.

See `imports/tan-gbrain/_AGENTS.md` and `_RESOLVER.md` for the routing structure.

## How to use imports

1. **Browse** the import directory to see what's available.
2. **Pick** a skill that maps to a workflow you actually run.
3. **Reshape** it: copy the SKILL.md, rewrite it against the Cheung contract template (`/SKILL_TEMPLATE.md`), strip out runtime-specific bits, save under `roles/<your-name>/SKILL.md`.
4. **Register** the new role in the top-level `AGENT.md` routing table.

## What's NOT imported

- Karpathy's LLM-Wiki — no role files exist to import (it's a concept piece + Jamie's video).
- hanyuancheung's `llm-skill` — the contract is adopted in `CONVENTIONS.md` and `SKILL_TEMPLATE.md` rather than imported as files.
- Debois's CDLC — pure framework; the four phases shape how this library is governed.
