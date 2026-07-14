# Handoff Reference block — template

**Purpose:** Step 10 of DA (SKILL.md v0.2.3+) requires a Handoff Reference block on the turn that shelves a Build Brief. This file is the canonical format. Fill every placeholder; omit nothing. Shelving without this block is a session defect.

**Rules:**
- Emit the block exactly in this layout, in chat, after shelving is verified (plan queued + git copy read back).
- `Revision` reflects the Project State plan's `current_revision` at shelving time.
- The pasteable prompt is one blockquote paragraph. Keep the five elements in order: execute instruction, Project State claim instruction (with plan_id / project / status transition), git location, dependency status line (only if the brief has upstream dependencies — state resolved or blocked), and the fork/hard-gate rules line.
- Adapt only bracketed placeholders. Do not restructure, reorder, or drop fields.

---

## Template

---

**HANDOFF REFERENCE — copy into build chat**

**Brief ID:** [BB-YYYY-MM-DD-slug]
**Project State plan:** "[exact plan title]"
**plan_id:** `[uuid]`
**Project slug:** `[project-slug]` · **Status:** `queued` · **Revision:** [N]
**Git copy:** `[owner/repo]` → `[docs/design/BB-....md]`

**Pasteable prompt:**
> Execute Build Brief [BB-ID]. Pull the plan from Project State (plan_id [uuid], project [project-slug], status queued — set it to running when you claim it). Git copy at [owner/repo/docs/design/BB-....md]. [Upstream dependency line if any: "<dependency> is <live and verified | blocked — see <blocker-id>>."] Follow the brief's fork-handling rules: answer forks autonomously with judgment-call tags; escalate only at hard gates ([name the brief's hard gates, or "none in this brief"]). [Any brief-specific routing rule, e.g. "Route all cbrain changes through the brief-review gate."]

---

## Worked example (from BB-2026-07-14-attia-intake, the block this template was locked from)

---

**HANDOFF REFERENCE — copy into build chat**

**Brief ID:** BB-2026-07-14-attia-intake
**Project State plan:** "BB-2026-07-14-attia-intake — Attia → cbrain Intake Loop"
**plan_id:** `4a389c93-65d2-4dea-9cf3-388bb63cd189`
**Project slug:** `health-intake` · **Status:** `queued` · **Revision:** 4
**Git copy:** `Chooch333/cbrain` → `docs/design/BB-2026-07-14-attia-intake.md`

**Pasteable prompt:**
> Execute Build Brief BB-2026-07-14-attia-intake. Pull the plan from Project State (plan_id 4a389c93-65d2-4dea-9cf3-388bb63cd189, project health-intake, status queued — set it to running when you claim it). Git copy at Chooch333/cbrain/docs/design/BB-2026-07-14-attia-intake.md. Upstream dependency subscription-content-mcp is live and verified. Follow the brief's fork-handling rules: answer forks autonomously with judgment-call tags; escalate only at hard gates (the member session credential). Route all cbrain changes through the brief-review gate.

---

## Changelog
- **1.0.0** (2026-07-14) — Initial template, locked from the format Claude produced in the attia-intake scoping chat; Charles approved same day.
