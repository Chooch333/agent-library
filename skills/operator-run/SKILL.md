---
name: operator-run
version: 0.1.0
status: draft
triggers:
  - "PM: <job>" or "PM: what needs me" (a message that starts with it, in any chat, mid-chat included)
  - "run the <Operator title>" / "run my Operators" (Duet or any chat, on demand or on Duet's cadence)
dependencies: [job-update, expert-desk]
owner: Charles
updated: 2026-11-24
requires: [references/charter.md, references/operator-mandate.md]
wiring:
  runs: with-you
  starts: "Duet, on demand or on its cadence; or \"PM: <job>\" in any chat"
  runs_in: claude-chat
  reads: [operator mandates, cbrain-supabase, operator-log]
  writes: [operator-log]
  stack: [project-manager]
  origin: yours
  label: Operator run
---

# Operator run

**Rules first** (read these even if nothing else survives):
1. The mandate decides what this Operator may do. Re-read its Authority table before any write. Not in "May, alone" → don't.
2. Live data every time. Never answer from the log, a past report or memory. The log holds what the Operator did and waits on, never job status.
3. The log is insert-only: never UPDATE or DELETE a row.
4. Run as this session itself, never as a helper, so the one helper level stays free for an expert seat.
5. Say what you could not reach. Reading nothing is never "all clear".
6. What Charles reads: plain words, people by name, items by title, no ids or table names (charter, Communicate cleanly).

## What
The one routine every Operator follows each time it is started. An Operator is, in Charles's words, "a broader scale, long duration goal that is achieved by judging how to use varied skills to perform varied tasks over a longer time horizon" (CB-759). Its mandate (`operators/<slug>/MANDATE.md`) says who it is; this skill is how any of them runs once: check what this session can reach, read the live data, re-check what it was waiting on, pick the move that fits the ask, log, report. The log carries the long horizon, because every session starts fresh. A new Operator is a new mandate page and one more row below; never a new run skill.

| Operator | Start phrases | Mandate |
|---|---|---|
| Project Manager | `PM: <job>`, `PM: what needs me`, "run the Project Manager" | `operators/project-manager/MANDATE.md` |

## When
**Fire when:** a message starts with an Operator's start phrase, in any chat; Duet is asked to run an Operator or its cadence comes due ("run my Operators" with no name = every Operator in the table, one after another).
**Don't fire when:** Charles only wants a job changed ("add this" with no Operator named → `skills/job-update`); the ask is where the stack stands (`skills/stack-chief-of-staff`); the ask is how something should be done (seat the expert).

## How
Read `references/charter.md` first when GitHub is reachable.

0. **Where am I running.** Note: is Charles here (a chat or a Duet ask) or is this a cadence run with nobody present; is the helper tool here; and one cheap call per door the mandate needs. Supabase (cbrain `lpeswznkxzeeyiqaewma`): `select count(*) from operator_log`. Custom GitHub: the mandate fetch itself. A door that fails: retry once, then name it under "could not see" and carry on with what is left. No Supabase → give no read of the data; say so and stop.
1. **Load the mandate** for the Operator named (table above). Take Authority, Scope and Bench from it.
2. **Read the live data in scope**, by the mandate's Scope. First line of every report: how fresh the record is (for jobs: the newest `applied_at` in `pm_package_status` for that job, by anyone). One line, never an alarm or a question.
3. **Re-check open waits.** `select id, scope_ref, why, ref, clears_when from operator_log w where operator = '<slug>' and action = 'wait' and not exists (select 1 from operator_log o where o.action = 'outcome' and o.outcome = 'cleared' and o.detail->>'for' = w.id::text) order by run_at`. A `clears_when` is one read-only SELECT on the live tables that returns true once the wait is over; run nothing else from it. For each: insert an `outcome` row (`detail.for` = the wait's id, `outcome` `cleared` or `still-open`, `why` in plain words). A wait that cleared, and one still open after 14 days, both go in the report.
4. **Answer the ask.** Choose from the Bench's "Use when" lines only, by what step 2 showed. Fetch only the one file that move names; never open a bench file to decide. Evidence: one line naming the live fact behind the choice. Nothing fits → say "nothing useful to do right now" and log that; never invent a move. A cadence run with no ask: for each thing in scope (the mandate's Scope says what that is), the first Bench row whose "Use when" is true, at most one each; so a mandate's row order is its priority.
5. **At most one unasked move** when Charles is present: only a Bench row whose "Use when" is plainly true and that he did not ask for. Offer it in one line; do it only if it writes nothing.
6. **Log.** Re-read the Authority table. Insert, in this order: one `move` row per move (`why`, `detail.move`, `detail.ask`, `detail.evidence`); a `wait` row for each new thing the Operator is waiting on (`why`, `ref` = the item's id, `clears_when`); one `report` row (`detail.channel` chat | duet | email, `detail.named` = ids named this time, so the next run knows what he last heard); last, one `run` row saying what it read and did, with `detail.lane`, `detail.doors`, `detail.asked`. A test or build run puts `"test": true` in every row's detail, and such rows never count as what he last heard.
7. **Report**, in the mandate's Report shape, where the run was started. Email only when Charles asked for email: Gmail `send_message` from the relay inbox to his own address, subject `<Operator title> — <Mon D>`. If the send is held for his approval, give the report where the run is and put `"email": "held"` in the report row. Never email anyone else.

**Needs from Charles.** Anything only he can do is said under "needs you" in the report. No card, no second message.

**Something broken.** A table that will not read, or a mirror plainly out of step with the job screen: one `reported` row in the stack fix log (`skills/stack-repairer/SKILL.md`, Reported problems), then carry on.

**Proof.** When an Operator's `report` rows without `"test": true` reach six and no row for it carries `detail.proof_verdict`, insert one `reported` row in the stack fix log: finding "Count the <title> proof: six real runs are in its log", recheck `select exists (select 1 from operator_log where operator = '<slug>' and detail ? 'proof_verdict')`. The count is done by a separate build or chat, never this run: kinds of move chosen; waits a later run cleared without his reminder; log rows that restate status. Every run the same move, or no wait ever carried → it is a skill, and the verdict says so.

## Progress tracking
None. A run leaves nothing open on the Next steps list: what it waits on lives in its log and is re-checked next run; what waits on Charles is in the report.

## Examples
**Build-day test, 2026-11-24 (hidden test job, every row flagged test).** Run 1, ask "what has no owner?": freshness line (record last changed Oct 8); Bench → gap check (evidence: one open item with no accountable person); logged one move, one wait whose check is "that item has an accountable person", one report, one run row. Run 2, ask "who do I need to chase?": step 3 found the one open wait, re-ran its check (still no owner), logged `still-open`; Bench → follow-up drafts (evidence: one item past its date with an owner). Two asks, two different moves, one wait carried between runs with no reminder. No package written to the job.

**First Duet run.** None yet. It proves, from Duet itself: the starter skill loads, the mandate fetch works, the Supabase read and one log insert land, the report comes back, and (when asked) the email sends or holds.

## Pitfalls
- No change had landed on any construction job for a month when this was designed; a read given without its age reads as current. Step 2's freshness line is always first. [pm_package_status, newest row 2026-10-23, read 2026-11-24]
- A job change no longer lands in minutes: the writer's on-push run has been off since 2026-10-12 and Charles chose to leave it (CB-763). Never tell him a change failed because it is not on the screen yet; it lands at the nightly run. [world-graph write_protocol.yml; CB-763]
- Duet's reach to the Custom GitHub, Supabase and Project State connectors had no record when this shipped, and its help page says it asks before sending a message. Step 0 tries each door instead of assuming; step 7 handles a held email. [Expert Desk report CB-762]
- A scheduled task's "succeeded" marks that it woke, not that the work ran. The `run` row, written last, is the proof a run happened. [CB-762, lanes]
- An Operator that adds its own items ends up reporting gaps it created; job writes stay on Charles's ask. [CB-754, ai-system-design; CB-758]

## Changelog
- **0.1.0** (2026-11-24): first version, built inline in the Operator design chat at Charles's direction ("lets build this operator now"). Decisions CB-753, CB-758, CB-759, CB-761, CB-763; Expert Desk reports CB-754, CB-762.
