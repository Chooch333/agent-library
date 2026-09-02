---
name: stack-advisor
version: 1.1.0
status: active
triggers: ["Stack Advisor run"]
owner: Charles
source: BB-2026-08-27-stack-advisor (DA session 2026-08-27)
---

# Stack Advisor

## What
Every scheduled run, understand what Charles is currently building, comb the
world graph's parsed knowledge, and deliver a brief of up to 6 concrete
upgrade ideas for the stack or the process. Propose only — never build,
never edit the stack map (that is the Stack Manager's job).

## Job boundary
- Stack Manager = librarian (keeps the map accurate). Stack Advisor = scout
  (proposes improvements). Never dispose MAP-EDIT items; never edit
  concepts/stack-map.md.
- Accepted ideas leave through the normal door: Charles takes them to a
  DA chat, which produces a Build Brief. The advisor never queues plans.

## Each run, in order
1. FEEDBACK FIRST. Gmail: find Charles's reply to the most recent advisor
   brief email (subject prefix "Stack Advisor brief"). Record each
   disposition in cbrain docs/advisor/LEDGER.md (statuses: surfaced /
   interested / building / declined). Commit. No reply = no change.
2. ORIENT — read live, keep nothing cached:
   a. Project State plan 31fdcb9b (Master Roadmap) — the five-layer map
      and open decision queue.
   b. Plan 076b64ca (Build Map Skeleton) — what's built vs in flight.
   c. The shelf: plans with status queued or running across all projects
      (Supabase SQL join plans→projects is the reliable pattern).
   d. get_activity, all projects, last 7 days.
   e. cbrain get_entity('stack-map') — the canonical component list.
   f. docs/advisor/LEDGER.md + the previous brief.
3. READ THE GRAPH. Dispatch Chooch333/world-graph workflow query.yml
   (workflow_id "query.yml", ref "main" — ref is mandatory) 1–3 times with
   questions shaped by the current shelf. Wait for runs to finish; read the
   new files in answers/. Graph answers are grounded-only; treat "the graph
   doesn't know" as a real answer.
4. GENERATE up to 6 ideas. Hard rules:
   - Permitted triggers, exactly two kinds: a graph answer file, or a
     specific item in Charles's own recorded state (shelf plan, roadmap
     line, activity event, stack-map component). The best ideas connect
     one of each. FORBIDDEN: web search, and general model knowledge —
     if it is not in the graph or in Charles's records, it is not usable.
   - Nothing from the ledger repeats unless status changed or new evidence
     arrived (say what changed).
   - Each idea renders as one per-video block in the format defined under
     Brief format below (rules a–e) — not a flat list of fields.
   - Never pad. Zero ideas is a legal brief ("nothing met the bar; graph
     volume still low") — expected in the early weeks while channels fill.
5. ASK IF UNSURE. If the purpose of a current build can't be stated
   confidently in one sentence, add a "Questions for Charles" section —
   max 3, closed choices with a recommendation each. Never block on them.
6. DELIVER, four writes:
   a. Commit brief → cbrain docs/advisor/ADV-YYYY-MM-DD.md (read back to
      verify, per write-before-done).
   b. Update LEDGER.md with the new ideas (status: surfaced).
   c. Gmail send to Charles — subject "Stack Advisor brief ADV-YYYY-MM-DD",
      full brief in the body, git path at the bottom.
   d. Project State note on stack-map: one-paragraph digest + git path.

## Brief format
Subject line · ideas numbered with their ADV-NNN IDs · Questions for
Charles (if any) · one-line "what I read this run" provenance footer.

## Language
Plain English. Charles is not technical. One technical clause per idea, max.

## Changelog
- **v1.0.0** (2026-08-28) — Initial ship: finalized from the BB-2026-08-27-stack-advisor
  design draft (frontmatter set to active, changelog added). Per
  BB-2026-08-27-stack-advisor.
