---
name: team-builder
version: 0.3.1
status: draft
triggers: ["Loaded by the Expert Desk at grow step G3 (expert mode)", "Loaded by the Expert Desk at team grow step T4 (team mode)", "Loaded by a build chat when its Build Brief names a new skill under Skills: (skill mode)", "Loaded by the Expert Desk's CE job at its Catch-up and fold step, the Sunday 01:00 firing of the scheduled task \"Expert CE\", pointed at the waiting lens-notes on expert-bench (update mode)"]
dependencies: []
owner: Charles
updated: 2026-11-04
requires: [references/expert-brief.md, CONVENTIONS.md, references/chat-capture.md, references/thread-checkin.md]
wiring:
  runs: with-you
  starts: "called by the Expert Desk (grow, team grow, or its Expert CE job) or by a build chat; never by a trigger phrase"
  runs_in: claude-chat
  reads: [the approved spec, agent-library experts, CONVENTIONS, SKILL_TEMPLATE, "waiting lens-notes on expert-bench (update mode)"]
  writes: ["experts/<slug>/BRIEF.md (new, active)", "the captain's BRIEF.md (revisions the spec names)", "experts/INDEX.md (one row)", "skills/expert-desk/profiles/<domain>.md (a new captain's row, or a new card marked ~; for a team, a reused captain's row)", "a reused captain's profiles: line (team mode)", "skills/<slug>/SKILL.md (new, draft)", "AGENT.md (one routing row)", "an existing experts/<slug>/BRIEF.md: Lens lines, version, changelog (update mode)", "lens-note tags: folded, folded-<sha7>, routed (update mode)", "Comms Table posts on expert-bench (update mode)", "Next steps cards, kind job (update mode)", "Archivist drafts: cbrain _briefs/BR-DRAFT-<date>-<suffix>.md (update mode)"]
  stack: []
  origin: yours
  label: Team Builder
---

# Team Builder

