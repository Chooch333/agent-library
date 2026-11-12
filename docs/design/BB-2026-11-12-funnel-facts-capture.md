# Build Brief — BB-2026-11-12-funnel-facts-capture

**Git home:** Chooch333/agent-library · `docs/design/BB-2026-11-12-funnel-facts-capture.md`
**Project State plan:** `94089c3e-a977-461e-8c41-5590c1623ef1` on `total-harness`
**Build:** 82
**Skills:** orchestrate-build
**Seated:** revision 2, report TH-200, seats c-stack, lanes, oversight, data-homes, github-integrations, ai-system-design
**Stack Flow:** edits `concepts/stack-map.md` lanes (chat, scheduled, scheduled-pc, github-action rows) and adds a "Lab run" part (lane github-action, pays_with github-actions) under the Chats dot, with its side-panel text.
**Step map:** no change — no workflow is added or changed.
**Overnight:** yes · **target_repo:** Chooch333/agent-library (also writes Chooch333/cbrain `concepts/stack-map.md`) · **after:** none
**Cost:** subscription only. Build ≈ 1 builder run. The new nightly fold step (step 5) runs a Team Builder helper only on nights with a new correction (≈ 2–3 a week, ≈ 150k tokens each). No Actions minutes.

**What this is:** First of four alignment-funnel builds. Make the stack map tell the truth about where Claude can run and reach, and make Charles's corrections land at their source the same day.
**What I'll do (build chat):** the six steps below.
**What you'll do:** nothing.

## Asked for — Charles, 2026-11-12 (frozen; as recorded in the handoff note TH-199)
> Goal: "tech work abides by his preferences and his stack without him in the middle. Not every chat can be forced; the target is that everything scoped and built passes the stack experts, R&D shows him honest paths, and his corrections become standards within a day." Accepted earlier in that chat: "same-day capture of his corrections."

