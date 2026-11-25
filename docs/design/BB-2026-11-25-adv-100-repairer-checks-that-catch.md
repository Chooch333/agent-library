# Build Brief — BB-2026-11-25-adv-100-repairer-checks-that-catch

**Plan id:** 1a3ce9bd-0854-4930-9fdd-c5efa888435b (Project State, project cbrain)
**Build:** unnumbered (Stack Advisor)
**Seated:** revision 1, report CB-782, seats oversight
**Overnight:** yes · **target_repo:** Chooch333/agent-library · **after:** none

**What this is:** Two small edits to the Stack Repairer's rules: its fix briefs may add (and must prove) the check that would have caught a recurring problem, and its grades count only records that finished.
**What I'll do:** Edit `skills/stack-repairer/SKILL.md` (0.5.3 → 0.5.4) in three places, add one changelog line, mark two LEDGER rows addressed.
**What you'll do:** Nothing — click Declined on the Stack screen to stop it.

## Current state going in
### Asked for
- ADV-100 (Stack Advisor ADV-2026-11-25): the Repairer's own "Reported problems" rule says an ongoing condition's fix includes a real check on the map, but its Short brief template's Scope says "Out: rules, skills, the stack map". The fingerprint refill brief (plan 48a8c723) obeyed the template and shipped with no check; the Nightly loader light had stayed green through the damage (EB-319). The Video Reader light fix (plan 5ef27f57) already overrode the template (EB-388).
- ADV-101 (same run): grade bb8cfc8e (2026-11-16) turned the rss-feeds fix green by counting "37 OpenAI News items fetched"; 11 had failed with no text (EB-318).
- Checked live: SKILL.md 0.5.3 (sha 18507807) read this run; row bb8cfc8e read this run. Trimmed to the template's Scope, one new template line, one Acceptance line, the Row shape recheck text and one step-2 sentence. Nothing else in the Repairer's limits changes ("Do NOT" list untouched: the Repairer itself still never edits the map).

## Receiving chat
The night runner.

## Scope
In: `skills/stack-repairer/SKILL.md` only — the Short brief template, the Reported problems Row shape `recheck` text, step 2's Reported rows bullet, version, changelog. Out: every other skill, rule and file; the stack map; the Repairer's "Do NOT" list.
**Stack Flow:** no change, because this edits only the Repairer's written rules; no part, timer or check changes.

## Directive
1. In the Short brief template, replace the Scope line with:
   `In: <the fix>; for an ongoing condition, also the check on the stack map that would have caught it (the dot's check block, with its threshold in the map, and its side-panel text). Out: rules, skills, other dots; anything past the failing dot.`
2. In the template, directly under the Scope line, add:
   `**Stack Flow:** <the check added or changed> | no change, because <why>.`
3. In the template's Acceptance, add a line:
   `<n>. For an ongoing condition: the new check turns red on the failing state and green once fixed, proved in <the place this brief names where the checker can be run>.`
4. In "Reported problems" → Row shape, change the `recheck` text to:
   `"recheck": "<a check anyone can run that passes once it is fixed; a count counts only records in their finished state (saved, filed, in the graph), never ones only fetched or tried>"`
5. In step 2, Reported rows bullet, after "is graded by running that recheck, not by its dot", add:
   `Run the recheck as written and put the query and what it returned in detail.evidence; a count that includes records only fetched or tried does not pass.`
6. Bump version to 0.5.4, `updated: 2026-11-26`, and add a changelog line naming this brief, ADV-100, ADV-101, report CB-782, and that it is a skill edit allowed by this brief.
7. Read the file back and confirm only these lines changed (diff against 0.5.3).
8. In cbrain `docs/advisor/LEDGER.md`, mark rows ADV-100 and ADV-101 `addressed` ("done for you — built 2026-11-26, BB-2026-11-25-adv-100-repairer-checks-that-catch"). Edit only those two rows.

## Acceptance
1. SKILL.md on agent-library main reads version 0.5.4 and contains the five new or changed lines exactly; the diff against 0.5.3 shows nothing else apart from version, date and changelog.
2. LEDGER rows ADV-100 and ADV-101 read `addressed`; no other row changed.

## Pasteable prompt
> Execute Build Brief BB-2026-11-25-adv-100-repairer-checks-that-catch. Pull the plan from Project State (project cbrain). Answer forks yourself; stop only at hard gates. Standing rules CB-185, CB-121, CB-103 apply.
