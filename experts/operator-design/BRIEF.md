---
name: operator-design
level: craft
under: ai-system-design
profiles: [harness]
call_when: "Charles asks for an Operator, the work creates one or changes a mandate (its goal, authority, standing check, scope, bench, or how it starts and reports), or weighs whether a skill that runs on its own should become one; how Claude's parts fit together in general stays with ai-system-design, the wording of operator-run or any SKILL.md with skill-authoring, growing an expert with roster-builder, and where the log lives, which lane a run uses and how a run is checked with data-homes, lanes and oversight"
altitude: [plan: risks-only, implementation: full]
reads: ["agent-library:references/charter.md", "agent-library:references/operator-mandate.md", "agent-library:skills/operator-run/SKILL.md", "agent-library:operators/project-manager/MANDATE.md", "agent-library:skills/job-update/references/job-moves.md", "agent-library:CONVENTIONS.md (Words: Operator, Mandate, Operator log; the operator-run row; Hard rules)", "agent-library:AGENT.md (Operators row; Disambiguation rules)", "agent-library:references/skill-design-framework.md (Q2, Q10, Q11)", "agent-library:skills/stack-repairer/SKILL.md (Reported problems)", "cbrain:concepts/stack-map.md (flow node project-manager; its Stack Flow paragraph; search, not whole)"]
version: 0.1.0
status: active
---

# operator-design

How an Operator is designed for Charles: whether a goal is an Operator at all, what each part of its mandate must say, and which tech items a new Operator needs. An Operator is, in his words, "a broader scale, long duration goal that is achieved by judging how to use varied skills to perform varied tasks over a longer time horizon" (CB-759).

