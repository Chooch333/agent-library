# Skill Design Framework (draft v0.1)
*agent-library reference — the method for designing a new skill or agent before its SKILL.md is written.*
*Status: **draft** — designed 2026-09-21 in a Design Assist session, dogfooded on the Inspector and Repairer (BB-2026-09-21-inspector-repairer). Owner: Charles.*

## Terms (locked 2026-09-21, CB-354)

- **Skill** — any written instruction file for one kind of job (every entry in agent-library).
- **Agent** — a skill that runs on its own: a trigger, tools, and nobody steering. A badge on a skill, not a separate category.
- "Role" is retired from Charles-facing text; the `roles/` folder name stays as plumbing.

## How to use this

Answer all twelve questions, in writing, before the SKILL.md is drafted. Questions marked **(Agent)** apply only to skills that run on their own. The answers travel in the Build Brief that creates the skill. `SKILL_TEMPLATE.md` and `CONVENTIONS.md` still govern the file's *format*; this framework governs the skill's *design*.

Same three-state rule as the brief-completeness framework: each question is **Answered**, **Defaulted** (standing convention named), or **N/A** (one line why). Silence is a defect.

## The twelve questions

1. **Job and "never."** One sentence for what it does; one sentence for what it must never do.

2. **Split test.** A new skill is justified only if at least one holds: (a) it needs write permission no existing skill has; (b) it must independently check another skill's work; (c) its trigger or cadence cannot share an existing run. File size, comfort, and naming are not reasons — use `references/` or extend an existing skill instead. The reverse also holds: an existing skill that both judges and fixes the same thing gets split (trace: Stack Manager, split into Inspector + Repairer 2026-09-21). Source: ADV-016 (Kavak simple-harness / Sierra don't-over-split).

3. **Write rights.** The exact list of what it may write, recorded in CONVENTIONS.md's exclusive-writes table. It never verifies anything it wrote.

4. **Trigger and runtime (Agent).** Must exist today: invoked by name, a Cowork scheduled task, or a GitHub Actions event. A trigger that depends on something not yet built is a defect (trace: SM-049 — Stack Manager waited two months on the never-built heartbeat-orchestrator).

5. **Where it leaves and picks up work.** Use an existing place — the build shelf (queued plans), the Comms Table (build questions and disclosures), or the Punch List (fixes to the system itself). Never use a Project State project as a queue (trace: the `stack-map` project mixing a suggestion queue with decisions and to-dos).

6. **Derived, never copied.** If the skill keeps a picture of something current, it checks the real thing rather than relying on others to report changes (trace: map suggestions — 22 filed, one ever applied, retired 2026-09-21).

7. **Step contract (ADV-017).** Every SOP step states four things: **precondition** (what must be true first), **action** (tool + parameters), **success evidence** (what proves the step worked), **recovery** (what to do when it didn't).

8. **Tool fit (ADV-031).** A fixed multi-call tool sequence the skill repeats every run becomes one bundled tool. Name it in the brief; don't hand-roll it forever.

9. **Safety (Agent).** A receipt so running twice does no harm; an attempt cap; a scope check (the change touched only what it claimed — ADV-019); hold back when unsure rather than act on a plausible guess (ADV-029); a protected list of things it never touches.

10. **Authority tiers.** Auto / needs a brief / the three hard gates (credentials only Charles can supply, real money, irreversible data change). Charles reads a trail, never a queue he must work.

11. **Proof and lifecycle.** One known-answer test in the acceptance run; cost per run and per week (real money flagged). Status stays `draft` until the first live run; pitfalls come only from real traces; the first live trace is folded into Examples before `status: active`.

12. **Registration and naming.** An AGENT.md routing row and a CONVENTIONS.md exclusive-writes row. The name must not collide with a locked term (trace: "auditor" is world-graph's fact-accuracy check, so the finder agent is the Inspector).

## Changelog

- **0.1** (2026-09-21) — Initial draft, designed in the Design Assist session that scoped the Inspector and Repairer; each question traces to a real incident or Stack Advisor idea (ADV-016, 017, 019, 029, 031). To be exercised and refined by BB-2026-09-21-inspector-repairer.
