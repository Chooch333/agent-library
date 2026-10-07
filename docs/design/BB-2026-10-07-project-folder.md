# Build Brief — BB-2026-10-07-project-folder

**Git home:** Chooch333/agent-library · `docs/design/BB-2026-10-07-project-folder.md`
**Project State plan:** `1b9f9b2d-1bed-4d2e-a39b-49a6d413daab` on `total-harness`
**Build:** 29
**Skills:** orchestrate-build
**Harness block:** 2 — Standard project folder (shared six)

**What this is:** A standard project folder every moonshot starts from — spec, feature list, progress log, checker rubric — plus a short skill that says how to start one, resume one, and close a session in one.

**What I'll do (build chat):** Commit the template and the skill to agent-library, prove them on one demo project in its own private repo, and prove a fresh session can resume from the files alone.

**What you'll do:** Nothing during the build. Afterwards, glance at the demo repo if you want.

**Cost:** $0. **Charles's time:** 0 during the build; ~5 min optional look after.

---

## Current state going in

**Asked for** (Charles, 2026-10-07, verbatim): "next block" — within the Total Harness project, whose standing order is: build the harness blocks in campaign order; block 2 is "Standard project folder: spec, feature list, progress log, checker rubric" (harness-map b02, kind "Custom, small").

- The blueprint (Working Document, "Total harness blueprint" tab) says: "State lives in files: a feature list, a progress log, version history. Every new session reads those files, not the old conversation." Status: "Missing: a standard project folder every moonshot starts from."
- Source pattern (verified 2026-10-07, Anthropic engineering post "Effective harnesses for long-running agents"): an initializer writes a JSON feature list (each entry has description, test steps, `passes: false`), a progress file, a run script, and a git repo; each later session reads git log + progress, picks the highest-priority unfinished feature, works one feature, verifies, commits, updates progress. JSON is used because the model is less likely to rewrite it; agents may only flip `passes`, never edit or delete features.
- Nothing like this exists yet: agent-library `skills/` holds checkpoint-deploy, execute-build-task, job-update, night-run, orchestrate-build only; no Project State item mentions a project folder template.
- Block 1 is done: cloud sessions reach Charles's laptop; workshop folder `C:\Users\cecou\code\workshop` is connected.
- Block 6 (planner, builder, checker roles) comes later and will *use* this folder. This build does not write those roles.

## Receiving chat

New build chat (Claude Code or Cowork) running orchestrate-build.

## Scope

**In scope**
1. `templates/project-folder/` in agent-library — the files drafted in Appendix A, committed as-is (fix only real errors).
2. `skills/project-folder/SKILL.md` in agent-library — drafted in Appendix B.
3. One demo project: private repo `Chooch333/moonshot-demo` created from the template, filled for the ask "a printable name keychain for Louis" (spec + 5–8 features + rubric filled; nothing printed or modelled).
4. The validator `check_folder.py` passing on the demo and failing on a deliberately broken copy.
5. A resume test: a fresh subagent given only "resume Chooch333/moonshot-demo using skills/project-folder" names the correct next feature and appends a progress entry.

**Out of scope (forks pre-answered)**
- Planner / builder / checker roles — block 6.
- Per-domain rubrics — block 17. `rubric.md` here is the per-project rubric only.
- Stop inbox / phone alert — block 4. `spec.md` lists stops; it does not send them.
- Cloning to the laptop. The PC working copy rule is written into the skill; no build step clones to the PC.
- An AGENT.md trigger row. The skill is used by builds and future roles, not fired by a phrase.
- A GitHub "template repository". Ruled out: an extra repo to keep in sync, and the template flag is unverified in the Custom GitHub MCP. New projects copy the files from agent-library.

## Directive

Steps (Custom GitHub MCP for every repo write, as Chooch333):
1. `create_or_update_file` each Appendix A file to `Chooch333/agent-library` `templates/project-folder/<name>` (branch main). Read each back.
2. `create_or_update_file` Appendix B to `skills/project-folder/SKILL.md`. Read back.
3. `create_repo` `Chooch333/moonshot-demo`, private, description "Harness block 2 demo — standard project folder". Following the skill's *Start* routine, copy the template in and fill it for the keychain ask. Commit message per file: "start: <file>".
4. Run `check_folder.py` against a local copy of the demo (cloud shell: clone or fetch the files) → must exit 0. Then delete `rubric.md` and set one feature's `passes` to true with empty `evidence` in a scratch copy → must exit non-zero naming both problems. Record both outputs.
5. Resume test: dispatch a fresh subagent (execute-build-task) with only: "Resume project Chooch333/moonshot-demo following agent-library skills/project-folder/SKILL.md. Do the Resume routine, then the Close routine without building anything; say which feature is next." Verify it named the first `passes:false` feature by priority and committed one new progress entry; validator still exits 0.
6. Close out per orchestrate-build (Session Log on `total-harness`, receipt). Mirror: add a world-graph write package `TH-block-2-done` (`set` status `done` on task `harness-map#b02` — look up its uuid in cbrain `pm_tasks` where `legacy_ref = 'harness-map#b02'`), author `claude`.

