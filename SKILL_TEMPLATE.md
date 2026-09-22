---
name: <skill-slug>
version: 0.1.0
status: draft
triggers:
  - <phrase or event 1>
  - <phrase or event 2>
dependencies: []
owner: Charles
updated: 2026-05-13
wiring:
  runs: on-its-own        # on-its-own | with-you
  starts: "Mon/Wed/Fri schedule"   # plain English: trigger phrase, schedule, or event
  runs_in: cowork         # claude-chat | cowork | claude-code | vercel | github-actions | claude-plugin
  reads: [world-graph, project-state]   # short plain names
  writes: [advisor-tables, email]
  stack: []               # stack-map component ids; [] = not on the map yet
  origin: yours           # yours | imported
  label: Stack Advisor    # optional plain display name (defaults to name)
---

# <Skill Name>

## What

One paragraph describing what this skill does and why it exists.

## When

**Fire this skill when:**
- <positive trigger 1>
- <positive trigger 2>

**Do NOT fire this skill when:**
- <negative trigger 1 — common confusion>
- <negative trigger 2 — common confusion>

## How

1. <Step one>
2. <Step two>
3. <Step three>

(Numbered SOP. Keep steps small and verifiable.)

## Examples

### Example 1: <descriptive name>

**Input:**
<input>

**Output:**
<output>

### Example 2: <descriptive name>

(Repeat as needed.)

## Pitfalls

> Every pitfall must come from a real trace. No fabrications.

- **Pitfall 1:** <description, with link or reference to the trace where it surfaced>
- **Pitfall 2:** <description, with link or reference>

## Changelog

- **0.1.0** (2026-05-13) — Initial draft.
