---
name: stack-manager
version: 0.2.0
status: deprecated
triggers: []
dependencies: []
owner: Charles
updated: 2026-09-22
wiring:
  runs: with-you
  starts: "deprecated — see Inspector and Repairer"
  runs_in: claude-chat
  reads: []
  writes: []
  stack: [cbrain, project-state]
  origin: yours
  label: Stack Manager (deprecated)
---

# Stack Manager (deprecated)

**This role is deprecated as of 2026-09-22 (BB-2026-09-21-inspector-repairer).** It never disposed more than one suggestion (SM-002 → decision SM-003, 2026-07-21) in its two months live, and its scheduled trigger depended on the never-built heartbeat-orchestrator (SM-049). Its single job — judge stack-map drift and fix it — has been split into two roles, per the design intent that the fixer must never grade itself:

- **Judging** (comparing the map to what shipped, deciding what's wrong) → `roles/inspector/SKILL.md`, whose map-comparison checklist is copied verbatim from this file's old step 3 and pitfall — see `roles/inspector/references/map-review-checklist.md`.
- **Editing** (applying an accepted change to `concepts/stack-map.md`) → `roles/repairer/SKILL.md`, whose editing procedure is copied verbatim from this file's old steps 5 and 8, and Rules section — see `roles/repairer/references/stack-map-playbook.md`.

The `MAP-EDIT` next-move suggestion queue this role was built to dispose of is also retired (chat-protocol PROTOCOL.md, "Stack-map upkeep" standing rule, 2026-09-22) — sessions no longer file suggestions; the Inspector compares the map to live state directly on its weekly walk instead.

This file's full original content (v0.1.0, `status: draft`) is preserved in git history at the commit before this one. Do not invoke this role; it has no working trigger.

## Changelog

- **0.2.0** (2026-09-22) — Reduced to a deprecated pointer. Split into Inspector (judging) and Repairer (editing/applying) per BB-2026-09-21-inspector-repairer, design intent "the fixer never grades itself."
- **0.1.0** (2026-07-21) — Initial skill (BB-2026-07-20-stack-map, Directive 6). Superseded by the split above; see git history for full content.
