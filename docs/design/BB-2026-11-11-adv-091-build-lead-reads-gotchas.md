# Build Brief — BB-2026-11-11-adv-091-build-lead-reads-gotchas

**Build:** unnumbered (Stack Advisor)
**Overnight:** yes · **target_repo:** Chooch333/agent-library · **after:** none
**Plan:** fc481ef5-fa64-492f-834b-0dfb5405d742 (Project State, project cbrain) · tags advisor-auto, build-brief, adv-091
**Git home:** Chooch333/agent-library docs/design/BB-2026-11-11-adv-091-build-lead-reads-gotchas.md

**What this is:** Builds started with "go build" and every night build skip the shared list of known tool traps, so they rediscover the same traps. One header line fixes that.
**What I'll do:** Add the known-traps file to the Build lead skill's required reading, plus one sentence telling it to pass any matching trap to its workers.
**What you'll do:** Nothing — click Declined on the Stack screen to stop it.

## Current state going in
### Asked for
- Stack Advisor idea ADV-091 (brief docs/advisor/ADV-2026-11-11.md in cbrain), from Anthropic's "The components of agent memory" (2026-11-06): keep a small top layer of checked notes and load it at the start of every session; a note that is never loaded does not help.
- Checked live this run (2026-11-11):
  - `references/gotchas.md` in agent-library is that small top layer (4 traps). It says one trap was rediscovered six times since June.
  - It is loaded by `skills/build` (interactive build chats), `skills/stack-repairer` and the Inspector/Repairer pair.
  - It is NOT in `skills/orchestrate-build` v1.9 `requires:` ([references/project-state.md, references/thread-checkin.md]) and not in `skills/night-run` v0.7.0 or `skills/execute-build-task` v1.2. Every "go build" and every night build runs as orchestrate-build, so autonomous builds never see the traps.
  - Two of the four traps (the "No approval received" SQL fallback, and GitHub Actions going dark) are things unattended builds hit.
- Trimmed: the article's bigger idea (a background pass that checks and promotes notes) already exists — the weekly Rules Inspector promotes repeated lessons into gotchas.md. Only the missing read is built here. No new file, task, account or cost.

## Receiving chat
The night runner.
## Scope
In: `skills/orchestrate-build/SKILL.md` only. Out: night-run, execute-build-task, gotchas.md itself, the stack map, any other skill.
## Directive
1. In `skills/orchestrate-build/SKILL.md` (agent-library, main), change the frontmatter `requires:` to `[references/project-state.md, references/gotchas.md, references/thread-checkin.md]`.
2. In step 2 ("Read the brief header"), add one sentence at the end: "Also read every file the `requires:` header names, including `references/gotchas.md` (known tool traps), before the first Project State write."
3. In step 4 ("Dispatch each task"), add to the list of what the worker gets: "and any trap from `references/gotchas.md` that touches the task, quoted".
4. Bump the version to 1.9.1 (frontmatter `version`, the title line, `updated:` the build date) and add a changelog line: "**v1.9.1** (<date>) — Build lead now reads `references/gotchas.md` (known tool traps) and passes matching traps to workers. Autonomous and night builds were the only builders not loading it. Stack Advisor done-for-you ADV-091 (BB-2026-11-11-adv-091-build-lead-reads-gotchas)."
5. Read the file back and confirm only these lines changed.
6. In Chooch333/cbrain `docs/advisor/LEDGER.md`, set the ADV-091 row to `addressed` with Response "done for you — built <YYYY-MM-DD>, BB-2026-11-11-adv-091-build-lead-reads-gotchas" (per skills/build, Advisor-origin closing hook). If the row is not there yet, add the note to the Session Log instead and say so in a disclosure.
## Acceptance
1. orchestrate-build `requires:` lists `references/gotchas.md`; steps 2 and 4 carry the two sentences; version 1.9.1 with changelog line (file read back).
2. No other line in the file changed (diff against the previous commit).
3. LEDGER row ADV-091 reads `addressed` (or handed off per step 6).
## Pasteable prompt
> Execute Build Brief BB-2026-11-11-adv-091-build-lead-reads-gotchas. Pull the plan from Project State (plan_id fc481ef5-fa64-492f-834b-0dfb5405d742, project cbrain). Answer forks yourself; stop only at hard gates. Standing rules CB-185, CB-121, CB-103 apply.
