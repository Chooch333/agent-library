# AGENT.md — Routing Schema

This file is the dispatcher. It points to skills; it does not contain domain knowledge.
Domain knowledge lives in individual SKILL.md files.

> Rule: not one line of domain knowledge belongs in this file.
> If you find yourself writing "how to do X" here, you're writing a skill, not routing.

## Active roles

### Plan-mode reviews

| Trigger phrases | Role |
|---|---|
| `office hours`, `I have an idea`, `brainstorm this`, `let's design`, `rethink from the start`, `what should I build` | `roles/office-hours/SKILL.md` |
| `review this plan`, `CEO review`, `think bigger`, `expand scope`, `is this ambitious enough`, `find the 10-star product`, `rethink this` | `roles/ceo-reviewer/SKILL.md` |
| `eng review`, `engineering review`, `tech review`, `review architecture`, `lock in the plan`, `check the implementation plan` | `roles/eng-reviewer/SKILL.md` |
| `design review`, `review the design`, `design plan review`, `rate this design`, `UI review` | `roles/design-reviewer/SKILL.md` |
| `devex review`, `DX review`, `developer experience review`, `review the dev experience`, `TTHW review` | `roles/devex-reviewer/SKILL.md` |
| `autoplan`, `run the full plan review`, `review chain`, `CEO design eng review` | `roles/autoplan/SKILL.md` |
| `design consultation`, `design the design system`, `create a DESIGN.md`, `what should this look like`, `design from scratch`, `design system kickoff` | `roles/design-consultation/SKILL.md` |

### Implementation + review

| Trigger phrases | Role |
|---|---|
| `review this PR`, `review the diff`, `pre-PR review`, `review before merge`, `code review`, `ship review` | `roles/pr-reviewer/SKILL.md` |
| `investigate this bug`, `debug this`, `find the root cause`, `why is this broken`, `what's causing`, `trace this issue` | `roles/investigate/SKILL.md` |
| `design shotgun`, `design variants`, `show me different design directions`, `give me design options` | `roles/design-shotgun/SKILL.md` |
| `generate HTML`, `implement this design`, `write the HTML`, `code this design`, `design to HTML` | `roles/design-html/SKILL.md` |

### Release + deploy

| Trigger phrases | Role |
|---|---|
| `ship it`, `ship this`, `open the PR`, `ready to ship`, `ship pre-flight` | `roles/ship/SKILL.md` |
| `land and deploy`, `merge and deploy`, `land it`, `deploy the PR`, `land this` | `roles/land-and-deploy/SKILL.md` |
| `document this release`, `update the docs`, `documentation sweep`, `doc sync` | `roles/document-release/SKILL.md` |

### Knowledge capture

| Trigger phrases | Role |
|---|---|
| `add to cbrain`, `build out cbrain`, `let's capture`, `I want to record`, `create an entity for`, or a person/org/project not yet in cbrain named during a knowledge-capture chat | Draft a brief per `references/chat-capture.md` → Charles approves → `roles/archivist/SKILL.md` files it |

## Natural sequences

The roles compose. Common flows:

- **From idea to plan:** `office-hours` → `ceo-reviewer` → `eng-reviewer` (+ `design-reviewer` if UI, + `devex-reviewer` if developer-facing) — or `autoplan` to chain all four
- **From plan to design:** `design-consultation` (if no design system) → `design-shotgun` (if exploring) → `design-html` (when ready to implement)
- **From code to ship:** `pr-reviewer` → `ship` → `land-and-deploy` → `document-release`
- **Something broken:** `investigate`

## Imported reference material

| Source | Path | Notes |
|--------|------|-------|
| Tan / gstack | `imports/tan-gstack/_AGENTS.md` | Full catalog of all 48 gstack skills with reshape status (✅/⏭️/◯) and skip reasons |
| Tan / gbrain | `imports/tan-gbrain/_RESOLVER.md` | Catalog of all 43 gbrain skills. None reshaped — gbrain requires Postgres + pgvector runtime |

## Disambiguation rules

- When multiple roles could match, prefer the most specific. (`pr-reviewer` if reviewing a diff that exists; `eng-reviewer` if reviewing a plan with no diff yet.)
- `design-reviewer` reviews a *plan's* design quality. `design-shotgun` generates *new* design directions. `design-html` writes the *code* for an approved design. `design-consultation` builds a *design system* from scratch.
- `ceo-reviewer` is strategic; `eng-reviewer` is architectural; both can fire on the same plan. Use `autoplan` to chain them.
- `ship` opens the PR; `land-and-deploy` merges and watches the deploy; `document-release` updates docs after shipping. Run in order.
- **Knowledge capture (cbrain).** When the content is durable knowledge about an entity (people, orgs, projects), the chat path drafts a brief per `references/chat-capture.md`; Charles approves it in chat; the Archivist (`roles/archivist/SKILL.md`) is the single write-authority that files it. The chat never commits to cbrain directly. This is NOT for work-state (decisions, next steps, status) — that's Project State. If the content is "what's true about a thing," it's cbrain (→ draft a brief); if it's "what we're doing or deciding," it's Project State.
- If unsure, ask before acting.

## Activation pattern (claude.ai chat)

Claude.ai has no native slash command system. To activate a role:
1. User names the role explicitly ("use CEO Reviewer on this plan") OR uses a trigger phrase from the table above
2. Claude fetches the matching `roles/<name>/SKILL.md` via Custom GitHub MCP
3. Claude announces the role ("Operating as the CEO Reviewer. First, picking a posture...") and follows its SOP

Confirmation is behavioral, not UI-driven. Watch for: explicit role announcement in the first response, the role's characteristic vocabulary, SOP-following.

## Changelog

- **2026-05-28** — Added `cbrain-entity-builder` (v0.1.0 draft) under new "Knowledge capture" section. First cbrain-focused role; writes entity files to the cbrain repo. Disambiguation rule added (cbrain = knowledge about things; Project State = work-state).
- **2026-05-13** — Routing populated with 13 active roles across plan-mode (6), implementation (4), and release (3). Catalog imports updated with reshape status. Natural-sequence guidance added.
- **2026-05-13** — Initial routing schema created. Imports populated.
