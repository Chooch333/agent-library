---
name: wake
version: 0.1.0
status: draft
triggers: [used by builds, moonshots and the Harness dispatcher when work must wait; no chat trigger]
owner: Charles
updated: 2026-10-07
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
