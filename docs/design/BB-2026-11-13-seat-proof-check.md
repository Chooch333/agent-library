# Build Brief — BB-2026-11-13-seat-proof-check

**Git home:** Chooch333/agent-library · `docs/design/BB-2026-11-13-seat-proof-check.md`
**Project State plan:** `bf9a262c-441d-48cb-8542-9918a8222597` on `total-harness`
**Build:** 83.2
**Skills:** orchestrate-build
**Seated:** not seated on purpose — the night session's step 3a seats it before it builds, which proves step 3a too.
**Stack Flow:** no change — removes a throwaway folder.
**Step map:** no change — no workflow.
**Overnight:** yes · **target_repo:** Chooch333/agent-library · **after:** Build 83.1
**Cost:** subscription only. About 4 seats in the night session (2 before, 2 after).

**What this is:** Checks that the first real night seat step (Build 83.1) did what night-run 0.9.0 says, records the evidence, then removes the proof folder.
**What I'll do (build chat):** read the records, delete two files, close out.
**What you'll do:** nothing.

## Asked for — Charles, 2026-11-12 (frozen; Build 83, decision TH-198)
> "When the night session seats an expert on the decisions a builder made, the expert's objection is used as a build revision instruction and applied the same night. It does not mark the build 'needs a fix' or stop it."

## Scope
**In:** reading night_runs, Project State notes and agent-library commits for Build 83.1; deleting `lab/seat-proof/`.
**Out:** any other file; any change to night-run, the Expert Desk or a running part. A failed proof is recorded, not fixed here.

## Directive
1. Read Build 83.1's plan (`dd53e29c-50d8-421b-9106-c752b22c1600`) and its `night_runs` rows (Supabase `ujditldbqdiqigazkcak`: `select result, line, created_at from night_runs where plan_id = 'dd53e29c-50d8-421b-9106-c752b22c1600' order by created_at`). Record the `built` row's trace line.
2. Find its `expert-desk-report` and `night-revision` notes on total-harness (`find_by_tags`, exact tags; the note text names the plan). Record their ids, and the revision's commits from the note, checked against `list_commits` on agent-library.
3. Delete `lab/seat-proof/tool.json` and `lab/seat-proof/README.md` (Custom GitHub `delete_file`, one commit each; the last is the final commit).
4. Close out per orchestrate-build 1.10.0 with the handoff block. Build 83.1's handed-off checks 2–4 are this plan's acceptance 1–3.
5. If the trace line shows no seat or no applied revision, or no `night-revision` note exists: the proof failed. Still remove the folder; record exactly what the records show in the Session Log; file one `lens-note` for `c-stack` on `expert-bench` (tags `lens-note`, `expert-c-stack`, `night-seat`) naming what did not happen; mark this plan `failed` with that reason. That is a trace, not a request to Charles.

## Inputs
- Build 83.1: `dd53e29c-50d8-421b-9106-c752b22c1600`, "Build 83.1: prove the night seat step" on total-harness.
- night-run 0.9.0 step 5a and the Seat step (agent-library `skills/night-run/SKILL.md`).

## Acceptance
1. The Session Log quotes Build 83.1's `built` trace line showing a seat and at least one applied revision.
2. The Session Log names Build 83.1's `night-revision` note id and its commits, matched against `list_commits`.
3. `lab/seat-proof/` no longer exists on agent-library main; the final commit's SHA is recorded.

## Decisions
- [Charles] Night session seats, objections revise, never gate (TH-198).
- [Claude-per-doctrine] The checks a proof build cannot see from its own close live in this second brief, built right after it on the same night.
- [Claude-per-doctrine] A failed proof is a trace (a lens-note for c-stack and a failed plan), never a card.

## Pasteable prompt
> Build 83.2 — execute Build Brief BB-2026-11-13-seat-proof-check. Pull the plan from Project State (plan_id bf9a262c-441d-48cb-8542-9918a8222597, project total-harness, status queued — set it to running when you claim it). Git copy at Chooch333/agent-library/docs/design/BB-2026-11-13-seat-proof-check.md. Build 83.1 must have landed. Follow the brief's fork-handling rules: answer forks autonomously with judgment-call tags; escalate only at hard gates (none in this brief).
