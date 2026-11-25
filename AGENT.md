# AGENT.md — Routing Schema

This file is the front door. Project instructions point here. It routes a first message to one skill; it holds no domain knowledge.

> Rule: not one line of domain knowledge belongs in this file.
> If you find yourself writing "how to do X" here, you're writing a skill, not routing.

## Every chat, before the first reply

Read `references/charter.md` (this repo) right after this file, in every chat, whether or not a trigger below matches. It makes the chat an expert on working with Charles: how he works and when to stop for him. It is not only for harness chats. How anything in a field should be done lives with the experts, not there. A chat that matches no trigger still reads it. (Charles, 2026-11-03: a chat with no trigger skipped it and gave a reply the charter rules out.)

**Memory stays current.** When a chat reads a claude.ai Project memory file and finds a line that a newer record contradicts (the charter, an expert's brief, a Project State record), or that only repeats the charter or an expert's brief, it fixes or removes that line in the same turn, without asking and without reporting it (Charles, 2026-11-19: "I don't need to get an audit of what gets sweeped out... if it's important, it'll come back up"). No scheduled sweep: memory is tidied where it is read. (Charles, 2026-11-19: memory should be audited "so that they are current... you can make a decision on how to do that best.")

**Re-read before tech answers.** A file read at the start of a chat fades as the chat grows. So before any reply that recommends, designs, fixes or builds something technical, re-read the charter (it is short) and check the reply against it before sending: the gates and talk-first items, one grounded recommendation, verified vs assumed marked, plain words, no ids. (Charles, 2026-11-19: "Make sure it gets reviewed before a chat response happens... especially when thinking about answering or solving something tech related.")

## Every chat, every message — experts

When Charles asks for judgment in a field — how something should be done, what's right, what could go wrong, a review of a plan or a choice, or a request to change a skill, a rule, the stack map or a running part — in any chat, on any message, mid-chat included: read `experts/INDEX.md` (the first time; keep its call_when lines in mind for the rest of the chat). If an active expert's call_when matches, say in one line which expert you're seating, then run the Expert Desk (`skills/expert-desk/SKILL.md`) in mode B with that seat, unasked. Two matches: both seats (mode B's limit). This rule applies whether or not a trigger below matches. "What did we miss" and "why did it do X" are judgment asks. A judgment-call decision logged in an active expert's corner, outside a skill run, says in its provenance `Seat: <expert>` or `Seat: none — <why>`. (2026-11-11: a Three.js version call and its post-mortem went unseated.)

Don't seat when the chat is carrying out a skill's steps (a build chat, game-maker, job-update logging, a scheduled run), the message asks for a plain fact or a lookup, or that expert already answered this question in this chat. Applying Charles's own stated correction (the corrections paragraph below) is exempt. Design Assist chats seat experts through their own step 6a; night builds are seated by the night session (`skills/night-run`, Seat step).

Needs the Agent tool. A chat without it answers itself and says in one line which expert it couldn't seat.

**Charles's corrections and decisions.** When Charles corrects how Claude worked, says how he wants something done, or decides how something in a field should be done (the same test Claude's memory uses: he said it, and it will still be true in a month), the chat, in the same turn and without asking him, so his experts learn the way memory does: (1) logs one Project State decision on the work's project, tagged `charles-directed` and `charles-correction`, quoting his words with the chat link when the chat can read it, else the chat's title and date (a Design Assist chat also passes its board tag as `chat_tag`); (2) applies it at its source, citing that decision: a skill it names → that skill is edited now (version bump, changelog line); a rule about working with Charles itself (how he wants answers and work handed to him, when to stop for him, how he is kept informed) that holds whatever the subject → `references/charter.md`: when it adds a line, add it with his words quoted; when it contradicts a line already there, ask one closed question with a recommended answer first, and on his yes replace that line in place, the replaced line named in the decision; a rule about how something in a field should be done, tech included → one `lens-note` (Charles calls it the expert's notebook) for the expert whose call_when matches, on `expert-bench`, citing the decision (no active expert matches: the nearest captain whose field covers it; no captain's field covers it: log the decision only, and file one note on `expert-bench` tagged `grow-ask` naming the missing field and citing the decision, so the expert gets grown; never a captain outside its field; never the charter). Test: would it hold in a chat on any subject where no expert is seated? Yes → charter; no → expert. Nothing goes in both. Applying his stated words needs no seat. Two of his decisions that clash: ask him in the chat, now. A chat without Project State or GitHub says so in one line and files nothing.

