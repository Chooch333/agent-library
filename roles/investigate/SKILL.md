---
name: investigate
version: 0.1.0
status: draft
triggers:
  - "investigate this bug"
  - "debug this"
  - "find the root cause"
  - "why is this broken"
  - "what's causing"
  - "trace this issue"
dependencies: []
owner: Charles
updated: 2026-05-13
source: Adapted from Garry Tan's gstack /investigate (https://github.com/garrytan/gstack/blob/main/investigate/SKILL.md). Stripped: gstack runtime bash, telemetry, gstack-learnings-search and gstack-learnings-log binaries, freeze/scope-lock filesystem ops, git command auto-execution, cross-project learnings prompt. Kept: Iron Law, 5-phase investigation structure, pattern table, 3-strike rule, red flags, regression-test requirement, debug-report format.
---

# Investigate

## What

Systematic root-cause debugging. The Iron Law is: **no fixes without root cause investigation first.** Symptoms-only fixes create whack-a-mole bugs that compound. This role forces a disciplined sequence — gather context, form a hypothesis, test it, then fix — and produces a structured debug report at the end.

## When

**Fire this skill when:**
- Something is broken or behaving incorrectly
- The user reports an error, timeout, wrong output, or intermittent failure
- The user asks to "debug," "investigate," "find the root cause," "trace this issue"
- A previous fix didn't hold and the bug is back

**Do NOT fire this skill when:**
- The user wants to add a new feature (use a planning role)
- The fix is mechanical (typo, obvious one-character bug) — just fix it
- The user is asking how something works (it's a question, not a bug)

## How

### Iron Law

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST.**

Fixing symptoms creates whack-a-mole debugging. Every fix that doesn't address root cause makes the next bug harder to find. Find the root cause, then fix it.

This rule has zero exceptions during investigation. If pressured to "just patch it for now," refuse and explain: "No patches without root cause. We can timebox the investigation, but we can't skip it."

### Phase 1: Root Cause Investigation

Gather context before forming any hypothesis.

1. **Collect symptoms.** Read error messages, stack traces, reproduction steps. If the user hasn't provided enough context, ask ONE question at a time.
2. **Read the code.** Trace from the symptom back to potential causes. Use grep to find references, read to understand logic. In Charles's environment, use Custom GitHub MCP `get_file_contents` and `search_code`.
3. **Check recent changes.** Was this working before? What changed? A regression means the root cause is in the diff. (`list_commits`, `list_pr_files`.)
4. **Reproduce.** Can you trigger the bug deterministically? If not, gather more evidence before proceeding.
5. **Check prior investigations.** Have you investigated this file or this area before? Recurring bugs in the same place are an architectural smell, not a coincidence.

Output: **"Root cause hypothesis: ..."** — a specific, testable claim about what is wrong and why.

### Phase 2: Pattern Analysis

Check if the bug matches a known pattern:

| Pattern | Signature | Where to look |
|---|---|---|
| Race condition | Intermittent, timing-dependent | Concurrent access to shared state |
| Nil/null propagation | NoMethodError, TypeError | Missing guards on optional values |
| State corruption | Inconsistent data, partial updates | Transactions, callbacks, hooks |
| Integration failure | Timeout, unexpected response | External API calls, service boundaries |
| Configuration drift | Works locally, fails in staging/prod | Env vars, feature flags, DB state |
| Stale cache | Shows old data, fixes on cache clear | Redis, CDN, browser cache, Turbo |

Also check:
- TODOS or known-issues docs for related items
- Recent commits for prior fixes in the same area — recurring bugs are an architectural smell, not a coincidence

**External pattern search.** If the bug doesn't match a known pattern, web search for:
- `{framework} {generic error type}` — **sanitize first:** strip hostnames, IPs, file paths, SQL, customer data. Search the error category, not the raw message.
- `{library} {component} known issues`

### Phase 3: Hypothesis Testing

Before writing ANY fix, verify the hypothesis.

1. **Confirm the hypothesis.** Add a temporary log/assertion at the suspected root cause. Run the reproduction. Does the evidence match?
2. **If wrong:** consider searching the (sanitized) error before forming the next hypothesis. Return to Phase 1. Gather more evidence. Do not guess.
3. **3-strike rule.** If 3 hypotheses fail, **STOP**. Ask:
   - A) Continue — new hypothesis is [describe]
   - B) Escalate — this needs someone who knows the system
   - C) Add logging and wait — instrument the area, catch it next time

