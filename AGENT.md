# AGENT.md — Routing Schema

This file is the front door. Project instructions point here. It routes a first message to one skill; it holds no domain knowledge.

> Rule: not one line of domain knowledge belongs in this file.
> If you find yourself writing "how to do X" here, you're writing a skill, not routing.

## Active skills

### Brainstorming

| Trigger phrases | Skill |
|---|---|
| `this is a brainstorm chat` (case-insensitive, must be in the very first message — mentioning brainstorming mid-chat is not an invocation) | `BRAINSTORM.md` — **owner=Chooch333, repo=chat-protocol** (not agent-library — the only row in this table that points outside this repo) |

### Build

| Trigger phrases | Skill |
|---|---|
| `this is a build chat` (case-insensitive, must be in the very first message — mentioning building mid-chat is not an invocation) | `skills/build/SKILL.md` |

### Design shaping

| Trigger phrases | Skill |
|---|---|
| `Design Assist` (exact phrase in prompt — the only trigger; do not auto-fire from adjacent phrases) | `skills/design-assist/SKILL.md` |

### Investment

| Trigger phrases | Skill |
|---|---|
| `this is an investment review` (case-insensitive, must be in the very first message — mentioning an investment review mid-chat is not an invocation) | `skills/investment-review/SKILL.md` |

### R&D lab

| Trigger phrases | Skill |
|---|---|
| `Tech discovery:` (the very first message must start with it, e.g. `Tech discovery: <name or link>` — the first look at a tech, no test; files a Discovery Brief) | `skills/tech-discovery/SKILL.md` |
| `Tech review:` (the very first message must start with it, e.g. `Tech review: <name or link>` — the test run of a tech, usually one that already has a Discovery Brief; files an R&D Report. Mentioning a tech review mid-chat is not an invocation) | `skills/tech-review/SKILL.md` |

### Family arcade

| Trigger phrases | Skill |
|---|---|
| `New game:` (a message that starts with it, e.g. `New game: squish things to earn coins`; in any chat, mid-chat included) and `Launch` said after a Game Maker game is on screen | `skills/game-maker/SKILL.md` |

### Plan-mode reviews

| Trigger phrases | Skill |
|---|---|
| `business concept` (Business Concept run: Startup mode + market research + Vetting Report), `office hours`, `I have an idea`, `brainstorm this`, `let's design`, `rethink from the start`, `what should I build` | `skills/office-hours/SKILL.md` |
| `business plan` (Business Plan run: business review + Business & Tech Plan report), `review this plan`, `CEO review`, `think bigger`, `expand scope`, `is this ambitious enough`, `find the 10-star product`, `rethink this` | `skills/ceo-reviewer/SKILL.md` |
| `eng review`, `engineering review`, `review architecture`, `lock in the plan`, `check the implementation plan` | `skills/eng-reviewer/SKILL.md` |
| `design review`, `review the design`, `design plan review`, `rate this design`, `UI review` | `skills/design-reviewer/SKILL.md` |
| `devex review`, `DX review`, `developer experience review`, `review the dev experience`, `TTHW review` | `skills/devex-reviewer/SKILL.md` |
| `autoplan`, `run the full plan review`, `review chain`, `CEO design eng review` | `skills/autoplan/SKILL.md` |
| `design consultation`, `design the design system`, `create a DESIGN.md`, `what should this look like`, `design from scratch`, `design system kickoff` | `skills/design-consultation/SKILL.md` |

### Implementation + review

| Trigger phrases | Skill |
|---|---|
| `review this PR`, `review the diff`, `pre-PR review`, `review before merge`, `code review`, `ship review` | `skills/pr-reviewer/SKILL.md` |
| `investigate this bug`, `debug this`, `find the root cause`, `why is this broken`, `what's causing`, `trace this issue` | `skills/investigate/SKILL.md` |
| `design shotgun`, `design variants`, `show me different design directions`, `give me design options` | `skills/design-shotgun/SKILL.md` |
| `generate HTML`, `implement this design`, `write the HTML`, `code this design`, `design to HTML` | `skills/design-html/SKILL.md` |

### Release + deploy

| Trigger phrases | Skill |
|---|---|
| `ship it`, `ship this`, `open the PR`, `ready to ship`, `ship pre-flight` | `skills/ship/SKILL.md` |
| `land and deploy`, `merge and deploy`, `land it`, `deploy the PR`, `land this` | `skills/land-and-deploy/SKILL.md` |
| `document this release`, `update the docs`, `documentation sweep`, `doc sync` | `skills/document-release/SKILL.md` |