## Active skills

### Build

| Trigger phrases | Skill |
|---|---|
| `this is a build chat` (case-insensitive, must be in the very first message — mentioning building mid-chat is not an invocation) | `skills/build/SKILL.md` |

### Design shaping

| Trigger phrases | Skill |
|---|---|
| `Design Assist` or its synonym `DA chat` (either phrase in prompt, case-insensitive — e.g. `this is a DA chat`; these are the only triggers; do not auto-fire from adjacent phrases or a bare "DA") | `skills/design-assist/SKILL.md` |

### Expert Desk

| Trigger phrases | Skill |
|---|---|
| `Expert desk:` (a message that starts with it, e.g. `Expert desk: <situation or plan link> — goal: <one line> — mode: A`, in any chat that can start helpers), or a judgment question that matches an expert's call_when (see "Every chat, every message — experts"; DA chats also seat experts at their step 6a), or `I need an expert in <x>` / `I need an expert for <x>` (a message that starts with it, in any chat that can start helpers), or `I need a team of experts for <x>` / `I need a group of experts for <x>` (a message that starts with it, mid-chat included, in any chat that can start helpers; the experts may have been named earlier in the chat), or `CE <expert>: <link or topic>` (a message that starts with it, in any chat that can start helpers) | `skills/expert-desk/SKILL.md` |

### Investment

| Trigger phrases | Skill |
|---|---|
| `this is an investment review` (case-insensitive, must be in the very first message — mentioning an investment review mid-chat is not an invocation) | `skills/investment-review/SKILL.md` |

### R&D lab

| Trigger phrases | Skill |
|---|---|
| `Tech discovery:` (the very first message must start with it, e.g. `Tech discovery: <name or link>` — the first look at a tech, no test; files a Discovery Brief; `Tech discovery: inbox` starts on a post shared from the phone) | `skills/tech-discovery/SKILL.md` |
| `Tech review:` (the very first message must start with it, e.g. `Tech review: <name or link>` — the test run of a tech, usually one that already has a Discovery Brief; files an R&D Report. Mentioning a tech review mid-chat is not an invocation) | `skills/tech-review/SKILL.md` |

### Family arcade

| Trigger phrases | Skill |
|---|---|
| `New game:` (a message that starts with it, e.g. `New game: squish things to earn coins`; in any chat, mid-chat included), `New character:` (a message that starts with it, with a drawing), `Drop in:` (a message that starts with it, e.g. `Drop in: Super Sweets → Louis's avatar`), `Remove:` (a message that starts with it, e.g. `Remove: Waddle Out from Louis' arcade`; in any chat), and `Launch` said after a Game Maker game is on screen | `skills/game-maker/SKILL.md` (0.7.0) — two Workflows cards: Game Maker (`New game:`, `Launch`, `Remove:`) and Character Maker (`New character:`, `Drop in:`) |

### Kids' Ed

| Trigger phrases | Skill |
|---|---|
| `New explainer:` (a message that starts with it, e.g. `New explainer: animal cell`; in any chat, mid-chat included), `Hide:` and `Show:` (a message that starts with it, naming an explainer on Explore, e.g. `Hide: Inside a Cell`), and `Publish` said after an Explainer Maker page is on screen | `skills/explainer-maker/SKILL.md` (0.1.1) |

### Plan-mode reviews

