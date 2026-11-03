---
name: expert-desk
version: 0.1.1
status: draft
triggers: ["Expert desk: <situation or plan link> — goal: <one line> — mode: A | A.1 | B (start of a message, any macro design chat)", "I need an expert in <x> / for <x> (a message that starts with it, in a macro design chat)"]
dependencies: []
owner: Charles
updated: 2026-11-03
requires: [skills/expert-desk/references/seat-template.md, skills/expert-desk/references/report-shape.md]
wiring:
  runs: with-you
  starts: "\"Expert desk:\" or \"I need an expert in\" in a macro design chat"
  runs_in: claude-chat
  reads: [agent-library experts, charter, stack-map]
  writes: ["experts/<slug>/BRIEF.md (drafts, via its helper)", "experts/INDEX.md (a grown expert's row, after its check passes)", "project-state notes (reframes, checks)"]
  stack: []
  origin: yours
  label: Expert Desk
---

# Expert Desk

## What
The one skill every expert interaction goes through. It seats experts and it grows
the bench. Experts are thought leadership at Charles's side for planning and design;
they judge, they never execute (TH-135). The desk gives no opinion of its own, never
runs a seat in its own context, never uses the paid orchestrator, never commits a
brief whose reframe Charles has not confirmed, and never checks a brief in the helper
that wrote or proposed it.

## When
**Fire when:** a message starts `Expert desk:`, or `I need an expert in <x>`, in a
macro design chat (Domain Expansion, Stack Advisor, Total Harness).
**Don't fire when:** grading finished work against a rubric (the checker); seven
framings of a brief (a brainstorm chat); a Design Assist chat executing decided work.

## Modes
| Mode | Seated | Output |
|---|---|---|
| A — evaluate and plan | profile's default captains + up to 2 by call_when | full |
| A.1 — pull in the technical people (`carry: <captains>`) | carried captains (default: those whose A findings were not all noted) + each craft under them on the index | captains full; craft risks-only unless `craft: full` |
| B — one expert, one issue (`seat: <expert>` or plain language) | the named seat or the call_when match; no match → Grow | that seat's output; no merge |
A.1 gets the distilled A report as context, never the A papers.

## How — review
| Step | Precondition | Action | Evidence | Recovery |
|---|---|---|---|---|
| 1 Read | situation or plan, goal, mode | Open the plan if it's a link. Load the profile (default `profiles/harness.md`). A.1: load the distilled A report. | Goal in one line | No goal: ask one question and stop. Never invent one. |
| 2 Seat | profile loaded | Read `experts/INDEX.md`. Seat per the mode table, at or under max_seats. | Seat list with mode per seat, plus one expert left out (A) or dropped (A.1) and why | No expert matches, or a craft is named with no brief: go to Grow. Never guess a seat. |
| 3 Brief | seats chosen; the Agent tool is in this session | One prompt per seat from `references/seat-template.md`, with the tools allowlist. Same context block for every seat. | Prompts written | No Agent tool: say "The Expert Desk needs a chat that can start helpers," and stop. Never run seats here; never use the Brainstorm Orchestrator. |
| 4 Run | prompts written | Start every seat in one message (parallel), `subagent_type: general-purpose`, foreground, tools allowlisted. Record tokens per helper. | One reply per seat | A seat fails: say which, retry once, then report without it. |
| 5 Merge | replies in | Merge duplicates and count the seats behind each. Rank *blocks* before *improves*. *noted* is a count only. Name disagreements; don't settle them. Drop any finding about a source its seat didn't read. B: no merge. | Report per `references/report-shape.md` | A seat returned nothing or broke the shape: say which. Don't fill in for it. |
| 6 Report | drafted | Give the report to the calling chat, raw replies collapsed under it. | One page | — |

## How — grow (one gate)
| Step | Precondition | Action | Evidence | Recovery |
|---|---|---|---|---|
| G1 Reframe | step 2 found no match, or Charles said "I need an expert in <x>" | Start a roster-builder helper. It reads the index, decides captain or craft (a craft names its captain; propose the captain first if none fits), writes the seed lens with a source per line, and files the reframe as a Project State note (`expert-proposal`, `expert-<slug>`). Show Charles three lines: name, level + under, call_when. **Stop until he confirms.** | Note id; his one-line confirmation | He changes the level or the line: rewrite the note and continue. He cuts: stop. |
| G2 Research | confirmed | Start a deep-dive helper pointed at the note with `references/expert-deep-dive.md`. It commits `experts/<slug>/BRIEF.md` as draft and reports the SHA. | Commit SHA | "Bigger than a craft" or "smaller than a captain": back to G1 with the new level, no new confirmation needed unless the name changes. |
| G3 Check | SHA | Start a fresh helper seated as the nearest captain (never the helper that wrote or proposed it). It fetches the committed file by SHA, runs the four checks (structural; overlap against every brief on the bench; provenance; first use pending) and files an `expert-check` note citing the SHA. PASS or PASS WITH FIXES: apply the fixes in one more commit and report. FAIL: show Charles the failure and stop. | Check note id; final SHA | Never fix a FAIL silently. |
| G4 Done | check filed | Tell Charles in two lines: the expert is on the bench as draft; it goes active after its first seat yields a finding he tags "new." | — | — |

**Landing.** The calling chat puts a review report into its living artifact as a drafted
block. A finding Charles tags *wrong*, or a miss that reaches him later, becomes a
`lens-note` (`references/expert-brief.md`, "Growing a lens").

## Progress tracking
None. The desk finishes in one run inside the calling chat; that chat's thread covers it.

## Examples
Filled from Build 61.1 run 1 before `status: active`. Grow: the roster-builder run of 2026-11-02 (TH-137 → TH-138 → TH-139).

## Pitfalls
- A proposal or a result carried as chat text or an attachment is lost between chats. Everything lands in the repo or Project State. [dry run 1, 2026-11-02]
- A seat with no tools allowlist can write. [TH-134 line 17]
- A check run on a note has no receipt; run it on the committed file and cite the SHA. [TH-139]
- The chat that proposed a lens then checked the brief that held it. [TH-136, caught by TH-138 line 12]
- Two experts seeded by one chat on one day share lines; overlap-check before commit. [TH-139]

## Changelog
- **0.1.0** (2026-11-03): first version (Build 61, BB-2026-11-02-expert-desk).
