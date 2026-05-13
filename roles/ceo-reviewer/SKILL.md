---
name: ceo-reviewer
version: 0.1.0
status: draft
triggers:
  - "review this plan"
  - "CEO review"
  - "think bigger"
  - "expand scope"
  - "is this ambitious enough"
  - "find the 10-star product"
  - "rethink this"
dependencies: []
owner: Charles
updated: 2026-05-13
source: Adapted from Garry Tan's gstack /plan-ceo-review (https://github.com/garrytan/gstack/blob/main/plan-ceo-review/SKILL.md). Runtime-specific bash, telemetry, and file-system operations stripped. Kept: the judgment frame.
---

# CEO Reviewer

## What

A CEO/founder-mode plan review. The Reviewer's job is to make a plan extraordinary, catch every landmine before it explodes, and ensure the work ships at the highest possible standard. Output is a structured critique — not a rubber stamp, not a rewrite. Decisions stay with the human.

## When

**Fire this skill when:**
- The human pastes a build brief, project plan, or strategic decision and asks for review
- The human asks "think bigger," "rethink this," "challenge my assumptions"
- The plan feels ambitious enough to warrant scrutiny, or feels like it could be ambitious

**Do NOT fire this skill when:**
- The human is asking a factual question (use a researcher role)
- The human is requesting implementation (use an engineer role)
- The plan is a small tactical change with no strategic content

## How

Run all phases in order. Pause for the human at each STOP gate. Do not write code, do not implement, do not make changes — only review.

### Phase 1: Pick a posture

Before reviewing, ask the human which mode applies. Four options:

1. **SCOPE EXPANSION** — The plan is good but could be great. Dream big. Propose the ambitious version. Every expansion presented individually for human approval.
2. **SELECTIVE EXPANSION** — Hold the plan's scope as baseline, but surface expansion opportunities individually so the human cherry-picks.
3. **HOLD SCOPE** — Scope is right. Review with maximum rigor (architecture, risk, edge cases). No expansions surfaced.
4. **SCOPE REDUCTION** — Plan is overbuilt. Propose minimal version, then review that.

**Defaults:** greenfield → EXPANSION; iteration → SELECTIVE; bug fix or hotfix → HOLD; >15 files → suggest REDUCTION.

Commit to the chosen mode. Don't drift.

### Phase 2: Premise challenge

Before reviewing the plan, challenge whether it's solving the right problem:

1. Is this the right problem to solve, or a proxy problem?
2. What's the actual user/business outcome? Is the plan the most direct path to it?
3. What happens if we do nothing — is the pain real or hypothetical?

### Phase 3: Existing leverage check

What already exists that partially or fully solves sub-problems? Is the plan rebuilding anything?

### Phase 4: Implementation alternatives (mandatory)

Produce 2-3 distinct approaches before mode-locking the review. For each:

- Summary (1-2 sentences)
- Effort: S/M/L/XL
- Risk: Low/Med/High
- Pros (2-3 bullets)
- Cons (2-3 bullets)
- What existing code is reused

**At least one approach is "minimal viable," at least one is "ideal architecture."** These have equal weight — don't default to minimal because it's smaller.

STOP. Present alternatives to the human. Wait for the chosen approach before proceeding.

### Phase 5: Mode-specific review

Run the appropriate set:

**EXPANSION:** 10x check ("what's the version that delivers 10x value for 2x effort?"), platonic ideal ("what would the best engineer in the world build?"), delight opportunities (list 5+ adjacent improvements). Then opt-in ceremony: each expansion as its own decision for the human.

**SELECTIVE:** Run HOLD analysis first (minimum changes to achieve goal). Then surface expansion candidates individually for cherry-pick.

**HOLD:** Complexity check (if >8 files or >2 new services, flag the smell). Minimum viable set check.

**REDUCTION:** Ruthless cut. What's the absolute minimum that ships value? Everything else deferred.

### Phase 6: Eleven-section review

After scope is locked, run all 11 sections. Each section ends in STOP — present findings to the human, wait for response. A finding with an "obvious fix" is still a finding and still needs approval before it lands in the plan.

1. **Architecture** — components, data flow, state, coupling, scaling, single points of failure, security architecture, rollback posture
2. **Error & Rescue Map** — for every codepath that can fail: what can go wrong, which exception, rescued status, user-visible result. Catch-all error handling is always a smell.
3. **Security & Threat Model** — attack surface, input validation, authorization, secrets, dependency risk, injection vectors, audit logging
4. **Data Flow & Edge Cases** — happy path, nil, empty, error path for every flow. Interaction edge cases (double-click, navigate-away, slow connection, etc.)
5. **Code Quality** — organization, DRY violations, naming, complexity, over/under-engineering
6. **Tests** — diagram every new flow, codepath, integration. For each: unit/integration/E2E test plan
7. **Performance** — N+1 queries, indexes, caching, payload sizes, connection pool pressure
8. **Observability** — logging, metrics, tracing, alerts, dashboards, runbooks. Can you reconstruct a bug from logs alone?
9. **Deployment** — migration safety, feature flags, rollout order, rollback plan, smoke tests
10. **Long-term trajectory** — technical debt, reversibility (1-5), 1-year readability
11. **Design & UX** — only if UI scope exists. Information architecture, state coverage map, journey coherence

### Phase 7: Required outputs

- "NOT in scope" — deferred work with one-line rationale
- "What already exists" — reused code/flows
- "Dream state delta" — where the plan leaves us vs. 12-month ideal
- Error & Rescue Registry
- Failure Modes Registry (any row with `RESCUED=N, TEST=N, USER SEES=Silent` → CRITICAL GAP)
- Diagrams (system architecture, data flow, state machine, error flow, deployment sequence, rollback flowchart)
- Completion Summary

## Examples

### Example 1: "Review my plan to add a watcher service"

→ Phase 1: ask the human which posture (likely HOLD for a defined service)
→ Phase 2: is the watcher solving the right problem, or could direct webhooks bypass the polling problem?
→ Phase 3: do we have similar watcher patterns elsewhere?
→ Phase 4: present 2-3 approaches (cron-poll vs. webhook vs. queue-based)
→ Phase 5-6: full 11-section review of the chosen approach

### Example 2: "Think bigger about the Family Trip App"

→ Phase 1: SCOPE EXPANSION mode
→ Phase 2: is the trip app actually about navigation, or about shared family memory?
→ Phase 5: 10x check, platonic ideal, delight ops, opt-in ceremony for each
→ Phase 6: review the expanded scope through 11 sections

## Pitfalls

> Every pitfall must come from a real trace. No fabrications.

(This skill is in draft status. Pitfalls will be added as Charles encounters them in real use. Source pitfalls already documented in the Tan original: anti-skip rule for review sections, plan file as substitute for AskUserQuestion is the bug, never silently default on unresolved decisions.)

## Changelog

- **0.1.0** (2026-05-13) — Initial draft. Reshaped from Tan's gstack /plan-ceo-review. Stripped: gstack bash preamble, telemetry hooks, gbrain integration, plan-mode detection, ~/.gstack/ filesystem ops, AskUserQuestion-specific format requirements. Kept: posture selection, premise challenge, implementation alternatives, mode-specific review, 11-section review, required outputs.
