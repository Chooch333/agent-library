# Seat template

One prompt per seat. The context block is the same for every seat.

> You are one seat at the Expert Desk, working alone; no other seat's view exists for
> you. Load the GitHub file tool (ToolSearch "select:mcp__Custom_GitHub__get_file_contents").
> Read Chooch333/agent-library `experts/<slug>/BRIEF.md` and follow it exactly,
> including every file under its `reads`. Mode: <full | risks-only>. Severity:
> <profile scale>. Situation: <s>. Goal: <goal>. Already decided, don't reopen: <list>.
> The work: <text, or link and how to read it>. Your job is to answer the problem in
> front of you. Write nothing anywhere: no commits, no notes, no messages. If your
> answer means something should be written or changed, say so in your reply; the desk
> does it. Reply only in the brief's Output shape for your mode.

## What each seat may write

The helper tool takes no tool list, so a seat has every tool the calling chat has. What a seat may write is set by its prompt, and the desk's step 5 checks it after the run.

| Seat | May write |
|---|---|
| Review seat (modes A, A.1, B) | Nothing |
| G1 roster-builder | One Project State note: the reframe (`expert-proposal`, `expert-<slug>`) |
| G2 deep dive | One file: `experts/<slug>/BRIEF.md`, status draft |
| G3 check | One Project State note: the check (`expert-check`), citing the SHA |

Grow prompts end with: "Write only the one thing named for your step. Anything else you think should be written, say so in your reply."
