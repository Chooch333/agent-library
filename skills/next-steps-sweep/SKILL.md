---
name: next-steps-sweep
version: 0.2.0
status: retired
owner: Charles
updated: 2026-10-23
source: BB-2026-10-20-next-steps-dev-tab (Build 44); retired by BB-2026-10-21-next-steps-panel
requires: []
wiring: {runs: alone, starts: "never (retired)", runs_in: claude-code-cloud,
  reads: [], writes: [], label: Next steps sweep (retired)}
---
# Next steps sweep (retired)

Retired 2026-10-23: use `skills/night-run/SKILL.md` step 7 "Re-check open cards", and `references/thread-checkin.md` "When and how" (jobs that run on their own check in when a run leaves something open). Do not create its scheduled task.

## Changelog

- 0.2.0 (2026-10-23) — Retired (Charles, 2026-10-22: skills report directly; the re-check moves into the night runner). Its scheduled task was never created. BB-2026-10-21-next-steps-panel.
- 0.1.0 (2026-10-21) — First version, Build 44 (BB-2026-10-20-next-steps-dev-tab).
  Seeded the list by one hand-run sweep the same night.
