# Build Brief — BB-2026-11-13-seat-proof

**Git home:** Chooch333/agent-library · `docs/design/BB-2026-11-13-seat-proof.md`
**Project State plan:** `dd53e29c-50d8-421b-9106-c752b22c1600` on `total-harness`
**Build:** 83.1
**Skills:** orchestrate-build
**Seated:** revision 2, report TH-200 (seated as directive 7 of Build 83; not pre-seated on purpose — see the plan's provenance)
**Stack Flow:** no change — a throwaway folder, no running part.
**Step map:** no change — no workflow.
**Overnight:** yes, on a night whose runner is night-run 0.9.0 or later · **target_repo:** Chooch333/agent-library · **after:** Build 83
**Cost:** subscription only. About 2 seats and 1 revision builder in the night session (≈ 470k tokens).

**What this is:** The first real run of the night seat step (night-run 0.9.0 step 5a and the Seat step). A tiny build leaves one value nobody chose; the after-build seat should object, a fresh revision builder should fix it the same night, and the night's trace line should show it.
**What I'll do (build chat):** create two small files, close out with the full handoff block.
**What you'll do:** nothing.

## Asked for — Charles, 2026-11-12 (frozen; Build 83, decision TH-198)
> "When the night session seats an expert on the decisions a builder made, the expert's objection is used as a build revision instruction and applied the same night."

## Scope
**In:** a new folder `lab/seat-proof/` in agent-library with two small files.
**Out:** any other file; any running part; any change to night-run or the Expert Desk.

## Directive
1. Create `lab/seat-proof/README.md`: three or four plain lines saying the folder is a throwaway proof of the night seat step (Build 83.1) and will be removed by Build 83.2.
2. Create `lab/seat-proof/tool.json`: a tiny config naming one tool the folder would use (for example a Node runtime or a linter), pinned to an exact version **of your choosing**, written as you would by habit, with no reason given in the file. The brief deliberately does not name the tool or the version.
3. One commit per file. Close out per orchestrate-build 1.10.0 step 7(a), handoff block in full: the pinned version goes in the list of values the brief didn't name.
4. Acceptance checks 2–4 below can only be seen after the night session's step 5a, which runs after you close: hand them off to Build 83.2 (plan `bf9a262c-441d-48cb-8542-9918a8222597`) as `handed-off`, per orchestrate-build step 7(c). Do not create a new follow-up plan.

## Inputs
- Build 83.2 follow-up plan: `bf9a262c-441d-48cb-8542-9918a8222597`, "Build 83.2: check the seat proof and remove it" on total-harness (queued, after this build).

## Acceptance
1. `lab/seat-proof/README.md` and `lab/seat-proof/tool.json` exist on main, one commit each; the Session Log carries the handoff block listing the pinned version as a value the brief didn't name.
2. The night's `built` row for this plan has the trace line with a seat and at least one applied revision ("seated: <slugs> · revisions 1 applied" or more). (Handed off to Build 83.2.)
3. A `night-revision` note for this plan exists on total-harness. (Handed off to Build 83.2.)
4. The `lab/seat-proof/` folder is removed by a final commit. (Handed off to Build 83.2.)

## Decisions
- [Charles] Night session seats, objections revise, never gate (TH-198).
- [Claude-per-doctrine] The proof brief is marked seated so step 3a skips it; the value nobody chose must survive to the after-build seat.
- [Claude-per-doctrine] Checks the builder cannot see from its own close go to a second tiny brief, Build 83.2, which runs after this one's seat step.

## Pasteable prompt
> Build 83.1 — execute Build Brief BB-2026-11-13-seat-proof. Pull the plan from Project State (plan_id dd53e29c-50d8-421b-9106-c752b22c1600, project total-harness, status queued — set it to running when you claim it). Git copy at Chooch333/agent-library/docs/design/BB-2026-11-13-seat-proof.md. Build 83 must have landed. Follow the brief's fork-handling rules: answer forks autonomously with judgment-call tags; escalate only at hard gates (none in this brief).
