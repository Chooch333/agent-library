---
name: team-builder
version: 0.2.0
status: draft
triggers: ["Loaded by the Expert Desk at grow step G3 (expert mode)", "Loaded by the Expert Desk at team grow step T4 (team mode)", "Loaded by a build chat when its Build Brief names a new skill under Skills: (skill mode)"]
dependencies: []
owner: Charles
updated: 2026-11-03
requires: [references/expert-brief.md, CONVENTIONS.md]
wiring:
  runs: with-you
  starts: "called by the Expert Desk or by a build chat; never by a trigger phrase"
  runs_in: claude-chat
  reads: [the approved spec, agent-library experts, CONVENTIONS, SKILL_TEMPLATE]
  writes: ["experts/<slug>/BRIEF.md (new, draft)", "the captain's BRIEF.md (revisions the spec names)", "experts/INDEX.md (one row)", "skills/expert-desk/profiles/<domain>.md (a new captain's row, or a new card marked ~; for a team, a reused captain's row)", "a reused captain's profiles: line (team mode)", "skills/<slug>/SKILL.md (new, draft)", "AGENT.md (one routing row)"]
  stack: []
  origin: yours
  label: Team Builder
---

# Team Builder

## What
The one skill that puts a new member on the team: an expert's brief or a skill's SKILL.md.
It takes an approved spec, writes the file to its format, runs the mechanical checks,
registers it, commits it as draft and reads it back. It judges nothing: whether the
expert or skill should exist was settled before it is called (the Roster Builder and
Charles's confirmation for an expert; a Build Brief for a skill). Experts judge, skills
execute (TH-135); this is the execution half of growing the team.

## When
**Fire when:** the Expert Desk reaches grow step G3 with an `expert-draft` note
(expert mode); the Expert Desk reaches team grow step T4 with a team note, its draft
notes and a fit note (team mode); or a build chat is executing a Build Brief whose `Skills:` header or
scope names a new skill (skill mode).
**Don't fire when:** deciding whether an expert is needed (the Roster Builder); editing
an existing skill's rules (an ordinary build under the Execute row); the content is a
Project State note, a cbrain entity or anything that is not a brief or a SKILL.md.

## How
| Step | Precondition | Action | Evidence | Recovery |
|---|---|---|---|---|
| 1 Read | the spec: expert mode, the `expert-draft` note (brief text + the captain's revisions); skill mode, the Build Brief section | Read the spec whole, `references/expert-brief.md` or `SKILL_TEMPLATE.md` + CONVENTIONS, and the captain's brief (expert mode). | Spec id; files read | No spec, or a spec with no name or no body: stop and say what is missing. Never invent content. |
| 2 Write | spec read | Expert: write `experts/<slug>/BRIEF.md` from the spec in the brief format, `status: draft`, changelog line; apply the captain's revisions to the captain's brief (version bump, changelog line). Skill: write `skills/<slug>/SKILL.md` from the template, `status: draft`. Draft locally first; nothing committed yet. | Draft files | A field the spec does not supply: leave it blank and list it in the receipt; never fill it from memory. |
| 3 Check | drafts written | Run the mechanical checks for the mode (below). | Check list with pass/fail per line | Any FAIL: stop, report the failing lines to the caller, commit nothing. Never fix a FAIL silently; the Roster Builder or the Build Brief supplies the fix. |
| 4 Register | checks pass | Expert: add the row to `experts/INDEX.md` (level, under, call_when copied word for word, status draft; replace a stub row if one exists). A captain: add it to `captains_default` of the profile card its brief names under `profiles:`; if no card of that name exists, write `skills/expert-desk/profiles/<name>.md` from `profiles/harness.md`'s shape, with the "Done means" and severity lines drawn from the spec and marked ~ for Charles to refine on first use. A craft never touches a card. Skill: add the AGENT.md routing row the Build Brief gives, and a CHANGELOG.md line. | Row text | Name collides with an existing row: stop and report. |
| 5 Commit | registered | One commit per file, each message naming the build or desk run. | Commit SHAs | A commit fails: retry once, then stop and report what landed. |
| 6 Read back | committed | Fetch every written file from main and compare to the drafts. | "read back: identical" per file | A mismatch: report it; do not re-commit without saying so. |
| 7 Receipt | read back | Return to the caller: files written, SHAs, index or routing row, any blank fields, check results. | Receipt | — |

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
- Header: all nine fields; `under` empty only for a captain; `status: draft`.
- Our way: a craft has 5 to 20 lines, a captain 0 to 20; each line names a job, how we do it, and ends with a source in brackets; a line with no record of Charles's behind it is marked `~ field default`; no digits outside a date or an ID; no client, job or employer names (the repo is public).
- Lens: 10 to 20 lines; every line ends with a source in brackets; no digits outside a date or an ID (the claim and the pointer, never the figure); an uncertain line marked ~.
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
None. Team Builder finishes in one run inside the calling chat and leaves nothing open; the receipt goes back to the caller.

## Examples
Expert mode: the Expert Desk's first grow run under this skill (none yet; the dry runs of 2026-11-02 were written by hand). Skill mode: the next Build Brief that names a new skill.

## Pitfalls
- A check run on a Project State note instead of the committed file has no receipt; "every reads path exists" was never really fetched. Check the file you wrote, then read it back from main. [TH-139]
- Two briefs seeded by one chat on one day shared six lens lines; the overlap check is against every brief on the bench, not the ones that come to mind. [TH-139]
- Figures in lens lines went stale within a day; keep the pointer, drop the number. [TH-139]
- A proposal carried as chat text or an attachment was lost between chats; the spec is a Project State note or a Build Brief, never a message. [dry run 1, 2026-11-02]
- Teammates researched in parallel each wrote revisions for the same captain; the fit note merges them once, and only lines for crafts that landed are applied. [Build 65]
- The check job once lived in an expert's brief and the expert seated to run it had never seen it; mechanical checks live here, in the skill that writes. [TH-J-045 follow-up, Build 64]

## Changelog
- **0.2.1** (2026-11-03): Our way check (expert-brief 0.2.0); team mode writes *refresh* rows, so an expert already on the bench can be rewritten to the new format inside a team grow. Charles: craft experts must know how things ought to go in their corner.
- **0.2.0** (2026-11-03): team mode, loaded at the Expert Desk's team grow step T4: captains first, the fit note's cuts and merged captain revisions applied, a failed expert stops only itself and its crafts, a reused captain joins the team's profile card within max seats, one team receipt (Build 65, BB-2026-11-03-team-grow).
- **0.1.0** (2026-11-03): first version (Build 64, BB-2026-11-03-team-builder).
