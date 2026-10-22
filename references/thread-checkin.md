# Thread check-in — shared rule (0.2.0)

Every with-Charles chat that can be left mid-way, and every job that leaves
something open, reports where it stands, so the Next steps list on cbrain's
Dev tab is never missing it.

Every skill carries a **Progress tracking** section (see "The section every
skill carries" below). That section is how a skill opts in. A chat or job with
no skill does not check in on its own.

## Naming convention

- **project_label** — the Claude project's name, as Charles named it ("Idea
  vetting", "Total Harness", "Kids ed app", "Brainstorm & Design Assist"),
  unless the skill's Progress tracking section names a fixed label. Jobs that
  run outside a Claude project use the label in their section (e.g. "cbrain",
  "Arch renders").
- **plain_name** — 3-6 plain words naming the specific thing this thread is
  about: the idea, the game, the build, the report ("Backyard compost
  subscription", "Run Around the World game"). Never the skill's name alone
  ("Office hours") and never an id or code.
- **thread_key** — this chat's tag if it has one (DA-MMDD-slug); otherwise
  "<kind>:<plain_name in lowercase, words joined by hyphens>"
  (e.g. "plan-review:backyard-compost-subscription"). Jobs: "job:plan-<id>",
  "job:draft-<id>", "job:wake-<id>" or "job:<skill>-<slug>". Same key every
  turn.
- **kind** — named in the skill's section.

## When and how

Chats: at the end of every turn, one call: Project State `checkin`.
Jobs: when a run leaves something open (a hand-off, a stuck build, a needs-you
note, a follow-up draft), one `checkin` for it; `close_thread` when the job
itself clears it.

- next_step: one or two sentences Charles can act on cold. Say what is next and,
  if he owes something, exactly what. No ids, tags, build codes or file names —
  say what the thing is. Name where it lives in words ("the Working Doc").
- waiting_on: you | claude | a-build | nobody.
- links: the chat's artifacts or pages worth opening.
- chat_url: on your first turn, call `recent_chats` (n 3). Your chat is the one
  whose title or first message matches this conversation; pass its url. If none
  matches, try again next turn; never guess. Claude Code sessions use the
  `Claude-Session:` url from their own commit trailer.

If nothing changed, send the same next_step: the list keeps the old line and its
date. Never write "still waiting" or "no change".

Close: when your skill's stated finish happens, call `close_thread` with
closed_how in words ("report filed", "brief on the shelf"). Nothing else closes it.
If the check-in fails, carry on; the night runner re-checks open cards.

## The section every skill carries

Every SKILL.md has a `## Progress tracking` section, after How. Fill it in;
never leave it out. Skills that leave work open:

```
## Progress tracking
Follows `references/thread-checkin.md` (naming convention and when to check in).
- kind: <kind from the table below>
- project_label: the Claude project's name   (or a fixed label, for jobs)
- plain_name: <what names one thread of this skill, e.g. "the idea in 3-6 words">
- Opens when: <the first moment work can be left unfinished>
- Checks in: end of every turn   (jobs: when a run leaves something open)
- Closes when: <this skill's stated finish>
```

Skills that finish in one go and never leave work open:

```
## Progress tracking
None. This skill finishes in one run and leaves nothing open.
```

## Kinds and close rules

| Skill / chat | kind | Closes when |
|---|---|---|
| design-assist | design-assist | brief shelved, or Charles parks it |
| build (interactive) | build-chat | plan succeeded and its needs-charles items done |
| tech-discovery | tech-discovery | Discovery Brief filed |
| tech-review | tech-review | R&D Report filed (plus handoff on Adopt now) |
| game-maker | game-maker | Launched |
| office-hours, autoplan, ceo-reviewer and other plan reviewers | plan-review | doc or review approved |
| speed run (project instructions, until it has a skill) | speed-run | finish line met or Charles stops it; next_step names the current stage |
| block chat (project instructions, until it has a skill) | block-chat | block marked done |
| any chat in a personal folder (project instructions, until it has a skill) | folder-chat | Charles clicks Done, or the chat says it's finished |
| jobs (night runs, builds, repairers, wake-ups, runners) | job | the job clears it, or Charles clicks Done |

New kinds are added here and to the database's kind list together.

The database refuses a next_step or plain_name with ids or codes in it ("Write
this without ids like TH-004 — say what it is."). Rewrite it in words and call
again.

## Changelog

- 0.2.0 (2026-10-22) — Naming convention (project_label defaults to the Claude
  project's name; plain_name names the specific thing; thread_key from kind +
  plain_name). The Progress tracking section every skill carries, with a "None"
  form. Chat link via `recent_chats` (searching past chats for yourself never
  worked). Jobs check in too. Charles, 2026-10-22.
- 0.1.0 (2026-10-21) — Made by Build 44 (Next steps list and the Dev tab).
