# Expert brief format (0.1.0, draft)

An expert's brief is the instructions for one seat at the Expert Desk. The desk
(`skills/expert-desk`) seats it in a fresh helper (subagent) with a tools allowlist.
Nothing in AGENT.md routes to a brief. "Brief" here is an expert's file; a Build Brief
is a different thing. The expert bench is `experts/`. Experts are thought leadership
for planning and design; they judge, they never execute (TH-135).

Folder: `experts/<slug>/BRIEF.md`. Longer material may go in `experts/<slug>/references/`.
Facts about a tool live in cbrain `concepts/` and are listed under `reads`, never copied in.

## Header (nine fields; `under` is empty only for a captain)
---
name: <slug>
level: captain | craft
under: <captain slug>              # craft: required. No craft without a captain.
profiles: [harness]
call_when: <one line; the desk routes on this only>
altitude: [concept, plan]          # craft: [plan: risks-only, implementation: full]
reads: [<repo>:<path> | <url>, ...] # read at run time; only what exists
version: 0.1.0
status: draft
---

## Body (in order)
1. **Lens** — 10–20 named ways work in this corner goes wrong. One line each, ending
   with its source in brackets: a trace (chat, build, ID), a document, or [research].
   The claim and the pointer, never the figure: numbers age, the paper does not.
   Grown from real misses; never invented. A line not fully carried by its source is
   marked ~ and says what is uncertain.
2. **Procedure** — (1) Read the situation, the goal and every file under `reads`.
   (2) Open the actual work; never judge from a summary when the source is reachable.
   (3) Walk each lens line against it. (4) Write the output in the mode the desk
   named: 8 findings at most (full), 3 (risks-only). (5) Read only, write nothing; you
   are alone and see no other seat.
3. **Output** — the fixed shapes below.
4. **Never** — speculate past what you read; pad to the cap; soften a blocker; advise
   outside your corner.
5. **Changelog**

## Output shape, full
**Seat:** <name> · **Mode:** full
**Options I would add** (≤3): option — its trade
**What I would change** (≤3)
**What goes wrong in my corner** — each tagged *blocks the goal* | *improves the plan*
| *noted*, naming the part of the work it is about
**What I would need to know** (≤2)
**If this failed in three months, why** — one line. Mandatory.
**Read:** every file or page you actually opened

## Output shape, risks-only (craft at plan altitude)
**Seat:** <name> · **Mode:** risks-only
**What goes wrong in my corner** (≤3, tagged as above)
**If this failed in three months, why** — one line
**Read:** as above

## Growing a lens
A finding Charles tags *wrong*, or a miss that reached him, becomes a Project State
note on the calling project tagged `lens-note` and `expert-<slug>`: one line, in his
words or the trace's. A later brief folds lens notes in (version bump, changelog).
A seat never edits its own brief. Lens notes go to the expert that owns the line;
no line is owned by two experts.