| Trigger phrases | Skill |
|---|---|
| `business concept` (Business Concept run: Startup mode + market research + Vetting Report), `office hours`, `I have an idea`, `brainstorm this`, `let's design`, `rethink from the start`, `what should I build` | `skills/office-hours/SKILL.md` |
| `business plan` (Business Plan run: business review + Business & Tech Plan report), `review this plan`, `CEO review`, `think bigger`, `expand scope`, `is this ambitious enough`, `find the 10-star product`, `rethink this` | `skills/ceo-reviewer/SKILL.md` |
| `eng review`, `engineering review`, `review architecture`, `lock in the plan`, `check the implementation plan` | `skills/eng-reviewer/SKILL.md` |
| `design review`, `review the design`, `design plan review`, `rate this design`, `UI review` | `skills/design-reviewer/SKILL.md` |
| `devex review`, `DX review`, `developer experience review`, `review the dev experience`, `TTHW review` | `skills/devex-reviewer/SKILL.md` |
| `autoplan`, `run the full plan review`, `review chain`, `CEO design eng review` | `skills/autoplan/SKILL.md` |
| `design consultation`, `design the design system`, `create a DESIGN.md`, `what should this look like`, `design from scratch`, `design system kickoff` | `skills/design-consultation/SKILL.md` |

### Implementation + review

| Trigger phrases | Skill |
|---|---|
| `review this PR`, `review the diff`, `pre-PR review`, `review before merge`, `code review`, `ship review` | `skills/pr-reviewer/SKILL.md` |
| `investigate this bug`, `debug this`, `find the root cause`, `why is this broken`, `what's causing`, `trace this issue` | `skills/investigate/SKILL.md` |
| `design shotgun`, `design variants`, `show me different design directions`, `give me design options` | `skills/design-shotgun/SKILL.md` |
| `generate HTML`, `implement this design`, `write the HTML`, `code this design`, `design to HTML` | `skills/design-html/SKILL.md` |

### Release + deploy

| Trigger phrases | Skill |
|---|---|
| `ship it`, `ship this`, `open the PR`, `ready to ship`, `ship pre-flight` | `skills/ship/SKILL.md` |
| `land and deploy`, `merge and deploy`, `land it`, `deploy the PR`, `land this` | `skills/land-and-deploy/SKILL.md` |
| `document this release`, `update the docs`, `documentation sweep`, `doc sync` | `skills/document-release/SKILL.md` |

### FAW jobs

