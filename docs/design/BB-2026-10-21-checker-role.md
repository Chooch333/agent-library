# Build Brief — BB-2026-10-21-checker-role

**Build:** 45 · **Harness block:** 6 — Planner, builder, checker roles · **Skills:** orchestrate-build, project-folder
**Git home:** Chooch333/agent-library · docs/design/BB-2026-10-21-checker-role.md
**target_repo:** Chooch333/agent-library (also writes Chooch333/arch-renders for the proof) · **after:** none · **Overnight:** yes · **Size:** M
**Cost:** $0. **Charles's time:** 0 during the build; ~10 min afterwards for the What-to-check list.

**What this is:** adds the one missing role. Planner and builder already exist; the checker does not. After this build, no feature in a project folder can be marked passed except by a separate checker that grades the real thing against the rubric, never the builder's own report.

---

## Current state going in

- **Planner — have it, adopt.** Design Assist + Build Briefs plan builds; `skills/project-folder` Start turns an ask into spec.md, features.json and rubric.md (Build 29). The blueprint's planner (sentence → spec) is that Start step.
- **Builder — have it, adopt.** `skills/orchestrate-build` (lead) + `skills/execute-build-task` (one-task workers), running in Claude Code.
- **Checker — missing.** `skills/project-folder` says "the builder does not grade itself when a checker is available (block 6)". Today the builder sets `passes: true` itself. Checkers have run ad hoc: Build 33's independent checker (2 rounds, caught 7 flaws), Build 42's robot live check (headless browser, after Launch). Nothing makes them standard or required.
- `templates/project-folder/check_folder.py` only checks that a pass has an evidence string.
- R&D Shelf: no rows name block 6. No open rd-handoff targets block 6.

**Lane:** one narrow checker skill + a mechanical rule in the folder checker that only a checker verdict can mark a feature passed, wired into project-folder and orchestrate-build. Proven by re-grading a real project and catching a planted fault.
**Ruled out:** separate planner and builder skills (they exist; rebuilding them adds nothing); an outside eval framework or grading service (adopt-before-build: Claude Code subagents already give a separate context for free); having the checker fix what it finds (a grader that edits stops being independent).

---

## Scope

**In:** checker skill + agent definition; check_folder.py rule; project-folder 0.3.0; orchestrate-build 1.6; template updates; proof on arch-renders; stack map.
**Out:** game-maker (its play/review gates and post-Launch live check stay as they are); cbrain-ui builds (CB-441 still governs them); any paid tool; physical checks (camera, measurement) beyond writing them into the skill's "How" list for later blocks.

---

## Directive

1. **Checker skill** — `skills/checker/SKILL.md` v0.1.0, wiring label "Checker", runs inside builds. It must say:
   - **Inputs:** the project's rubric.md, the feature's `description` and `check` lines, and the paths/URLs of the thing. **Never** the builder's `evidence` field, progress.md, or the builder's report; it forms its own verdict first.
   - **How it grades:** per rubric row's How: run tests/scripts, re-run the step, read model/geometry files, look at renders and screenshots (Read on images), measure. For screen work it may take headless-browser screenshots and click through when the rubric says so (see Hard gates note on CB-441). Function must work; recreational finish is fine.
   - **Verdict:** writes `checks/<feature-id>-<n>.md` (n = attempt) with: PASS, FAIL, or CAN'T CHECK; what it ran; what it saw; for FAIL, the specific gap and a one-line fix hint. Only on PASS does it set the feature's `passes: true` and `evidence` to point at the check file. It never edits the thing being checked.
   - **Three-strikes:** after a third FAIL on one feature, set README Status to `stopped: <feature> failed 3 checks` and write a diagnosis section (what keeps failing, likely cause, what Charles must decide). The builder stops that feature.
   - **CAN'T CHECK** is not a pass: the feature stays false with the reason.
