---
name: project-folder
version: 0.3.0
status: draft
triggers: [used by builds and harness roles when a moonshot starts or resumes; no chat trigger]
dependencies: [checker]
owner: Charles
updated: 2026-10-23
requires: [references/thread-checkin.md]
wiring:
  runs: inside-builds
  reads: [project repo]
  writes: [project repo]
  stack: [total-harness]
  origin: yours
  label: Project folder
---

# Project folder

Every moonshot lives in one standard folder so any session can pick it up from the files, not from an old chat.

## Where it lives
- Home: a private GitHub repo `Chooch333/<slug>` (slug = short, lowercase, hyphens).
- PC working copy, only when a step needs the PC: `C:\Users\cecou\code\workshop\<slug>`. The repo stays the record; push from the PC copy at the end of each PC session.
- Big outputs (renders, meshes, video) go in `outputs/`, which is not committed.

## Roles
- **Planner:** Start steps 3–4 (spec.md from the ask; features and rubric rows from "Works means"). Design Assist and Build Briefs plan the builds.
- **Builder:** agent-library `skills/orchestrate-build` (lead) + `skills/execute-build-task` (one-task workers). The builder builds and marks a feature ready; it never sets `passes`.
- **Checker:** agent-library `skills/checker`. A separate helper in a fresh context grades each ready feature against `rubric.md` and writes `checks/<id>-<n>.md`. Only its PASS sets `passes: true`.

## Start (once per project)
1. Create the repo (Custom GitHub MCP `create_repo`, private).
2. Copy every file in agent-library `templates/project-folder/` (including `checks/README.md`; `features.json` starts with `"checker": true`).
3. Fill `spec.md` from the ask. The Ask section is Charles's words, verbatim, never edited.
4. Turn "Works means" into the first features (priority 1..n) and into the rubric rows.
5. Fill `run.md` and `README.md`. Write the first progress entry.
6. Run `check_folder.py`; it must print OK. Commit.
7. Stop at the concept stop (spec.md Stops #1) before building.

## Resume (start of every session)
1. Read `README.md`, the newest `progress.md` entry, and recent commits.
2. Run the quick health check in `run.md`.
3. Pick the lowest-priority-number feature with `passes: false`. Work only that feature. If its newest verdict in `checks/` is a FAIL, start from that verdict's gap and fix hint.

## Close (end of every session)
1. **Mark ready, don't grade.** When the builder thinks a feature works, it names the feature as ready in its progress entry. The builder never sets `passes` or `evidence`.
2. **The checker grades it.** Dispatch the checker (agent-library `skills/checker`) on that feature, with only its inputs: `rubric.md`, the feature's id, description and check lines, and the paths of the thing. Its verdict lands in `checks/<id>-<n>.md`; only a PASS sets `passes: true` with evidence pointing at that file. A FAIL or CAN'T CHECK leaves the feature false; the builder takes the gap into the next session. A third FAIL stops the feature (README Status `stopped: <id> failed 3 checks`) until Charles decides.
3. Never edit or delete a feature; add new ones at the end.
4. Add one entry at the top of `progress.md`: did, checked (name the verdict files), next, stops.
5. Run `check_folder.py`; it must print OK. Commit with a plain message.

## Waiting
When the next step has to wait (a print, a delivery, a reply), park it with a wake line (agent-library `skills/wake/SKILL.md`): `do: resume Chooch333/<slug> per skills/project-folder`, `where: pc` if the next step needs the laptop. Set README Status to `stopped: waiting on <what>`. Then close the session.

## Rules
- One feature at a time.
- The builder never grades itself. Only a checker verdict in `checks/` can mark a feature passed; `check_folder.py` refuses a pass without one when `features.json` has `"checker": true` (older folders opt in by adding it).
- Money always stops. Safety rules in spec.md never relax.

## Progress tracking
Follows `references/thread-checkin.md` (naming convention and when to check in).
- kind: job
- build: the moonshot's name in words, e.g. "Backyard drone build" (thread_key "job:project-folder-<slug>")
- Opens when: a session stops at a stop in spec.md (the concept stop first), or parks with a wake line (README Status `stopped: waiting on <what>`), or a feature fails three checks (README Status `stopped: <id> failed 3 checks`)
- Checks in: at every session close that leaves the project stopped or waiting (next_step = the stop or the wait, in words)
- Closes when: every feature in the folder passes and Charles accepts it, or Charles clicks Done

## Changelog
- 0.3.0 (2026-10-23) — Checker role (Build 45, BB-2026-10-21-checker-role): Close marks a feature ready and the checker grades it; the builder never sets passes. Roles section (planner, builder, checker). Template gains `"checker": true` and `checks/`.
- 0.2.1 (2026-10-23) — Progress tracking section. Per BB-2026-10-21-next-steps-panel.
- 0.2.0 — Waiting section (Build 30, wake-up set)
- 0.1.0 — First version (Build 29, standard project folder)