## What
The one skill that puts a new member on the team: an expert's brief or a skill's SKILL.md.
It takes an approved spec, writes the file to its format, runs the mechanical checks,
registers it, commits it (an expert as active, a skill as draft) and reads it back. It judges nothing: whether the
expert or skill should exist was settled before it is called (the Roster Builder and
Charles's confirmation for an expert; a Build Brief for a skill). Experts judge, skills
execute (TH-135); this is the execution half of growing the team. In update mode it
also keeps the team current: it folds waiting lens-notes into existing briefs by
mechanical rules, in a scheduled run with nobody present, and routes what it may not
write to the Archivist or to Charles.

## When
**Fire when:** the Expert Desk reaches grow step G3 with an `expert-draft` note
(expert mode); the Expert Desk reaches team grow step T4 with a team note, its draft
notes and a fit note (team mode); a build chat is executing a Build Brief whose `Skills:` header or
scope names a new skill (skill mode); or the Expert Desk's CE job reaches its Catch-up
and fold step (the Sunday 01:00 firing of the scheduled task "Expert CE") with lens-notes
waiting on `expert-bench` (update mode).
**Don't fire when:** deciding whether an expert is needed (the Roster Builder); editing
an existing skill's rules (an ordinary build under the Execute row); the content is a
Project State note, a cbrain entity or anything that is not a brief or a SKILL.md
(update mode only drafts a cbrain brief; the Archivist files it after Charles approves).

## How
| Step | Precondition | Action | Evidence | Recovery |
|---|---|---|---|---|
| 1 Read | the spec: expert mode, the `expert-draft` note (brief text + the captain's revisions); skill mode, the Build Brief section | Read the spec whole, `references/expert-brief.md` or `SKILL_TEMPLATE.md` + CONVENTIONS, and the captain's brief (expert mode). | Spec id; files read | No spec, or a spec with no name or no body: stop and say what is missing. Never invent content. |
| 2 Write | spec read | Expert: write `experts/<slug>/BRIEF.md` from the spec in the brief format, `status: active`, changelog line; apply the captain's revisions to the captain's brief (version bump, changelog line). Skill: write `skills/<slug>/SKILL.md` from the template, `status: draft`. Draft locally first; nothing committed yet. | Draft files | A field the spec does not supply: leave it blank and list it in the receipt; never fill it from memory. |
| 3 Check | drafts written | Run the mechanical checks for the mode (below). | Check list with pass/fail per line | Any FAIL: stop, report the failing lines to the caller, commit nothing. Never fix a FAIL silently; the Roster Builder or the Build Brief supplies the fix. |
| 4 Register | checks pass | Expert: add the row to `experts/INDEX.md` (level, under, call_when copied word for word, status active; replace a stub row if one exists). A captain: add it to `captains_default` of the profile card its brief names under `profiles:`; if no card of that name exists, write `skills/expert-desk/profiles/<name>.md` from `profiles/harness.md`'s shape, with the "Done means" and severity lines drawn from the spec and marked ~ for Charles to refine on first use. A craft never touches a card. Skill: add the AGENT.md routing row the Build Brief gives, and a CHANGELOG.md line. | Row text | Name collides with an existing row: stop and report. |
| 5 Commit | registered | One commit per file, each message naming the build or desk run. | Commit SHAs | A commit fails: retry once, then stop and report what landed. |
| 6 Read back | committed | Fetch every written file from main and compare to the drafts. | "read back: identical" per file | A mismatch: report it; do not re-commit without saying so. |
| 7 Receipt | read back | Return to the caller: files written, SHAs, index or routing row, any blank fields, check results. | Receipt | — |

### Update mode
Loaded by the Expert Desk's CE job at its Catch-up and fold step (the Sunday 01:00
firing of "Expert CE"), pointed at the waiting lens-notes on `expert-bench`. Nobody is
present: nothing here asks a question or waits on an approval, and every outcome is a
commit, a tag, a post, a card, a draft or a receipt line. Team Builder still judges
nothing about whether an expert should exist; it sorts each note by the rules below and
writes only what the sort allows. Steps 1 to 7 above do not apply; these rules do.

**Rules**
1. **Waiting** = a note on `expert-bench` whose tags hold `lens-note` and one `expert-<slug>`, and neither `folded` nor `routed`. `find_by_tags` expands tags fuzzily: keep only rows whose own tags match exactly. A note with no `expert-` tag, with two, or whose slug has no `experts/<slug>/BRIEF.md` (or only a stub row) is left waiting and listed in the receipt.
2. **Never** edit an Our way line, or a line whose source is Charles's own record, except by sort (e) Proved. Never edit the header (except `version`) or any section but Our way, Lens and Changelog. Never write a figure into a brief. Never write an Our way line without its origin mark (`references/expert-brief.md`). Never change a note's text or delete it; tags are the only write to a note. Never seal or file a cbrain brief.
3. **Sort each note.** Check in this order, (a), (e), (c), (b), (d); the first that fits wins, so a proved change folds even when it touches an Our way line or carries a tool fact, and an unproved Our way change reaches Charles before its tool fact is drafted.
   - **(a) Already folded:** the note's display id (EB-xxx) is in that brief's Changelog. Find the commit that folded it: `list_commits` on main (up to the last hundred), the newest message with "Expert CE fold" and that id. Add tags `folded` and `folded-<first seven characters of its SHA>`; no such commit → `folded` alone, listed in the receipt. Write nothing else.
   - **(e) Proved:** the note's change rests on a record newer than the line it changes: a Charles decision or dated statement, a shipped build (plan succeeded), a test, a stack fix log row (`stack_repairs`), or a file read cited in the note. Confirm the record in this run: `search_state` or a Project State read for a decision, lesson, note or plan (plans: status succeeded); a cbrain read for a `stack_repairs` row; `get_file_contents` for a cited file. Confirmed → fold it in place (rule 4): rewrite the Our way or Lens line the note names, or add the line it proposes, cite the record in its bracket, and set an Our way line's origin mark from the record (a Charles decision or dated statement → `Charles ·`; a build, test, stack fix log row, judgment call or file read → `Claude ·`; an outside default → `field ·`; the line keeps a higher mark it already had from sources that still stand). Changelog `folded EB-… (proved: <record>)`. A record that cannot be found, is older than the line, or says something else → not (e); sort on.
   - **(c) For Charles:** only two cases. Two of Charles's decisions clash (the note's record and the line's source are both his and say different things); or a new opinion with no record behind it would change or add an Our way line. Never edited here. A new opinion that reads as a risk (how work in the corner goes wrong), not a practice, is not (c): it lands as a ~ Lens line under (d), and reaches Charles only when a design wants to adopt it as Our way (as EB-059 did). First `list_judgment_calls` on `expert-bench`; a post already naming this display id → only tag. Otherwise `post_judgment_call` on `expert-bench` (plan_id: the plan the CE job passes, else the Build 68 brief `0e08817e-5ff9-4e63-a3cf-72d96c572ed7`), title "Expert CE: <expert> — <the line, by what it covers>", `action_needed: needs-charles`, `plain_summary` one plain sentence naming the expert, the line and what the note says should change, context with the display id, the note's text, the line quoted and the brief's path (and, if the note also carries a tool fact, that it does: its capture is drafted in a chat with Charles after he answers, not here). Then the Next steps card (rule 5). Then tag `routed`.
   - **(b) A tool fact:** the note says how a tool, service or connector behaves (what it exposes, accepts, refuses or returns), not how work in the corner goes wrong. Tool facts live in cbrain `concepts/`, never in a brief (expert-brief.md). Draft one capture brief for this note per `references/chat-capture.md`, type `concept`: check `concepts/` for the slug (exists → `enrich_field`, else `create_entity`); intents only, no `observations`; no questions asked: a field the note does not supply stays blank and is named in the body, and follow-on entities or new predicates are listed in the body for Charles, never added as intents. File it on cbrain main as `_briefs/BR-DRAFT-<YYYY-MM-DD>-<four random hex>.md` (path taken → new suffix) with `status: draft`, `created`, `producer: team-builder`, `source: { kind: lens-note, ref: <note id>, catalyst: "Expert CE, <slug>", received_at: <note created_at>, detail: { subject: "Expert CE tool fact for <expert>: <one line>", display_id: <EB-xxx> } }`, `intents`. The Archivist files only after Charles approves (AGENT.md): the Stack Inspector's approval-gate check lists the draft, and a later chat seals it with `seal_brief` and that file name. Tag the note `routed`.
   - **(d) A Lens line:** everything else. One Lens line in that expert's brief: the claim in one line, no digits outside a date or an ID, starting `~ ` when the note says Inferred, ending with the note's display id in brackets (the note's own sources may precede it inside them). A note that corrects a named Lens line whose source is not Charles's record rewrites that line in place, keeping its number and sources and adding the display id.
4. **Writing a brief** (all (e) and (d) notes for one expert together):
   - Read `experts/<slug>/BRIEF.md` from main and keep its blob sha. Build the new file from that text: the Our way and Lens lines folded, added or rewritten, `version` patch-bumped, one Changelog line `- <version> (<date>): folded EB-… (proved: <record>), EB-… (Expert CE)`; nothing else changes.
   - Run the expert-mode Our way and Lens checks on the result. Our way: every line ends with a source in brackets that starts with its origin mark (`Charles ·`, `Claude ·` or `field ·`), and no `~ field default` remains; a line without a mark is a FAIL, even one this run did not touch. Lens: at least ten lines (no upper limit), each ending with a source in brackets, no digits outside dates or IDs, no more than three lines shared with any other brief on the bench. A FAIL → commit nothing for that brief, leave its notes waiting, list the failing lines in the receipt.
   - Commit with one whole-file `create_or_update_file` on main through the GitHub connector, keyed on the blob sha just read; message "Expert CE fold: <slug> — EB-…, EB-…". One commit per brief.
   - A conflict (409, sha mismatch): re-read the file, layer this run's changes on top of what is there now (bump from the version now there; a note now named in its Changelog becomes (a)), rerun the checks, retry once more. Still failing → stop that brief, leave its notes waiting, list it in the receipt.
   - Fetch the brief from main and compare it to what was sent. Identical → tag each folded note `folded` and `folded-<sha7>`. A mismatch → no tags, its notes stay waiting, the receipt says so; never re-commit without saying so.
5. **Next steps card** (every (c)): one `checkin` per expert per run, kind `job`, `source: job`, thread_key `job:team-builder-ce-<slug>`, plain_name "<expert> brief changes to decide", waiting_on `you`, next_step in plain words with no ids: what the expert's brief would change and that the ask is on the Comms Table. Two notes for one expert in a run share one next_step naming both.
6. **Receipt** to the caller, per expert: notes folded as proved (display ids, the record each rests on, commit SHA), notes folded as Lens lines (display ids and commit SHA), routed to the Archivist (display ids and draft file names), routed to Charles (display ids and post ids), left waiting and why (no brief, a check FAIL with its lines, a conflict, a read-back mismatch). Plus any note with no expert or two.

### Team mode
Expert mode, once per expert, in the team note's build order: captains before their crafts.
- **Read** the team note, every draft note and the fit note. Apply the fit's cuts and rewordings to each draft before step 2.
- **Captain revisions** come from the fit note's merged set, not the drafts. Apply to a captain only the lines tagged with crafts that passed their checks; lines for a craft that stopped are left out and listed in the receipt.
- **Refresh rows** (an expert on the bench rewritten whole to the current brief format): overwrite its BRIEF.md, keep its name, bump its version, add a changelog line; update its index row only if call_when changed; skip the overlap check against its own old brief.
- **Overlap check** runs as each expert lands, so later teammates are checked against earlier ones as well as the bench.
- **A FAIL** stops that expert and every craft under it in this team; commit nothing for them; carry on with the rest. Never fix a FAIL silently.
- **Profile card.** New captains: step 4 as usual. A captain marked *on the bench* that the team note places on a card: add the card to its `profiles:` line (version bump, changelog line) and to the card's `captains_default`, unless that would put the defaults past the card's `max_seats`; then leave both and list it in the receipt.
- **Receipt:** one table for the team: expert, landed or stopped (with the failing lines), SHAs, index row, captain lines left out, card changes.

### Mechanical checks, expert mode
- Header: all nine fields; `under` empty only for a captain; `status: active`.
- Our way: a craft has at least 5 lines, a captain 0 or more, with no upper limit (never merge or cut a sourced line for length); most important first; each line names a job, how we do it, and ends with a source in brackets that starts with its origin mark, `Charles ·`, `Claude ·` or `field ·` (`references/expert-brief.md`; several sources take the highest, Charles then Claude then field; unclear is Claude, never Charles by guess); a line without a mark, or still marked `~ field default`, is a FAIL; no digits outside a date or an ID; no client, job or employer names (the repo is public).
- Lens: at least 10 lines, no upper limit; every line ends with a source in brackets; no digits outside a date or an ID (the claim and the pointer, never the figure); an uncertain line marked ~.
- Every path under `reads` exists (fetch each one).
- No more than three lens lines shared with any brief on the bench (word-overlap, then eyeball the hits).
- `call_when` present and one line; the index row matches it word for word.
- The name is not a locked word in CONVENTIONS and not an existing expert's name.
- The captain's revisions (lines moved, call_when changes) are applied, with its version bumped and a changelog line.

### Mechanical checks, skill mode
- Seven contract fields; seven body sections in order; a `wiring:` block.
- Every pitfall carries a trace in brackets.
- Under 500 lines; rules at the top (a skill is read once and only its first 5,000 tokens return after compaction [TH-134 line 15]).
- The name is not a locked word and not an existing skill's name.
- The AGENT.md row the Build Brief gives is present; `description` is present if the surface routes on it [TH-134 line 13].

## Progress tracking
Expert, team and skill mode: none; they finish in one run inside the calling chat and the receipt goes back to the caller.
Update mode follows `references/thread-checkin.md` (naming convention and when to check in).
- kind: job
- build: the expert's name + "brief changes to decide", e.g. "lanes brief changes to decide" (thread_key "job:team-builder-ce-<slug>", `source` "job")
- Opens when: a run routes a note to Charles (rule 3 (c), or a full Lens)
- Checks in: when a run leaves something open (rule 5; waiting_on `you`)
- Closes when: Charles clicks Done. A CE run never closes or reopens the card.

## Examples
Expert mode: the Expert Desk's first grow run under this skill (none yet; the dry runs of 2026-11-02 were written by hand). Skill mode: the next Build Brief that names a new skill.

Update mode, a dry sort of the four notes waiting on 2026-11-04 (no run has happened yet): EB-017 (intake: a second half of an Our way line superseded by Charles's "Yes sources"), EB-018 (c-stack: a candidate Our way line from Charles's own words), EB-019 (lanes: an Our way line and a Lens line said wrong, with a suggested line) and EB-020 (lanes: an Our way line that cannot be done from a chat, plus how the scheduled-task tools behave) all sort to (c): four Comms Table posts, needs-charles; three Next steps cards (intake, c-stack, and one for lanes naming both its notes); each note tagged `routed`; no brief is committed. EB-020's tool fact is named in its post, not drafted, because (c) is checked before (b).

## Pitfalls
- A check run on a Project State note instead of the committed file has no receipt; "every reads path exists" was never really fetched. Check the file you wrote, then read it back from main. [TH-139]
- Two briefs seeded by one chat on one day shared six lens lines; the overlap check is against every brief on the bench, not the ones that come to mind. [TH-139]
- Figures in lens lines went stale within a day; keep the pointer, drop the number. [TH-139]
- A proposal carried as chat text or an attachment was lost between chats; the spec is a Project State note or a Build Brief, never a message. [dry run 1, 2026-11-02]
- Teammates researched in parallel each wrote revisions for the same captain; the fit note merges them once, and only lines for crafts that landed are applied. [Build 65]
- The check job once lived in an expert's brief and the expert seated to run it had never seen it; mechanical checks live here, in the skill that writes. [TH-J-045 follow-up, Build 64]
- A scheduled run cannot answer an approval prompt: the first live Stack Repairer run's edits hung and saved nothing, most likely waiting on a confirmation nobody could give. Nothing in update mode waits on a question; every outcome is a write or a receipt line. [stack-repairer 0.2.0 changelog, 2026-10-07]
- Two runs can write one brief (a rerun of the 01:00 job, or a chat folding by hand the same night). The write is whole-file and keyed on the blob sha just read; a 409 means re-read and layer this run's change on top, never overwrite what the other run wrote. [BB-2026-11-03-expert-ce, directive 3]
- The first four waiting lens-notes all asked to change Our way lines, which are Charles's own record, not Lens lines a run may write on its own; Our way changes go to Charles, every time. [EB-017 to EB-020, 2026-11-03]

## Changelog
- **0.3.1** (2026-11-04): no upper limit in the expert-mode checks (Our way at least 5 for a craft, Lens at least 10) or in update mode's Lens check; the full-Lens route to Charles (needs-design-check) and its Next steps card are gone. Lines most important first; never merge or cut a sourced line for length. Charles 2026-11-04, bench-wide (expert-brief 0.4.0).
- **0.3.0** (2026-11-04): update mode, loaded by the Expert Desk's CE job at Catch-up and fold (Sunday 01:00, scheduled task "Expert CE"), safe with nobody present: each waiting lens-note is sorted (already folded → tags only; touches Our way or a Charles-sourced line → Comms Table needs-charles plus a Next steps card; a tool fact → a draft cbrain capture brief for the Archivist in `_briefs/`; else one Lens line, or needs-design-check when the Lens is full); whole-file sha-keyed writes with re-read-and-layer on a 409, Lens checks before commit, read-back, then `folded` + `folded-<sha7>` tags; one receipt per expert (Build 68, BB-2026-11-03-expert-ce).
- **0.2.1** (2026-11-03): Our way check (expert-brief 0.2.0); team mode writes *refresh* rows, so an expert already on the bench can be rewritten to the new format inside a team grow. Charles: craft experts must know how things ought to go in their corner.
- **0.2.0** (2026-11-03): team mode, loaded at the Expert Desk's team grow step T4: captains first, the fit note's cuts and merged captain revisions applied, a failed expert stops only itself and its crafts, a reused captain joins the team's profile card within max seats, one team receipt (Build 65, BB-2026-11-03-team-grow).
- **0.1.0** (2026-11-03): first version (Build 64, BB-2026-11-03-team-builder).
