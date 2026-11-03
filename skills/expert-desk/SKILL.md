---
name: expert-desk
version: 0.3.0
status: draft
triggers: ["Expert desk: <situation or plan link> — goal: <one line> — mode: A | A.1 | B (start of a message, any macro design chat)", "I need an expert in <x> / for <x> (a message that starts with it, in any chat that can start helpers)", "I need a team of experts for <x> / I need a group of experts for <x> (a message that starts with it, mid-chat included, in any chat that can start helpers)"]
dependencies: [team-builder]
owner: Charles
updated: 2026-11-03
requires: [skills/expert-desk/references/seat-template.md, skills/expert-desk/references/report-shape.md]
wiring:
  runs: with-you
  starts: "\"Expert desk:\", \"I need an expert in\" or \"I need a team of experts for\""
  runs_in: claude-chat
  reads: [agent-library experts, charter, stack-map]
  writes: ["project-state notes (expert-proposal, expert-team-proposal, expert-draft, expert-team-fit)"]
  stack: []
  origin: yours
  label: Expert Desk
---

# Expert Desk

## What
The one skill every expert interaction goes through. It seats experts and it grows
the bench. Experts are thought leadership at Charles's side for planning and design;
they judge, they never execute (TH-135). The desk gives no opinion of its own, never
runs a seat in its own context, never uses the paid orchestrator, and never has a
helper write anything: experts answer the problem in front of them, the desk files
their answers as Project State notes, and `skills/team-builder` writes files. The desk
never calls Team Builder for an expert whose reframe Charles has not confirmed.

## When
**Fire when:** a message starts `Expert desk:` in a macro design chat (Domain
Expansion, Stack Advisor, Total Harness) or a Design Assist chat; a Design Assist chat
seats experts on its own at its steps 5–6 (design space and traps) whenever the work
matches a call_when on the index; or `I need an expert in <x>` in any chat
that can start helpers, since the need for an expert shows up where the work is;
or `I need a team of experts for <x>` (or `a group of experts`) in any chat that can
start helpers, usually a few turns in, after Charles has talked through which experts
the work needs. Names are optional: with them, the roster-builder starts from his list;
without, it finds the team from the situation.
Grow-run notes always go on the Project State project `expert-bench`, whatever chat
the ask came from; experts span every domain Charles works in, not only the harness.

**Words.** With Charles, use only the bench's own terms: expert, domain captain (or
captain), craft expert (or craft), brief, bench, index, seat, lens, roster-builder,
Team Builder. Never translate them: no "role", "lead", "parent", "persona" or
"reviewer". He reads these files; a synonym costs him the thread.
**Don't fire when:** grading finished work against a rubric (the checker); seven
framings of a brief (a brainstorm chat); a build chat executing decided work.

## Modes
| Mode | Seated | Output |
|---|---|---|
| A — evaluate and plan | profile's default captains + up to 2 by call_when | full |
| A.1 — pull in the technical people (`carry: <captains>`) | carried captains (default: those whose A findings were not all noted) + each craft under them on the index | captains full; craft risks-only unless `craft: full` |
| B — one expert, one issue (`seat: <expert>` or plain language) | the named seat or the call_when match; no match → Grow | that seat's output; no merge |
A.1 gets the distilled A report as context, never the A papers. The roster-builder
(`altitude: [grow]`) is never seated in a review mode.

