---
name: chat-access
level: craft
under: c-stack
profiles: [harness]
call_when: "the work assumes what a chat lane can reach: the Agent tool, its tools, connectors, scheduled vs live, PC"
altitude: [plan: risks-only, implementation: full]
reads: ["cbrain:concepts/stack-map.md (lanes:)", "agent-library:skills/checker/SKILL.md"]
version: 0.1.0
status: draft
---

# chat-access

## Lens

1. No Agent tool in overnight sessions [TH-J-001, TH-J-022]
2. A chat opened before a deploy cannot see new tools [board rule 11]
3. The PC unreachable unattended [TH-J-024]
4. A connector present but empty [Build 55]
5. One chat cannot start another chat [dry run 2026-11-02]
6. A helper's fixed overhead left out of what a run will use [probe, BB-2026-11-02-expert-desk]
7. A helper inherits all tools unless allowlisted [TH-134 line 17]
8. A helper sees no conversation, no invoked skills and no read files unless told [TH-134 line 16]
9. A protected preview URL assumed fetchable from a cloud session [CB-286, CB-378]
10. Memory and past-chat search assumed the same on every surface; each environment-dependent step needs a named fallback [MB-007]
11. A dry run prescribed that needs a browser the session does not have [CB-142]

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

- 0.1.0 (2026-11-03): seed lens from BB-2026-11-02-expert-desk Appendix D, plus lessons CB-286, CB-378, MB-007 and CB-142.