## Current state going in (checked 2026-11-12)
- **[verified]** `concepts/stack-map.md` lanes (lines 162–236 at cbrain 52e9f75): the chat row says "from phone or web the PC is not reachable"; it has no network line; the scheduled row has no helpers line and says reach is "only what was declared at creation: its connector list"; there is no row or part for lab-run; no PC hardware anywhere.
- **[verified]** TH-195: lab-run.yml on arch-renders (d97b6b9) is hand-started, runs `lab/<job>/run.sh` on a GitHub-hosted machine; run 43139228081 reached OpenAI, Google AI, Black Forest Labs, Hugging Face, Runpod, Meshy, fal and Replicate (eight tested); the chat workspace is refused by all eight and reaches GitHub including Releases.
- **[verified]** TH-194: the PC answered from a phone-started chat with zero folders attached; without a folder the PC shell refuses to run. The "folder requests refused unless Charles's message names the folder" rule was read in approval text, not tested.
- **[verified]** EB-072 (2026-11-06) and night-run step 4: the Night builds session starts helpers; the builder helper it starts has no Agent tool. Other scheduled tasks are unproven (CB-600: each task's tool set differs).
- **[verified]** EB-101: a task's connector list is not what its runs can reach.
- **[verified]** TH-170: PC is a laptop, Intel i7-10850H, NVIDIA Quadro T2000 with 4 GB graphics memory (rules out image models needing 8 GB or more).
- **[verified]** Runpod spend approvals TH-171/TH-172 were superseded by TH-201/TH-202 in the design chat (Runpod out, TH-195).
- **[verified]** Today a correction from Charles reaches a standard about a week later at best: lens-notes fold Sunday (Expert CE), the charter is edited by hand, and the step-in scorer reads one Project weekly (TH-197). Team Builder update mode folds every waiting note; it has no way to fold only some.
- **[assumed]** Private-repo Actions minutes left this cycle: unknown; no tool reads the level (the meter only detects a lock, CB-550).

## Scope
**In:** lane rows and the Lab run part; the corrections rule; Team Builder `only:`; the night fold step; the step-in scorer's dedupe.
**Out:** night-build seats (Build 83); R&D rules and lab-run.yml changes (Build 84); the Stack Advisor (Build 85); rotating or deleting the Runpod-stored GitHub key (governance, parked); Projects whose instructions don't fetch AGENT.md (a paste only Charles can make; not asked).

## Directive
1. **Lane rows** (cbrain main, `concepts/stack-map.md`; anchored `replace_in_file` on the smallest unique anchor, `[skip ci]` on every commit but the last; read each back by blob SHA from the `concepts/` listing and a size check, then `get_entity('stack-map')` parses, then `rebuild_index`):
   - chat: add `network:` "claude.ai Project chat workspace (environment cloud_default), tested 2026-11-11: refused by OpenAI, Google AI, Black Forest Labs, Hugging Face, Runpod, Meshy, fal, Replicate; GitHub (incl. Releases) answers; package registries inferred, not timed [TH-193, TH-195]". Replace the phone clause in `reach:` with "from a phone-started chat the PC answered, but its shell refuses to run with no folder connected [TH-194]; a folder request is refused unless Charles's message names the folder (read in the approval text, not tested)". Re-word `changes_mid_run` to drop the claim TH-194 contradicts. Update `verified:` with the date and surface.
   - scheduled: add `helpers:` "Night builds: yes, proven 2026-11-06 [EB-072]; the builder helper it starts cannot start helpers [EB-188]. Other tasks: unproven — prove it from the task that will use it [CB-600]". Replace the connector-list sentence in `reach:` with "its connector list is not its reach; check what a run actually did [EB-101]".
   - scheduled-pc: add `hardware:` "Laptop, Intel i7-10850H, NVIDIA Quadro T2000 4 GB; rules out image models needing 8 GB or more [TH-170, TH-068]". Complete next move TH-170.
   - github-action: widen `label`/`reach` to say who starts it (a schedule, a push, by hand, or a chat's `run_workflow`) and that lab-run reached the eight vendor hosts above (2026-11-11, run 43139228081); add `meter: github-actions — private-repo minutes from a 3,000-minute monthly pool shared with world-graph; level unreadable; locked once (CB-550)`.
   - No Runpod row anywhere.
2. **Lab run part** (Stack Flow): under the Chats dot's `made_of`, add "Lab run" — lane `github-action`, lives arch-renders `.github/workflows/lab-run.yml`, runs_on GitHub-hosted machine, thinks_with no AI, started by a chat's `run_workflow`, saves_to `lab/<job>/out` in arch-renders, pays_with github-actions, plus a plain `story`. Add the line Chats → GitHub if missing. Side-panel text in plain words.
3. **The corrections rule** (agent-library `AGENT.md`): extend the existing "Every chat, every message — experts" section with one paragraph; no new section:
   > **Charles's corrections.** When Charles corrects how Claude worked or says how he wants something done from now on, the chat, in the same turn: (1) logs one Project State decision on the work's project, tagged `charles-directed` and `charles-correction`, quoting his words with the chat link; (2) applies it at its source, citing that decision: a skill it names → that skill is edited now (version bump, changelog line); a rule for all work → `references/charter.md`, replacing the line it overrides in place, his words quoted, the replaced line named in the decision; judgment inside one expert's corner → one `lens-note` for that expert on `expert-bench`, citing the decision. Applying his stated words needs no seat. Two of his decisions that clash: ask him in the chat, now. A chat without Project State or GitHub says so in one line and files nothing.
4. **Team Builder `only:`** (`skills/team-builder/SKILL.md` update mode): accept `only: <note ids or a tag>`; with it, sort and fold only those notes; without it, unchanged. Version bump, changelog.
5. **Night fold step** (`skills/night-run/SKILL.md`, new step 6b after the build loop, before step 7, inside the 05:00 rule): (a) find decisions tagged `charles-correction` created since the last night's `night-start` row (all projects, exact tag); for each that replaced a charter line, grep agent-library `experts/*/BRIEF.md`, `skills/`, `AGENT.md` for the replaced line's words or its decision id and file one `lens-note` per hit citing the new decision; (b) one helper runs Team Builder update mode with `only:` the day's `lens-note`s whose text cites a `charles-correction` decision; (c) file one note on total-harness tagged `night-fold`: "fold: N notes, M briefs changed", then the note and commit list. Nothing reaches Charles. If the helper fails, the notes stay waiting for Sunday's fold.
6. **Step-in scorer dedupe** (`skills/step-in-scorer/SKILL.md` S4): a step-in whose chat link matches a `charles-correction` decision counts as already on record; never filed twice.

## Acceptance
1. The four lane rows read as in step 1 on cbrain main; `get_entity('stack-map')` parses; the index rebuilt; TH-170 completed.
2. The Lab run part shows on the Chats dot with lane github-action and pays_with github-actions.
3. AGENT.md's experts section carries the corrections paragraph (one paragraph, no new section).
4. A dry fold with `only:` on one test lens-note (filed, then folded, then its brief line reverted by a forward commit) touches only that note.
5. night-run step 6b and step-in-scorer S4 read as above; both version-bumped.

## Decisions
- [Charles] Same-day capture of his corrections (TH-199 item 6).
- [Claude-per-doctrine] One record per correction (a decision); copies cite it. Seats: data-homes. Ruled out: lens-note as the only record (sort (e) needs a record to prove against).
- [Claude-per-doctrine] Apply at the source — skill, charter or expert — not experts only. Seat: ai-system-design ("experts judge, skills execute", TH-135).
- [Claude-per-doctrine] Expert folds run in the night session, not in the chat: chats load no extra skill, and the night session has helpers. Within a day meets the goal. Seats split (data-homes same turn, ai-system-design overnight).
- [Claude-per-doctrine] A charter change sweeps the lines that copy it. Seat: data-homes.
- [Claude-per-doctrine] lab-run is a part on the github-action lane, not a lane of its own. Seat: lanes.
- Ruled out: a corrections inbox (one more place to read); keying charter edits on trigger words (EB-092).

## Pasteable prompt
> Build 82 — execute Build Brief BB-2026-11-12-funnel-facts-capture. Pull the plan from Project State (plan_id 94089c3e-a977-461e-8c41-5590c1623ef1, project total-harness, status queued — set it to running when you claim it). Git copy at Chooch333/agent-library/docs/design/BB-2026-11-12-funnel-facts-capture.md. Follow the brief's fork-handling rules: answer forks autonomously with judgment-call tags; escalate only at hard gates (none in this brief).
