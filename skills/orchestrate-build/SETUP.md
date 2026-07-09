# SETUP: orchestrate-build system (v1)

One-time installation on the build machine, plus the conventions the whole system rides on.

## 1. Bootstrap (drop into CC config)

Add to the project's `CLAUDE.md` (or `~/.claude/CLAUDE.md` for machine-wide). This is deliberately minimal — location knowledge only:

```
Build briefs are plans in Project State (Project State MCP).
When told to "go build <plan-id or 'next'> [on <project>]":
fetch the brief; its header names required skills; fetch each from
Chooch333/agent-library at skills/<name>/SKILL.md and follow them.
Start with skills/orchestrate-build/SKILL.md if the brief names no skills.
```

## 2. Worker definition
Install `.claude/agents/execute-build-task.md` per the block in `skills/execute-build-task/SKILL.md`.

## 3. Lead model
Launch build sessions with the lead pinned to Fable (e.g. `claude --model claude-fable-5`, or set in CC settings). Workers are pinned to Opus by their definition file.

## 4. MCP wiring (connect in CC)
- **Project State** — briefs, statuses, session logs (required)
- **Custom GitHub** — skill fetching + repo work (required)
- **Supabase** — as briefs require
- **Vercel** — as briefs require

## 5. Brief header convention
Every build brief saved to Project State starts with:

```
harness: orchestrate-build v1
skills: <comma-separated additional skills, if any>
project: <project-state project>
```

## 6. Queue convention
- Design/planning chats save finished briefs as plans with status **queued**.
- "go build next" = oldest queued plan on the named project.
- Orchestrator flips queued → in-progress on pickup, → completed state on verified close.

## 7. Proof round (gate before trusting the system)
Run one small real brief end-to-end. In order, this proves:
1. Project State MCP connects from CC at all (biggest unknown)
2. Bootstrap fires from a bare "go build" prompt
3. Skill fetch from agent-library works
4. Worker dispatch runs on Opus and reports evidence
5. A deliberate fork in the brief gets answered by the lead, not the human
6. Session Log lands back in Project State

Do not queue real builds until all six pass.
