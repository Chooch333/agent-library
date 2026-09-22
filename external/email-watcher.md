---
name: email-watcher
description: "Watches Gmail and turns matching mail into cbrain briefs."
source: Chooch333/email-watcher/api/cron/watch.ts
updated: 2026-09-22
wiring:
  runs: on-its-own
  starts: "timer (Vercel cron)"
  runs_in: vercel
  reads: [gmail]
  writes: [cbrain-briefs]
  stack: [intake-extractors]
  origin: yours
  label: "Email watcher"
---

Pointer — instructions live at Chooch333/email-watcher/api/cron/watch.ts.
