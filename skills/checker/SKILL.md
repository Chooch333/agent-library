---
name: checker
version: 0.1.0
status: draft
triggers: [dispatched by a build lead or project-folder Close to grade one feature; no chat trigger]
dependencies: [project-folder]
owner: Charles
updated: 2026-10-23
wiring:
  runs: inside-builds
  reads: [project repo rubric.md, features.json description + check lines, the thing being checked]
  writes: [project repo checks/, features.json passes + evidence, README Status on three strikes]
  stack: [build-flywheel, total-harness]
  origin: yours
  label: Checker
---

# SKILL: checker (v0.1.0)

The checker grades one feature of a project folder against the project's rubric, in a fresh context, and writes a verdict. It is the only role that can mark a feature passed. The builder never grades its own work.

## Inputs (and only these)
- The project's `rubric.md`.
- The feature's `id`, `description` and `check` lines from `features.json`.
- The paths or URLs of the thing to check (model files, outputs, code, a deployed page).

**Never read** the feature's `evidence` field, `progress.md`, the builder's report, commit messages that describe the work, or earlier verdict files for the same feature. Form your own verdict first. If an input you need is missing, the verdict is CAN'T CHECK, not a guess.

## How it grades
Run the rubric row's **How** for this feature, against the real thing:
- run the tests or scripts the row names; re-run the step if the row says so;
- read model, geometry and data files directly (parse them; do not trust a summary of them);
- look at renders and screenshots (Read on the image);
- measure: compute the numbers the row's **Pass when** names, and compare to its threshold;
- for a website rubric row in a project folder, you may drive a headless browser: click through, take a screenshot, read the result (TH-084). This does not apply to cbrain-ui builds, which stay under CB-441.

Function must work; recreational finish is fine. Later blocks may add physical checks (camera, measurement on a real part); name them as CAN'T CHECK until a tool exists.

## Proportion
Run the rubric's How for the feature and stop. Do not invent extra checks, do not re-derive the whole project, and do not grade style. Build-and-iterate is the house rule (TH-085): the checker exists to catch broken function, not to be thorough for its own sake.

## Verdict
Write `checks/<feature-id>-<n>.md`, where `n` is the attempt number (1 for the first check of that feature, then 2, 3, ...; count the existing `checks/<id>-*.md` files by name only, do not read them). The first line is the verdict and nothing else comes before it:

```
PASS — <one line: what was measured against what threshold>
```
or `FAIL — <the specific gap>` or `CAN'T CHECK — <what was missing>`. Then:
- **Ran:** the commands, scripts or reads you did (enough for someone to repeat them).
- **Saw:** the numbers and observations, with the rubric threshold next to them.
- **Gap** (FAIL only): the specific thing that is wrong, named precisely (which part, which number, how far off).
- **Fix hint** (FAIL only): one line.
- **Inputs:** the files and lines you were given.

Then:
- **PASS:** set the feature's `passes: true` and `evidence: "checks/<id>-<n>.md"` (the evidence points at the verdict file; nothing else in the feature changes).
- **FAIL or CAN'T CHECK:** set `passes: false` and `evidence` to `"checks/<id>-<n>.md: <one-line reason>"`. CAN'T CHECK is never a pass.
- **Never edit the thing being checked.** A grader that fixes what it finds stops being independent. You touch only `checks/`, the feature's `passes` and `evidence`, and README Status on a third strike.

## Three strikes
If this verdict is the **third FAIL** for the same feature (count FAIL first lines across `checks/<id>-*.md`; the count is the one exception to "do not read earlier verdicts", and you read only first lines, after writing your own verdict):
1. Set README `**Status:** stopped: <feature id> failed 3 checks`.
2. Append a diagnosis to your verdict file: what keeps failing, the likely cause, and what Charles must decide.
3. The builder stops that feature until Charles decides.

`check_folder.py` enforces this: with `"checker": true`, three FAIL verdicts and no later PASS fail the folder unless README Status says `stopped:`.

## What check_folder enforces
With `"checker": true` in `features.json` (the template default since Build 45; older folders opt in), every `passes: true` needs a `checks/<id>-<n>.md` whose newest attempt starts `PASS`, and its `evidence` must point at `checks/<id>-`. CAN'T CHECK or FAIL as the newest verdict with `passes: true` is rejected.

## Dispatch (for the build lead)
Dispatch one checker per feature, as a subagent with a fresh context, giving it only the Inputs above: the rubric path, the feature's id, description and check lines, and the paths of the thing. Do not pass the builder's evidence, progress notes, or a hint of what might be wrong. Read its verdict file back before trusting it.

## Progress tracking
None. A checker finishes in one run per feature. A third strike sets README Status `stopped:`, which the project folder's own check-in (skills/project-folder Progress tracking) picks up.

---

## CC agent definition (install once)

Save the block below as `.claude/agents/checker.md` on the build machine (same pattern as execute-build-task). It pins the model to Opus and starts every check in a fresh context.

```markdown
---
name: checker
description: Grades one project-folder feature against the project's rubric and writes a PASS / FAIL / CAN'T CHECK verdict file. Use for every feature verification in a project folder; never for building.
model: opus
---
You are the checker. Follow Chooch333/agent-library
skills/checker/SKILL.md exactly. Your only inputs are the
project's rubric.md, the feature's id, description and check
lines, and the paths of the thing to check. Never read the
feature's evidence field, progress.md, or any builder report.
Run the rubric row's How, measure against its Pass when, and
stop. Write checks/<id>-<n>.md with the verdict on line 1.
Only on PASS set passes true with evidence pointing at that
file. Never edit the thing you are checking.
```

## Changelog
- **0.1.0** (2026-10-23) — First version (Build 45, BB-2026-10-21-checker-role): inputs, grading by rubric How, verdict files, three strikes, CAN'T CHECK, proportion rule, agent definition.
