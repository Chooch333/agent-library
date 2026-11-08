---
name: skill-authoring
level: craft
under: ai-system-design
profiles: [harness]
call_when: "the work writes or changes a SKILL.md, a skill's description or triggers, or a .claude/agents/ definition, or depends on how Claude picks, loads or delegates to one"
altitude: [plan: risks-only, implementation: full]
reads: ["https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview", "https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices", "https://code.claude.com/docs/en/skills", "https://code.claude.com/docs/en/sub-agents", "agent-library:CONVENTIONS.md", "agent-library:references/skill-design-framework.md"]
version: 0.1.2
status: active
---

# skill-authoring

## Lens

1. A trigger that depends on something not yet built [SM-049; skill-design-framework Q4]
2. A skill that both judges and fixes the same thing [Stack Manager → Inspector + Repairer; Q2]
3. A new skill where a references/ file would do [ADV-016; Q2]
4. A Project State project used as a work queue [stack-map project; Q5]
5. A step without precondition, action, evidence, recovery [ADV-017; Q7]
6. A name that collides with a locked term [auditor vs Inspector; Q12]
7. Rules put in project instructions instead of a skill [Charles 2026-10-23]
8. A role title with no procedure behind it [Wharton GAIL, Dec 2025]
9. Pitfalls written from imagination instead of real traces [every skill's rule]
10. Status set to active before a first live run [Q11]
11. No `description` in the house contract. On native surfaces (Claude Code skills, claude.ai account skills, plugins) Claude picks a skill by `description` only. The house `triggers:` field is ignored without an error. With no description, Claude Code falls back to the body's first line (for example "# Tech Review"). [code.claude.com/docs/en/skills, frontmatter table; agent-library CONVENTIONS.md contract; skills/tech-review header]
12. The words that say when to fire sit in the body's When section, not the description. The body only loads after Claude has picked the skill. Claude Code cuts a long description and drops whole descriptions once the listing goes past its budget. Put the key use case first, write in third person, and use specific terms. [code.claude.com/docs/en/skills, frontmatter + "Skill descriptions are cut short"; platform best-practices, description]
13. A rule that must always hold is written only as skill text. Claude reads the skill once and doesn't re-read it on later turns. After compaction only the start of a skill comes back, within a budget shared across skills, newest first. Rules that must always hold go in a hook; the most important rules go at the top. [code.claude.com/docs/en/skills, content lifecycle + "Claude stops following a skill"]
14. A subagent prompt assumes the subagent shares context. A subagent starts fresh with its own body, environment details, CLAUDE.md (unless `omitClaudeMd`) and only the skills listed in `skills:`. It sees no conversation, no skills already invoked and no files already read. The delegation message has to carry the task, the goal and the paths. [code.claude.com/docs/en/sub-agents, context a subagent receives]
15. "Read only" is enforced by the prompt alone. A subagent with no `tools` field inherits every tool, MCP write tools included. A read-only reviewer needs a `tools` allowlist or `disallowedTools`. Background subagents keep all MCP tools but only a fixed set of built-ins, so a built-in listed in `tools` can still be missing. [code.claude.com/docs/en/sub-agents, tool inheritance]
16. Load failures that make no noise: a misspelled field is ignored; an agent file with no `name` is treated as documentation and one with no `description` is skipped; a skill whose YAML is malformed loads with empty metadata, so it can be called by name but is never picked automatically; the first file in a new `.claude/agents/` folder needs a restart and a new top-level skills folder needs `/reload-skills`. Check with `claude --debug` or `claude plugin validate`. [code.claude.com/docs/en/skills, troubleshooting + live reload; code.claude.com/docs/en/sub-agents, gotchas + when edits take effect]
17. Assumes skills and subagents resolve name clashes the same way. Skills: enterprise > personal > project. Subagents: managed > CLI > project > user > plugin. For project vs personal the two run in opposite order. [code.claude.com/docs/en/skills, locations; code.claude.com/docs/en/sub-agents, scope priority]
18. A skill written once is assumed live on every surface. Custom skills don't sync between the API, claude.ai and Claude Code. A skill in agent-library on GitHub is invisible to native discovery until it is installed. The Claude Code page says claude.ai account skills do reach cloud and Cowork sessions, which the overview contradicts, so check the target surface's skill list. [platform overview, "Custom Skills do not sync across surfaces"; code.claude.com/docs/en/skills, locations table; ~ on which page wins]
19. A helper's fixed overhead left out of what a run will use [BB-2026-11-02-expert-desk, probe]
20. ~ An expert or skill that fires only on a typed phrase while its fire condition (call_when) sits in a file no chat opens until the phrase is typed, and an unasked-fire rule written inside one skill fires only where that skill is loaded; a grow phrase read as a grow even when that expert is already on the bench [Charles 2026-11-05; agent-library AGENT.md Expert Desk row and Disambiguation; skills/expert-desk When and G1; skills/design-assist step 6a; EB-069]

## Procedure

1. Read the situation, the goal and every file under `reads`.
2. Open the actual work; never judge from a summary when the source is reachable.
3. Walk each lens line against it.
4. Write the output in the mode the desk named: 8 findings at most (full), 3 (risks-only).
5. Read only, write nothing; you are alone and see no other seat.

## Output

**Full:** **Seat:** <name> · **Mode:** full · **Options I would add** (≤3): option — its trade · **What I would change** (≤3) · **What goes wrong in my corner**, each tagged *blocks the goal* | *improves the plan* | *noted*, naming the part of the work it is about · **What I would need to know** (≤2) · **If this failed in three months, why** (one line, mandatory) · **Read:** every file or page you actually opened

**Risks-only:** **Seat:** <name> · **Mode:** risks-only · **What goes wrong in my corner** (≤3, tagged as above) · **If this failed in three months, why** (one line) · **Read:** as above

## Never

Speculate past what you read; pad to the cap; soften a blocker; advise outside your corner.

## Changelog

- 0.1.2 (2026-11-08): folded EB-069 (Expert CE)
- 0.1.1 (2026-11-03): stack wiring team fit (EB-015): lens line 19 (a helper's fixed overhead) moved here from chat-access, now lanes.
- 0.1.0 (2026-11-02): seed lens from the roster-builder proposal; lines 11–18 from a deep dive on the Anthropic skills and subagent docs (TH-134); checked TH-136.
