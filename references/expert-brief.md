# Expert brief format (0.3.0, draft)

An expert's brief is the instructions for one seat at the Expert Desk. The desk
(`skills/expert-desk`) seats it in a fresh helper (subagent) that answers and writes
nothing. A new brief is proposed and researched by the roster-builder, confirmed once
by Charles, and written, checked, registered and committed by `skills/team-builder`.
Nothing in AGENT.md routes to a brief. "Brief" here is an expert's file; a Build Brief
is a different thing. The expert bench is `experts/`. Experts are thought leadership
for planning and design; they judge, they never execute (TH-135).

An expert knows two things about its corner: how work there ought to go for Charles
(Our way) and how it goes wrong (Lens). A brief with only a lens is a critic, not an
expert (Charles, 2026-11-03).

Folder: `experts/<slug>/BRIEF.md`. Longer material may go in `experts/<slug>/references/`.
Facts about a tool live in cbrain `concepts/` and are listed under `reads`, never copied in.
agent-library is public: no client, job, employer or person specifics in a brief. Point
to the record (a decision or lesson ID, a build, a cbrain entity) instead of quoting it
(Charles, 2026-11-03, design-build-delivery).

## Header (nine fields; `under` is empty only for a captain)
---
name: <slug>
level: captain | craft
under: <captain slug>              # craft: required. No craft without a captain.
profiles: [harness]
call_when: <one line; the desk routes on this only>
altitude: [concept, plan]          # craft: [plan: risks-only, implementation: full]
reads: [<repo>:<path> | <url>, ...] # read at run time; only what exists
version: 0.2.0
status: active                     # an expert is active from the day it lands; no check gate (Charles, 2026-11-04)
---

## Body (in order)
1. **Our way** — how work in this corner ought to go for Charles: what he decided,
   what he prefers, what was tried and dropped. Required for a craft (5–20 lines); a
   captain may carry its field's standing choices (0–20). One line per job that keeps
   coming up in the corner:
   `<job>: <how we do it>; not <what was dropped or ruled out>, because <reason> [source]`
   The source is Charles's own record: the charter, a decision or lesson ID, a build,
   or his stated preference with its date. Where his record is silent and the field
   has a settled default, the line may stand on that, marked `~ field default`. The
   claim and the pointer, never the figure. Our way points to the record; it is not a
   copy of it. At run time the seat checks the live record, and a newer decision beats
   the brief.
2. **Lens** — 10–20 named ways work in this corner goes wrong. One line each, ending
   with its source in brackets: a trace (chat, build, ID), a document, or [research].
   The claim and the pointer, never the figure: numbers age, the paper does not.
   Grown from real misses; never invented. A line not fully carried by its source is
   marked ~ and says what is uncertain. A lens line does not repeat an Our way line.
3. **Procedure** — (1) Read the situation, the goal, `agent-library:references/charter.md`
   and every file under `reads`. (2) Search Project State across all projects for
   decisions and lessons in this corner, using its terms; where one is newer than an
   Our way line and differs, the record wins, and you say so. (3) Open the actual work;
   never judge from a summary when the source is reachable. (4) Walk each Our way line
   and each Lens line against it. (5) Write the output in the mode the desk named.
   (6) Read only, write nothing; you are alone and see no other seat.
4. **Output** — the fixed shapes below.
5. **Never** — speculate past what you read; pad to the cap; soften a blocker; advise
   outside your corner; propose a way the record already ruled out without naming
   the decision that ruled it out.
6. **Changelog**

## Output shape, full
**Seat:** <name> · **Mode:** full
**How I'd do it** — one path, or two when there is a real fork: an A-to-Z sequence of
steps, each citing the Our way line or record it rests on; a step with nothing behind
it is marked *~ new*. (A captain with no Our way lines omits this.)
**Where the work departs from our way** — the line quoted, what the work does instead
**What I would change** (≤3)
**What goes wrong in my corner** (≤8) — each tagged *blocks the goal* | *improves the plan*
| *noted*, naming the part of the work it is about
**Newer than my brief** — any decision or lesson found in step 2 that changes an Our
way line (the desk files it as a lens-note), or "none"
**What I would need to know** (≤2)
**If this failed in three months, why** — one line. Mandatory.
**Read:** every file or page you actually opened, and the searches you ran

## Output shape, risks-only (craft at plan altitude)
**Seat:** <name> · **Mode:** risks-only
**Where the work departs from our way** (≤3)
**What goes wrong in my corner** (≤3, tagged as above)
**Newer than my brief** — as above
**If this failed in three months, why** — one line
**Read:** as above

## Growing a lens
An expert learns from six places (Build 68):

| Where an expert learns | Lands | Written by |
|---|---|---|
| Sources: feeds and pages labeled for it (`experts: [<slug>]` in world-graph `feeds.json`; yt-relay `channels.json`) | the weekly CE run | the CE run |
| A finding Charles tags *wrong* or *new*; a miss that reaches him | at once, lens-note | the desk or the calling chat |
| Decisions newer than its brief (*Newer than my brief*, desk step 6) | at once, lens-note | the desk |
| The stack fix log, stack experts only (`c-stack` and its crafts): `stack_repairs` rows and `stack-incident` lessons | the weekly CE run | the CE run |
| `CE <expert>: <link or topic>` in any chat that can start helpers | at once | the desk |
| Web search (TinyFish `search` only while its wallet shows $0) | the weekly CE run | the CE run |

Each lands as a Project State note on `expert-bench` tagged `expert-<slug>`:
- a **lens-note** (`lens-note`): a change to a line of the brief, one line, in
  Charles's words or the trace's, or marked "Inferred" with the page cited when the
  expert drew it from what it read;
- a **field note** (`field-note`): a CE finding that is not a lens line, something
  true in the corner worth knowing at the next seat, one finding, the page cited.

Every seat reads its waiting lens-notes (no `folded` or `routed` tag) and its latest
field notes before answering (`skills/expert-desk/references/seat-template.md`). Team
Builder update mode folds the waiting lens-notes into the brief at the Sunday 01:00 CE
run (`skills/expert-desk`, CE job): into Our way or the Lens, version bump, changelog.
A seat still never edits its own brief. A note goes to the expert that owns the line;
no line is owned by two experts.

## Changelog
- 0.3.0 (2026-11-04): "Growing a brief" is now "Growing a lens" (the name the desk and
  the roster-builder already used): every way an expert learns, field notes, waiting
  notes read at every seat, folded by Team Builder update mode at the Sunday 01:00 CE
  run. Build 68 (BB-2026-11-03-expert-ce).
- 0.2.0 (2026-11-03): Our way section (required for a craft), How I'd do it and
  Newer than my brief in the output, the charter and a Project State search in the
  procedure, the public-repo rule. Charles: craft experts must know how things ought
  to go in their corner, especially his stack's decisions and preferences.
- 0.1.0 (2026-11-03): first version (Build 61).
