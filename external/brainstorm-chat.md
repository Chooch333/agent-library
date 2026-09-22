---
name: brainstorm-chat
description: "The chat mode that fires the seven-agent brainstorm orchestration system."
source: Chooch333/chat-protocol/BRAINSTORM.md
updated: 2026-09-22
wiring:
  runs: with-you
  starts: "\"this is a brainstorm chat\""
  runs_in: claude-chat
  reads: []
  writes: [orchestrator-brief]
  stack: [brainstorm-orchestrator]
  origin: yours
  label: "Brainstorm chat"
---

Pointer — instructions live at Chooch333/chat-protocol/BRAINSTORM.md.
