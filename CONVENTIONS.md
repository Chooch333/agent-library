# Conventions

Rules for the agent-library. Adapted from hanyuancheung's `llm-skill` contract.

## Three meta-skills with exclusive write rights

| Meta-skill | Reads | Writes | Cannot |
|---|---|---|---|
| **Execute** | The schema + up to 3 SKILL.md files | Nothing in the skill system, **except**: a build chat executing an approved Build Brief may create or edit exactly the skill files and AGENT.md routing rows that brief names | Touch any skill file, AGENT.md row, or schema its brief doesn't name |
| **Inspector** | Project State evidence, cbrain's stack-map, shipped repos (read-only) | Only Punch List rows (`punch_items`, `punch_item_notes`, `punch_checkpoints`) | Edit a target file directly, or write anywhere outside the Punch List |
| **Repairer** | Punch List rows (`auto`-tier, `open` items), the live target it's about to edit | The target file/repo an item names, plus that item's Punch List write-back | File a Punch List item, or verify its own repair |
| **expert-desk** | `experts/INDEX.md`, expert briefs, the charter, the stack map's lanes, the work under review | `experts/<slug>/BRIEF.md` (draft, after a confirmed reframe); that expert's row in `experts/INDEX.md` (after its check passes); Project State notes tagged `expert-proposal` and `expert-check` | Commit a brief whose reframe Charles has not confirmed, check a brief in the helper that wrote or proposed it, or write anything else in any repo |

An agent that can mutate its own rules while executing is a debugging nightmare. Keep the writes mutually exclusive so every change is traceable.

## Schema rules

- `AGENT.md` is routing only. No "how to" content.
- Routing table format: `Trigger → Skill path`.
- Disambiguation rules live in AGENT.md; SOPs live in skills.
- A routing row is written by the build that registers the skill it points to (Amendment 2, decision A-080, per the Execute row above). Drift between a routing row and the skill it names — a stale trigger phrase, a moved path — is fixed by the Repairer under the same auto-tier rules as any other Punch List item, not by hand-editing during unrelated work.

## Words

- **Skill** — written instructions for one kind of job. It does nothing on its own. Every entry on the tab is a skill.
- **Agent** — a skill that runs on its own: it has a trigger (a schedule or an event), tools, and nobody steering each step. On the tab this is a badge, "Runs on its own", not a separate list.
- **Role** — retired from anything Charles reads (UI labels, briefs, artifacts). The old role folder was folded into `skills/` (Build 38, 2026-10-15).
- **Expert Desk** — the one skill every expert interaction goes through.
- **Expert bench** — the folder `experts/`.
- **Expert** — thought leadership for planning and design; judges, never executes (TH-135).
- **Domain captain** — an expert that holds a field's judgment and is seated first.
- **Craft expert** — an expert in one technique, always under a captain.
- **Brief** — an expert's file, `experts/<slug>/BRIEF.md`. A Build Brief is a different thing.
- **Profile card** — the desk's per-domain settings: default captains, severity scale, max seats (`skills/expert-desk/profiles/`).
- **Lens** — the named ways work in an expert's corner goes wrong, each with its source.
- **Roster-builder** — the expert that proposes, researches, checks and retires experts.
- **Mode A / A.1 / B** — A: captains evaluate and plan. A.1: carried captains plus their craft experts. B: one expert, one issue.

## Skill file rules

Every SKILL.md has two parts:

### Contract (YAML front-matter — all seven fields required)

```yaml
---
name: <slug>
version: <semver>
status: draft | active | deprecated
triggers: [phrases or events that fire this skill]
dependencies: [other skills this one chains to]
owner: <name>
updated: <YYYY-MM-DD>
---
```

### Body (seven fixed sections)

