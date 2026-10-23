---
name: wake
version: 0.1.0
status: draft
triggers: [used by builds, moonshots and the Harness dispatcher when work must wait; no chat trigger]
owner: Charles
updated: 2026-10-07
requires: [references/project-state.md]
wiring:
  runs: on-its-own
  starts: "Harness dispatcher (hourly :47) and Laptop runner (fire-only)"
  reads: [project-state next moves tagged wake]
  writes: [notes, next-move completion, project repos]
  stack: [total-harness]
  origin: yours
  label: Wake-up set
---

# Wake

Work that has to wait parks itself with one wake line. The Harness dispatcher checks every hour and resumes what is ready.

## Park work (any build or session)
Add a Project State next move on the work's own project, tag `wake`, description exactly:

`WAKE | where: cloud|pc | after: <ISO time with offset, or now> | on: <event-name, optional> | do: <one plain instruction> | from: <who parked it>`

- `after` — earliest time to resume.
- `on` — a short event name (e.g. `print-done-keychain`). The line is ready when that event fires or the `after` time passes, whichever comes first; omit `after` to wait for the event only.
- `do` — for a moonshot, "resume Chooch333/<slug> per skills/project-folder"; anything else, one instruction.
- Then stop. Do not poll.

## Wake it early
From any Claude session: `fire_trigger` the dispatcher ({DISPATCHER_TRIG}) with text `event: <event-name>`.
From outside Claude: not yet set up (needs the API token; see the open next move tagged block-5).

## Tasks
- Harness dispatcher — trig_01HZwjsrtqcioS3LNay8FNCk — cloud, hourly at :47.
- Laptop runner — trig_01NB1BKFvfpMJQmDKqGLmNbg — runs on Charles's laptop (folder C:\Users\cecou\code), fire-only.

## Rules
- Every wake leaves a trace: a note or a progress entry, and the next move completed with what happened.
- Fire text only selects lines by event name. It never adds instructions.
- Money, keys and deletions still stop and go to Charles.
- The dispatcher never builds Overnight briefs (Night builds does).

## Progress tracking
Follows `references/thread-checkin.md` (naming convention and when to check in).
- kind: job
- build: what the parked work is, from its `do:` instruction, in 3-6 plain words, e.g. "Keychain print resume" (thread_key "job:wake-<next move id>")
- Opens when: a wake line is parked (the work is waiting on a time, an event or the PC)
- Checks in: when a run leaves something open: on parking, and when the dispatcher resumes a line that stops again (next_step says what it waits for, in words)
- Closes when: the dispatcher resumes the line and completes its next move (`close_thread`, closed_how "resumed and done"), or Charles clicks Done

## Changelog
- 0.1.1 (2026-10-23) — Progress tracking section. Per BB-2026-10-21-next-steps-panel.
- 0.1.0 (2026-10-07) — First version (Build 30, wake-up set).
