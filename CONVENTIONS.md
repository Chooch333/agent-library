# Conventions

Rules for the agent-library. Adapted from hanyuancheung's `llm-skill` contract.

## Three meta-skills with exclusive write rights

| Meta-skill | Reads | Writes | Cannot |
|---|---|---|---|
| **Execute** | The schema + up to 3 SKILL.md files | Nothing in the skill system | Touch any skill file or schema |
| **Distill** | Raw conversation traces, tool output, errors | Only SKILL.md files | Touch the schema |
| **Guide** | Skill front-matter only | Only the schema's routing table + changelog | Put domain knowledge in the schema |

An agent that can mutate its own rules while executing is a debugging nightmare. Keep the writes mutually exclusive so every change is traceable.

## Schema rules

- `AGENT.md` is routing only. No "how to" content.
- Routing table format: `Trigger → Skill path`.
- Disambiguation rules live in AGENT.md; SOPs live in skills.

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

## Hard rules

- No SKILL.md over 500 lines. Spill to `references/` under the skill directory.
- Maximum 3 SKILL files loaded per task. Preserves lazy loading.
- Pitfalls must reference a real trace. Fabricated pitfalls fail validation.
- Imports stay in `imports/`. Reshape into `roles/` when actually adopted.

## The Hook protocol

- Every task ends with a `should-distill` check: "did anything happen worth capturing?"
- Hook cannot be silently removed.
- If yes → Distill writes a new or updated SKILL.md.
- If no → nothing happens. That's the correct outcome most of the time.

## Validation

A skill commit can be rejected mechanically if it violates the contract. Convention is not enough — the contract must be enforced.
