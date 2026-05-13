---
name: autoplan
version: 0.1.0
status: draft
triggers:
  - "autoplan"
  - "auto plan"
  - "run the full plan review"
  - "review chain"
  - "CEO design eng review"
dependencies: [ceo-reviewer, design-reviewer, eng-reviewer, devex-reviewer]
owner: Charles
updated: 2026-05-13
source: Adapted from Garry Tan's gstack /autoplan (https://github.com/garrytan/gstack/blob/main/autoplan/SKILL.md). Stripped: gstack runtime bash, Codex CLI cross-model second opinion, telemetry, ~/.gstack/ filesystem ops. Kept: 6 decision principles, decision classification (Mechanical / Taste / User Challenge), sequential phase execution rule, two non-auto-decided exceptions.
---

# AutoPlan

## What

Chains the four plan-mode review roles into a single sequential run: CEO Reviewer → Design Reviewer → Eng Reviewer → DevEx Reviewer. Auto-decides intermediate questions using six explicit principles, surfaces only the final approval gate to the user. Saves the user from having to walk through 30+ individual review questions when most of them have clear right answers.

This is a meta-role — it doesn't add new judgment; it sequences the other four roles efficiently.

## When

**Fire this skill when:**
- The user asks for "autoplan," "run the full review," "review chain," "all four reviews"
- A build plan needs the full strategic + design + technical + DX gate but the user doesn't want to micromanage every intermediate question
- The plan is substantive enough to warrant all four reviews

**Do NOT fire this skill when:**
- The user wants a specific single review (use that role directly)
- The plan has no UI (design phase makes no sense)
- The plan has no developer-facing surface (DX phase makes no sense)
- The user explicitly wants to be in the loop on every question — they should use the individual roles

If the plan has no UI, skip the Design phase. If no developer-facing surface, skip the DevEx phase. Announce which phases apply at the start.

## How

### The 6 Decision Principles

These rules auto-answer every intermediate question across the four reviews:

1. **Choose completeness.** Ship the whole thing. Pick the approach that covers more edge cases.
2. **Boil lakes.** Fix everything in the blast radius (files this plan touches + direct importers). Auto-approve expansions that are in blast radius AND under 1 day of effort (< 5 files, no new infra).
3. **Pragmatic.** If two options fix the same thing, pick the cleaner one. 5 seconds choosing, not 5 minutes.
4. **DRY.** Duplicates existing functionality? Reject. Reuse what exists.
5. **Explicit over clever.** 10-line obvious fix beats 200-line abstraction. Pick what a new contributor reads in 30 seconds.
6. **Bias toward action.** Merge > review cycles > stale deliberation. Flag concerns but don't block.

**Conflict resolution (context-dependent tiebreakers):**
- **CEO phase:** P1 (completeness) + P2 (boil lakes) dominate
- **Eng phase:** P5 (explicit) + P3 (pragmatic) dominate
- **Design phase:** P5 (explicit) + P1 (completeness) dominate
- **DX phase:** P1 (completeness) + P6 (bias toward action) dominate

### Decision Classification

Every auto-decision is classified into one of three buckets:

**Mechanical** — one clearly right answer. Auto-decide silently.
*Example:* "Should we add a regression test for this bug fix?" → Always yes.

**Taste** — reasonable people could disagree. Auto-decide using the principles, but surface at the final gate for visibility.
*Example:* Two viable approaches with different tradeoffs.

**User Challenge** — the analysis suggests the user's stated direction should change (merge, split, add, remove features the user specified). This is NEVER auto-decided. Always surfaces to the user with rich context:
- What the user said (original direction)
- What the analysis recommends (the change)
- Why (the reasoning)
- What context we might be missing (explicit blind spots)
- If we're wrong, the cost is (what happens if the user's original direction was right)

The user's original direction is the default. The analysis must make the case for change, not the other way around.

### Sequential Execution — MANDATORY

Phases MUST execute in strict order:

```
CEO Reviewer → Design Reviewer → Eng Reviewer → DevEx Reviewer
```

Each phase MUST complete fully before the next begins. NEVER run phases in parallel — each builds on the previous.