## Acceptance

1. Template files and skill exist on agent-library main and read back identical to what was committed.
2. `Chooch333/moonshot-demo` exists (private) with every template file filled; spec carries the ask verbatim.
3. Validator exits 0 on the demo and non-zero on the broken copy, naming each problem.
4. Fresh-session resume names the correct next feature and leaves one new progress entry; validator still 0.
5. cbrain task b02 shows `done` (`pm_tasks.status`) after write_protocol runs.

## Hard gates

None expected. No money, no credentials beyond the existing GitHub MCP, nothing destroyed (the broken copy is scratch only).

## Inputs

- cbrain `concepts/harness-map.md` (b02, b06, b16, b17).
- Working Document blueprint tab: claude.ai/artifact/6Ua3T5qYfErF9DbPJKvvzJ.
- https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents
- world-graph `docs/contracts/WRITE_PACKAGE.md` (the `set` op); example `data/project_writes/TH-block-1-done.json`.

## Judgment calls made in scoping [Claude-per-doctrine]
- Home of each project = its own private GitHub repo (reachable from phone, cloud and any session, history for free); the laptop holds a working copy under `code\workshop\<slug>` only when a step needs the PC. Ruled out: projects living only on the laptop (unreachable when it sleeps) and one mono-repo for all moonshots (one build per repo at a time would serialize them).
- Template lives in agent-library beside the skills that use it.
- Feature list is JSON; everything else is Markdown.
- Build number 29 (28 taken by BB-2026-10-07-wire-new-app the same day).

---

## Appendix A — template files (draft)

### `templates/project-folder/README.md`
```markdown
# {Project name}

**Ask (verbatim):** {the one sentence Charles said}
**Lane:** {one line — what is being built and how}
**Status:** {planning | building | stopped: <why> | done}
**Project State:** {plan id or "none"}
**PC working copy:** {C:\Users\cecou\code\workshop\<slug> or "none"}

Start here: read `progress.md` (latest entry first), then `features.json`.
How this folder works: agent-library `skills/project-folder/SKILL.md`.
```

### `templates/project-folder/spec.md`
```markdown
# Spec — {Project name}

## Ask
{verbatim, never edited; later changes are added below as dated lines in Charles's words}

## What I am building
{plain description, one lane}
Ruled out: {alternatives, one line each}

## Works means
{3–6 testable statements; these become the top features and the rubric}

## Stops
Points where Charles reacts before work continues. Money always stops.
1. Concept stop — after this spec, before building.
2. {money stop: what would be bought, est. $}
3. Final stop — delivery.

## Budget
Money: ${est} (nothing bought without Charles's yes). Charles's hours: {est}.

## Safety
{rules for this domain, or "standard"}

## Tools
{what this needs: software, accounts, machines; where each step runs: cloud | PC | bench}
```

### `templates/project-folder/features.json`
```json
{
  "project": "{slug}",
  "rules": "Work one feature at a time. Only change passes and evidence. Never edit or delete a feature; add new ones at the end.",
  "features": [
    {
      "id": "F01",
      "priority": 1,
      "description": "{what is true when this is done}",
      "check": ["{step a checker can follow}"],
      "passes": false,
      "evidence": ""
    }
  ]
}
```

### `templates/project-folder/progress.md`
```markdown
# Progress — {Project name}

Newest entry first. One entry per session. Never rewrite an old entry.

## {YYYY-MM-DD HH:MM} — {session: who/what}
- Did: {what changed}
- Checked: {what was verified, how}
- Next: {feature id and first step}
- Stops/notes: {anything waiting on Charles}
```

