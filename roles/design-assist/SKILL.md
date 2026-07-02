---
name: design-assist
version: 0.1.0
status: draft
triggers:
  - "Design Assist"
dependencies: []
owner: Charles
updated: 2026-07-02
source: Original. Designed in-chat 2026-07-02 by Charles + Claude, dogfooding the process on itself. Absorbs the alternatives-generation idea from office-hours (Tan gstack lineage) into the convergence loop; otherwise independent of the office-hours → CEO/Eng review chain, which serves go-to-market interrogation, not hobby design.
---

# Design Assist

## What

Claude leads Charles from a fuzzy concept to a build-ready spec/plan, teaching him the territory along the way. The job in one line: **help Charles understand this territory and shape a design for HIS use case.**

This is hobby-mode design across any domain — robotic lawn mowers, high-speed drones, 3D printing and micro-manufacturing, apps, personal dashboards. The process is domain-agnostic; the spec format adapts (software gets an MCP-first build spec; hardware gets a bill of materials, sourcing, build sequence, and test plan).

The session's source of truth is a single living **Design State artifact** — rewritten each update, never appended — showing current shape, decisions made, open items, and assumptions. Not Project State; the artifact. Project State is used only as periodic snapshot storage and for one light log at exit.

## When

**Fire when:** Charles says "Design Assist" in the prompt. That is the only trigger. Do not auto-fire from adjacent phrases.

**Do not fire when:** the design is already shaped and he wants execution (build chat), viability interrogation (office-hours), or a one-shot multi-perspective read (brainstorm chat).

## The Design State artifact

Created from `references/design-state-template.md` at intake. Rules:

- **Current state only.** Superseded ideas are dropped, not archived. Decision *reasons* stay (one line each) so settled questions don't get relitigated.
- **Rewritten after every decision or material turn.** The header carries date and turn count.
- **Language balance.** Plain English first. Jargon defined inline on first use. One technical clause per idea, max. Charles is not technical; the artifact must communicate the design shape to him and to a future technical executor at the same time.
- **Five sections:** The Shape / Decisions Made / Open Items / Assumptions / Out of Scope. Open Items ordered by what blocks the most downstream work.

**Snapshot rule:** save the full artifact text to Project State at every **phase boundary** (end of Orient, end of Constrain, convergence milestones, exit) and whenever Charles says "save state" — not every turn. First save uses `write_plan` (project per `list_projects` fit-check, per PROTOCOL.md); later saves use `update_plan_content`, which keeps revision history automatically. This is storage, not ceremony — no Session Log per save.

## How — four phases, ten steps

Steps run in order, but the process is a loop, not a rail: new information can reopen an earlier step. When that happens, update the Design State and say so.

### Phase A — Orient

1. **Intake.** Charles dumps the raw idea, however messy. Capture it verbatim into the artifact before shaping anything. Create the Design State artifact now.
2. **Restate.** Say what Charles is really trying to do — including the goal behind the stated goal, and how it serves *his* use case specifically (his skills, his shop, his family, his stack). Iterate until he says it lands.
3. **Domains.** Name the disciplines and bodies of practice involved (e.g., for a mower: robotics, battery systems, blade safety, outdoor navigation, weatherproofing).
4. **Concepts & vocabulary.** Explain the key ideas at a high level, plainly. This is also where Charles gets precision language — the words that let him say what he means in this territory.
5. **Design space map.** The 2–4 main archetypes people use to solve this class of problem, what each optimizes for, and what each costs. Buy vs. modify vs. build-from-scratch is almost always one of the axes for hardware. *(Primary fan-out point — see Fan-out below.)*
6. **Traps & unknown unknowns.** Hidden assumptions, common failure patterns, the questions Charles doesn't know to ask. For physical builds, always include safety and regulatory traps (blades, LiPo batteries, FAA drone rules, etc.).

### Phase B — Constrain

7. **Constraints & success criteria.** What must be true: budget, time, skills he has vs. would need, tools and equipment on hand, who uses the thing, where it lives. Then what "done well" looks like — concrete and testable where possible ("mows the back half-acre unattended without eating a sprinkler head").

### Phase C — Converge

8. **Decision loop.** One fork at a time, phrased as a closed choice with a recommendation (per PROTOCOL.md engagement rules). Every answer updates the Design State. Where the old office-hours process generated 2–3 alternatives once, this loop generates alternatives *per fork* — same muscle, applied repeatedly at finer grain. Loop ends when Open Items is empty or every remaining item is explicitly deferred with a reason.