**Red flags — slow down if you see any of these:**
- "Quick fix for now" — there is no "for now." Fix it right or escalate.
- Proposing a fix before tracing data flow — you're guessing.
- Each fix reveals a new problem elsewhere — wrong layer, not wrong code.

### Phase 4: Implementation

Once root cause is confirmed:

1. **Fix the root cause, not the symptom.** Smallest change that eliminates the actual problem.
2. **Minimal diff.** Fewest files touched, fewest lines changed. Resist refactoring adjacent code.
3. **Write a regression test** that:
   - Fails without the fix (proves the test is meaningful)
   - Passes with the fix (proves the fix works)
4. **Run the full test suite.** No regressions allowed. Paste the output.
5. **If the fix touches >5 files:** flag the blast radius and ask:
   - A) Proceed — the root cause genuinely spans these files
   - B) Split — fix the critical path now, defer the rest
   - C) Rethink — maybe there's a more targeted approach

### Phase 5: Verification & Report

**Fresh verification.** Reproduce the original bug scenario and confirm it's fixed. This is not optional.

Run the test suite and paste the output.

Debug report format:
```
DEBUG REPORT
════════════════════════════════════════
Symptom:         [what the user observed]
Root cause:      [what was actually wrong]
Fix:             [what was changed, with file:line references]
Evidence:        [test output, reproduction attempt showing fix works]
Regression test: [file:line of the new test]
Related:         [TODO items, prior bugs in same area, architectural notes]
Status:          DONE | DONE_WITH_CONCERNS | BLOCKED
════════════════════════════════════════
```

## Examples

### Example 1: "Investigate why the Family Trip App's slideshow keeps showing the same photo twice"

→ Phase 1: read the slideshow component, the photo-selection logic, the trip data; check recent commits to trip-tour.tsx
→ Hypothesis: "The photo-selection RNG isn't deduping across slides."
→ Phase 2: matches "state corruption" pattern
→ Phase 3: confirm with a log on the selected-photos array — yes, duplicates appear
→ Phase 4: fix the dedup logic, add a regression test that builds a 6-slide tour and asserts unique photos
→ Phase 5: report

### Example 2: "Debug why the watcher service is missing emails"

→ Phase 1: gather logs, error messages, Supabase row counts
→ Hypothesis 1: "OAuth token expired silently." Test → no, refresh logs are clean.
→ Hypothesis 2: "Vercel cron is hitting timeout before all emails processed." Test → yes, cron logs show 10s timeout on batches >50 emails.
→ Phase 2: matches "integration failure" pattern, also "configuration drift" (prod batch size higher than local)
→ Phase 4: fix by paginating the watcher loop, adding regression test that mocks 100 emails and confirms all are processed
→ Phase 5: report. Status: DONE_WITH_CONCERNS — flag that we should also increase Vercel timeout as defense-in-depth

## Pitfalls

> Pitfalls come from real traces.

(Draft. Tan documents two critical pitfalls: (1) skipping reproduction before forming a hypothesis — you'll guess. The Iron Law exists because the temptation to "just try this fix" is constant. (2) Refactoring adjacent code "while we're in there" — turns a 3-line fix into a 30-file diff that's impossible to review. Minimal-diff discipline.)

## Changelog

- **0.1.0** (2026-05-13) — Initial draft. Reshaped from Tan's gstack /investigate. Stripped: gstack runtime bash, telemetry, gstack-learnings-search/log binaries, freeze/scope-lock filesystem ops, automatic git command execution, cross-project learnings prompt. Adapted: file/code access now uses Custom GitHub MCP. Kept: Iron Law, 5-phase investigation, pattern table, 3-strike rule, red flags, regression-test requirement, debug-report format.
