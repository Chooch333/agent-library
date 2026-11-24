# Job moves (0.1.0)

Four read-only moves over a FAW job's live data. Used by the Project Manager Operator (`operators/project-manager/MANDATE.md`) and by any chat asked the same thing. Data and queries: `skills/job-update/SKILL.md`, Read. **None of these writes anything to a job.** A change to a job still goes through Job Update's Write, on Charles's ask only.

Rules for all four:
- Read the live tables every time. Never answer from a log, a past report or memory.
- Say the record's age in one line first (newest applied change for the job in `pm_package_status`). Never an alarm, never a question.
- Plain words. People by name, items by title. No ids, table names or codes in what Charles reads.
- Nothing found is a real answer: say so in one line.

## 1. Where the job stands
For one job, or across all jobs (one short block per job that has anything to say; skip jobs with nothing open).
- **Needs you:** open items where Charles is accountable or responsible, oldest due first; at most five, then a count.
- **Since you last heard:** what changed after the last report (items added, closed, dates moved, decisions made), from `pm_task_history` and `pm_decisions`.
- **What is slipping:** open items past their date, or waiting on an item that is itself late.
- **Could not see:** any table or job the run could not read.

## 2. Meeting prep
Use when a milestone of kind `meeting` falls within the next 3 working days.
- The open items that belong to that meeting's people (anyone accountable or responsible who is on the job's team), grouped by person.
- Decisions made since the last meeting of the same name.
- Three or fewer questions worth asking in the room: an item with no owner, a date with no basis, two items waiting on each other.
- Output is a draft agenda in the reply. Nothing is sent or filed.

## 3. Follow-up drafts
Use when an open item is past its date and has an accountable person.
- One short draft per person (not per item), listing their late items with the date each was due and what it is holding up.
- In Charles's voice, plain and brief, for him to send himself. Drafts stay in the reply. Never sent, never saved to a mailbox unless he asks.

## 4. Gap check
Use when open items have no accountable person, no date, or have not changed in 30 days.
- Three counts, then up to five items under each, oldest first.
- For each item, one suggested fix in plain words ("give this to the person who raised it", "close it: the decision on the wall finish replaced it"). A suggestion only; nothing is changed.

## Changelog
- 0.1.0 (2026-11-24): first version, written with the Operator category. One file with four sections, not four skills: same data, same door, same trigger (seat skill-authoring, report CB-754).
