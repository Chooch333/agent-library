# Thread check-in — shared rule

Every with-Charles chat that can be left mid-way reports where it stands, so the
Next steps list on cbrain's Dev tab is never missing it.

When: at the end of every turn. One call: Project State `checkin`.
- thread_key: this chat's tag if it has one (DA-MMDD-slug), else "<kind>:<slug>",
  e.g. "tech-review:prism-room". Same key every turn.
- kind: your skill's kind (see your skill's Check in step).
- project_label: the personal project in plain words ("Family arcade",
  "Arch renders", "Kids ed app", "cbrain"). Folder chats use the label in their
  project instructions.
- plain_name: what this thread is, 3-6 words ("Prism Room 3D explainer review").
- next_step: one or two sentences Charles can act on cold. Say what is next and,
  if he owes something, exactly what. No ids, tags, build codes or file names —
  say what the thing is. Name where it lives in words ("the Working Doc").
- waiting_on: you | claude | a-build | nobody.
- links: the chat's artifacts or pages worth opening.
- chat_url: from turn 2 on, if not yet set, search past chats for your
  thread_key or plain_name and pass this chat's url.

If nothing changed, send the same next_step: the list keeps the old line and its
date. Never write "still waiting" or "no change".

Close: when your skill's stated finish happens, call `close_thread` with
closed_how in words ("report filed", "brief on the shelf"). Nothing else closes it.
If the check-in fails, carry on; the 5 am sweep backfills.

## Kinds and close rules

| Skill / chat | kind | Closes when |
|---|---|---|
| design-assist | design-assist | brief shelved, or Charles parks it |
| build (interactive) | build-chat | plan succeeded and its needs-charles items done |
| tech-discovery | tech-discovery | Discovery Brief filed |
| tech-review | tech-review | R&D Report filed (plus handoff on Adopt now) |
| game-maker | game-maker | Launched |
| office-hours, autoplan | plan-review | doc or review approved |
| speed run (project instructions) | speed-run | finish line met or Charles stops it; next_step names the current stage |
| block chat (project instructions) | block-chat | block marked done |
| any chat in a personal folder | folder-chat | Charles clicks Done, or the chat says it's finished |

The database refuses a next_step or plain_name with ids or codes in it ("Write
this without ids like TH-004 — say what it is."). Rewrite it in words and call
again.

Made by Build 44 (Next steps list and the Dev tab), 2026-10-21.