### Phase D — Exit

9. **Spec generation.** Write the build spec/plan from the final Design State.
   - **Software/system:** MCP-first per PROTOCOL.md — each step names the tool that executes it (Supabase MCP, GitHub MCP, Vercel MCP...), with parameters.
   - **Hardware:** bill of materials with sourcing links and prices, tools required, build sequence, wiring/assembly notes, test plan, safety checklist.
   - **Hybrid** (e.g., drone + telemetry dashboard): both, cross-referenced.
10. **Handoff.** Package execution as one or more Build Briefs per PROTOCOL.md, or continue inline if small. Commit the final Design State and spec to the target project's repo (`docs/design/`) if one exists. Close with one light Session Log to Project State: the decision set, the spec location, next action.

## Fan-out — automated multi-agent loops

Fan-out is **Claude-decided, Claude-executed, Claude-aggregated**. Charles is told a fan-out is running and reads the distilled result; he does not assemble briefs or paste anything.

**Two fan-out points:**

- **Design space survey (step 5).** When the territory is broad or unfamiliar, one agent per approach archetype researches it independently — how it works, who uses it, real costs, failure modes — and returns a structured one-pager. Claude distills them into the design space map.
- **Fork panel (step 8).** Fires when BOTH are true: Claude's confidence in its own recommendation is low, AND the fork is expensive to reverse (money already spent, parts ordered, architecture locked). One agent per branch argues *for* its branch; position papers come back; Claude distills; Charles decides. If either condition is absent, Claude just recommends — no panel.

**Mechanism:** the Brainstorm Orchestrator with a custom prompt set. Insert a row into the orchestrator's `briefs` table (Supabase project `drjtbqkizrqrwajofsea`) with the shared context as `content` and the per-agent prompts in `agent_prompts` — the database trigger auto-fires the run, same as a brainstorm chat. Poll per BRAINSTORM.md Step 4–6 mechanics (45s first wait, up to 4 checks, same failure diagnostics). Read the compiled output, **distill it into the Design State** — unlike brainstorm chats, synthesis is the point here — and link the full output for Charles.

**Aggregation rules:** agents never touch the Design State; only the conducting chat writes it. Distillation names where agents disagreed. The full output link is always provided so Charles can read the raw papers.

*(Until the `agent_prompts` capability ships in the orchestrator, fall back to running the perspectives sequentially in-chat and say that's what happened. Do not silently skip fan-out.)*

## Examples

### "Design Assist — I want to build a robotic lawn mower"

→ A: intake verbatim; restate ("you want to stop mowing, learn robotics with the boys, and keep it under $X — not start a mower company"); domains (robotics, batteries, blades/safety, navigation, weatherproofing); vocabulary (RTK GPS, perimeter wire, brushless motors, IP ratings); design space fan-out → agents on (1) buy-and-hack a commercial unit, (2) kit build, (3) scratch build on an open platform like OpenMower; traps (blade liability with kids, LiPo fire safety, GPS drift near trees)
→ B: budget, shop tools, solder skills, yard shape, "done well" = unattended half-acre
→ C: forks one at a time — platform, navigation method, blade type, power system; fork panel fires on nav method if confidence is low and parts are pricey
→ D: hardware spec — BOM with links, build sequence, test plan, safety checklist; Build Brief for the companion dashboard if wanted

### "Design Assist — personal web dashboard for the rental portfolio"

→ A–B compressed (familiar territory, fewer unknowns — say so and move fast)
→ C: forks on data sources, hosting, auth
→ D: MCP-first software spec; handoff to a build chat via Build Brief

## Pitfalls

> Pitfalls come from real traces.

(Draft — none yet. Watch for: skipping Orient because the territory *feels* familiar; letting the artifact lag behind chat decisions; firing fork panels on cheap-to-reverse forks; teaching at engineer depth instead of Charles depth.)

## Changelog

- **0.1.0** (2026-07-02) — Initial draft. Designed by dogfooding the process on itself. Four phases / ten steps, Design State artifact spec, phase-boundary snapshots via Project State plan tools, automated fan-out via orchestrator custom prompt sets (pending `agent_prompts` capability), hardware + software + hybrid spec formats. Explicitly decoupled from the office-hours → CEO/Eng go-to-market chain.
