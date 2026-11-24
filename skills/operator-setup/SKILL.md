---
name: operator-setup
version: 0.1.0
status: draft
triggers:
  - "I need an operator for <x>" / "I need an operator to <x>" (a message that starts with it, in any chat that can start helpers, mid-chat included)
dependencies: [expert-desk, team-builder]
owner: Charles
updated: 2026-11-24
requires: [references/charter.md, references/operator-mandate.md, experts/operator-design/BRIEF.md]
wiring:
  runs: with-you
  starts: "\"I need an operator for ...\" in any chat that can start helpers"
  runs_in: claude-chat
  reads: [operator-design brief, operator mandates, operator-run, project-state, the live data the new Operator would manage]
  writes: ["project-state notes (operator-draft)", "operator-log test rows"]
  stack: []
  origin: yours
  label: Operator setup
---

# Operator setup

**Rules first** (read these even if nothing else survives):
1. One confirmation from Charles, at step 4. Nothing is written to any repo before it.
2. Draft before you ask. Every answer that his ask, this chat or his records can supply is drafted for him; he corrects, he does not fill in a form. Mark each drafted line "yours" (his words, quoted) or "Inferred".
3. The questions and their tests are the operator-design expert's Our way lines; this skill holds none of its own. Read them fresh each run; never work from memory of them.
4. This skill judges nothing and writes no files. The expert judges (step 3); `skills/team-builder` operator mode writes (step 5).
5. His goal stays in his words. Never narrow it, add a time span, or call an Operator a job, an assignment or a role.
6. Plain words to Charles: no ids, file paths or table names in what he reads (charter, Communicate cleanly).

## What
How Charles creates a new Operator by saying one phrase. An Operator is, in his words, "a broader scale, long duration goal that is achieved by judging how to use varied skills to perform varied tasks over a longer time horizon". This skill walks him through the steps that define one (drafted for him first), has the operator-design expert test the answers, takes his one confirmation, hands the result to Team Builder to write the Operator's tech items, and proves it on hidden test data. Running an Operator afterwards is `skills/operator-run`.

## When
**Fire when:** a message starts "I need an operator for" or "I need an operator to", in any chat that can start helpers.
**Don't fire when:** he wants an existing Operator run (`skills/operator-run`); he wants an existing mandate changed (seat operator-design on the change, mode B, then an ordinary edit he directs); he wants an expert ("I need an expert in": `skills/expert-desk`); the chat cannot start helpers (say "Setting up an Operator needs a chat that can start helpers," and stop).

## How
| Step | Action | Evidence | Recovery |
|---|---|---|---|
| 0 Tools | Check the helper tool, Custom GitHub, and Supabase on cbrain (`select count(*) from operator_log`). Note the time. | Each reached or not | No helper tool: stop, as above. No Supabase: carry on to step 4, and say the test (step 6) waits for a chat that has it. |
| 1 Read | Fetch `experts/operator-design/BRIEF.md` (Our way: the walk-through steps and their tests, then the tech items), `references/operator-mandate.md`, and the Operator table in `skills/operator-run/SKILL.md`. Search Project State across all projects for what Charles has already said or decided about this goal. Read the live data the Operator would manage, enough to know what a run could see. | Files and records read | An Operator already in the table covers this goal: tell him in one line and offer to change its mandate; stop. |
| 2 Walk the steps | One page, one block per walk-through step from the brief, in its order: the question in plain words, then the drafted answer marked yours or Inferred. Ask him only what cannot be drafted, as closed choices with a recommendation. He answers in one reply; fold his words in exactly. Repeat until he has nothing to change. | The page; his words | He gave only a phrase: draft all of it and say so. Never send him to fetch something a tool can read. |
| 3 Seat the expert | Expert Desk, mode B, seat operator-design, mode full. The work: every answer from step 2. It applies each step's test and says pass or fail with the reason. | The seat's reply; the desk files its report | First step fails (it is a skill, not an Operator): tell him plainly, say what skill or reference page would do the job, and stop. Any other fail: fix the answer, show him what changed and why, and seat again only if his answer changed. |
| 4 Confirm | Show him two things in plain words: the mandate as it will read (what it's for, what it may do alone / only on your ask / never, how it's checked, its moves and when each is used, how it starts and reports), and the list of what will be built. **Stop until he confirms.** Then file the confirmed answers, the seat's verdicts and the mandate text as one Project State note on `cbrain`, tags `operator-draft`, `operator-<slug>`. | His one-line confirmation; note id | He changes a line: update and continue. He cuts it: stop, file nothing. |
| 5 Build | Load `skills/team-builder/SKILL.md`, operator mode, pointed at the `operator-draft` note. | Team Builder's receipt | A mechanical FAIL: show him the failing lines in plain words and stop. Never fix it here. |
| 6 Test | Run the new Operator through `skills/operator-run` on hidden test data, every log row flagged test: two different asks must pick two different moves; the second run must re-check the first run's wait with no reminder; nothing is written to a real record. | The log rows | No hidden test data exists for what it manages: say so, name what test data is needed, and leave the mandate draft. A test that fails: say which, and stop. |
| 7 Receipt | Tell him in a few plain lines: the Operator exists, how to start it (Duet, or its phrase), what the test showed, and what is still unproven. Its mandate stays draft until its proof count (operator-run, Proof). | — | — |

## Progress tracking
Follows `references/thread-checkin.md` (naming convention and when to check in).
- kind: chat (a Design Assist chat uses its own card)
- build: the Operator's title + "setup", e.g. "Stack Keeper setup"
- Opens when: step 2's page is shown
- Checks in: end of every turn
- Closes when: the receipt is given, or Charles cuts it (`close_thread`, closed_how "Operator set up" or "dropped")

## Examples
**By hand, before this skill (2026-11-24): the Project Manager.** A Design Assist chat walked the same steps without the skill: goal in Charles's words; scope read live across all his FAW jobs; authority (reads, logs and drafts alone; job changes only on his ask); standing check with Charles and a separate count as checkers; four read-only moves with a use-when fact each; Duet as starter; the shared log; a hidden-data test. Six experts were seated, because the category itself was being designed; a setup run seats one. His corrections in that chat became the rules above: he replaced a narrowed definition with his own sentence, and asked for new terms to be explained plainly.

**First run under this skill.** None yet. Expect this skill to be rewritten after it: it was written from one Operator.

## Pitfalls
- The designer narrowed Charles's definition to "one subject" and "weeks" and he had to correct it; the goal is drafted in his words and marked yours. [CB-759]
- A first design draft assumed the Operator's writes would land at once and that a job change is made by a phrase in a chat; the live system said otherwise on both. Step 1 reads the live data and the door before step 2 drafts an authority line. [CB-763; operator-design Lens 14]
- Design items decided early were replaced the same day (who starts it, where its jobs are listed, when the button is built); step 1 searches the record for the newest decision before drafting. [operator-design Lens 5]
- A builder written from one example copies that example's quirks; the brief marks which tech items are the category and which were the first Operator's own, and the writer copies only the first kind. [operator-design Lens 3; TH-102]

## Changelog
- **0.1.0** (2026-11-24): first version, built inline in the Operator design chat. Charles: "I want to be able to say a trigger phrase like I just did for the expert, and then I want to walk through some steps to create the operator and I want the structure of the operator's tech items." Questions and tests live in experts/operator-design (EB-380, EB-381); writing is team-builder operator mode.
