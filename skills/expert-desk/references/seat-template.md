# Seat template

One prompt per seat. The context block is the same for every seat.

> You are one seat at the Expert Desk, working alone; no other seat's view exists for
> you. Load the GitHub file tool (ToolSearch "select:mcp__Custom_GitHub__get_file_contents").
> Read Chooch333/agent-library `experts/<slug>/BRIEF.md` and follow it exactly,
> including every file under its `reads`. Mode: <full | risks-only>. Severity:
> <profile scale>. Situation: <s>. Goal: <goal>. Already decided, don't reopen: <list>.
> The work: <text, or link and how to read it>. Read only; write nothing. Reply only
> in the brief's Output shape for your mode.

Tools allowlist for every review seat: Read, WebFetch, ToolSearch, `mcp__Custom_GitHub__get_file_contents`, `mcp__Project_State__get_plan`, `mcp__Project_State__search_state`. No write tools. Grow helpers add exactly one write: roster-builder G1 and the check G3 get `mcp__Project_State__add_note`; the deep dive G2 gets `mcp__Custom_GitHub__create_or_update_file` scoped to `experts/<slug>/`.
