# Build Brief — BB-2026-11-09-expert-fold-rule
**Git home:** Chooch333/agent-library · `docs/design/BB-2026-11-09-expert-fold-rule.md`
**Project State plan:** `0ad994c3-51c2-4802-bcfa-cb1bad4d444d` on `expert-bench`

**What this is:** Build 77. Take Charles out of the Sunday expert update. A change backed by his own later decision, or by something a build or test proved, goes straight into the expert's brief and cites its proof. Every Our way line gets an origin mark, Charles, Claude or field, so it is always clear whose rule a line is.
**Stack Flow:** no change — Team Builder still runs inside the Sunday Expert CE run.
**Step map:** no change — no workflow is added or changed.
**Skills:** orchestrate-build. **After:** none. **Target repo:** Chooch333/agent-library.

**What I'll do (build chat):** change Team Builder's sorting rule, add the origin mark to the brief format and its check, mark every Our way line on the bench.
**What you'll do:** nothing.

## Asked for — Charles, 2026-11-09 (frozen)
"Take him out of the weekly expert update: yes. A line overtaken by his own later decision, or by a fact a build or test proved, is updated and cites it. Only a new opinion or a clash between two of his decisions reaches him." (TH-155.) "Fix the Sunday expert update so I'm out of it, add the origin mark, and clear EB-J-009 to EB-J-025 under the new rule."

## Current state going in (verified 2026-11-09)
- Team Builder update mode sends every note that touches an Our way line to Charles (rule 3c). That put 17 posts on his desk (EB-J-009 to EB-J-025).
- **Done in the design chat, not by this build:** all 17 cleared under the new rule. 16 folded with their proof cited; EB-059 (an outside talk idea with no record behind it) landed as a ~ Lens line, not an Our way line. One commit, 979d646, eight briefs; notes tagged `folded`, `folded-979d646`; posts disposed; eight Next steps cards closed.
- Today's brief format marks only `~ field default`; nothing says whether a line is Charles's or Claude's.

## Scope
**In:** `skills/team-builder/SKILL.md` 0.4.0 (update mode rules 3 and 4, mechanical checks); `references/expert-brief.md` 0.5.0 (origin mark); every active `experts/*/BRIEF.md` (marks only, version patch bump, changelog line).
**Out:** anchor sources per expert (decided, separate build); the experts' outside reading and the $0 web-search rule (open); the cbrain Experts view.

## Directive
1. **New sort (e) Proved**, checked before (c). The note's change rests on a record newer than the line: a Charles decision or dated statement, a shipped build, a test, a stack fix log row, or a file read cited in the note. The run confirms the record (`search_state`, `get_file_contents`). Then fold it in place in Our way or Lens, cite the record, set the line's origin from it, bump the version, changelog `folded EB-… (proved: <record>)`.
2. **(c) For Charles narrows** to: two of his decisions clash; or a new opinion with no record would change an Our way line. A new opinion that reads as a risk, not a practice, lands as a ~ Lens line instead and reaches him only when a design wants to adopt it (as EB-059 did).
3. **Origin mark.** Every Our way line's bracket starts with its origin: `[Charles · …]` (his words with a date, the charter, a decision or lesson he made or approved), `[Claude · …]` (a build's or chat's judgment call, a lesson Claude wrote, a file read), `[field · …]` (an outside default; replaces `~ field default`). Several sources: Charles beats Claude beats field. Unclear: Claude, never Charles by guess (Charles is never recorded as the author of AI inference).
4. **Mark the bench.** One pass over every active brief: mark each Our way line from its existing sources.
5. **Mechanical check.** Expert mode and update mode both refuse an Our way line without a mark.
6. **Dry sort** the 17 historical notes under the new rules and compare with the design chat's handling.

## Acceptance criteria
1. Team Builder 0.4.0 and expert-brief 0.5.0 on main, read back identical.
2. A script over `experts/*/BRIEF.md` finds no Our way line without a mark.
3. The dry sort matches the design chat: 16 proved, EB-059 to a Lens line, none to Charles.

## Cost
Subscription only.

## Decisions
- [Charles] The fold rule itself (TH-155).
- [Claude-per-doctrine] The mark reuses each line's existing source bracket, not a new field (c-stack seat).
- [Claude-per-doctrine] An outside idea with no record goes to the Lens, not to Charles, unless it would change how we do things. Pushback from the c-stack seat noted: it wanted Charles-sourced lines to move only on a newer Charles decision; his own rule also allows a proved fact, so his rule stands.

## Pasteable prompt
> Build 77 — execute Build Brief BB-2026-11-09-expert-fold-rule. Pull the plan from Project State (plan_id 0ad994c3-51c2-4802-bcfa-cb1bad4d444d, project expert-bench). Answer forks yourself; stop only at hard gates.
