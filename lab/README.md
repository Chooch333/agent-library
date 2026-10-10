# lab/ — the R&D lab's record

Written by `Tech review:` chats (`roles/tech-review/SKILL.md`). Read by the R&D tab on the Total Harness screen in cbrain-ui. Plain files. Nothing here is a cbrain page, and the Skills screen ignores this folder.

## Files

- `shelf/<tool>.md` — one file per tool. The front matter is the shelf row. The body holds `## Verdict history`, newest line first.
- `cards/<review>.md` — one file per review: the tech card. A review of a suite covers several tools.
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
| `card` | File name in `cards/` without `.md`. May be empty. |
| `reviewed` | Date of the latest review, `YYYY-MM-DD`. |
| `draft` | `true` until Charles approves the card. Remove it or set `false` on approval. |

## History line

`- YYYY-MM-DD · <Verdict> (<note>) · <reason, or "First review (<card>)">`

Newest on top. A line is never edited or deleted. A change of verdict adds a line such as `Shelf (was Adopt now)`.

## Card file

Front matter: `title`, `reviewed`, `tools` (shelf file names the card covers), `draft`. The body is the tech card: the sections named in the lab rules, as `##` headings in order. "Verdict by tool" is the verdict on the review date; the shelf file holds the current one.

Every claim carries a mark: ✓ checked at a source today, ✓✓ run hands-on, ~ assumed.
