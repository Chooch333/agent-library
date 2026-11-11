---
name: explainer-maker
description: 'Use when Charles (or a boy with him) says "New explainer: <topic>" in a Claude chat: build a kids'' 3D explainer page from the kids-ed explainer kit (its playbook and template), run the playbook checks, show it as an artifact, and on "Publish" put it on the boys'' Explore site after a robot check. "Hide: <explainer>" takes one off Explore; "Show: <explainer>" puts it back.'
version: 0.1.0
status: draft
triggers: ["New explainer: <topic>", "Publish (after an Explainer Maker page is on screen)", "Hide: <explainer>", "Show: <explainer>"]
owner: Charles
source: Design Assist chat DA-1111-ed-explainer-home (2026-11-11); R&D lab cell build (2026-11-10/11)
requires: [references/thread-checkin.md]
wiring:
  runs: in-chat
  reads: [Chooch333/kids-ed kit/README.md, kit/explainer-kit.js, kit/<kit>/PLAYBOOK.md, kit/<kit>/template/index.html, tools/publish.md]
  writes: [Chooch333/kids-ed public/explainers/<slug>/, cbrain db ed_explainers, runs/<slug>/]
  stack: [kids-ed]
  origin: yours
  label: Explainer Maker
---

# Explainer Maker

Turns "New explainer: <topic>" into a 3D explainer page the boys open on **Explore**, their
explainers site. The know-how lives in the kit (playbook, template, shared engine). This skill only sets the order and
the stops. Charles decides when a page is published.

## 1. Read the kit (every time, before writing a line)
Custom GitHub MCP `get_file_contents`, owner `Chooch333`, repo `kids-ed`:
`kit/README.md` first. It lists the kits and which topics each one fits. If no kit fits the topic (the cell
kit is the only one so far), say so in one line and stop. Never stretch a kit to a topic it wasn't made for.
Only when a kit fits, read that kit's `PLAYBOOK.md` (the rulebook) and `template/index.html`, and
`kit/explainer-kit.js` (paste it unchanged). If the repo can't be read, say so and stop. Never build from memory
of the kit.
**The template is starting code, not a topic.** If the topic matches an explainer already in `ed_explainers`
(Supabase `execute_sql`, project `lpeswznkxzeeyiqaewma`: `select slug, title, status from public.ed_explainers;`),
or is the template's own subject (the cell template is the animal cell), say so and offer to edit that one
instead of building a copy.

## 2. Build (one answer, whole)
- Follow the playbook: its "Before starting" list, then its Order of work. Start from the template, never a
  blank file. Keep everything the playbook marks "keep exactly".
- One self-contained HTML artifact. The kit pasted unchanged between the `EXPLAINER-KIT:START` /
  `EXPLAINER-KIT:END` markers. An inline `#explainer-json` block: slug, title, line (one plain sentence for the
  list), subject, kit, version "1", stops.
- **Science as you write.** Every tour line and every "How the Model is Different" note is checked against a
  source while it is written (textbook, university or agency page). Keep a `science.md`: stop, claim, source
  link. A line no source supports is rewritten or cut.

## 3. Check before showing
- With a code workspace: fetch `tools/check-explainer.mjs` and its `package.json` from the repo and run it on the
  file (`--file`). Fix what fails. Three failed rounds on the same check: stop and tell Charles in plain words
  what failed, what was tried and what you think is wrong. Look once at the contact sheet it makes (every
  stop, three angles) for the look checks the robot can't judge (four tones, curved tone lines, nothing
  passing through anything, no empty ring, different heights, clear views).
- Without a code workspace: say in one line that the checks run at Publish.
- Show the artifact, the check table in plain words, and the playbook checks not run.

## 4. Feedback rounds
Each round: one plain line of what changed, then the whole updated artifact. When feedback slows, one line:
"Ready to publish." or "One thing to fix first: …" (and fix it). Then exactly:
**"If it looks right, tell me Publish and I'll put it in Explore."**

## 5. Publish (only when Charles says "Publish")
Follow `tools/publish.md` step by step. In short: files to `public/explainers/<slug>/` with `[wip]`,
`check-explainer.yml` on the files (all true), the `ed_explainers` row, the poster commit with `[deploy]`,
Vercel READY, `check-explainer.yml` against the live site (all true). Only after a pass, report one line:
`In Explore: <title> · <address>/?e=<slug>` and show `poster.png`. A re-publish bumps `version`.

## 6. Hide and Show
"Hide: <explainer>": Supabase `execute_sql`, project `lpeswznkxzeeyiqaewma`, `ed_*` tables only:
`update public.ed_explainers set status = 'hidden' where slug = '<slug>';` Files stay.
"Show: <explainer>" sets it back to `'live'`. Unclear which explainer: ask once. Report one line.

## 7. Lessons
After a Publish: one Project State note on total-harness (`add_note`, tags `explainer-maker`, `kids-ed`):
topic, rounds, what the check caught, what the boys said, any kit rule that should change (a suggestion, not an
edit to the kit).

## Progress tracking
Follows `references/thread-checkin.md`.
- kind: chat
- build: the explainer's title + "explainer", e.g. "Plant cell explainer" (thread_key `explainer-maker:<slug>`)
- Opens when: the first turn, once the page is on screen
- Checks in: end of every turn
- Closes when: the page is published and its live check passed (`close_thread`, closed_how "published");
  a standalone Hide or Show when its report is sent (closed_how "hidden" / "shown")

## Changelog
- 0.1.0 (draft) — first version, Build 81.
