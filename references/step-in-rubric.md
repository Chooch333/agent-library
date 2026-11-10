# Step-in rubric (draft)

What the step-in scorer (`skills/step-in-scorer`) counts. A **step-in** is a turn where Charles had to correct Claude, redo something himself, or say the same thing again. His plain answer to a fair question Claude asked is not a step-in; it is counted separately as an **ask**.

Pick exactly one pattern per step-in. Tag `pattern-<name>`.

| Pattern | Counts when | Example |
|---|---|---|
| `resettled-wiring` | Claude re-decided or got wrong something his record already settles (where a job runs, which project, which tool) | put a nightly timer on GitHub Actions though Actions timers are off |
| `cant-reach` | Claude said something doesn't exist or can't be reached without trying the obvious routes | "there's no transcript" after one web fetch |
| `asked-to-fetch` | Claude asked him to fetch, paste, test or check what Claude could | "send me the file" when it's in a connected repo |
| `option-list` | Claude gave a menu where the record or the charter settles one path | three options for where a cron lives |
| `translated-terms` | Claude swapped his locked words for others | "lead role" for captain |
| `same-correction-twice` | he corrected something he already corrected in an earlier chat (add this tag beside the main pattern) | the second "no transcript" |
| `other` | none of the above fits; say what in the record | |

Each record holds, and nothing else: the chat link, the turn, the skill and section in play (`skill-<slug>`, or `skill-none`), one line on what Claude did, one line on what Charles wanted. No quotes of his words over a few, no people, clients, jobs or amounts.
