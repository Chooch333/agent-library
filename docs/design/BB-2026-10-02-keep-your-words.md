# Build Brief — BB-2026-10-02-keep-your-words

**Git home:** Chooch333/agent-library · `docs/design/BB-2026-10-02-keep-your-words.md`
**Project State plan:** none — executed inline in a Design Assist chat at Charles's direction (same pattern as ADV-009 / decision C-070); recorded via a Session Log and Decision on `chat-protocol`.
**Build:** unnumbered

**What this is:** Every Build Brief keeps a short, word-for-word record of what was asked and by whom, frozen at the top; later changes are added as dated lines. Adopts ADV-033 narrower.

**What I'll do:** Edit three Design Assist files in agent-library, read each back, update ADV-033's LEDGER row, close with a Session Log.

**What you'll do:** Nothing. The next brief any DA chat shows Charles should open with his own words.

## Current state going in

**Asked for — in Charles's words** *(frozen; never reworded)*
> "Scope ADV-033 from the Stack Advisor into a build brief: Interview the idea's originator before writing a brief." — Charles, 2026-10-02

> "Before a build brief gets written, have the AI interview whoever raised the idea until it genuinely understands it, and write that understanding down first." — Stack Advisor, ADV-033, 2026-09-18 · Charles: Scope it

- 2026-10-02 Charles approved: "approve recommendations for all 3 items" (goal as restated; adopt narrower; execute inline).

- [verified] The interview already existed: design-assist SKILL.md v0.2.15 steps 1–2 (verbatim intake, restate until it lands) and template gate 1 (Charles confirmed).
- [verified] The written-intent part already existed: framework domain 11 (design intent narrative), [Charles]/[Claude-per-doctrine] decision markers, plan revision history.
- [verified] The gap: the raw ask lived in the working appendix, which collapses at build-ready; finished briefs (e.g. BB-2026-09-24-stack-interested-stays) carried only the DA's intent paragraph.
- [verified] orchestrate-build v1.4 step 5 decides forks "using the brief's intent" — no edit needed there.
- [assumed] No logged case of a build going wrong from lost intent (one cross-project lesson search); the fix is insurance, kept small.

## Receiving chat
Executed inline by the scoping DA chat, 2026-10-02.

## Scope
**In scope:** "Asked for" block in the brief template + gate 1 wording (S); DA skill steps 1–2 (S); framework domain 11 (S); LEDGER ADV-033 → addressed (S). Cost $0.

**Out of scope:** a separate intent file (duplicates the brief); a new interview step or questionnaire (the Restate loop is the interview); PROTOCOL.md's template (block sits inside an existing field); orchestrate-build (already reads the brief's intent); rewriting old briefs; revision tracking (already handled).

## Directive (as executed)
1. `roles/design-assist/references/build-brief-template.md` — gate 1 wording (commit 08bac60); "Asked for" block as first item of Current state going in (commit c8dc899).
2. `roles/design-assist/references/brief-completeness-framework.md` — domain 11: the block wins over the narrative (commit ed65b70).
3. `roles/design-assist/SKILL.md` — step 1 (2c61764), step 2 (c31d476), v0.2.16 (91577f7), changelog (81173bc).
4. Read back all three files — only the named lines changed.
5. `Chooch333/cbrain` `docs/advisor/LEDGER.md` ADV-033 → `addressed`.

## Acceptance criteria
1. Template shows the "Asked for" block first under Current state going in, and the new gate 1 wording. — met (read back)
2. SKILL.md is v0.2.16 with the step 1 and step 2 text and a changelog line. — met (read back)
3. Framework domain 11 contains the "block wins" sentence. — met (read back)
4. No other lines in the three files changed. — met (read back)
5. LEDGER ADV-033 reads `addressed` with the actual response.

## Design intent
The cheapest version of Anthropic's intent.md idea that fits a one-person shop. Charles is both the person with the idea and the person who approves it, so a separate file and a second sign-off add nothing. Protect: no new step for Charles, no new file to keep in sync.

## Decisions
- [Charles] Goal: every brief carries his own words for what he asked, without an interview step or work for him.
- [Charles] Adopt narrower — keep-your-words block, no intent file, no new step.
- [Charles] Execute inline rather than shelve for a build chat.
- [Claude-per-doctrine] Block lives inside the existing "Current state going in" field rather than a new PROTOCOL.md field — smallest blast radius.
