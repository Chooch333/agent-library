# Stack work moves — bench page for the Chief Engineer and the Harness Pathfinder (0.3.0)

Moves for the Operators at `operators/chief-engineer/MANDATE.md` and `operators/harness-pathfinder/MANDATE.md`, run by `skills/operator-run/SKILL.md`. A run fetches this page only when its Bench picks one of these moves, and reads only that section. No skill owns the Next steps list, the shelf and the board together, so this page sits beside `references/thread-checkin.md` (operator-design seat, 2026-11-24).

## Rules for every move
- Writes nothing but the run's own log rows. No card is opened, reworded, closed or reopened here; no brief is shelved.
- In scope means what the running Operator's mandate says under Scope. For the Chief Engineer: a chat of the Stack Work Project, and the card, design-board topic, brief or build that carries that chat's link or board tag. For the Harness Pathfinder: its pushes, including Total Harness records with no chat on them. Anything the mandate does not place is not placed; say how many, once per report, never item by item.
- Matching a chat to its card. The link alone is not enough: a chat in this Project checks in with its session link, and the past-chat tools list the same chat under a different link (build-day test, 2026-11-24: the one chat that had a card matched nothing by link). Try in this order and stop at the first hit: the same link; the card's board tag (DA-MMDD-slug) found in the chat; the card's chat label equal to the first line of the chat's first message; a card opened within a day of the chat's start whose name plainly names the same work. Say "no card" only after all four miss.
- Listing the chats. One past-chats call returns only a few chats (five on 2026-11-24, whatever number is asked for). Page back with `before` until twenty chats or fourteen days are covered, five calls at most; say how far back the run saw.
- What a chat was for is re-read from the chat every time (past-chat tools: find the spot, read one page). Never from the log, a past report or memory.
- A card's night-run status (stand, done, left, verdict) is read as written. Do not re-derive it.
- At most five pieces of work per report, oldest first; the rest is a count. Never read a list back to Charles.
- Plain words to Charles: things by their titles, no ids, tags, table or tool names.
- The day marks below (14 and 7) are Inferred; nobody chose them. Change them in the mandate, not here.

## 1 Read a chat
**For:** a Project chat that has no card, open or closed.
1. Open the chat at its start and at its last turns (two reads at most).
2. Say, in three lines: what Charles was trying to do (his words where he said it); what is left; one recommended next move (finish it here, scope a build, or nothing: it was a question that got its answer).
3. A chat that was a plain question with nothing left open is said in one line and not counted as hanging.
**Log:** one `move` row; `detail.evidence` = "chat with no card", `ref` = the chat's link.

## 2 Re-test the ask
**For:** an in-scope card that has waited on Charles for 14 days or more.
1. Read the card's next step and its night-run status.
2. Apply the Hand it on test in `references/thread-checkin.md` (Closing out, bin 4): is it a key, sign-in or setting only he has, money, an irreversible change, a change to his rules, a clash between two of his decisions, or a direction no record backs? Search Project State for a decision that already answers it before saying it needs him.
3. Say one of: it truly needs him (the closed choice, with a recommendation); a record already answers it (name the record in words); Claude could do it (say where it should be queued). Recommend, never act.
**Log:** one `move` row; `detail.evidence` = the card's age in days and the verdict.

## 3 What's left
**For:** an in-scope draft brief older than 14 days, or an in-scope build marked running or blocked for more than 7 days.
1. Read the brief's own done-list (its acceptance checks).
2. Match each check to evidence that exists today (a commit, a record, a live read). A remembered verdict is not evidence.
3. Say what is proved, what is left, and one recommended next move: finish it (name the chat that would), drop it (say why it no longer matters), or it is already done and only the record is behind.
**Log:** one `move` row; `detail.evidence` = the brief's age and how many checks have evidence.

## 4 Scope it
**For:** Charles says "finish" or "scope" a thing, in this run.
1. Find the thing in scope; if two things match his words, ask which, once.
2. Read its chat (move 1, steps 1 to 2) so the aim is his, not a guess.
3. Give him one line to say that opens the Design Assist chat for it, with the aim and what is left folded in. The run does not load Design Assist itself.
4. Log a `wait`: `why` = what will finish it, `clears_when` = the one Project State read that shows it landed (see the mandate's Log section). No brief yet: the wait is on the card for that Design Assist chat appearing.
**Log:** one `move` row and one `wait` row.

## 5 Sort the cards
**For:** an open Next steps card with no project, or one sitting in a project that no longer fits. The one move on this page that writes, and the Chief does it alone (Charles, 2026-11-25: "it should be able to adjust and reorganize as make sense to it").
1. Read the central project list (the one the Dev tab's project dropdown reads). Never invent a project name that is not on it; a card that fits none is said in the report as "needs a new project: <name it would give>".
2. For each such card, pick the project from what the card and its chat say the work is for. A card he sorted himself is moved only when its work plainly changed.
3. Set it through Project State's tool for a card's project. No such tool exists yet (2026-11-25: the field is written only from the Dev tab): until it does, write nothing and give the sorting in the report, one line per project with a count.
**Log:** one `move` row; `detail.evidence` = how many cards had no project, how many were set or proposed.

## Changelog
- 0.2.0 (2026-11-25): renamed for the Chief Engineer; new move 5, Sort the cards (Charles, decision CB-783).
- 0.1.0 (2026-11-24): first version, written by Team Builder operator mode from draft note CB-768 (Charles confirmed in the chat; decision CB-769). Seat: operator-design, report CB-767.
