# Build Brief Completeness Framework (draft v0.1)
*Design Assist reference — expands the 10-gate checklist in `build-brief-template.md`.*
*Status: **draft** — designed 2026-07-10, dogfooding session. Owner: Charles.*

## The one rule everything hangs on

A build agent picking this brief off the queue must never have to guess — and Charles must never be the tiebreaker. When a worker returns a fork, **the orchestrator decides it and moves forward, without escalation**. The brief's job is to make those decisions answerable: any domain the brief is silent on degrades the orchestrator's ability to decide well.

The **only** escalation triggers are genuine hard gates: credentials or access only Charles can supply, spending real money, or destroying/irreversibly changing data. Everything else — including forks the brief didn't anticipate — the orchestrator resolves from the design intent narrative (domain 11) and logs. Charles reviews the completed build and the fork log afterward; he does not babysit the build.

Therefore: **every domain below must be in exactly one of three states before a brief is queue-ready.**

| State | Meaning |
|---|---|
| **Answered** | A decision is written down, with a one-line reason. |
| **Defaulted** | No decision was needed; the standing convention applies, and the brief names it (e.g., "TypeScript, per repo convention"). |
| **N/A** | The domain genuinely doesn't apply to this build, and the brief says so in one line. |

Silence is a defect. "N/A" written down is fine; nothing written is not.

---

## The eleven decision domains

### 1. Purpose & users
Why this is being built and who touches it.
- **Build purpose:** learning project / personal daily-use tool / production system others depend on. This one decision sets the bar for everything else (error handling, polish, testing depth).
- **Users:** who uses it, how often, on what device.
- **Goal behind the goal:** the one-liner from Phase A restate.

### 2. Acceptance criteria
What proves it worked — concrete and testable ("a never-before-seen email produces a filed brief within 5 minutes"), not vibes ("works well"). Include the **verification run** itself: what the executor does to demonstrate done, and what that run needs to exist (lesson E-266: verification paths are dependencies too).

### 3. Runtime & execution
Where and how the thing actually runs.
- **Host:** Vercel / Supabase edge function / Claude Code local / Cowork scheduled task / browser-only.
- **Trigger model:** on a schedule, on an event (webhook, new email), or on demand.
- **Language & framework:** named, or "per repo convention" as a default.
- **Third-party dependencies:** libraries or services the build will pull in, with any real-money cost.

### 4. Data — schema
The shape of the information.
- Tables/entities and their fields, or the entity-page + frontmatter shape for cbrain-style storage.
- New vs. changed: does this build create schema, or migrate existing schema? Migrations get named explicitly — they're higher-risk.
- Contracts at boundaries: if another system reads this data, the field names are the contract (per BRIEF_SCHEMA precedent: committed contract supersedes brief wording).

### 5. Data — storage & recall
Where the data lives and how it comes back out. These are two decisions, not one.
- **Storage engine:** Supabase tables / GitHub markdown / flat files / nowhere (stateless).
- **Recall type:** exact lookup (SQL by ID), semantic search (embeddings), graph traversal (tuples), or full-text. The recall type drives schema and indexing choices, so it's decided here, not discovered during the build.
- **Provenance & retention:** does this data need source-tracking, history, or deletion rules?

### 6. Interconnectivity
What this build talks to, in both directions.
- Systems consumed (reads from) and systems fed (writes to), each with the interface named: which MCP, which API, which table, which repo path.
- The data format crossing each boundary.
- Failure behavior at each boundary: retry, skip, or halt — and **breakage notification** (standing convention: email on breakage for pipelines).

### 7. Access, permissions & hard gates
What the executor may touch and where it stops.
- Exact repos, tables, services, and paths in scope (worker rule 2: touch only named paths).
- Credentials needed and where they live (env vars, MCP auth). Missing credentials are a **gated item**, named before queueing — not discovered mid-build.
- Hard gates restated per-build — and this is the **complete** list: (1) access/credentials only Charles can supply, (2) spending real money, (3) destroying or irreversibly changing data. Nothing else halts a build. Every other fork, ambiguity, or brief-versus-reality conflict is the orchestrator's to decide and log.

### 8. Skills & tools
What the executor loads before working.
- The brief header names required skills (`skills:` line) — the orchestrator fetches them from `agent-library` per its loop step 2.
- Each Directive step names its MCP tool and parameters (existing gate 6, kept).
- If the build requires a tool or skill that doesn't exist yet, building it is either in scope (sequenced first) or a named upstream dependency — never implied.

### 9. Build sequence & dependencies
The order of work and what must exist first.
- Upstream builds this depends on (by plan ID), including what the *verification* consumes, not just what the code consumes.
- Internal sequencing when order matters (schema before code before wiring).
- **Staleness instruction (lesson E-306):** named file scope is a starting point — the executor reads live code/DB state at start and reconciles. If the brief conflicts with live state, the orchestrator resolves the conflict per the design intent narrative and logs the resolution — it does not halt (unless the resolution itself crosses a hard gate).

### 10. Assumptions & risks
- Assumptions: genuinely unverifiable items only, each with what would eventually confirm it. A checkable claim here is a defect (doctrine rule 2).
- Known failure modes and the intended response (retry / degrade / notify).

### 11. Design intent narrative
The paragraph that lets the orchestrator answer forks the way Charles would — because the orchestrator **will** answer them; escalation is not an option outside hard gates. Plain English: why this shape was chosen over the obvious alternatives, which conventions matter, what "good" looks like here, and which qualities to protect when trade-offs appear (e.g., "prefer simple over fast," "never lose provenance"). A thin narrative doesn't stall the build — it just means the orchestrator decides with less of Charles's judgment in hand. Write it like instructions to a competent contractor who cannot call you.

---

## Operational rules (carried from lessons, restated as gates)

- **Fork log is mandatory.** The orchestrator records every fork encountered and the answer it gave (per orchestrate-build step 7). This log is Charles's review surface — he checks the completed build plus the fork log, instead of supervising the build live. A build closed without its fork log is not closed.
- **Durable home:** the brief is committed to the target project's repo at `docs/design/` at authoring (`chat-protocol/briefs/` only when no target repo exists), AND written as a Project State plan on the target project with the git fetch path in its header (E-280 superseded 2026-07-14; E-282 fetch-path rule kept).
- **Confidence labels throughout:** [verified] / [assumed] / [draft] on Inputs and Current State (existing rule, kept).
- **Effort & cost tags:** every scoped component carries S/M/L and real-money cost (doctrine rule 8).

## Replacement completeness gate

The 10-gate checklist in the template is replaced by: gates 1–10 as-is, **plus one new gate 11 — "All eleven domains Answered / Defaulted / N-A — none silent."** The domain table travels in the brief body as a compact status table, so the queue reviewer (and the orchestrator) can see coverage at a glance:

| Domain | State | Where answered |
|---|---|---|
| 1 Purpose & users | Answered | §Scope |
| 2 Acceptance criteria | Answered | §Acceptance |
| 3 Runtime & execution | Defaulted (repo convention) | §Directive |
| … | | |