Between each phase, emit a phase-transition summary and verify required outputs from the prior phase are present before starting the next.

### What "Auto-Decide" Means

Auto-decide replaces the USER'S judgment with the 6 principles. It does NOT replace the ANALYSIS. Every section in the loaded role's SOP must still be executed at the same depth as the interactive version. The only thing that changes is who answers the question: this role does, using the 6 principles, instead of the user.

**Two exceptions — NEVER auto-decided:**
1. **Premises** (the premise-challenge phase in each review) — these require human judgment about what problem to solve
2. **User Challenges** — when the analysis suggests the user's stated direction should change

### Operating loop

1. Announce which phases apply (skip Design if no UI; skip DX if no developer surface)
2. **CEO phase**: load `roles/ceo-reviewer/SKILL.md`, run the full SOP, auto-decide all mechanical and taste questions using the 6 principles, escalate premises and User Challenges only
3. **Design phase** (if applicable): load `roles/design-reviewer/SKILL.md`, same pattern
4. **Eng phase**: load `roles/eng-reviewer/SKILL.md`, same pattern
5. **DevEx phase** (if applicable): load `roles/devex-reviewer/SKILL.md`, same pattern
6. **Final gate**: present a consolidated review report — list all auto-decisions (Mechanical + Taste), all User Challenges surfaced, all unresolved premises. Ask the user to approve, override, or request a specific re-review.

### Final report format

```
# AutoPlan Review Report

## Phases run
- CEO Reviewer (X auto-decisions, Y escalations)
- Design Reviewer (X auto-decisions, Y escalations)
- Eng Reviewer (X auto-decisions, Y escalations)
- DevEx Reviewer (X auto-decisions, Y escalations)

## Escalated to user
1. [Premise] ...
2. [User Challenge] ...

## Auto-decisions taken (Taste category — visible)
- CEO: ...
- Eng: ...
- Design: ...
- DevEx: ...

## Mechanical decisions (silent — surface on request)
- 47 mechanical decisions taken using P1-P6

## Recommendations needing approval
1. ...
```

## Examples

### Example 1: "AutoPlan the watcher service plan"

→ Announce: all four phases apply
→ CEO phase: principle-based auto-decisions on scope (P2 boil lakes → expand to include idempotency layer since it's in blast radius), surface one User Challenge ("CEO Reviewer suggests considering webhooks instead of polling — your original direction was cron-poll")
→ Design phase: skipped (no UI)
→ Eng phase: full 4-section review, auto-decisions on architecture/code-quality/tests/performance
→ DevEx phase: skipped (internal service, no developer surface)
→ Final report: 1 User Challenge to resolve (poll vs webhook), 8 auto-decisions visible, 23 mechanical taken silently

### Example 2: "AutoPlan the Property Analyzer monitoring dashboard"

→ Announce: all four phases apply (UI + dev API)
→ CEO phase: premise check on whether monitoring dashboard is the right wedge or whether direct-deal-flow is
→ Design phase: 7-pass review, auto-decisions on hierarchy/states/AI-slop, surface User Challenge if design analysis recommends materially different layout than user specified
→ Eng phase: auto-decisions on storage layer (P4 DRY → reuse existing IRR calculator)
→ DevEx phase: if the dashboard exposes an API, run the 8 DX passes; otherwise skip
→ Final report: consolidated approval gate

## Pitfalls

> Pitfalls come from real traces.

(Draft. Tan flags two critical pitfalls from the original: (1) running phases in parallel to "save time" — this corrupts the chain because each phase informs the next; (2) auto-deciding User Challenges silently — this is the failure mode the User Challenge classification exists to prevent. The user must be the decider when the analysis disagrees with the user's stated direction.)

## Changelog

- **0.1.0** (2026-05-13) — Initial draft. Reshaped from Tan's gstack /autoplan. Stripped: gstack runtime bash, telemetry, Codex CLI integration for cross-model verification, ~/.gstack/ filesystem ops. Kept: 6 decision principles, decision classification (Mechanical / Taste / User Challenge), sequential phase execution rule, two never-auto-decided exceptions (premises, User Challenges), final gate format.
