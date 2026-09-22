---
name: brainstorm-panel
description: "Renders the output doc when a brief lands in the brainstorm orchestrator."
source: Chooch333/brainstorm-orchestrator/app/output/[briefId]/page.tsx
updated: 2026-09-22
wiring:
  runs: on-its-own
  starts: "a brief lands in the orchestrator"
  runs_in: vercel
  reads: [orchestrator-brief]
  writes: [output-doc]
  stack: [brainstorm-orchestrator]
  origin: yours
  label: "Brainstorm panel"
---

Pointer — instructions live at Chooch333/brainstorm-orchestrator/app/output/[briefId]/page.tsx.
