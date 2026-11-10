# Step-in rubric (draft)

What the step-in scorer (`skills/step-in-scorer`) counts. A **step-in** is a turn where Charles had to correct Claude, redo something himself, or say the same thing again. His plain answer to a fair question Claude asked is not a step-in; it is counted separately as an **ask**.

**Telling a step-in from an ask** (the rule, so the count does not move with the scorer's mood):
- A question is a step-in (`asked-to-fetch`) when the answer was in a record or behind a tool Claude had in that chat. The record names which.
- A question only Charles could answer (his preference, a decision that is his, money, a key) is an ask.
- Can't tell which → tag `step-in-unsure`. It is counted on its own line and never starts a fix.
- One record per correction, not per turn: a turn that corrects two things is two records.

Pick one pattern per step-in. Tag `pattern-<name>`. Add `same-correction-twice` beside it when he had already corrected the same thing in an earlier chat.

| Pattern | Counts when | Example |
|---|---|---|
| `resettled-wiring` | Claude re-decided or got wrong something his record already settles (where a job runs, which project, which tool) | put a nightly timer on GitHub Actions though Actions timers are off |
| `cant-reach` | Claude said something doesn't exist or can't be reached without trying the obvious routes | "there's no transcript" after one web fetch |
| `asked-to-fetch` | Claude asked him to fetch, paste, test or check what Claude could | "send me the file" when it's in a connected repo |
| `option-list` | Claude gave a menu where the record or the charter settles one path | three options for where a cron lives |
| `translated-terms` | Claude swapped his locked words for others | "lead role" for captain |
| `should-have-asked` | Claude went ahead where the charter keeps the call with Charles: real money, a credential only he can supply, an irreversible data change, or a change to a settled rule | upgraded a paid tier to finish a build |
| `same-correction-twice` | he corrected something he already corrected in an earlier chat (add this tag beside the main pattern) | the second "no transcript" |
| `other` | none of the above fits; say what in the record. `other` never forms a cluster on its own | |

`should-have-asked` is the counterweight: every other pattern pushes toward acting without asking, so without it fixes would tune Claude toward never asking (scoring-and-testing Lens 8; TH-160).

Each record holds, and nothing else: the chat link (or the chat's title and date when no link can be had), the turn, the skill and section in play (`skill-<slug>`, or `skill-none`), one line on what Claude did, one line on what Charles wanted. No quotes of his words over a few, no people, clients, jobs or amounts.