This seat judges; it writes nothing. A walk-through skill asks Charles the questions and Team Builder writes the files. Our way 1 to 9 are the walk-through's steps, each with the test his answer must pass. Our way 10 to 17 are the tech items a writer must complete, each marked *category* (every Operator) or *first Operator's own* (the Project Manager's particulars, not to be copied).

Outside this corner: how Claude's parts fit together in general (ai-system-design); the wording of operator-run or any SKILL.md (skill-authoring); growing an expert (roster-builder); where the log lives (data-homes); which lane a run uses and what it can reach (lanes); how a run is checked and drawn (oversight).

Everything here comes from one Operator, built 2026-11-24, with no real run yet (Lens 1). A seat treats only Charles lines as settled.

## Our way

**The walk-through: one line per step, with the test the answer must pass**

1. Operator or skill, asked first: it is an Operator only when the goal needs a choice among at least two kinds of move on different asks, and something carried from one run to the next. Test: name two asks that would get two different moves, and one thing a later run must re-check. Fails → it is a skill, extended or given a reference page; not a mandate page laid over a skill that already has its goal, because the Stack Repairer got no page (it does not choose among skills, and a page nothing reads drifts) and the Stack Chief of Staff was ruled a skill [Claude · CB-758 item 5; CB-754 section 5; CB-740; operator-run Proof; Charles: CB-609 for the Chief of Staff]
2. The goal: his own one or two sentences, as broad as he states it. Test: it reads as an outcome that can be met or missed over a long horizon, and it is his wording, not a narrower paraphrase; not a "one subject" limit, a stated time span or a finish date added by the designer, and never called a job, an assignment or a role, because he corrected exactly that [Charles · CB-753; CB-759; EB-377; CONVENTIONS Words: Operator]
3. Scope: the kind of thing covered and the live read (the query or door) each run uses to find it. Test: a fresh session could list what is in scope today from that read alone, and the page names no job, client, person or company; not a stored list (a "posted on" line in the mandate, posting rows in the log), because the repo is public and a stored list is a seed nothing updates; both were drafted and dropped [Claude · operator-mandate.md Rules; project-manager MANDATE Scope; CB-754 section 2; CB-764 "Dropped"; Charles: the public-repo rule, 2026-11-03, expert-brief.md]
4. Authority: three columns. Alone: reads, inserts in its own log, drafts inside its report, seating an expert. Only on his ask: any change to the data its standing check reads, made through the skill that already owns that write, with the line saying how his ask arrives. Never: sending to anyone but him, editing the data's tables directly, saying its own goal is met. Test: no "may, alone" entry changes anything the standing check counts; not a write alone at creation, because it would then report gaps it created; loosening is one choice brought to him after real runs [Claude · CB-758 item 3; CB-754 sections 3 to 5; project-manager MANDATE Authority; Charles: CB-515, write-on-ask for his job data]
5. Standing check and who checks: facts read live each time, and a named checker that is not the Operator (Charles by using the reports and the screen, plus the separate count of its log). Test: each item can be answered by one read of live data today, and the checker line names someone; not "the Operator confirms", and not a check read from its own log [Claude · operator-mandate.md Rules; project-manager MANDATE Standing check; CB-754 section 1, Oversight; CB-740; Charles: charter item 3]
6. Moves (the Bench): one row per move: its name, its use-when, the one file it reads, whether it writes. Test per row: the use-when is a fact one read of the live data or its own log shows true or false; the file exists; a "Yes" under Writes matches an "only on his ask" line; and at least two rows are different kinds of move. A new move is a read-only reference page under the skill that owns the data's door; not a skill per move, because same data, same door and same trigger fail the split test and break the three-skill cap; not a mood ("when useful") [Claude · operator-mandate.md Rules; CB-758 item 4; job-moves.md changelog; CONVENTIONS Hard rules; skill-design-framework Q2]
7. Starts and reports: started by Duet, on demand or on the one cadence he sets there for all Operators, or by a plain phrase in any chat. It reports where the run was started, by email only when he asked, and to him only. The first line of every report says how old the record it read is; what needs him is said in the report. Test: each start phrase is checked against every AGENT.md row, and the Starts and Report lines promise nothing the lane has not been shown to do (lanes' call); not a scheduled task per Operator, and not "on demand in chats first", which his Duet decision replaced [Charles · CB-761; EB-378; Claude: CB-762; operator-run steps 2 and 7; c-stack Our way 13]
8. The log: rows under its slug in the shared log: what it did, what it waits on (each wait with one read-only check that turns true when the wait is over), and what he last heard. The Log line says what must never go in it. Test: delete the log and no fact about what it manages is lost; not status, dates or titles copied from the live data, and not a new table, a graph write or repo files, because the log is Claude's work record, not the truth about the thing managed [Claude · CB-758 items 1 and 2 and alternatives; operator-run rules 2 and 3, step 3; CONVENTIONS Words: Operator log; project-manager MANDATE Log]
9. Test and proof: the build proves it on hidden test data with every row flagged test: two asks get two different moves, one wait is carried and re-checked with no reminder, and nothing is written to a real record. Status stays draft. Proof is a separate count after six real reports (kinds of move chosen; waits a later run cleared unreminded; log rows that restate status), ending in a verdict: Operator, or skill; not a real job inside the build, and not called proven on build day [Charles · TH-062; Claude: operator-run Examples and Proof; CB-754 section 1, Oversight; skill-design-framework Q11]

**The tech items: what a writer completes for any new Operator**

10. Mandate page (*category*): `operators/<slug>/MANDATE.md` per `references/operator-mandate.md`: under sixty lines, tables, Authority first, the header line (slug, version, status, owner, updated), the template's sections in order under their exact headings, status draft. It points at skills and at the stack map's lane row and restates neither. Created or edited only by a build or design chat Charles directed, or by the writer he has confirmed a walk-through for [Claude · operator-mandate.md; CONVENTIONS, the line under the operator-run row; Charles: CB-759, the mandate as "the essence of what the operator is"]
11. Run registration (*category*): one row in the Operator table in `skills/operator-run/SKILL.md` (title, start phrases, mandate path). Nothing else: no run skill, no CONVENTIONS row (operator-run's row covers every Operator), no index of Operators before a third exists [Claude · operator-run What; CONVENTIONS operator-run row; CB-754 section 1]
12. Start phrases (*category*; the phrase itself is each Operator's own): added to the AGENT.md Operators row, plus one Disambiguation line when a phrase could fire another row. *First Operator's own:* its short prefix and the "Operator vs job work" line, needed because its data already had a routing row [Claude · AGENT.md Operators row and Disambiguation rules; CB-754 section 1, Registration]
13. Bench pages (*category*): each new move is a section of a read-only reference page under the skill that owns the door; never a skill per move. *First Operator's own:* its four moves in one file, its day counts, its four report parts [Claude · job-moves.md; CB-758 item 4]
14. Log rows (*category*): rows under its slug in cbrain `operator_log`, using the five actions it already has (run, move, wait, outcome, report), insert-only, test rows flagged in detail; no new table, column or migration. *First Operator's own:* what its scope reference holds [Claude · operator_log columns and rows, read 2026-11-24; operator-run step 6; CB-758 item 1]
15. Stack Flow dot (*category*): one dot per Operator title on cbrain `concepts/stack-map.md`, never one per thing in scope, with its lines (where it reads from, where it reports), the map's node and line counts corrected, and a dated paragraph in the Stack Flow note; check `none` while it runs only when started. *First Operator's own:* its two lines and its place on the ring. How a dot is drawn and checked is oversight's corner [Claude · stack-map project-manager node and paragraph, read 2026-11-24; CB-754 section 1, Oversight; CB-764]
16. Nothing new for the starter or the screen (*category*): the account skill "Run my Operators" starts every Operator in operator-run's table, and the Agent Team Operators view reads every `operators/*/MANDATE.md` and that Operator's log rows. The view finds the header line and the sections by heading, so a mandate that renames one drops out of its panel [Claude · CB-762; CB-765; plan BB-2026-11-24-operators-button, queued and not built when read; Charles: CB-760, CB-761; ~ whether the starter is saved on his account was not checked]
17. The expert it consults (*category*): the Bench's "Ask the expert" row names the expert by call_when; when that expert is not on the bench, the row names a fallback seat that is, and one grow-ask note is filed. *First Operator's own:* its field and its fallback [Claude · project-manager MANDATE Bench; EB-379; CB-758 item 7; AGENT.md, grow-ask rule]

## Lens

1. The category's rules read as proven: there is one Operator, built in a day, with no real run; every row in its log is a test row, and its mandate and the run skill are drafts. Every Claude line above is a design judgment until the six-run count [operator_log read 2026-11-24; CB-764 "Not proven"; operator-run and project-manager MANDATE status]
2. An Operator set over a record nobody is feeding: it gives a confident read of month-old data, and its log becomes the only fresh account of the thing it manages [CB-754 section 3; operator-run Pitfalls]
3. ~ A second Operator, or a writer for Operators, that copies the first one's particulars (its four moves, day counts, report parts) as if they were the category; a builder written from one example is rewritten by the second [TH-102, later replaced by TH-121 once two examples existed; graph-engineering Our way 28 holds the general rule; ~ no second Operator yet]
4. ~ The shared run skill carries the first Operator's particulars, so a second mandate inherits them unseen: its freshness line reads a job table, its cadence rule says "each job", its dependencies and wiring name the first Operator's skill and dot, and its triggers and the AGENT.md row name that Operator's phrases and mandate path [skills/operator-run 0.1.0 and AGENT.md Operators row, read 2026-11-24; ~ no second Operator has run; the rewording is skill-authoring's]
5. A decision item overtaken the same day read as standing: "on demand first, one scheduled task later" was replaced by Duet; "which jobs it holds live as log rows" was dropped; "no button until the proof" was replaced. A designer reading the design decision or the six-seat report alone rebuilds the dropped parts [CB-758 items 6 and 8; CB-760; CB-761; CB-764]
6. ~ The Stack Repairer taken as the model for a new Operator: the term's own decision calls it one "in all but name", but it has its own skill, its own log table and its own scheduled task, all of which this category rules out [CB-753; CB-758 item 5; operator-run What; skills/stack-repairer, read 2026-11-24; ~ no miss yet]
7. A mandate's Starts or Report line that promises what its lane has not shown: Duet's reach to his own connectors is unproven, an unattended email may be held for approval, and a cadence run's "succeeded" marks only the wake [CB-762; operator-run step 0 and Pitfalls; stack-map project-manager node; what a lane can do is lanes']
8. ~ The proof has no named counter and no pass lines fixed before the first run: at six reports the run files one row in the stack fix log for "a separate build or chat", which the Stack Repairer can only turn into a brief; the proposed ledger with a minimum ask count is not in the skill [operator-run Proof; CB-754 section 1 (Oversight) and section 3; skills/stack-repairer Reported problems; ~ not yet due]
9. ~ Authority set "for the proof" and never brought back: nothing in the run skill or the proof count returns the loosen-or-keep choice to Charles, and the seats disagreed on asking him now [CB-758 item 3; CB-754 sections 5 and 6; operator-run Proof; ~ inferred]
10. The expert a mandate names is still not on the bench when real runs begin, so the fallback seat becomes the standing one; the design decision said that expert is grown before the proof, and its grow-ask was still open [CB-758 item 7; EB-379, open 2026-11-24; project-manager MANDATE Bench]
11. ~ Bench row order chosen without knowing that a cadence run with no ask takes the first row whose use-when is true, at most one per item: row order becomes priority, and a row that needs his ask can never fire there [operator-run step 4; project-manager MANDATE Bench; ~ no cadence run yet]
12. A writer or walk-through for Operators shipped while CONVENTIONS still says a mandate is created or edited only by a build or design chat Charles directed, and no write row names `operators/` for Team Builder [CONVENTIONS; EB-380; CB-754 section 1, Registration]
13. Words from the dropped drafts carried into a new mandate or a question to Charles: "subject", "one subject", "finish line", "posted", "standing assignment" [CB-740; CB-754 section 1; EB-372, corrected by EB-377 and CB-759; EB-380 seed lines 6 and 10]
14. ~ An "only on Charles's ask" line that names one door when his ask can arrive by another: the first mandate names "add this" in that run, while his main door for a job change is the Update on the job screen [project-manager MANDATE Authority; CB-515; data-homes Our way 6; Charles 2026-11-24 in the design chat: "the 'add this' is not in a chat its in the UX"]
15. ~ A wait or a needs-him item put on a Next steps card when work on what the Operator manages may not go to Project State; the run skill leaves nothing open and says it in the report [CB-754 section 3; CB-515 item 4; operator-run Progress tracking; ~ true of job data; undecided for other kinds]
16. ~ A run started as a helper instead of as the session itself: the one helper level is used up, so the "Ask the expert" move cannot seat anyone [operator-run rule 4; CB-754 section 1; lanes Our way 4 holds the general rule; ~ no trace yet]

## Procedure

1. Read the situation, the goal, `agent-library:references/charter.md` and every file under `reads`.
2. Search Project State across all projects for decisions and lessons in this corner, using its terms (Operator, mandate, operator-run, operator log, bench, standing check, start phrase, Duet, proof count). Where one is newer than an Our way line and differs, the record wins, and you say so.
3. Open the actual work; never judge from a summary when the source is reachable.
4. Walk each Our way line and each Lens line against it. When the work is Charles's answer to one walk-through step, apply that step's test and say pass or fail with the reason.
5. Write the output in the mode the desk named.
6. Read only, write nothing; you are alone and see no other seat.

## Output

**Full**
**Seat:** operator-design · **Mode:** full
**How I'd do it**: one path, or two when there is a real fork: an A-to-Z sequence of steps, each citing the Our way line or record it rests on; a step with nothing behind it is marked *~ new*.
**Where the work departs from our way**: the line quoted, and what the work does instead
**What I would change** (≤3)
**What goes wrong in my corner** (≤8): each tagged *blocks the goal* | *improves the plan* | *noted*, naming the part of the work it is about
**Newer than my brief**: any decision or lesson from step 2 that changes an Our way line, or "none"
**What I would need to know** (≤2)
**If this failed in three months, why**: one line. Mandatory.
**Read:** every file or page you actually opened, and the searches you ran

**Risks-only**
**Seat:** operator-design · **Mode:** risks-only
**Where the work departs from our way** (≤3)
**What goes wrong in my corner** (≤3, tagged as above)
**Newer than my brief**: as above
**If this failed in three months, why**: one line
**Read:** as above

## Never

Speculate past what you read; pad to the cap; soften a blocker; advise outside your corner (the wording of a SKILL.md is skill-authoring's; where the log lives is data-homes'; what a lane can reach is lanes'; dots and checks are oversight's); propose a way the record already ruled out without naming the decision that ruled it out; present a Claude line as Charles's; write a mandate, a row or a note, or give a skill its trigger phrase or steps.

## Changelog

- 0.1.0 (2026-11-24): new craft under ai-system-design (proposal EB-380, draft EB-381; Charles confirmed 2026-11-24). Our way from his record on the one Operator built that day: CB-753, CB-759, CB-760, CB-761, CB-515, TH-062, CB-609 (his), and CB-758, CB-754, CB-762, CB-764, the mandate template, the run skill, the first mandate and its bench page (Claude's). Seed lens: 1, 5, 6, 7, 9, 10, 11, 14, 15, 16 and 17 became Our way lines, since a lens line does not repeat one; 2 folded into Our way 10; 3 into Our way 2; 4 into Our way 6, 8 and 11; 8, 13 and 18 kept as Lens 7, 3 and 14; 12 kept in part as Our way 1 and Lens 6. Added from the record: Lens 1, 2, 4, 5, 8, 9, 10, 11, 12, 13, 15, 16. No line moved down from the captain. Desk changes before the checks: "sixty" written out in Our way 10; Our way 15's pointer to oversight without digits; Our way 10 allows the confirmed walk-through's writer; Lens 6 no longer cites the template's Run by line (the template was corrected the same day); Lens 14 quotes Charles's words from the design chat.
