---
name: pr-reviewer
version: 0.1.0
status: draft
triggers:
  - "review this PR"
  - "review the diff"
  - "pre-PR review"
  - "review before merge"
  - "code review"
  - "ship review"
dependencies: []
owner: Charles
updated: 2026-05-13
source: Adapted from Garry Tan's gstack /review (https://github.com/garrytan/gstack/blob/main/review/SKILL.md). Stripped: gstack runtime bash, telemetry, ~/.gstack/ filesystem ops, Codex CLI cross-model challenge, gstack-diff-scope binary, Greptile integration, workspace-aware ship queue, Persist-Eng-Review-result file writes. Kept: critical pass categories, confidence calibration, fix-first pipeline structure, scope drift detection, adversarial review prompt, the framing that a 5-line auth change can be critical regardless of LOC.
---

# PR Reviewer

## What

Pre-PR / pre-merge code review. Reads the diff between the current branch and base, applies a structured critical pass (security, race conditions, LLM trust boundaries, enum completeness, shell injection, etc.), runs an adversarial pass to find what the structured review misses, and produces a fix-first report. Built to catch bugs that pass CI but break in production.

In Charles's environment, this role uses Custom GitHub MCP to fetch the diff and PR metadata. It does not run git locally and does not auto-commit fixes — it produces a structured report Charles acts on.

## When

**Fire this skill when:**
- A PR is open and ready for review before merge
- A diff exists that needs scrutiny before shipping
- The user asks for "review this PR," "review the diff," "code review," "pre-PR review"

**Do NOT fire this skill when:**
- The work is still being planned (use eng-reviewer or autoplan instead)
- The diff is purely formatting/whitespace (run a linter, not a reviewer)
- The user wants implementation, not review

## How

### Step 0: Branch and scope check

Confirm the PR or branch being reviewed. Fetch:
- The diff (Custom GitHub MCP: `list_pr_files`, then `get_file_contents` on changed files)
- The PR description if there is one
- Any linked issues

If no PR exists yet but a diff is described, ask the user to confirm what's being reviewed.

### Step 1: Scope drift detection

Compare the diff against the original plan (if there was one). Look for:

- **Implementation items** — code that was meant to be written. Was it?
- **Test items** — was the plan's test list actually delivered?
- **Migration items** — DB migrations, env var additions, infrastructure changes — present?
- **Cross-repo items** — did this PR touch repos the plan didn't anticipate?

If the diff materially exceeds the plan's scope, flag and ask before proceeding. Scope creep silently buried in a PR is a critical pattern to surface.

### Step 2: Critical pass

Apply these categories against the diff:

**Critical (always flag):**
- **SQL & Data Safety** — string interpolation in queries, missing indexes on join columns, missing transactions where they're needed, schema mismatches
- **Race Conditions & Concurrency** — shared state without locks, async ordering assumptions, time-of-check vs time-of-use bugs
- **LLM Output Trust Boundary** — places where LLM output is used as code, SQL, or shell without validation
- **Shell Injection** — string interpolation into `exec`/`spawn`, untrusted input in commands
- **Enum & Value Completeness** — when the diff adds a new enum value or status, **read files outside the diff** to find sibling cases. Is the new value handled everywhere it should be? This is the one category where within-diff review is not enough.

