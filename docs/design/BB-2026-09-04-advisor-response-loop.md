# Build Brief — BB-2026-09-04-advisor-response-loop

**Git home:** Chooch333/agent-library · `docs/design/BB-2026-09-04-advisor-response-loop.md`
**Project State plan:** `{PLAN_ID}` on `stack-map`

**What this is:** Build the response-loop mechanism that gives every Stack Advisor idea a visible disposition plus a required response — written at scoping (the Build Brief / DA chat) and again at landing (the Build Chat) — so the advisor reads a real, closed answer instead of inferring adoption from a `building` status. ADV-010's build (BB #1) is this mechanism's first live test case.

**What I'll do:** Add an `addressed` terminal state and a Response line to the advisor LEDGER; add a response requirement to the DA skill (at scoping) and to PROTOCOL.md + the advisor skill (at landing and at suppression). Verify each file edit by reading it back.

**What you'll do:** Nothing — autonomous execution. Documentation and skill-file edits only; no hard gate.

---

## Current state going in

The Stack Advisor emails ideas as `ADV-NNN`, tracked in `cbrain/docs/advisor/LEDGER.md` (human-facing disposition: `surfaced → interested → building → declined`) and `pool.json` (its private ranked memory). The DA skill (v0.2.9) already requires, at handoff, that an advisor-origin Build Brief carry `ADV-NNN` in the plan's tags + provenance and flip the ledger row to `building`. The advisor's suppression rule reads three signals to avoid re-surfacing an adopted idea: ledger row `building`/`declined`; a plan/decision citing the ADV ID; or the change already being live in the named component.

**The gap:** all three suppression signals are *inferred by the advisor*, never *confirmed by the work*. There is no closing response ("done, here's how"), no terminal `addressed` state (a build that ships leaves the idea at `building` forever), and no way to record "addressed differently" (partial adoption, solved-better, already-covered, declined-with-reason). Live evidence: **ADV-004 has resurfaced twice and still shows `surfaced`** even though a partial fix shipped this week — precisely because nothing closed the loop with a readable response.

**Fork resolved (Charles, this session):** the `addressed` state and Response text live in the **LEDGER**, not on a Project State plan field — disposition already lives there and it keeps the advisor's memory in one home.

## Receiving chat

New build chat.

## Scope

**In scope — four coordinated edits:**

1. **LEDGER convention** (`cbrain/docs/advisor/LEDGER.md`): extend the status vocabulary to `surfaced → interested → building → addressed | declined`, and add a **Response** column (short free-text: what was done, appropriate to the comment, not lengthy). Update the header legend that defines the status values. `building` becomes a way-station, not a terminus.

2. **DA skill — scoping hook** (`roles/design-assist/SKILL.md`, Step 10, the advisor-origin provenance rule): add that when flipping the ledger row to `building`, the DA chat also writes a one-line **intended response** into the Response field — one of the four shapes: *adopting as asked* / *adopting narrower (say what)* / *already covered by X* / *declining because Y*.

3. **PROTOCOL.md — landing hook** (Build Brief rules / return contract): add one line — a Build Chat executing an advisor-origin brief closes by writing the **actual response** (what really landed, if different) and setting the ledger row to `addressed`. This is part of "done," and it rides the existing external-review gate: a self-certified response is a build defect caught the same way a self-certified review is.

4. **Advisor skill — suppression + resurface reading** (advisor's SKILL.md suppression rule): add signal (4) — ledger row `addressed` is authoritative adoption, never resurface; and instruct the advisor to *read the Response* when weighing whether a resurfaced theme was genuinely handled (the check that would have stopped ADV-004).

**Out of scope:** How the advisor scores or selects ideas. ADV-004's actual content fix (a separate idea). Auto-emailing the advisor a reply — the LEDGER *is* the reply; the design principle is "don't make Charles the relay." Any Project State schema change (Fork 1 chose the LEDGER, so no plan field is added).

## Directive

Make the four edits above. For each: `get_file_contents` live first, use `replace_in_file` against a unique anchor (or `create_or_update_file` where a section is added), then read back to confirm. Where a worked example helps a future chat copy the pattern, include one one-liner per response shape (adopted / partial / already-covered / declined) in the DA skill so wording is copied, not reinvented. Bump each skill file's version and changelog per its existing convention.

## Inputs

- `cbrain/docs/advisor/LEDGER.md` — status legend + rows.
- `Chooch333/agent-library/roles/design-assist/SKILL.md` — Step 10 advisor-origin provenance rule (v0.2.9).
- `Chooch333/chat-protocol/PROTOCOL.md` — Build Brief rules / return contract.
- The advisor's own SKILL.md (agent-library `roles/`), suppression rule — the "Already acted on — never again" block.
- Reference incident: ADV-004's double resurface (the failure this closes).

## Acceptance criteria

- ADV-010 ends showing ledger status `addressed`, Response "Added the SQL-fallback paragraph to PROTOCOL.md standing rules," responding-BB recorded. (BB #1 performs the write; this brief makes the mechanism BB #1 uses exist.)
- The advisor's next run reads ADV-010 as `addressed` and does not re-surface it.
- Each of the four response shapes has a worked one-liner in the DA skill.
- All four files read back with the intended edits and bumped changelogs.

## Response requirement (this brief is itself advisor-adjacent, not advisor-origin)

BB #2 is a Charles-directed mechanism build, not itself an ADV idea, so it carries no ADV response of its own. It is the thing that *creates* the response requirement.

## Pasteable prompt

> Execute build brief BB-2026-09-04-advisor-response-loop. Fetch it from `Chooch333/agent-library/docs/design/BB-2026-09-04-advisor-response-loop.md` and follow it exactly. Reconcile against current Project State and read each target file live before editing. Close with your own Session Log on `stack-map` referencing the brief ID.