1. **What** — one paragraph on what the skill does
2. **When** — positive and negative examples of when to fire it
3. **How** — numbered SOP
4. **Progress tracking** — how this skill reports open work to the Next steps list: kind, build (the chat's own name for its work), opens / checks in / closes, per `references/thread-checkin.md`; or "None" for a skill that never leaves work open. Required in every skill.
5. **Examples** — concrete worked cases
6. **Pitfalls** — every pitfall must come from a real trace (no fabrications)
7. **Changelog** — versioned notes

### Designing a new skill

Before writing a new SKILL.md, answer the twelve questions in `references/skill-design-framework.md` — that document governs the skill's *design*; this file (with `SKILL_TEMPLATE.md`) governs its *format*. The answers travel in the Build Brief that creates the skill.

### Expert briefs

`experts/<slug>/BRIEF.md` follows `references/expert-brief.md` instead of the seven-section body. Briefs are seated by the Expert Desk and never routed by AGENT.md. A build with a Build Brief edits them, the same as skills; the desk's deep-dive helper creates one as draft after Charles confirms its reframe.

## Optional wiring block

Any SKILL.md (and the new `external/` pointer files) may carry an optional `wiring:` map inside its YAML front-matter, consumed by cbrain-ui's Skills tab:

```yaml
wiring:
  runs: on-its-own        # on-its-own | with-you
  starts: "Mon/Wed/Fri schedule"   # plain English: trigger phrase, schedule, or event
  runs_in: cowork         # claude-chat | cowork | claude-code | vercel | github-actions | claude-plugin
  reads: [world-graph, project-state]   # short plain names
  writes: [advisor-tables, email]
  stack: []               # stack-map component ids; [] = not on the map yet
  origin: yours           # yours | imported
  label: Stack Advisor    # optional plain display name (defaults to name)
  replaced_by: [inspector, repairer]  # optional: skill slugs shown as "replaced by ..." when status is deprecated/retired
```

A skill whose `status` is `deprecated` or `retired` (case-insensitive) — regardless of what runs it or where — shows in the Skills tab's **Retired** lane instead of its platform lane, greyed out with its `replaced_by` labels (if set) shown as "replaced by ...". The skill file itself is not removed or hidden; only its tab placement changes.

## Hard rules

- No SKILL.md over 500 lines. Spill to `references/` under the skill directory.
- Maximum 3 SKILL files loaded per task. Preserves lazy loading.
- Pitfalls must reference a real trace. Fabricated pitfalls fail validation.
- Imports stay in `imports/`. Reshape into `skills/` when actually adopted.

## Keeping the rules current

- The per-task `should-distill` hook this section used to describe was never built (the "Distill" meta-skill it depended on never shipped) and is retired.
- In its place: the Inspector's weekly walk (`skills/inspector/SKILL.md`) is what checks whether the system's own rules, skills, and stack-map need a fix — on a schedule, not per-task. It files what it finds on the Punch List; the Repairer (`skills/repairer/SKILL.md`) applies the safe ones.
- This is a coarser cadence than the old per-task hook by design (BB-2026-09-21-inspector-repairer, design intent: "when in doubt, hold back — a missed fix costs a week; a wrong rule change costs every chat").

## Validation

A skill commit can be rejected mechanically if it violates the contract. Convention is not enough — the contract must be enforced.

## Changelog

- 2026-11-03 — expert-desk writes row: a grown expert's row in `experts/INDEX.md`, after its check passes. Per BB-2026-11-03-expert-index-row (Build 61.2, TH-J-044).
- 2026-11-03 — Expert Desk registered: an "Expert briefs" subsection under Skill file rules, an exclusive-writes row for expert-desk, and the locked words per TH-135. Per BB-2026-11-02-expert-desk (Build 61).
- 2026-10-22 — Body grows to seven sections: **Progress tracking** (after How) is required in every skill, per `references/thread-checkin.md` 0.2.0 and `SKILL_TEMPLATE.md`. Charles: "a section of each skill dedicated to this progress tracking rule … the skill creation template must make sure to include it."
- 2026-09-22 — Added optional `wiring.replaced_by` and documented the `status: deprecated`/`retired` → Skills tab Retired lane rule. Per BB-2026-09-22-skills-lanes step 2.
- 2026-09-22 — Amendment 2 (decision A-080): the Execute row now allows a build chat executing an approved Build Brief to create or edit exactly the skill files and AGENT.md routing rows that brief names; added a Schema rules bullet on routing-row authorship and Repairer-driven drift-repair. Per BB-2026-09-21-inspector-repairer step 12a.
- 2026-09-22 — Replaced the Execute/Distill/Guide meta-skill table with Execute/Inspector/Repairer (Distill and its should-distill hook were never built; replaced by the Inspector's scheduled walk). Added a pointer to `references/skill-design-framework.md` under Skill file rules. Per BB-2026-09-21-inspector-repairer Phase 2.
- 2026-09-22 — Added the Words section (Skill/Agent/Role) and the optional `wiring` header block, for cbrain-ui's Skills tab (BB-2026-09-21-skills-tab).
