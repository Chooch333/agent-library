---
name: land-and-deploy
version: 0.1.0
status: draft
triggers:
  - "land and deploy"
  - "merge and deploy"
  - "land it"
  - "deploy the PR"
  - "land this"
dependencies: [ship]
owner: Charles
updated: 2026-05-13
source: Adapted from Garry Tan's gstack /land-and-deploy (https://github.com/garrytan/gstack/blob/main/land-and-deploy/SKILL.md). Tan's original handles git merge, CI wait, deploy strategy detection (Vercel/Fly/Render/Netlify), canary verification with browser, revert flow. This reshape uses Custom GitHub MCP for merge and Vercel MCP for deploy status — Charles's actual stack. Browser-based canary verification is dropped; Charles handles that manually.
---

# Land and Deploy

## What

Post-PR-approval orchestration. Merges the PR, watches the deploy, verifies production health, and produces a deploy report. The hand-off from `ship` — ship opens the PR, land-and-deploy closes it out.

In Charles's environment, this role uses Custom GitHub MCP for merge operations and Vercel MCP for deploy status and runtime logs. It does not handle Fly.io, Render, or Netlify (Charles's stack is Vercel-only at present).

## When

**Fire this skill when:**
- A PR is approved and ready to merge
- The user says "land and deploy," "merge and deploy," "land it"
- CI has passed (or is intentionally being merged without CI for hotfix reasons)

**Do NOT fire this skill when:**
- The PR hasn't been reviewed yet (use pr-reviewer first)
- The PR has unresolved review findings (address them first)
- The user wants to deploy without merging (uncommon; ask before proceeding)

## How

### Step 1: Pre-merge checks

Verify the PR is ready:
- PR review (`pr-reviewer`) completed — no critical findings outstanding
- CI status: passing, pending, or failing? Custom GitHub MCP `list_workflow_runs` shows this.
- Any merge conflicts? If yes, STOP and ask Charles to resolve before continuing.

### Step 2: Wait for CI (if pending)

If CI is pending, poll until complete. Standard interval: check every 30s, max 10 minutes.

If CI fails: STOP. Surface the failing job and ask: (A) investigate the failure, (B) merge anyway (rare — only for hotfixes), (C) wait for a re-run.

### Step 3: Pre-merge readiness gate

Final check before merging:
- VERSION bumped (from ship's step 3)?
- CHANGELOG updated?
- TODOs synced?
- Documentation sweep done?

If anything's missing, surface it as a soft warning. The user can still proceed.

### Step 4: Merge

Merge via Custom GitHub MCP. Default to squash merge unless the branch was specifically structured for merge-commit history. Squash produces a cleaner main-branch log; merge-commit preserves the commit-by-commit story.

Strategy:
- Squash if: branch had >5 commits, branch was a feature spike with messy commits, or no specific preference
- Merge-commit if: each commit was deliberately structured for bisecting

After merge, capture the merge commit SHA.

### Step 5: Deploy detection

Charles's deploys are all Vercel-based. After merge:
- Vercel auto-deploys main branch on push (or whichever branch is the production branch)
- Pull the deployment status via Vercel MCP (`list_deployments`, filter by `branch=main`)

If the project doesn't auto-deploy, surface that and ask the user how to trigger it.

### Step 6: Wait for deploy

Poll Vercel MCP every 30s for deployment status:
- `BUILDING` → wait
- `READY` → proceed to canary verification
- `ERROR` → STOP, surface logs via `get_deployment_build_logs`

Max wait: 15 minutes for production deploys, 5 minutes for previews.

### Step 7: Health verification (lightweight)

After deploy is READY:
- Fetch runtime logs for the first 60 seconds post-deploy via Vercel MCP `get_runtime_logs`
- Look for error patterns: 500s, unhandled rejections, OAuth failures, database connection errors
- If any errors appear, surface them and ask: (A) investigate, (B) revert, (C) accept and monitor

If logs are clean, proceed.

**Charles handles deeper canary verification manually** — opening the deployed app, walking through the changed flow, confirming visual + behavioral correctness. The role doesn't automate this (Tan's original used Playwright via the browse daemon; Charles doesn't have that runtime).

### Step 8: Revert flow (if needed)

If the deploy is broken:
- Custom GitHub MCP can't revert directly through the merge UI, so the path is:
  1. Identify the merge commit SHA from Step 4
  2. Either: create a revert PR (`create_or_update_file` with reverted content) and re-run land-and-deploy on the revert; or: use the GitHub UI's "Revert" button manually
- Vercel will auto-deploy the revert once it lands on main
- Surface the deploy URL and confirm the revert is live before declaring "rolled back"

### Step 9: Deploy report

Final summary:

```
DEPLOY REPORT
═══════════════════════════════════════════
PR:               #N — [title]
Merge commit:     [SHA]
Version:          [X.Y.Z]
Deploy URL:       https://...
Deploy status:    READY (took N min)
Runtime errors:   0 in first 60s | [N errors — listed below]
Documentation:    updated / N/A
Status:           SHIPPED | SHIPPED_WITH_CONCERNS | REVERTED
═══════════════════════════════════════════
```

### Step 10: Suggest follow-ups

- Update Project State (Family Trip App or Property Analyzer status snapshot, depending on which project shipped)
- If a Build Brief was the source, log completion against it
- If new TODOs surfaced from review, confirm they're on the list

## Examples

### Example 1: "Land and deploy the slide dedup fix"

→ Step 1: PR review clean, CI green
→ Step 4: squash merge to main
→ Step 5: Vercel auto-deploys family-trip-app
→ Step 6: deploy READY in 90s
→ Step 7: runtime logs clean for first 60s
→ Step 9: SHIPPED report

### Example 2: "Land and deploy the watcher service"

→ Step 1: PR clean, CI green
→ Step 4: squash merge
→ Step 5: Vercel deploys
→ Step 6: deploy READY
→ Step 7: runtime logs show 3 OAuth refresh errors in first 60s
→ Step 7 ask: investigate or accept?
→ Charles: investigate → status is SHIPPED_WITH_CONCERNS, follow-up to watcher logging hardening

## Pitfalls

> Pitfalls come from real traces.

(Draft. Tan documents two pitfalls: (1) declaring "shipped" before logs are checked — the deploy can be `READY` and still have runtime errors in the first minute. Always check logs. (2) The revert temptation — when something looks slightly off, reverting is sometimes the right call but more often it's premature. The investigate-before-revert pattern from `investigate` applies here too.)

## Changelog

- **0.1.0** (2026-05-13) — Initial draft. Reshaped from Tan's gstack /land-and-deploy. Stripped: gstack runtime bash, telemetry, multi-platform deploy detection (Fly/Render/Netlify — kept only Vercel), workspace-aware ship queue (VERSION drift), browse-daemon canary verification, Codex challenge, ~/.gstack/ filesystem ops. Adapted: merge operations via Custom GitHub MCP, deploy status via Vercel MCP, runtime log fetch via Vercel MCP. Kept: pre-merge readiness gate, squash-vs-merge decision, deploy wait pattern, lightweight log-based health check, revert flow guidance, deploy report format.
