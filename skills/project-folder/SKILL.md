---
name: project-folder
version: 0.1.0
status: draft
triggers: [used by builds and harness roles when a moonshot starts or resumes; no chat trigger]
dependencies: []
owner: Charles
updated: 2026-10-07
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

## Start (once per project)
1. Create the repo (Custom GitHub MCP `create_repo`, private).
2. Copy every file in agent-library `templates/project-folder/`.
3. Fill `spec.md` from the ask. The Ask section is Charles's words, verbatim, never edited.
4. Turn "Works means" into the first features (priority 1..n) and into the rubric rows.
5. Fill `run.md` and `README.md`. Write the first progress entry.
6. Run `check_folder.py`; it must print OK. Commit.
7. Stop at the concept stop (spec.md Stops #1) before building.

## Resume (start of every session)
1. Read `README.md`, the newest `progress.md` entry, and recent commits.
2. Run the quick health check in `run.md`.
3. Pick the lowest-priority-number feature with `passes: false`. Work only that feature.

## Close (end of every session)
1. Set `passes: true` only with evidence (a test result, screenshot path, measurement). Never edit or delete a feature; add new ones at the end.
2. Add one entry at the top of `progress.md`: did, checked, next, stops.
3. Run `check_folder.py`; it must print OK. Commit with a plain message.

## Rules
- One feature at a time.
- The builder does not grade itself when a checker is available (block 6); until then, evidence is required for every pass.
- Money always stops. Safety rules in spec.md never relax.
