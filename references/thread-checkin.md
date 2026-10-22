# Thread check-in — shared rule (0.3.0)

Every with-Charles chat that can be left mid-way, and every job that leaves
something open, reports where it stands, so the Next steps list on cbrain's
Dev tab is never missing it.

Every skill carries a **Progress tracking** section (see "The section every
skill carries" below). That section is how a skill opts in. A chat or job with
no skill does not check in on its own.

## Naming convention

- **build** — the body of work this chat or job is part of, inferred by you,
  2-5 plain words ("Next steps list", "Total Harness wake-ups", "Backyard
  compost subscription"). Many chats share one build: a design chat, its build
  chats and their follow-ups all name the same build. Reuse before you invent:
  on your first turn, read the existing builds (`list_builds`; until that tool
  exists, the build names on open cards from `list_open_threads`) and take the
  one this work belongs to; name a new build only when none fits. Never an id or
  code. Until the `build` field exists on `checkin` (the Next steps side
  panel build), send the build name as `project_label`.
- **project** and **campaign** — never set by a chat or job. Charles fills
  them in on cbrain's Dev tab.
- **plain_name** — 3-6 plain words naming what THIS chat or job does within the
  build ("Phone screens design", "Office hours vetting", "Run Around the World
  game"). Never the skill's name alone and never an id or code.
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
- build: <how this skill infers the body of work it belongs to, e.g. "the idea's name"; reuse an existing build first>
- plain_name: <what this chat or job does within the build, e.g. "Office hours vetting">
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

- 0.3.0 (2026-10-22) — **build** is the main grouping: the chat infers it, reuses
  an existing one first, and many chats share it. project and campaign are
  filled in by Charles on the Dev tab, never by a chat. plain_name now names
  what this chat does within the build. Replaces 0.2.0's "project_label = the
  Claude project's name", which grouped unrelated work together. Charles,
  2026-10-22.
- 0.2.0 (2026-10-22) — Naming convention (project_label defaults to the Claude
  project's name; plain_name names the specific thing; thread_key from kind +
  plain_name). The Progress tracking section every skill carries, with a "None"
  form. Chat link via `recent_chats` (searching past chats for yourself never
  worked). Jobs check in too. Charles, 2026-10-22.
- 0.1.0 (2026-10-21) — Made by Build 44 (Next steps list and the Dev tab).
