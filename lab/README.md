# lab/ — the R&D lab's record

Written by `Tech discovery:` chats (`skills/tech-discovery/SKILL.md`, the first look, no test) and `Tech review:` chats (`skills/tech-review/SKILL.md`, the test run). Read by the R&D tab on the Total Harness screen in cbrain-ui. Plain files. Nothing here is a cbrain page, and the Skills screen ignores this folder.

## Files

- `shelf/<tool>.md` — one file per tool. The front matter is the shelf row. The body holds `## Verdict history`, newest line first.
- `briefs/<tech>.md` — one file per discovery: the Discovery Brief. Kept apart from `cards/` so the two show separately. A brief is never edited by a test run.
- `cards/<review>.md` — one file per test run: the R&D Report (older files are tech cards). A review of a suite covers several tools.
- `speed-run.md` — the speed-run brief. Read at the start of each review. Not shown on the screen.

## Shelf file fields

| Field | Meaning |
|---|---|
| `tool` | The tool's name. |
| `does` | One line: what it does. |
| `verdict` | `adopt-now`, `shelf` or `never`. |
| `verdict_note` | Short qualifier such as `as a trial`. May be empty. |
| `come_back_when` | The one trigger for a shelf or never verdict. Empty for adopt-now. |
| `blocks` | Total Harness block numbers it touches, such as `[16, 17, 19]`. May be empty. |
| `brief` | File name in `briefs/` without `.md`. May be empty (tools reviewed before 2026-10-14 have none). A test run finds the brief through this field. |
| `card` | File name in `cards/` without `.md`. Empty until the tool has a test run. |
| `reviewed` | Date of the latest review, `YYYY-MM-DD`. |
| `draft` | `true` until Charles approves the card. Remove it or set `false` on approval. |

## History line

`- YYYY-MM-DD · <Verdict> (<note>) · <reason, or "First review (<card>)">`

Newest on top. A line is never edited or deleted. A change of verdict adds a line such as `Shelf (was Adopt now)`.

## Discovery Brief file (in `briefs/`)

Since 2026-10-14. Front matter: `title`, `type: discovery-brief`, `discovered` (date), `tools` (shelf file names the brief covers), `brief_url` (the published page), `draft`. Body sections, in order: What it is, Verdict by tool, Where it fits, What we could use it for, What we checked, What else does this job, Requirements check, Risks and cover, If adopted, Test run if we do one, Sources. Evidence marks: Published or Assumed (never Tested). Verdicts are Shelf or Never only. A new shelf row's first history line reads `Discovery (<brief>)`.

## R&D Report file (in `cards/`)

Since 2026-10-14 each review files an R&D Report, not a tech card. The folder keeps the name `cards/` so the R&D tab keeps reading it. Template: `templates/rd-report.html`. First report: `cards/flythrough-renderer-blender.md`.

Front matter: `title`, `type: rd-report`, `brief` (the Discovery Brief's file name, when there is one), `reviewed`, `test_date`, `test_completed`, `status`, `tools` (shelf file names the report covers), `report_url` (the published page), `clips` (one `env` + `file` per test environment, `""` when none), `clips_home`, `draft`. The body follows the section order in the lab rules (`R&D REPORT`). The results table gives the verdict per environment on the review date; the shelf file holds the current one.

Every claim carries one evidence mark: Tested (run hands-on), Published (from the maker's own documentation), Assumed (judgment). Older cards use ✓✓, ✓ and ~ for the same three.
