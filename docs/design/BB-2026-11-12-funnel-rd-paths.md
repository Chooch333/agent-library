# Build Brief — BB-2026-11-12-funnel-rd-paths

**Git home:** Chooch333/agent-library · `docs/design/BB-2026-11-12-funnel-rd-paths.md`
**Project State plan:** `dc04b8ea-7b9e-45fd-81aa-35be097c6bfe` on `total-harness`
**Build:** 84
**Skills:** orchestrate-build
**Seated:** revision 2, report TH-200, seats c-stack, lanes, oversight, data-homes, github-integrations, ai-system-design
**Stack Flow:** edits the Chats dot's Tech review and Tech discovery parts (run place, reach check) and the Lab run part's side-panel text (one folder per test, run id, secret scan); no new dot.
**Step map:** no change — no workflow is added or changed.
**Overnight:** yes · **target_repo:** Chooch333/agent-library (also writes Chooch333/arch-renders `.github/workflows/lab-run.yml`) · **after:** Build 82
**Cost:** subscription only, no dollars. Each lab-run test draws private-repo Actions minutes from the shared 3,000-minute monthly pool (a reach check ≈ 1–2 minutes; TH-195 ran in 66 s). The build's own proof run ≈ 2 minutes.

**What this is:** Third of four alignment-funnel builds. R&D shows Charles a path that runs with what Claude already has, tests it without asking, and states up front anything an alternate path would need from him.
**What I'll do (build chat):** the six steps below.
**What you'll do:** nothing.

## Asked for — Charles, 2026-11-11 and 2026-11-12 (frozen)
> "The fact that I have to do this much for this test is crazy." (TH-193) · "When something needs a test, run it, do not ask." Runpod is out. (TH-195) · R&D: "always a primary path that keeps to the charter and uses only what Claude already has; an alternate path only when it gives a real advantage, with what it needs from him stated up front ('needs X app set up, Y secret')." (TH-199 item 4)

## Current state going in (checked 2026-11-12)
- **[verified]** tech-review step 4 designs the test plan and then says "stop and wait for my yes before running any test"; nothing names where a test runs or checks reach first. tech-discovery names no run place.
- **[verified]** lab-run.yml (arch-renders d97b6b9): hand-started, input `job`, runs `lab/<job>/run.sh`, commits `lab/<job>/out` back with `git add -f` under `if: always()`; passes OPENAI/GEMINI/BFL keys when the secrets exist (none do). Concurrency keeps one waiting run per job.
- **[verified]** Reach from lab-run: eight vendor hosts answered (TH-195). The chat workspace reaches none of them.
- **[verified]** Actions minutes: 3,000 a month shared with world-graph (WG-112); locked once (CB-550); a locked run ends in about 2 s with zero steps.
- **[verified]** The expert room's path for this rule (TH-196, ai-system-design and c-stack, 2026-11-12): run place from the lanes list, only places and keys Claude holds, one "Needs from Charles" line, a reach probe before the plan is shown, the five-reason test, seats only on what survives.
- **[verified]** The PC counts as a run place only when a folder is already connected in that chat; otherwise it needs the desktop app open and Charles naming the folder (lanes seat, TH-194).

## Scope
**In:** tech-review step 4; tech-discovery's run-place line; lab-run.yml hardening; services' call_when.
**Out:** any vendor key (no use case needs one yet); Runpod (out); a self-hosted runner on the PC (the R&D lab's own open test).

## Directive
1. **tech-review step 4** (replace the last two sentences of step 4; no new section). The plan names its run place: the chat workspace, or lab-run; the PC only when `get_device_info` already shows a connected folder in this chat. It uses only run places and keys Claude already holds. **Primary path** always; an **alternate path** only when it gives a real advantage, written as "needs: <app>, <secret>, $<amount>, <his minutes>" and described, not set up, until Charles says yes. One line: "Needs from Charles: none" (or the alternate's needs). Before the plan is shown, a **reach check** from the run place for every host, key and folder the plan names that the github-action lane row hasn't verified in the last 30 days (lab-run job `reach-<date>-<slug>`). Then the **five-reason test** on each step for Charles (money, a credential only he holds, irreversible, safety, a settled rule); a step that fails is removed. Seat c-stack plus the matching craft (mode B, two seats) only when "Needs from Charles" is still not "none" or the plan adds a run place, key, account, repo or paid vendor; the seats judge, the chat rewrites. Then **run the primary path at once**: no stop for a yes. Money still stops.
2. **tech-discovery** step that drafts "Test run, if we do one": add one line naming the run place a test would use, from the same list. No seat.
3. **lab-run.yml** (arch-renders main; read back): one folder per test (`lab/<YYYY-MM-DD>-<slug>/`); write `run_id.txt` with `${{ github.run_id }}` into `out/` first; before commit, fail if any secret value appears in `out/` and refuse any file over 25 MB; `timeout-minutes: 20`; concurrency group per job folder. **tech-review** reads outputs only from the commit whose `out/run_id.txt` matches the run it started (`list_workflow_runs` after dispatch; `get_workflow_run` shows steps above zero). A run with zero steps or no matching commit is "not run — Actions allowance locked or the run failed", reported as untested, never read from an older `out/`; it does not become a money stop.
4. **services call_when** (`experts/INDEX.md`): add "paid outside vendors and rented machines, their accounts and keys". File one lens-note for services citing this brief so its brief catches up on Sunday.
5. **Stack Flow**: Tech review part on the Chats dot says where tests run and that reach is checked first; Lab run part's side panel names one folder per test, the run id and the secret scan.
6. **Proof**: write `lab/2026-11-13-reach-proof/run.sh` (curl the eight hosts, print status codes), start lab-run with that job, confirm `out/run_id.txt` matches the run and the committed `reach.txt` lists eight answers; record the date on the github-action lane row's `verified:`.

## Acceptance
1. tech-review step 4 reads as step 1 (no "wait for my yes"), tech-discovery names a run place; both version-bumped with changelog lines.
2. lab-run.yml carries the run id, the secret scan, the size cap, the timeout and per-job concurrency.
3. The proof run's `out/run_id.txt` matches its run, with eight host answers; the lane row's date is updated.
4. services' call_when reads as step 4; the lens-note exists.

## Decisions
- [Charles] Primary path with only what Claude has; alternate with needs stated up front; Runpod out; run tests, don't ask (TH-195, TH-199).
- [Claude-per-doctrine] Test the primary path first; the alternate is described, not set up, until Charles says yes. Follows from TH-195 ("run it") and the five hard stops; logged as a judgment call, not put to Charles. Seat: c-stack.
- [Claude-per-doctrine] The PC is primary only with a folder already connected. Seat: lanes.
- [Claude-per-doctrine] One folder per test plus run id; a locked run is "not run", never stale output. Seat: github-integrations.
- [Claude-per-doctrine] No vendor key now: the proposed fal.ai key has no use case or dollar figure yet, so it is not a money stop; a review that needs it states it as the alternate's needs. Seat: c-stack.

## Pasteable prompt
> Build 84 — execute Build Brief BB-2026-11-12-funnel-rd-paths. Pull the plan from Project State (plan_id dc04b8ea-7b9e-45fd-81aa-35be097c6bfe, project total-harness, status queued — set it to running when you claim it). Git copy at Chooch333/agent-library/docs/design/BB-2026-11-12-funnel-rd-paths.md. Build 82 (lane facts) must have landed. Follow the brief's fork-handling rules: answer forks autonomously with judgment-call tags; escalate only at hard gates (money: a lab-run test that would need a paid vendor key stops).
