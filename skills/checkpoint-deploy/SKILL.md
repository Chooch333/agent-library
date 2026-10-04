---
name: checkpoint-deploy
version: 0.2
status: adopted
triggers: [a Build Brief header lists checkpoint-deploy among its skills]
dependencies: [orchestrate-build, execute-build-task]
owner: Charles
updated: 2026-09-28
wiring:
  runs: on-its-own
  starts: "loaded by Build lead when named in a brief header"
  runs_in: claude-code
  reads: [assigned-brief]
  writes: [commit-messages, session-log]
  stack: [build-flywheel]
  origin: yours
  label: Checkpoint deploys (pilot)
---

# SKILL: checkpoint-deploy (v0.1 — pilot)

An add-on to `orchestrate-build` and `execute-build-task`. It changes one thing: **how often a build triggers a Vercel preview build.** Nothing else about the build loop, evidence rules, forks, close-out, or the done receipt changes.

Only applies when a Build Brief's header names this skill. Builds that don't name it run exactly as before.

## Why

Today every task commit to `review` triggers a full cbrain-ui build on Vercel (~1 min each, billed as Build CPU Minutes). One build brief produced ~46 preview builds in a day. Only the last one before each live check actually matters.

## Scope (pilot)

cbrain-ui only (`Chooch333/cbrain-ui`, branch `review`). The `cbrain` repo (cbrain-sync) and `main` are out of scope.

## The rule

Every commit the build makes to `review` carries a marker in its commit message:

- **`[wip]`** — the default for every commit. Vercel skips building it. The commit is still pushed to GitHub, so nothing is lost if the session dies, and the worker's commit SHA is still valid evidence.
- **`[deploy]`** — a checkpoint. Vercel builds it (a build always contains everything committed before it, including the skipped `[wip]` commits).

Put a `[deploy]` commit:
1. Immediately before any step that needs the live preview (smoke tests such as `graph-smoke` / `pm-smoke`, "hit the endpoint" verification).
2. As the build's final commit on `review`.

Target: 2–5 `[deploy]` commits per build, not one per task.

If a checkpoint needs a build but the last real change is already committed as `[wip]`, make the checkpoint with a tiny commit (e.g. a line in the brief's git copy or a build note under `docs/`) whose message includes `[deploy]`. `[deploy]` forces a build even for docs-only commits.

## Lead (orchestrate-build) changes

- **Dispatch:** include in every worker task: "Commit message must include `[wip]`." Workers never write `[deploy]`; only the lead decides checkpoints.
- **Verification:** group live-site checks after a checkpoint instead of after every task. File-level checks (read the file back, re-run the query) still happen per task as normal.
- **Before any live check:** confirm the checkpoint's deployment is READY — Vercel `list_deployments` with `projectId: cbrain-ui`, `sha: <checkpoint SHA>`, `teamId: team_8nMi0Bd6orQHGeTrMZYWCamm`.
- **Before close-out (step 7):** confirm a READY deployment exists for the **final** `review` SHA. If the final commit was `[wip]`, make a `[deploy]` checkpoint first. A build must never end with the preview behind the code.

## Worker (execute-build-task) changes

- Add `[wip]` to every commit message. That's all. Evidence rules unchanged — the SHA exists on GitHub.

## Prerequisite (one-time, first task of the pilot build)

cbrain-ui's `vercel.json` must honor the markers. Replace the existing `ignoreCommand` with:

```json
"ignoreCommand": "if [ \"$VERCEL_GIT_COMMIT_REF\" = \"review\" ]; then case \"$VERCEL_GIT_COMMIT_MESSAGE\" in *\"[deploy]\"*) exit 1;; *\"[wip]\"*) exit 0;; esac; fi; git diff --quiet HEAD^ HEAD -- . ':(exclude)docs' ':(exclude)README.md'"
```

Behavior: on `review`, `[deploy]` always builds, `[wip]` always skips; everything else (no marker, or any other branch including `main`) falls through to the existing docs-only skip rule, unchanged. Builds that don't use this skill are unaffected.

This commit itself is a `[deploy]` commit, and its preview must reach READY before any `[wip]` commits are made (proves the config parses and builds).

## Pilot report (required in the Session Log)

At close, add a "Checkpoint-deploy pilot" section to the Session Log:
- Commits made to `review` during the build.
- Vercel deployments created for cbrain-ui during the build, split by READY / CANCELED (skipped) / ERROR — from `list_deployments` with `since` = build start.
- Any check that was harder, slower, or caught later because of batching.
- Any `[wip]` commit that built anyway, or `[deploy]` commit that didn't.

Also post one disclosure (`post_judgment_call`, `plain_title` "Checkpoint-deploy pilot result") summarizing the numbers, so the reviewing DA chat decides whether to adopt system-wide.

## Rollback

Revert the `ignoreCommand` line to its prior value. No other state to undo.

## Changelog

- **v0.1** (2026-09-28) — Pilot. Created from a Vercel bill review: Build CPU Minutes 4.57K vs 252 prior cycle, driven by one preview build per task commit. Overlay rather than edit, per "extend, never modify."