**Informational (flag if relevant):**
- Async/Sync mixing
- Column/Field name safety
- LLM prompt issues
- Type coercion bugs
- Frontend/View issues
- Time window safety (off-by-one on date ranges)
- Completeness gaps (code path that's silently incomplete)
- Distribution & CI/CD

**Search before recommending.** When recommending a fix pattern, verify it's current best practice for the framework version in use. Check for built-in solutions before recommending workarounds. APIs change between versions.

### Step 3: Confidence calibration on every finding

Every finding includes a confidence score (1-10):

| Score | Meaning | Display |
|---|---|---|
| 9-10 | Verified by reading specific code. Concrete bug or exploit demonstrated. | Show normally |
| 7-8 | High confidence pattern match. Very likely correct. | Show normally |
| 5-6 | Moderate. Could be a false positive. | Show with caveat |
| 3-4 | Low confidence. Pattern is suspicious but may be fine. | Appendix only |
| 1-2 | Speculation. | Only if severity would be P0 |

Finding format: `[SEVERITY] (confidence: N/10) file:line — description`

Example: `[P1] (confidence: 9/10) family-trip-app/src/api/trips/route.ts:42 — SQL injection via string interpolation in where clause`

### Step 4: Adversarial pass (always-on)

After the structured pass, run an adversarial review with a different framing. Think like an attacker and a chaos engineer. Look for:
- Edge cases the structured pass missed
- Race conditions not on the explicit checklist
- Security holes
- Resource leaks
- Failure modes — what happens when this fails?
- Silent data corruption paths
- Logic errors that produce wrong results silently
- Error handling that swallows failures
- Trust boundary violations

Be adversarial. Be thorough. No compliments — just the problems.

For each adversarial finding, classify:
- **FIXABLE** — you know how to fix it. Goes into the Fix-First pipeline.
- **INVESTIGATE** — needs human judgment. Presented as informational.

End with ONE canonical recommendation line:
> "Recommendation: [action] because [one-line reason naming the most exploitable finding]"

Examples:
- `Recommendation: Fix the unbounded retry at queue.ts:78 because it'll DoS the worker pool under sustained 429s`
- `Recommendation: Ship as-is because the strongest finding is a theoretical race that requires conditions we can't trigger in production`

Generic reasons like "because it's safer" do not qualify. The reason must point to a specific finding.

### Step 5: Fix-first pipeline

Don't just report — propose fixes for FIXABLE findings.

For each fixable finding:
1. Quote the problematic code
2. Show the fix as a diff
3. State the impact: what does the fix prevent?
4. Note any tradeoff (does it slow something down? add complexity?)

In Charles's environment, fixes get proposed in the report. Charles (or a downstream coding session) applies them via Custom GitHub MCP (`replace_in_file` or `create_or_update_file`).

### Step 6: TODOs cross-reference

If the repo has a `TODOS.md`, check:
- Are any deferred items in this PR's blast radius?
- Could any deferred items be bundled into this PR without expanding scope?
- Does this PR create new work that should be a TODO?

### Step 7: Documentation staleness

Did this PR change behavior, APIs, or schemas? Are docs updated to match? Flag stale documentation in touched files.

### Final report format

```
# PR Review: <PR title or branch>

## Scope drift
[any mismatch between plan and diff]

## Critical pass findings
1. [SEVERITY] (confidence: N/10) file:line — description
   Fix: <code diff>
2. ...

## Informational findings
[lower-severity items, in confidence order]

## Adversarial findings
[anything the structured pass missed]
- FIXABLE: ...
- INVESTIGATE: ...

## Recommendation
[the one-line canonical recommendation]

## TODO updates
[new TODOs surfaced by this review]

## Doc staleness
[docs that need updates]
```

## Examples

### Example 1: "Review the watcher service PR"

→ Step 0: fetch diff via Custom GitHub MCP
→ Step 1: scope check — plan had 5 files, diff has 12; flag the extras
→ Step 2 critical pass: flag the Vercel timeout risk (architectural), the prompt-injection vector in email subject parsing
→ Step 4 adversarial: catch the unbounded OAuth refresh-retry that wasn't on the checklist
→ Recommendation: "Fix the OAuth refresh retry at watcher.ts:142 before merging — it'll lock you out of Outlook after 100 sequential failures."

### Example 2: "Review the cash-out refi calculator PR"

→ Step 0: fetch diff
→ Step 1: plan matched diff
→ Step 2 critical pass: flag type-coercion on the LTV inputs (string vs number), flag missing rounding on the dollar amounts
→ Step 4 adversarial: flag what happens when interest rate is 0 (division by zero in the amortization formula)
→ Recommendation: "Fix the divide-by-zero at refi.ts:88 before merging — a user could plug in 0% and crash the analyzer."

## Pitfalls

> Pitfalls come from real traces.

(Draft. Tan documents two critical pitfalls: (1) using LOC as a proxy for risk — a 5-line auth change can be more dangerous than a 500-line refactor. The structured pass must run regardless of size. (2) The "Enum & Value Completeness" trap — when a new enum value is added, the bug is almost always in the file that wasn't touched. Within-diff review misses these. Grep for sibling values and read those files.)

## Changelog

- **0.1.0** (2026-05-13) — Initial draft. Reshaped from Tan's gstack /review. Stripped: gstack runtime bash, telemetry, ~/.gstack/ filesystem ops, Codex CLI cross-model challenge, gstack-diff-scope binary, Greptile integration, workspace-aware ship queue, Step 5.8 persist-result file writes. Adapted: git operations now go through Custom GitHub MCP. Kept: scope drift detection, critical pass categories, confidence calibration, fix-first pipeline, adversarial review prompt and canonical recommendation format, TODO cross-reference, documentation staleness check.
