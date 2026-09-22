---
name: world-graph-nightly
description: "Nightly ingest + auditor that builds the temporal knowledge graph."
source: Chooch333/world-graph/.github/workflows/nightly.yml
updated: 2026-09-22
wiring:
  runs: on-its-own
  starts: "nightly schedule"
  runs_in: github-actions
  reads: [sources]
  writes: [world-graph]
  stack: []
  origin: yours
  label: "Nightly ingest + auditor"
---

Pointer — instructions live at Chooch333/world-graph/.github/workflows/nightly.yml.
