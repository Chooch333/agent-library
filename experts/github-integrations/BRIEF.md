---
name: github-integrations
level: craft
under: c-stack
profiles: [harness]
call_when: "the work uses Actions, the GitHub MCP, branch or file ops, or a repo as a queue"
altitude: [plan: risks-only, implementation: full]
reads: ["agent-library:references/gotchas.md", "cbrain:concepts/stack-map.md (lanes:)"]
version: 0.1.0
status: draft
---

# github-integrations

## Lens

1. Actions goes dark (billing lock, disabled workflow) and silence is read as success [gotchas.md; CB-427, CB-496]
2. Push-triggered runs that never fired are assumed to replay after an outage [CB-438]
3. A new MCP tool expected to be callable after a deploy; the manifest is frozen at handshake until the connector is reconnected [gotchas.md; E-085, D-083]
4. Branch ops that only fast-forward treated as a merge [BB-2026-11-02-expert-desk Appendix D; ~ no trace found for this line, confirm on first use]
5. Reads the wrong ref: a repo's `main` shows only what is live while builds land on another branch [CB-185, CB-530]
6. A write tool's `branch` left out, so the edit lands on `main` [CB-233]
7. "Already exists" on a write brushed aside; it is a collision signal: stop and read what is there [C-061]
8. A new dispatchable workflow committed only to a working branch; it must exist on the default branch first [CB-173, CB-144]
9. A run cancelled with no steps diagnosed as a code bug; it is a runner hiccup, re-dispatch it [CB-520]
10. A dispatch input's default trusted instead of passed explicitly [CB-210]
11. A change split across commits so an in-between commit does not build [F-088; TH-J-007]
12. A large file sent as one inline commit, which times out; anchored edits land it [E-196]
13. A large block matched in an edit, silently deleting what sat inside it [CB-045]
14. A file move assumed byte-safe through content-based tools; it is not [E-150]
15. A code-search miss taken as proof; the index lags a push and only covers `main` [A-070, CB-258]
16. A token whose scopes look right in the dashboard but fails on a real dispatch [CB-138]
17. A bot-triggered Action run assumed to work like a hand-dispatched one; the Claude action refuses bots unless allowed [A-064]

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

- 0.1.0 (2026-11-03): seed lens from BB-2026-11-02-expert-desk Appendix D, mined from gotchas.md and lessons across projects.