## How — review
| Step | Precondition | Action | Evidence | Recovery |
|---|---|---|---|---|
| 1 Read | situation or plan, goal, mode | Open the plan if it's a link. Load the profile card for the work's domain from `profiles/` (`harness` for Charles's stack, `construction` for a construction project or pursuit; one card per domain, named in each captain's `profiles:`). A.1: load the distilled A report. | Goal in one line | No goal: ask one question and stop. Never invent one. |
| 2 Seat | profile loaded | Read `experts/INDEX.md`. Seat per the mode table, at or under max_seats. | Seat list with mode per seat, plus one expert left out (A) or dropped (A.1) and why | No expert matches, or a craft is named with no brief: go to Grow. Never guess a seat. |
| 3 Brief | seats chosen; the Agent tool is in this session | One prompt per seat from `references/seat-template.md`. Same context block for every seat. Note the time. | Prompts written; start time | No Agent tool: say "The Expert Desk needs a chat that can start helpers," and stop. Never run seats here; never use the Brainstorm Orchestrator. |
| 4 Run | prompts written | Start every seat in one message (parallel), `subagent_type: general-purpose`, foreground. Seats are read-only by instruction: the helper tool takes no tool list, so each seat has every tool this chat has. Record tokens per helper. | One reply per seat | A seat fails: say which, retry once, then report without it. |
| 5 Check | replies in; start time | List what changed since the start time: commits on agent-library and on any repo the work names, and new Project State rows on the calling project. A review run expects none. | Writes found, or "none" | Anything found goes under *Writes during the run* in the report, with what and where (it may be another session's). Never undo it silently. |
| 6 Merge | replies in | Merge duplicates and count the seats behind each. Rank *blocks* before *improves*. *noted* is a count only. Name disagreements; don't settle them. Drop any finding about a source its seat didn't read. B: no merge. | Report per `references/report-shape.md` | A seat returned nothing or broke the shape: say which. Don't fill in for it. |
| 7 Report | drafted | Give the report to the calling chat, raw replies collapsed under it. | One page | — |

## How — grow (one gate)
| Step | Precondition | Action | Evidence | Recovery |
|---|---|---|---|---|
| G1 Propose | step 2 found no match, or Charles said "I need an expert in <x>" | Note the time. Start a roster-builder helper for its Proposal output. It returns name, level, under, call_when, documents, seed lens and deep-dive scope as text. The desk files that as a Project State note on `expert-bench` (`expert-proposal`, `expert-<slug>`) and shows Charles three lines: name, level + under, call_when. **Stop until he confirms.** | Note id; his one-line confirmation | He changes the level or the line: update the note and continue. He cuts: stop. |
| G2 Research | confirmed | Start a second roster-builder helper for its Research output, pointed at the proposal note and `references/expert-deep-dive.md`. It returns the whole new BRIEF.md and the captain's revisions as text. The desk files that as a note on `expert-bench` (`expert-draft`, `expert-<slug>`). The level (captain or craft) is the roster-builder's call in G1; the desk never asks Charles to pick it. | Note id | "Bigger than a craft" or "smaller than a captain": back to G1 at the new level; no new confirmation unless the name changes. |
| G3 Build | draft note filed | Load `skills/team-builder/SKILL.md`, expert mode, pointed at the draft note. It writes the brief, applies the captain's revisions, runs the mechanical checks, adds the index row, commits, reads back and returns a receipt. | Team Builder's receipt: SHAs, index row, check results | A mechanical FAIL: show Charles the failing lines and stop. Nothing is committed. Never fix it here. |
| G4 Done | receipt | Run step 5's check from G1's start time. Expected writes: the two notes and Team Builder's commits; show Charles anything else. Then tell him in two lines: the expert is on the bench and the index as draft, and the captain's brief changed (what moved); it goes active after its first seat yields a finding he tags "new." | — | — |

## How — grow a team (one gate)
Same rules as single grow; the difference is that every expert is laid out against its
teammates before any is researched. Helpers never see this chat, so step T0's team ask
is all they get of it.

| Step | Precondition | Action | Evidence | Recovery |
|---|---|---|---|---|
| T0 Ask | Charles said "I need a team (or group) of experts for <x>" | Note the time. Write the team ask from this chat: the situation in one paragraph, quoting Charles; every expert he named or the chat surfaced, each with his own words for it; this chat's link. Read every file or plan the chat named. | Ask text | No situation can be stated from the chat: ask one question and stop. Never invent one. |
| T1 Team proposal | ask written | Start one roster-builder helper for its Team proposal output, given the ask. It returns one row per expert (new, on the bench, fills a stub, merged, cut, or added), the build order and the profile card. The desk files ask and answer as one note on `expert-bench` (`expert-team-proposal`, `expert-team-<slug>`) and shows Charles one table: name · level + under · call_when · new / on the bench / fills a stub / merged / cut / added, with the count of experts to research. **Stop until he confirms.** | Note id; his one-line confirmation | He changes a row: update the note and continue. He cuts a row: drop it. He cuts all: stop. |
| T2 Research | confirmed | Start one roster-builder helper per row marked new, fills a stub or added, all in one message (parallel), each for its Research output, pointed at the team note, its own row and `references/expert-deep-dive.md`. File each answer as a note (`expert-draft`, `expert-<slug>`, `expert-team-<slug>`). | One note id per row | A helper fails: retry once, then that row stops and the rest go on; a captain's stop also stops its crafts in this team. "Bigger than a craft" or "smaller than a captain": that row alone goes back through T1 at the new level; no new confirmation unless its name changes. |
| T3 Fit | every running row has a draft note | Start one fresh roster-builder helper for its Fit output, given the team note, every draft note and the bench. It returns the lines to cut or reword where teammates overlap, one merged set of revisions per captain (each moved line keeps the craft it moves to), and any two call_when lines that would fire on the same work. File it (`expert-team-fit`, `expert-team-<slug>`). | Note id | — |
| T4 Build | fit note filed | Load `skills/team-builder/SKILL.md`, team mode, pointed at the team note, the draft notes and the fit note. | Team Builder's team receipt | A mechanical FAIL stops that expert and any craft under it in this team; the rest land. Show Charles the failing lines; never fix them here. |
| T5 Done | receipt | Run step 5's check from T0's start time. Expected writes: this run's notes and Team Builder's commits; show Charles anything else. Then tell him in a few lines: who is on the bench as draft, who stopped and why, which captain briefs changed, and which profile card now seats the team. | — | — |

**Landing.** The calling chat puts a review report into its living artifact as a drafted
block. A finding Charles tags *wrong*, or a miss that reaches him later, becomes a
`lens-note` (`references/expert-brief.md`, "Growing a lens").

## Progress tracking
None. The desk finishes in one run inside the calling chat; that chat's thread covers it.

## Examples
Filled from Build 61.1 run 1 before `status: active`. Grow: the roster-builder run of 2026-11-02 (TH-137 → TH-138 → TH-139) was the old four-step flow; the first run under this version fills this in.

## Pitfalls
- A proposal or a result carried as chat text or an attachment is lost between chats. Every helper answer lands in a Project State note before the next step. [dry run 1, 2026-11-02]
- The helper tool takes no tool list per call, so every seat has every tool the chat has; read-only rests on the instruction, and step 5 checks what was written. [TH-134 line 17; TH-J-045]
- A check run on a note has no receipt; Team Builder checks the file it wrote and reads it back from main. [TH-139]
- Two experts seeded by one chat on one day share lines; Team Builder's overlap check runs against every brief on the bench. [TH-139]
- A grown expert written to the bench but not the index is never seated, and the desk tries to grow it again; Team Builder writes the index row in the same run. [TH-J-044]
- A captain seated to pass judgment on a craft in a field it does not hold; the captain's brief is revised when a craft joins, it is not asked to approve it. [Charles 2026-11-03, Build 64]
- A team asked for a few turns into a chat: the experts were named earlier, in Charles's words, and a helper never sees the chat. The team ask quotes them and is filed in the proposal note. [Charles 2026-11-03, Build 65]
- Teammates researched in parallel are blind to each other; two crafts joining one captain would each rewrite its brief. The fit pass reads them together and merges each captain's revisions once. [Build 65; TH-139]

## Changelog
- **0.3.0** (2026-11-03): grow a team. `I need a team of experts for <x>` (or `a group`), mid-chat included: team ask from the chat → one team proposal → Charles confirms once → research in parallel → fit pass → Team Builder team mode, captains first, a failed expert stops only itself and its crafts. Single grow unchanged (Build 65, BB-2026-11-03-team-grow).
- **0.2.2** (2026-11-03): grow-run notes go on the new Project State project `expert-bench`, not `total-harness`, because experts span every domain Charles works in (Charles, first grow run). Words rule added: the bench's terms only, never role, lead, parent, persona, reviewer.
- **0.2.1** (2026-11-03): `I need an expert in` fires in any chat that can start helpers; the level is the roster-builder's call, never a question to Charles. From the first grow run, asked in a FAW job chat, which had no Project State project to file on.
- **0.2.0** (2026-11-03): grow is propose → confirm → research → build. Helpers write nothing; the desk files notes; `skills/team-builder` writes the brief, the captain's revisions and the index row. The captain check step is removed (Build 64, BB-2026-11-03-team-builder).
- **0.1.2** (2026-11-03): experts answer and write nothing; the desk writes. The tools allowlist is dropped (the helper tool cannot set one); new step 5 lists anything written during a run, and grow's G4 does the same (Build 61.3, BB-2026-11-03-expert-seats-answer; TH-J-045).
- **0.1.1** (2026-11-03): grow step G3 adds the expert's row to `experts/INDEX.md` after its check passes, in the desk's fix commit (Build 61.2, BB-2026-11-03-expert-index-row; TH-J-044).
- **0.1.0** (2026-11-03): first version (Build 61, BB-2026-11-02-expert-desk).