### FAW jobs

| Trigger phrases | Skill |
|---|---|
| `add this`, `log this`, `put this on the job` (or plainly the same ask) about an FA Wilhelm job's tasks, dates, milestones, meetings, team or decisions — mid-chat included; also a question about a job's current state (`what's open on <job>?`) | `skills/job-update/SKILL.md` (writes only on that ask; general construction/permitting talk is never logged) |

### Knowledge capture

| Trigger phrases | Skill |
|---|---|
| `add to cbrain`, `build out cbrain`, `let's capture`, `I want to record`, `create an entity for`, or a person/org/project not yet in cbrain named during a knowledge-capture chat | Draft a brief per `references/chat-capture.md` → Charles approves → `skills/archivist/SKILL.md` files it |
| `define a new entity type`, `new entity type`, `add a type to the schema`, `cbrain needs a type for`, or defining a new KIND of thing that has no `type` in `SCHEMA.md` yet | `skills/entity-type-creator/SKILL.md` (single-approval SCHEMA.md addition; auto-deploys to the watcher) |

### Self-maintenance

| Trigger phrases | Skill |
|---|---|
| `Inspector: walk` | `skills/inspector/SKILL.md` |
| `Repairer: run` | `skills/repairer/SKILL.md` |
| `Stack Repairer: run` | `skills/stack-repairer/SKILL.md` |

## Natural sequences

The skills compose. Common flows:

- **Vetting a business idea:** `business concept` (office-hours → Vetting Report) → if PURSUE, `business plan` (ceo-reviewer → Business & Tech Plan) → if GO, `eng review` on the tech plan
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

- When multiple skills could match, prefer the most specific. (`pr-reviewer` if reviewing a diff that exists; `eng-reviewer` if reviewing a plan with no diff yet.)
- `design-reviewer` reviews a *plan's* design quality. `design-shotgun` generates *new* design directions. `design-html` writes the *code* for an approved design. `design-consultation` builds a *design system* from scratch.
- `ceo-reviewer` is strategic; `eng-reviewer` is architectural; both can fire on the same plan. Use `autoplan` to chain them.
- `ship` opens the PR; `land-and-deploy` merges and watches the deploy; `document-release` updates docs after shipping. Run in order.
- **Knowledge capture (cbrain).** When the content is durable knowledge about an entity (people, orgs, projects), the chat path drafts a brief per `references/chat-capture.md`; Charles approves it in chat; the Archivist (`skills/archivist/SKILL.md`) is the single write-authority that files it. The chat never commits to cbrain directly. This is NOT for work-state (decisions, next steps, status) — that's Project State. If the content is "what's true about a thing," it's cbrain (→ draft a brief); if it's "what we're doing or deciding," it's Project State.
- **Job work vs knowledge capture.** "Add this" about a job's work (a task, a date, a milestone, a meeting, who's on the job) → `job-update` (graph). "Add this" about what's true of a person, company or place → chat-capture → Archivist (cbrain).
- **New TYPE vs new INSTANCE vs new FIELD (cbrain).** A new KIND of thing that no `type` in `SCHEMA.md` fits → `skills/entity-type-creator/SKILL.md` (it edits the schema; the watcher reads the schema at runtime, so the commit auto-deploys). A new INSTANCE of an existing type (a person, an org, a project) → chat-capture → Archivist, NOT the type creator. An existing type that just wants one more optional field → a small direct schema edit, not a new type. Test: is there no `type` value this thing could carry? Only then is it a new type.
- A first message that matches no trigger has no skill. Plain conversation, quick questions and other non-build work proceed normally; no default is assumed.
- If unsure, ask before acting.

## Activation pattern (claude.ai chat)

Claude.ai has no native slash command system. To activate a skill:
1. User names the skill explicitly ("use CEO Reviewer on this plan") OR uses a trigger phrase from the table above
2. Claude fetches the matching `skills/<name>/SKILL.md` via Custom GitHub MCP
3. Claude announces the skill ("Operating as the CEO Reviewer. First, picking a posture...") and follows its SOP

A skill that reads or writes Project State declares `requires: references/project-state.md`; fetch what the header names after the skill. (`requires:` paths are from the agent-library repo root.)

Confirmation is behavioral, not UI-driven. Watch for: explicit skill announcement in the first response, the skill's characteristic vocabulary, SOP-following.

## Changelog

See `CHANGELOG.md` (moved out of this file 2026-10-15, Build 39).