2. **Agent definition** — in the skill, a block to install as `.claude/agents/checker.md` (same pattern as execute-build-task): Opus, fresh context, instructions pointing to the skill. Install it in the build session.
3. **check_folder.py** (template) — new rule, on when features.json has `"checker": true`: every `passes: true` needs a `checks/<id>-*.md` whose newest file starts `PASS`. `"checker": true` becomes the template default; older folders opt in.
4. **Templates** — features.json gets `"checker": true`; add `checks/README.md` (one paragraph: verdict files, written only by the checker); rubric.md note that the checker grades against it.
5. **project-folder 0.3.0** — Close step: the builder marks a feature ready (progress entry names it); the checker grades it; the builder never sets `passes`. Replace the "until block 6" line. Add a short Roles section: planner = Start steps 3–4, builder = orchestrate-build + execute-build-task, checker = skills/checker.
6. **orchestrate-build 1.6** — step 6: on a build that works in a project folder, each feature's verification is a checker subagent with only the checker inputs, never the lead reading the worker's report. The brief's own acceptance checks stay lead-verified as now.
7. **Proof on arch-renders** (`Chooch333/arch-renders`):
   a. Run check_folder.py from the new template against arch-renders as-is → expect FAIL (7 passes, no checks/). Record the output.
   b. Set `"checker": true`; dispatch the checker on F01–F07. Re-run the pipeline or fetch the stored assets (cbrain `workflow_assets` for run 5bc91fe6) as the checker chooses. Each gets a verdict file. Any honest FAIL or CAN'T CHECK flips that feature to false; that is a valid outcome, not a build failure. F08 stays false.
   c. **Planted fault:** on a scratch branch, shift one exterior wall 6 in. in the v1 model (or the traced geometry) and leave F03/F04 marked passed. Dispatch the checker on F03 and F04 with no hint. It must FAIL at least one, naming the wall. Delete the scratch branch.
   d. **Three-strikes:** on the scratch branch before deleting, run the checker on the faulted feature three times → README Status shows `stopped:` with a diagnosis.
   e. check_folder.py on arch-renders main → OK. Progress entry. Commit.
8. **AGENT.md** — no change (skills fire inside builds; no chat trigger).
9. **Stack Flow** — `concepts/stack-map.md` (Chooch333/cbrain): add a Checker dot on the build flywheel between Build worker and the plan close, with a line from the project folder's rubric.

---

## Acceptance

1. `skills/checker/SKILL.md` committed with inputs, grading, verdict file, three-strikes, CAN'T CHECK, and the agent definition block.
2. Template check_folder.py: rejects a `passes: true` with no PASS verdict when `"checker": true`; accepts it with one (unit fixture, both cases run).
3. project-folder 0.3.0 and orchestrate-build 1.6 committed with the changes in steps 5–6.
4. Proof 7a recorded (FAIL as expected).
5. Proof 7b: verdict files for F01–F07 on arch-renders main; every `passes: true` points at a PASS file.
6. Proof 7c: checker FAILed the planted fault, naming the moved wall; it was not told what was changed.
7. Proof 7d: `stopped:` status + diagnosis after three FAILs; scratch branch deleted.
8. check_folder.py on arch-renders main prints OK.
9. Stack map updated.
10. Session Log on total-harness, fork log, What to check list.

## Hard gates

None expected: $0, no keys, nothing irreversible (the planted fault lives only on a deleted branch).
**CB-441 note:** CB-441 bans browser tests in builds. The checker's headless-browser use is limited to rubric rows that ask for it in project folders; cbrain-ui builds are untouched. This build's proof needs no browser. If Charles declines the carve-out, delete that one sentence from the skill; nothing else changes.

## Design intent

The builder never grades its own work. The checker is cheap (a subagent), independent (fresh context, no builder evidence), and mechanical where it can be (check_folder refuses a pass without a verdict). An honest FAIL on arch-renders is a better outcome than a rubber-stamp PASS.

## Pasteable prompt

Build 45 — execute Build Brief BB-2026-10-21-checker-role. Fetch it from Chooch333/agent-library docs/design/BB-2026-10-21-checker-role.md (Custom GitHub get_file_contents), load skills/orchestrate-build/SKILL.md and skills/project-folder/SKILL.md, and run it per orchestrate-build.
