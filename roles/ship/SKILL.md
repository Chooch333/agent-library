---
name: ship
version: 0.1.0
status: draft
triggers:
  - "ship it"
  - "ship this"
  - "open the PR"
  - "ready to ship"
  - "ship pre-flight"
dependencies: [pr-reviewer]
owner: Charles
updated: 2026-05-13
source: Adapted from Garry Tan's gstack /ship (https://github.com/garrytan/gstack/blob/main/ship/SKILL.md). Tan's original is a 3,000-line orchestration covering tests, version bump, CHANGELOG, TODOS, commits, push, doc sync, PR creation, persisted metrics. Most of that depends on Claude Code's local file system and git. This reshape keeps the *order of operations* and *gates*, adapted to Charles's stack — tests run locally by Charles, while review, version bump, CHANGELOG, commits, and PR creation flow through Custom GitHub MCP.
---

# Ship

## What

Pre-ship orchestration. Walks through the gates that prevent broken code from leaving the branch: review, version bump, CHANGELOG, commits, push, PR creation. The role does not run tests — Charles runs tests locally (Vercel preview, manual). The role handles everything else through Custom GitHub MCP.

The discipline this enforces: never skip the gates. A PR opened without a CHANGELOG entry will be reviewed for the CHANGELOG, slowing the loop. The order is the point.

## When

**Fire this skill when:**
- A branch is ready to leave the local environment
- The user says "ship it," "open the PR," "ready to ship"
- A feature or fix is complete and tested locally

**Do NOT fire this skill when:**
- The code still has known issues (use investigate first)
- The plan or design hasn't been reviewed (use pr-reviewer first)
- The user wants to deploy something already merged (use land-and-deploy)

## How

### Step 1: Pre-flight

Confirm the basics:
- Branch name and current state
- What's in the diff (scope summary)
- Have tests been run? (Yes/no question. If no, the user should run them before continuing.)
- Is there a linked plan, build brief, or issue? (Pull context if so.)

### Step 2: PR Review (the gate)

If this branch hasn't been through `pr-reviewer` in its current state, run it now. PR Reviewer produces:
- Critical findings (must address before ship)
- Informational findings (judgment call)
- Adversarial findings (one final pass)
- The canonical recommendation line

If critical findings exist, STOP. Address them, then re-run.

If only informational findings, present them and ask: "Address before ship, or carry as known?"

### Step 3: Version bump (auto-decide)

If the repo follows semver and has a VERSION file or version field in package.json:
- **Patch** — bug fixes, no API changes, no behavior changes user-visible. Most common.
- **Minor** — new features, backward-compatible. Use when adding a new endpoint, new component, or expanded functionality.
- **Major** — breaking changes. Use only when an existing user would have to update their code/config.

Default to **patch** unless the diff clearly warrants more. Auto-decide unless the user wants to override.

For Charles's apps (Property Analyzer, Family Trip App), this is mostly aesthetic — there are no external consumers requiring strict semver — but it makes the CHANGELOG more readable.

### Step 4: CHANGELOG (auto-generate)

Generate or update CHANGELOG.md entry:

```markdown
## [VERSION] — YYYY-MM-DD

### Added
- [user-visible new things]

### Changed
- [user-visible changed things]

### Fixed
- [user-visible bug fixes]

### Removed
- [things that were removed]
```

Pull from the diff and commit messages. Skip empty categories. Use plain English — what a future-Charles would want to read. Not "Bumped version" — say what shipped.

### Step 5: TODOS.md (auto-update)

If the repo has a TODOS.md:
- Remove any TODOs this PR completes
- Add any new TODOs surfaced during review (with what / why / context per the pr-reviewer format)

### Step 6: Commits (bisectable chunks)

Review the commits on the branch. If they're a mess of "wip" and "fix typo" commits, propose squashing into logical chunks:
- One commit per logical change
- Commit message in imperative ("Add cash-out refi calculator", not "Added")
- First line ≤72 chars, blank line, then prose body for context

If the user prefers to ship as-is, that's fine — just confirm.

### Step 7: Push

Push the branch via Custom GitHub MCP (`create_or_update_file` for each commit, or treat the branch as ready if commits were made through other means).

### Step 8: Documentation sync (one-pass)

Did this PR change behavior, APIs, schemas, or env vars? Sweep docs and update what's stale:
- README.md
- Any `docs/` files referenced by the changed code
- API documentation if applicable
- Inline JSDoc/comments that reference changed signatures

### Step 9: Create PR/MR

Open the PR via Custom GitHub MCP. Body template:

```markdown
## Summary
[1-2 sentence what + why]

## Changes
[bullet list of meaningful changes, in user-visible terms]

## Test plan
[how was this tested locally — manual, Vercel preview, unit tests]

## Pre-Landing Review
[link to or summary of pr-reviewer findings]

## Scope drift
[any mismatch between original plan and diff]

## Documentation
[docs updated: ✅, or N/A]
```

### Step 10: Ship report

Final summary:
- PR URL
- Version bumped to: X
- CHANGELOG entry: [paste]
- TODOs added/removed
- Anything outstanding for follow-up

## Examples

### Example 1: "Ship the family trip app slide dedup fix"

→ Pre-flight: tests run (Vercel preview shows fix working), no linked plan since this was an investigate output
→ PR review: pr-reviewer was run, one informational finding about edge case (0-photo trip), Charles chose to carry as known
→ Version bump: patch (bug fix only)
→ CHANGELOG: "Fixed slideshow showing duplicate photos across slides"
→ TODOs: removed the related TODO
→ Push → PR opened → ship report

### Example 2: "Ship the property analyzer cash-out refi calculator"

→ Pre-flight: tests run, linked to a build brief
→ PR review: pr-reviewer flagged divide-by-zero; Charles fixed it; re-ran; clean
→ Version bump: minor (new feature)
→ CHANGELOG: "Added cash-out refinance calculator with LTV cap and DSCR feasibility check"
→ TODOs: added two new TODOs from review (insurance escrow handling, multiple refi scenarios)
→ Documentation: updated README's feature list, added section on refi math to docs/analyzer.md
→ PR opened → ship report

## Pitfalls

> Pitfalls come from real traces.

(Draft. Tan documents the biggest pitfall: skipping the review gate because "I already reviewed it myself." The shipper is the last person who should review their own code — they're tired and want to ship. The pr-reviewer gate exists for that reason. In Charles's environment, the equivalent is shipping without running pr-reviewer in agent-library — the discipline only works if the gate fires.)

## Changelog

- **0.1.0** (2026-05-13) — Initial draft. Reshaped from Tan's gstack /ship. Stripped: gstack runtime bash, telemetry, ~/.gstack/ filesystem ops, automatic test runner integration, Greptile review, Codex challenge, gstack-version-queue (workspace-aware), persist-ship-metrics file write. Adapted: git/push/PR-create operations now route through Custom GitHub MCP. Kept: pre-flight, review gate, version bump auto-decision, CHANGELOG auto-generation, TODOs sync, commit hygiene, documentation sync, PR body template, ship report.
