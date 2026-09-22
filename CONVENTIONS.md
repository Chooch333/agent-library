# Conventions

Rules for the agent-library. Adapted from hanyuancheung's `llm-skill` contract.

## Three meta-skills with exclusive write rights

| Meta-skill | Reads | Writes | Cannot |
|---|---|---|---|
| **Execute** | The schema + up to 3 SKILL.md files | Nothing in the skill system, **except**: a build chat executing an approved Build Brief may create or edit exactly the skill files and AGENT.md routing rows that brief names | Touch any skill file, AGENT.md row, or schema its brief doesn't name |
| **Inspector** | Project State evidence, cbrain's stack-map, shipped repos (read-only) | Only Punch List rows (`punch_items`, `punch_item_notes`, `punch_checkpoints`) | Edit a target file directly, or write anywhere outside the Punch List |
| **Repairer** | Punch List rows (`auto`-tier, `open` items), the live target it's about to edit | The target file/repo an item names, plus that item's Punch List write-back | File a Punch List item, or verify its own repair |

An agent that can mutate its own rules while executing is a debugging nightmare. Keep the writes mutually exclusive so every change is traceable.

## Schema rules

- `AGENT.md` is routing only. No "how to" content.
- Routing table format: `Trigger → Skill path`.
- Disambiguation rules live in AGENT.md; SOPs live in skills.
- A routing row is written by the build that registers the skill it points to (Amendment 2, decision A-080, per the Execute row above). Drift between a routing row and the skill it names — a stale trigger phrase, a moved path — is fixed by the Repairer under the same auto-tier rules as any other Punch List item, not by hand-editing during unrelated work.

## Words

- **Skill** — written instructions for one kind of job. It does nothing on its own. Every entry on the tab is a skill.
- **Agent** — a skill that runs on its own: it has a trigger (a schedule or an event), tools, and nobody steering each step. On the tab this is a badge, "Runs on its own", not a separate list.
- **Role** — retired from anything Charles reads (UI labels, briefs, artifacts). The `roles/` folder name stays as plumbing.

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

### Body (six fixed sections)

1. **What** — one paragraph on what the skill does
2. **When** — positive and negative examples of when to fire it
3. **How** — numbered SOP
4. **Examples** — concrete worked cases
5. **Pitfalls** — every pitfall must come from a real trace (no fabrications)
6. **Changelog** — versioned notes

### Designing a new skill

Before writing a new SKILL.md, answer the twelve questions in `references/skill-design-framework.md` — that document governs the skill's *design*; this file (with `SKILL_TEMPLATE.md`) governs its *format*. The answers travel in the Build Brief that creates the skill.

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
- Imports stay in `imports/`. Reshape into `roles/` when actually adopted.

## Keeping the rules current

- The per-task `should-distill` hook this section used to describe was never built (the "Distill" meta-skill it depended on never shipped) and is retired.
- In its place: the Inspector's weekly walk (`roles/inspector/SKILL.md`) is what checks whether the system's own rules, skills, and stack-map need a fix — on a schedule, not per-task. It files what it finds on the Punch List; the Repairer (`roles/repairer/SKILL.md`) applies the safe ones.
- This is a coarser cadence than the old per-task hook by design (BB-2026-09-21-inspector-repairer, design intent: "when in doubt, hold back — a missed fix costs a week; a wrong rule change costs every chat").

## Validation

A skill commit can be rejected mechanically if it violates the contract. Convention is not enough — the contract must be enforced.

## Changelog

- 2026-09-22 — Amendment 2 (decision A-080): the Execute row now allows a build chat executing an approved Build Brief to create or edit exactly the skill files and AGENT.md routing rows that brief names; added a Schema rules bullet on routing-row authorship and Repairer-driven drift-repair. Per BB-2026-09-21-inspector-repairer step 12a.
- 2026-09-22 — Replaced the Execute/Distill/Guide meta-skill table with Execute/Inspector/Repairer (Distill and its should-distill hook were never built; replaced by the Inspector's scheduled walk). Added a pointer to `references/skill-design-framework.md` under Skill file rules. Per BB-2026-09-21-inspector-repairer Phase 2.
- 2026-09-22 — Added the Words section (Skill/Agent/Role) and the optional `wiring` header block, for cbrain-ui's Skills tab (BB-2026-09-21-skills-tab).
