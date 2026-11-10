# Build Brief — BB-2026-11-09-closing-out

**Git home:** Chooch333/agent-library · `docs/design/BB-2026-11-09-closing-out.md`
**Project State plan:** `a06154bc-7c3a-4e3d-bdf1-dfd58faf190e` on `total-harness`
**Build:** 78
**Skills:** orchestrate-build
**Stack Flow:** no change — no running part is added, removed or re-routed; the Stack Repairer's recap reads one more table it already reaches.
**Step map:** no change — no workflow is added or changed.
**Overnight:** yes · **target_repo:** Chooch333/agent-library · **after:** Builds 76 and 77 (both edit skills this build touches)

**What this is:** Finish the no-loose-ends rule. Clean out your to-do list, bring every skill in line with the rule, make the evening recap and the list one list, and stop a "click Done" card from being saved at all.
**What I'll do (build chat):** the five steps below.
**What you'll do:** nothing.
**Cost:** subscription only.

## Asked for — Charles, 2026-11-09 (frozen)
"Claude chats have an annoying habit of ending DA chats or build chats with loose ends that require more work, and sometimes more work to figure out what the loose end means. I need to figure out a way to have chats end without loose ends. Either those sorts of things get decided by claude and just taken care or, if claude can't make the decision, it gets put onto a to-do list. It leaves me with the feeling that the thing I think is done isn't actually gonna work and has more to do."

## Current state going in (verified 2026-11-09)
- **Done in the design chat:** the rule, "Closing out", in `references/thread-checkin.md` 0.4.0 (do it / decide it / queue it / hand it on; a card closes itself when nothing waits on Charles). AGENT.md points to it. `skills/build` 1.4.0 and `skills/night-run` 0.5.0 follow it (the night check now closes cards it has proved done). Four cards that said "nothing left" were closed. The three loose ends from the example chat were cleared: whole-bench overlap check run (pass), the lanes line fixed under the fold rule (lanes 0.2.4), the small-edits bend kept (sha-keyed edits read back; as safe as one whole-file write).
- The Next steps list had 51 open cards waiting on Charles; about 47 are left. Many are not asks: "glance at", "try the screen", an overnight yes or no (automatic since 2026-11-09), duplicates.
- 13 skills still end a card on "Charles clicks Done": arch-massing, arch-render, arch-renders-run, archivist, inspector, night-run (kinds line only), orchestrate-build, pascal-editor, project-folder, repairer, stack-repairer, team-builder, wake. `references/chat-capture.md` and `skills/design-assist/references/brief-artifact-style.md` use "Needs from you" in the old sense.
- The Stack Repairer's 17:00 recap lists only its own needs-you rows. Build 71 (draft, side finds) also sends asks to that recap. Two lists.
- Project State `checkin` already refuses ids in a next_step (`Chooch333/project-state-mcp` `lib/threads.ts`, `lib/tools.ts`).

## Scope
**In:** the five steps. **Out:** step-in scoring of closing replies (Build 76's job); a new card kind in the database beyond `chat`; any change to the fold rule (Build 77).

## Directive
1. **Sweep the list.** `list_open_threads`. For every card waiting on Charles: read the source its thread_key names (as night-run step 7 does), then sort it by Closing out. Done → `close_thread` "nothing left for you". Claude can decide it (a question a record answers; no money, nothing irreversible) → decide, log a Project State decision tagged `judgment-call`, act, close. An overnight yes or no → `set_overnight true`, close. "Glance at", "read and confirm", "try the screen" → close. Duplicates (two cards, one ask) → keep one, close the other "merged". Real hand-ons → rewrite next_step as a closed choice with a recommendation. A card whose source can't be read stays open, untouched. File one note on `total-harness` (tag `closing-out-sweep`): counts first, then each card and what happened.
2. **Skills.** In each file listed above, change a "Charles clicks Done" finish to "nothing on it waits on Charles" and add the thread-checkin pointer where a skill reports done; "Needs from you" means hand-ons only. Version bump and changelog line in each. Read each back.
3. **One list.** `skills/stack-repairer` step 7: Needs you = every open Next steps card waiting on Charles (`list_open_threads`), in the card's words, plus its own open needs-you rows (which already have cards). Edit Build 71's draft so its "daily recap" line says the recap reads the list.
4. **Refuse a non-ask.** `project-state-mcp` checkin: refuse `waiting_on: you` when next_step contains "click Done", "nothing is left", "nothing left", "when you've seen this" or "glance at" (case-insensitive), with a plain message: "Nothing here waits on Charles — close the card, or say what he must choose." Add `chat` to the allowed kinds and to thread-checkin's kinds table (replacing the `folder-chat` stand-in in its intro). Deploy; prove with one refused and one accepted test check-in (then close the test card).
5. **Proof.** One `list_open_threads` read: no card waiting on Charles carries the refused phrases or an overnight question, and every one is a closed choice.

## Acceptance
1. The sweep note exists, and its counts match the before and after `list_open_threads` reads.
2. `grep -rn "clicks Done"` on agent-library main finds only changelog lines.
3. Stack Repairer step 7 reads the list; Build 71's draft says the same.
4. A "click Done" check-in is refused live; a closed-choice one is accepted.
5. Step 5's read passes.

## Decisions
- [Charles] Leftovers get decided and handled by Claude, or go on a to-do list (2026-11-09).
- [Claude-per-doctrine] The rule lives in `references/thread-checkin.md` (every skill and job loads it), not in AGENT.md (routing only, and jobs don't read it). Seats: ai-system-design, oversight.
- [Claude-per-doctrine] The night check closes only cards whose every line it read. Charles's 2026-11-09 words replace Build 44's "Charles clicks Done".
- [Claude-per-doctrine] "Try the new screen" is not a to-do: the charter (2026-10-29/30, "Don't ask him to test something") is newer than the 2026-09-26 wish for a check-the-deploy task.
- Ruled out: a separate to-do store. The Next steps list already is one.

## Pasteable prompt
> Build 78 — execute Build Brief BB-2026-11-09-closing-out. Pull the plan from Project State (plan_id a06154bc-7c3a-4e3d-bdf1-dfd58faf190e, project total-harness). Answer forks yourself; stop only at hard gates.