| Trigger phrases | Skill |
|---|---|
| An FA Wilhelm job comes up — its tasks, issues, dates, milestones, meetings, team, RACI or design decisions (e.g. `what's open on IMI?`, `add this`, `log this`, `put this on the job`) — mid-chat included; fetch once per chat | `skills/job-update/SKILL.md` (reads any time; writes only on Charles's ask; general construction/permitting talk is not a job and loads no job skill; the experts rule still applies) |

### Operators

| Trigger phrases | Skill |
|---|---|
| `PM: <job>` or `PM: what needs me` (a message that starts with it, in any chat, mid-chat included), or `Check in` (a message that starts with it, in a chat inside the Stack Work Project, mid-chat included), or `Chief: check in` / `Chief: finish <thing>` / `Chief: close <thing>` (a message that starts with it, in any chat or Duet), or `run the Project Manager` / `run the Chief Engineer` / `run my Operators` (any chat or Duet, on demand or on Duet's cadence) | `skills/operator-run/SKILL.md`, which loads the named Operator's mandate from its table (`operators/project-manager/MANDATE.md`, `operators/chief-engineer/MANDATE.md`) and, when a move needs it, `skills/job-update` |
| `I need an operator for <x>` / `I need an operator to <x>` (a message that starts with it, in any chat that can start helpers, mid-chat included) | `skills/operator-setup/SKILL.md` (walks the steps with Charles, seats the operator-design expert, one confirmation, then `skills/team-builder` operator mode writes it) |

### Outside content

| Trigger phrases | Skill |
|---|---|
| A YouTube link (youtube.com or youtu.be) in any message, mid-chat included, when the chat needs what the video says; fetch once per chat | `references/youtube-transcript.md` (never say a video has no transcript, or ask Charles to paste one, before its steps) |
| An X (x.com, twitter.com) or Instagram link whose post has a video, in any message, mid-chat included, when the chat needs what the video shows; fetch once per chat | `references/watch-video.md` (never say a video can't be seen, or ask Charles to describe it, before its steps; needs the built-in browser on a linked PC) |

### Browser use

| Trigger phrases | Skill |
|---|---|
| No phrase: before the first browser tool call in any chat (opening a page on Charles's PC, driving ChatGPT or Gemini, a download); mid-chat included; fetch once per chat | `references/browser-use.md` (navigation rules only: which browser, which of his two PCs, what to do when a page stops; never pick a PC yourself, and never say a browser job can't be done before its steps) |
| No phrase: before telling Charles a step is his to click (creating, sharing or saving a key, token or permission, or a setting only he can change); mid-chat included; fetch once per chat | `references/his-only-clicks.md` (open every page in order, one card of exact clicks; reads browser-use first) |
| Charles asks for ChatGPT's or Gemini's view on something (e.g. `ask Gemini what it thinks`, `get GPT's take`); mid-chat included | `references/ask-another-model.md` (draft; reads browser-use first) |

### Knowledge capture

| Trigger phrases | Skill |
|---|---|
| `add to cbrain`, `build out cbrain`, `let's capture`, `capture this`, `I want to record`, `create an entity for`, or a person/org/project not yet in cbrain named during a knowledge-capture chat | Draft a brief per `references/chat-capture.md` → Charles approves → `skills/archivist/SKILL.md` files it |
| `define a new entity type`, `new entity type`, `add a type to the schema`, `cbrain needs a type for`, or defining a new KIND of thing that has no `type` in `SCHEMA.md` yet | `skills/entity-type-creator/SKILL.md` (single-approval SCHEMA.md addition; auto-deploys to the watcher) |

### Self-maintenance

| Trigger phrases | Skill |
|---|---|
| `Inspector: walk` | `skills/inspector/SKILL.md` |
| `Repairer: run` | `skills/repairer/SKILL.md` |
| `Stack Repairer: run` | `skills/stack-repairer/SKILL.md` |
| `what's going on with my stack`, `stack status`, `Chief of Staff` (any chat, mid-chat included, Duet included; on demand, never scheduled) | `skills/stack-chief-of-staff/SKILL.md` |

## Natural sequences

The skills compose. Common flows:

- **Vetting a business idea:** `business concept` (office-hours → Vetting Report) → if PURSUE, `business plan` (ceo-reviewer → Business & Tech Plan) → if GO, `eng review` on the tech plan
- **From idea to plan:** `office-hours` → `ceo-reviewer` → `eng-reviewer` (+ `design-reviewer` if UI, + `devex-reviewer` if developer-facing) — or `autoplan` to chain all four
- **From plan to design:** `design-consultation` (if no design system) → `design-shotgun` (if exploring) → `design-html` (when ready to implement)
- **From code to ship:** `pr-reviewer` → `ship` → `land-and-deploy` → `document-release`
- **Something broken:** `investigate`

## Imported reference material

| Source | Path | Notes |
|--------|------|-------|
| Tan / gstack | `imports/tan-gstack/_AGENTS.md` | Full catalog of all 48 gstack skills with reshape status (✅/⏭️/◯) and skip reasons |
| Tan / gbrain | `imports/tan-gbrain/_RESOLVER.md` | Catalog of all 43 gbrain skills. None reshaped — gbrain requires Postgres + pgvector runtime |
| Charles | `references/charter.md` | How to work with Charles: how he works, when to stop for him. Read in every chat before the first reply and by every scheduled run before its first step (see "Every chat, before the first reply" above). The harness's mission and end state are in `experts/c-stack/BRIEF.md`. |
| cbrain | `Chooch333/cbrain concepts/stack-map.md` `lanes:` | The rules of each place Claude runs. Read before designing anything that runs unattended or touches the PC. |

## Disambiguation rules

- When multiple skills could match, prefer the most specific. (`pr-reviewer` if reviewing a diff that exists; `eng-reviewer` if reviewing a plan with no diff yet.)
- `design-reviewer` reviews a *plan's* design quality. `design-shotgun` generates *new* design directions. `design-html` writes the *code* for an approved design. `design-consultation` builds a *design system* from scratch.
- `ceo-reviewer` is strategic; `eng-reviewer` is architectural; both can fire on the same plan. Use `autoplan` to chain them.
- `ship` opens the PR; `land-and-deploy` merges and watches the deploy; `document-release` updates docs after shipping. Run in order.
- **Knowledge capture (cbrain).** When the content is durable knowledge about an entity (people, orgs, projects), the chat path drafts a brief per `references/chat-capture.md`; Charles approves it in chat; the Archivist (`skills/archivist/SKILL.md`) is the single write-authority that files it. The chat never commits to cbrain directly. This is NOT for work-state (decisions, next steps, status) — that's Project State. If the content is "what's true about a thing," it's cbrain (→ draft a brief); if it's "what we're doing or deciding," it's Project State.
- **Job work vs knowledge capture.** "Add this" about a job's work (a task, a date, a milestone, a meeting, who's on the job) → `job-update` (graph). "Add this" about what's true of a person, company or place → chat-capture → Archivist (cbrain).
- **New TYPE vs new INSTANCE vs new FIELD (cbrain).** A new KIND of thing that no `type` in `SCHEMA.md` fits → `skills/entity-type-creator/SKILL.md` (it edits the schema; the watcher reads the schema at runtime, so the commit auto-deploys). A new INSTANCE of an existing type (a person, an org, a project) → chat-capture → Archivist, NOT the type creator. An existing type that just wants one more optional field → a small direct schema edit, not a new type. Test: is there no `type` value this thing could carry? Only then is it a new type.
- **Operator vs job work.** A message that starts `PM:` or asks to run an Operator → `operator-run`, which loads `job-update` itself when a move needs it; do not also fire the FAW jobs row. A plain "add this" or a question about one job with no Operator named → `job-update`, as before.
- **Chief vs Chief of Staff.** `Check in` at the start of a message in a Stack Work chat, or a message that starts `Chief:` in any chat → `operator-run` (the Chief Engineer; Charles calls it "the Chief"), even when later words say "DA chat", "review this plan" or "how's my stack"; do not also fire Design Assist or a plan reviewer. Only the full words "Chief of Staff" (or "stack status", "what's going on with my stack") → the Stack Chief of Staff. Every chat in the Stack Work Project is the Chief Engineer (its Project instructions say so): it reads `operators/chief-engineer/MANDATE.md` after the charter and keeps its own card current each turn; that is not a full run. The opening line a run hands Charles for a Design Assist chat fires Design Assist only when he sends it himself.
- **New workflow vs changing one.** Designing a new workflow happens in a Design Assist chat, which loads `skills/workflow` (and `skills/speed-run` when steps are unknown). Changing an existing workflow's steps, screens or rules is an ordinary Design Assist brief (rules 12-13).
- A first message that matches no trigger has no skill. Plain conversation, quick questions and other non-build work proceed normally; no default is assumed. The experts rule ("Every chat, every message — experts") is the one exception: it applies to every message.
- A broken running part you notice outside your job → one `reported` row (shape in stack-repairer, Reported problems). Design questions stay on the Comms Table.
- If unsure which skill fits, ask before acting. Anything else unsure is sorted by Closing out.

## Activation pattern (claude.ai chat)

Claude.ai has no native slash command system. To activate a skill:
1. User names the skill explicitly ("use CEO Reviewer on this plan") OR uses a trigger phrase from the table above
2. Claude fetches the matching `skills/<name>/SKILL.md` via Custom GitHub MCP
3. Claude announces the skill ("Operating as the CEO Reviewer. First, picking a posture...") and follows its SOP

A skill that reads or writes Project State declares `requires: references/project-state.md`; fetch what the header names after the skill. (`requires:` paths are from the agent-library repo root.)

Confirmation is behavioral, not UI-driven. Watch for: explicit skill announcement in the first response, the skill's characteristic vocabulary, SOP-following.

## Changelog

See `CHANGELOG.md` (moved out of this file 2026-10-15, Build 39).
