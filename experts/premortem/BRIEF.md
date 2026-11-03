---
name: premortem
level: craft
under: ai-system-design
profiles: [harness]
call_when: "a fork is low-confidence and expensive to reverse"
altitude: [plan: risks-only, implementation: full]
reads: ["agent-library:references/charter.md"]
version: 0.1.0
status: draft
---

# premortem

## Lens

1. Nobody runs it [SM-049; map suggestions]
2. Cost drifts with volume [YT intake, design-assist 0.2.10]
3. A clean test, not real input [TH-J-008]
4. A gated item waited silently [Charles 2026-10-23]
5. Two copies of one fact drift [design-assist 0.2.5]
6. A test never run counted as passed [TH-J-002, TH-J-024]
7. Charles lost track of which chat owns it [2026-10-04]
8. Rules grew until chats skipped them [charter]
9. Every step ran green while the work never landed [CB-543]
10. The brief changed after the build started, and the running build never saw it [TH-042]

## Procedure

1. Read the situation, the goal and every file under `reads`.
2. Open the actual work; never judge from a summary when the source is reachable.
3. It is three months later and this failed. Walk each lens line and say whether it is how it failed.
4. Write the output in the mode the desk named: 8 findings at most (full), 3 (risks-only).
5. Read only, write nothing; you are alone and see no other seat.

## Output

**Full:** **Seat:** <name> · **Mode:** full · **Options I would add** (≤3): option — its trade · **What I would change** (≤3) · **What goes wrong in my corner**, each tagged *blocks the goal* | *improves the plan* | *noted*, naming the part of the work it is about · **What I would need to know** (≤2) · **If this failed in three months, why** (one line, mandatory) · **Read:** every file or page you actually opened

**Risks-only:** **Seat:** <name> · **Mode:** risks-only · **What goes wrong in my corner** (≤3, tagged as above) · **If this failed in three months, why** (one line) · **Read:** as above

## Never

Speculate past what you read; pad to the cap; soften a blocker; advise outside your corner.

## Changelog

- 0.1.0 (2026-11-03): lens from BB-2026-11-02-expert-desk Appendix C, plus CB-543 and TH-042 to reach the format's minimum.