### `templates/project-folder/rubric.md`
```markdown
# Rubric — {Project name}

The checker grades against this, not against the builder's report.
Each line: what is checked, how, and what passes.

| # | Check | How | Pass when |
|---|-------|-----|-----------|
| 1 | {from "Works means"} | {test, render, measurement, screenshot} | {threshold} |

Finish standard: function must work; recreational finish is fine.
```

### `templates/project-folder/run.md`
```markdown
# Run — {Project name}

How any session gets this project running again.
- Where: {cloud | PC: C:\Users\cecou\code\workshop\<slug> | bench}
- Setup once: {installs, accounts}
- Run / build: {commands or steps}
- Quick health check: {one thing to run first each session}
```

### `templates/project-folder/.gitignore`
```
outputs/
*.tmp
.DS_Store
```

### `templates/project-folder/check_folder.py`
```python
"""Check a project folder against the standard. Usage: python check_folder.py [folder]"""
import json, sys, pathlib

REQUIRED = ["README.md", "spec.md", "features.json", "progress.md", "rubric.md", "run.md"]

def main(root="."):
    root = pathlib.Path(root)
    problems = []
    for name in REQUIRED:
        if not (root / name).is_file():
            problems.append(f"missing {name}")
    fpath = root / "features.json"
    if fpath.is_file():
        try:
            data = json.loads(fpath.read_text(encoding="utf-8"))
            feats = data.get("features")
            if not isinstance(feats, list) or not feats:
                problems.append("features.json: no features")
            else:
                seen = set()
                for f in feats:
                    fid = f.get("id", "?")
                    for key in ("id", "priority", "description", "check", "passes", "evidence"):
                        if key not in f:
                            problems.append(f"{fid}: missing {key}")
                    if fid in seen:
                        problems.append(f"{fid}: duplicate id")
                    seen.add(fid)
                    if f.get("passes") is True and not str(f.get("evidence", "")).strip():
                        problems.append(f"{fid}: passes without evidence")
        except json.JSONDecodeError as e:
            problems.append(f"features.json: not valid JSON ({e})")
    spec = root / "spec.md"
    if spec.is_file() and "{" in spec.read_text(encoding="utf-8").split("## Ask", 1)[-1].split("##", 1)[0]:
        problems.append("spec.md: Ask still a placeholder")
    for p in problems:
        print("FAIL", p)
    if not problems:
        print("OK", root)
    return 1 if problems else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
```

## Appendix B — `skills/project-folder/SKILL.md` (draft)

```markdown
---
name: project-folder
version: 0.1.0
status: draft
triggers: [used by builds and harness roles when a moonshot starts or resumes; no chat trigger]
dependencies: []
owner: Charles
updated: 2026-10-07
wiring:
  runs: inside-builds
  reads: [project repo]
  writes: [project repo]
  stack: [total-harness]
  origin: yours
  label: Project folder
---

# Project folder

Every moonshot lives in one standard folder so any session can pick it up from the files, not from an old chat.

## Where it lives
- Home: a private GitHub repo `Chooch333/<slug>` (slug = short, lowercase, hyphens).
- PC working copy, only when a step needs the PC: `C:\Users\cecou\code\workshop\<slug>`. The repo stays the record; push from the PC copy at the end of each PC session.
- Big outputs (renders, meshes, video) go in `outputs/`, which is not committed.

## Start (once per project)
1. Create the repo (Custom GitHub MCP `create_repo`, private).
2. Copy every file in agent-library `templates/project-folder/`.
3. Fill `spec.md` from the ask. The Ask section is Charles's words, verbatim, never edited.
4. Turn "Works means" into the first features (priority 1..n) and into the rubric rows.
5. Fill `run.md` and `README.md`. Write the first progress entry.
6. Run `check_folder.py`; it must print OK. Commit.
7. Stop at the concept stop (spec.md Stops #1) before building.

## Resume (start of every session)
1. Read `README.md`, the newest `progress.md` entry, and recent commits.
2. Run the quick health check in `run.md`.
3. Pick the lowest-priority-number feature with `passes: false`. Work only that feature.

## Close (end of every session)
1. Set `passes: true` only with evidence (a test result, screenshot path, measurement). Never edit or delete a feature; add new ones at the end.
2. Add one entry at the top of `progress.md`: did, checked, next, stops.
3. Run `check_folder.py`; it must print OK. Commit with a plain message.

## Rules
- One feature at a time.
- The builder does not grade itself when a checker is available (block 6); until then, evidence is required for every pass.
- Money always stops. Safety rules in spec.md never relax.
```
