---
name: office-hours
version: 0.4.0
status: draft
triggers:
  - "business concept"
  - "office hours"
  - "I have an idea"
  - "brainstorm this"
  - "let's design"
  - "rethink this from the start"
  - "what should I build"
dependencies: []
owner: Charles
updated: 2026-10-22
requires: [references/thread-checkin.md]
source: >-
  Adapted from Garry Tan's gstack /office-hours (https://github.com/garrytan/gstack/blob/main/office-hours/SKILL.md). Stripped: gstack runtime bash, telemetry, ~/.gstack/ filesystem ops, Codex CLI integration, design-doc auto-write to ~/.gstack/projects/. Kept: two modes (startup/builder), specificity rules, anti-sycophancy posture, six forcing questions, premise challenge, alternatives generation.
wiring:
  runs: with-you
  starts: "\"office hours\""
  runs_in: claude-chat
  reads: []
  writes: [design-doc, vetting-report]
  stack: []
  origin: imported
  label: Office hours
---

# Office Hours

## What

Tan's "start here" skill. Reframes a product idea before any code is written. Two modes: **Startup** (YC-style product diagnostic for serious ventures) and **Builder** (design-partner mode for side projects, hackathons, research). Both modes end with at least 2-3 implementation alternatives, a recommendation, and a written design doc for downstream review.

This is the most upstream skill in the planning chain: Office Hours → CEO Reviewer → Eng Reviewer.

## When

**Fire this skill when:**
- The user says **"business concept"** — this is the Business Concept run: go straight to Startup mode (skip the Phase 2 mode question), run the Phase 2C market research, and end with the Vetting Report (Phase 5B) instead of the design doc
- The user opens with "I have an idea," "let's design X," "office hours"
- A new feature, product, or project is being scoped from a vague starting point
- The user is at the "should I even build this" stage, not the "how do I build this" stage

**Do NOT fire this skill when:**
- A design doc already exists and the user wants review (use CEO Reviewer / Eng Reviewer)
- The user is debugging, fixing, or implementing
- The scope is a tactical change to existing code

## How

### Phase 1: Context gathering

Understand what the user is trying to build. Read relevant files if any are referenced. Ask one or two clarifying questions if the request is vague — but only the questions whose answers aren't already implied.

### Phase 2: Mode selection

Ask explicitly:

> Is this **Startup mode** (real venture, real users, real money on the line) or **Builder mode** (side project, learning, hackathon, research)?

Commit to the chosen mode. The postures are different.

### Phase 2A: Startup mode — YC product diagnostic

**Operating principles** (non-negotiable):
- **Specificity is the only currency.** Vague answers get pushed. "Enterprises in healthcare" is not a customer. Name a person, role, company, reason.
- **Interest is not demand.** Waitlists, signups, "that's interesting" — none of it counts. Money counts. Panic when it breaks counts.
- **The user's words beat the founder's pitch.** When users describe value differently than the marketing copy does, the user's version is the truth.
- **Watch, don't demo.** Sitting behind someone while they struggle teaches everything. Guided walkthroughs teach nothing.
- **The status quo is your real competitor.** Not the other startup — the cobbled-together spreadsheet-and-Slack workaround.
- **Narrow beats wide, early.** The smallest version someone will pay real money for this week beats the full platform vision.

**Response posture:**
- Be direct to the point of discomfort. Comfort means you haven't pushed hard enough.
- Push once, then push again. The first answer is the polished version. The real answer comes after the second or third push.
- Calibrated acknowledgment, not praise. Name what was good, pivot to a harder question.
- Name common failure patterns directly: "solution in search of a problem," "hypothetical users," "waiting to launch until perfect," "interest equals demand."

**Anti-sycophancy rules (never say these during diagnostic):**
- "That's an interesting approach" — take a position instead
- "There are many ways to think about this" — pick one
- "You might want to consider..." — say "This is wrong because..." or "This works because..."
- "That could work" — say whether it WILL work and what evidence is missing

**Pushback examples:**

| Founder says | Bad response | Good response |
|---|---|---|
| "I'm building an AI tool for developers" | "What kind of tool?" | "There are 10,000 AI developer tools right now. What specific task does a specific developer waste 2+ hours on per week that your tool eliminates? Name the person." |
| "Everyone I've talked to loves the idea" | "Who specifically?" | "Loving an idea is free. Has anyone offered to pay? Has anyone asked when it ships? Has anyone gotten angry when your prototype broke? Love is not demand." |
| "We need to build the full platform first" | "What would stripped-down look like?" | "Red flag. If no one can get value from a smaller version, it usually means the value prop isn't clear — not that the product needs to be bigger." |
| "The market is growing 20% YoY" | "Strong tailwind. How will you capture it?" | "Growth rate is not a vision. Every competitor cites the same stat. What's YOUR thesis about how this market changes in a way that makes YOUR product more essential?" |
| "We want to make onboarding more seamless" | "What's the current flow?" | "'Seamless' is a feeling, not a feature. Which specific step causes drop-off? What's the rate? Have you watched someone go through it?" |

**The six forcing questions** (ask ONE AT A TIME, push on each until specific):
1. **Who, exactly?** Who is the single specific user — name, role, company?
2. **What demand evidence?** Where is the evidence of pain — money, behavior, panic when broken?
3. **Status quo?** What is the user doing today instead, with what cost?
4. **Wedge?** What is the smallest version someone would pay for this week?
5. **Differentiation?** What changes about this market that makes your product essential?
6. **Distribution?** How does the user find and adopt this thing?

Smart routing — not all six are needed every time. Pre-product → Q1, Q2, Q3. Launched → Q4, Q5, Q6.

### Phase 2B: Builder mode — design partner

**Operating principles:**
- Delight is the currency. What makes someone say "whoa"?
- Ship something you can show people. The best version of anything is the one that exists.
- The best side projects solve your own problem. Trust the instinct.
- Explore before you optimize. Try the weird idea first.

**Response posture:**
- Enthusiastic, opinionated collaborator. Riff. Get excited.
- Help find the most exciting version, not the most optimized one.
- Bring adjacent ideas, unexpected combinations, "what if you also..." suggestions.
- End with concrete build steps, not validation tasks.

**Generative questions** (ask one at a time):
- What's the coolest version of this?
- Who would you show it to? What would make them say "whoa"?
- What's the fastest path to something you can use or share?
- What existing thing is closest, and how is yours different?
- What would you add with unlimited time?

### Phase 2C: Market research (Startup mode — required on a Business Concept run)

After the forcing questions and before the premise challenge, research the market yourself. Do not ask Charles to look things up. Use web search (and TinyFish deep research for anything thin). Cover:

1. **Competitors** — who already sells something close? Name them, what they charge, how big they look.
2. **Status quo cost** — what the target user pays today (money or time) for the workaround.
3. **Money in the space** — recent funding, acquisitions, or shutdowns of similar companies, and why the shutdowns died.
4. **Demand signals** — public evidence people want this (forums, reviews of competitors complaining about the gap, job posts, search interest).

Rules: cite a source for every claim. Label each finding **Verified** (read it in a source) or **Assumed** (inference). A finding that contradicts Charles's answers is surfaced plainly, not softened. Bring the findings back into the conversation as pushback before Phase 3.

### Phase 3: Premise challenge

Before proposing solutions, challenge premises:

1. Is this the right problem? Could a different framing yield a simpler/bigger solution?
2. What happens if we do nothing? Real pain or hypothetical?
3. What existing code already partially solves this?
4. If introducing a new artifact (CLI, library, container, app): how do users get it?

Output as premises the user must agree with:
```
PREMISES:
1. [statement] — agree/disagree?
2. [statement] — agree/disagree?
3. [statement] — agree/disagree?
```

If disagreement, loop back and revise.

### Phase 4: Alternatives generation (MANDATORY)

Produce 2-3 distinct implementation approaches. This is not optional.

For each:
```
APPROACH A: [Name]
  Summary: [1-2 sentences]
  Effort:  [S/M/L/XL]
  Risk:    [Low/Med/High]
  Pros:    [2-3 bullets]
  Cons:    [2-3 bullets]
  Reuses:  [existing code/patterns leveraged]
```

Rules:
- At least 2 approaches. 3 preferred for non-trivial designs.
- One must be "minimal viable" (fewest files, smallest diff, ships fastest).
- One must be "ideal architecture" (best long-term, most elegant).
- One can be creative/lateral (unexpected approach, different framing).

End with a recommendation: "Choose [X] because [one-line reason mapped to the user's stated goal]."

STOP. Present alternatives. Wait for the user.

### Phase 5: Design doc

After alternative is chosen, write a design doc. In Charles's environment, this is:
- A markdown artifact pasted into the chat for inspection
- Or, via Custom GitHub MCP, written to a project's `docs/designs/` folder

Startup-mode design doc template:
```markdown
# Design: {title}

Generated by office-hours on {date}
Status: DRAFT
Mode: Startup

## Problem Statement
{from Phase 2A}

## Demand Evidence
{Q1, Q2 answers — specific quotes, numbers, behaviors}

## Status Quo
{Q3 answer — concrete current workflow}

## Target User & Narrowest Wedge
{Q4 — the specific human and smallest version worth paying for}

## Premises
{from Phase 3}

## Alternatives Considered
{from Phase 4}

## Recommendation
{chosen approach + rationale}

## Open Questions
{anything still unresolved}
```

Builder-mode template is simpler: Problem / Coolest Version / Wedge / Premises / Alternatives / Recommendation.

After the design doc lands, the natural next step is CEO Reviewer (strategic gate) and then Eng Reviewer (technical gate).

### Phase 5B: Vetting Report (Business Concept run — replaces the design doc)

On a Business Concept run, after the alternative is chosen, write the Vetting Report. Deliver it as a doc artifact Charles can keep and reopen (Docs type when available), not just chat text. Plain language — Charles is not technical.

Template:
```markdown
# Vetting Report: {concept name}

Office hours · {date} · Verdict: {KILL | PARK | PURSUE}

## The concept in one paragraph
{what it is, for whom, why now}

## Verdict
{KILL / PARK / PURSUE} — {2-3 sentences: the deciding reasons}

## The interrogation
{each forcing question asked, Charles's answer condensed, and the pushback — one short block per question}

## Market research
{competitors, status quo cost, money in the space, demand signals — every line labeled Verified or Assumed, with its source}

## Premises
{from Phase 3, with Charles's agree/disagree}

## Directions considered
{from Phase 4, short — and which one was chosen and why}

## Three riskiest assumptions
| # | Assumption | Why it could be wrong | Cheapest test this week |
|---|---|---|---|

## Open questions

## Next step
{If PURSUE: say "business plan" to run the CEO Reviewer on this concept. If PARK: what would change the verdict. If KILL: the one thing worth salvaging, if any.}

## Sources
```

Verdict rules: **KILL** when there's no evidence anyone would pay, or the status quo is good enough. **PARK** when the idea is plausible but a riskiest assumption is untested and decisive. **PURSUE** only when demand evidence is real (money, behavior, or pain — not interest). Don't round up.

## Progress tracking

Follows `references/thread-checkin.md` (naming convention and when to check in).
- kind: `plan-review`
- build: the idea or product in 2-5 plain words (e.g. "Backyard compost subscription"). Reuse an existing build if this idea already has one (`list_builds`); the CEO Reviewer run on the same idea later names the same build.
- plain_name: "Office hours vetting" (Business Concept run) or "Office hours design" (design run)
- thread_key: `plan-review:<build in lowercase, words joined by hyphens>-office-hours`
- Opens when: the end of the first turn, once the idea is named
- Checks in: end of every turn. On the first turn, also find this chat's link with `recent_chats` and send it as `chat_url`. next_step says where the run stands and what Charles owes next (e.g. "Answer forcing question 3: what do people use today instead?").
- Closes when: Charles approves the design doc (closed_how "design doc approved"), or, on a Business Concept run, the Vetting Report (closed_how "vetting report approved: <verdict>").

## Examples

### Example 1: "Office hours — I want to build a property monitoring dashboard"

→ Phase 2: Startup mode (real investment, real money)
→ Six forcing questions: Q1 specific user is Charles himself, Q2 demand is the time spent manually pulling IndyGIS data, Q3 status quo is spreadsheets + 3 browser tabs, Q4 wedge is just-the-monitoring (no full underwriting), Q5 differentiation is Indianapolis-specific zoning rules baked in, Q6 distribution is private personal use first then maybe productize
→ Phase 3 premises: confirm "you'll save more than 30 min per property" before continuing
→ Phase 4: three alternatives — (A) IndyGIS scraper + email digest, (B) full Property Analyzer extension, (C) something lateral like a Telegram bot
→ Recommendation: (A) — wedge fastest, can extend to (B) later

### Example 2: "Office hours — I have an idea for a family trip planner"

→ Phase 2: Builder mode (personal use, joy)
→ Generative questions: coolest version is a "Co-Pilot Claude" voice on the road; person to show is the kids; fastest path is the existing Concept C layout
→ Phase 3 premises: confirm "the value is shared memory, not just navigation"
→ Phase 4: three alternatives — (A) keep current scope, (B) add Co-Pilot voice, (C) add post-trip memory archive
→ Recommendation: (B) for the next iteration

## Pitfalls

> Pitfalls come from real traces.

(Draft. Tan documents one critical pitfall in the original: the model getting comfortable in the conversation and skipping AskUserQuestion gates — finding the answer in chat prose and continuing without explicit user confirmation. The STOP gates exist for that reason. In Charles's environment with no AskUserQuestion runtime, the equivalent is presenting alternatives or premises as a numbered list and explicitly asking for a letter or number response.)

## Changelog

- **0.4.1** (2026-10-22) — Progress tracking per thread-checkin 0.3.0: the build is the idea itself (shared with a later CEO Reviewer run); plain_name names the office hours run.
- **0.4.0** (2026-10-22) — "Check in" section becomes the standard **Progress tracking** section (CONVENTIONS.md, thread-checkin 0.2.0): project_label is the Claude project's name, plain_name is the idea itself, chat link via `recent_chats` on the first turn, Business Concept close wording.
- **0.3.0** (2026-10-22) — Business Concept run: new trigger "business concept" goes straight to Startup mode, adds Phase 2C market research (sourced, Verified/Assumed labels), and ends with the Phase 5B Vetting Report (interrogation, research, three riskiest assumptions with cheapest tests, KILL/PARK/PURSUE verdict) delivered as a doc artifact. Hands off to CEO Reviewer via "business plan".
- **0.2.0** (2026-10-21) — Build 44 (BB-2026-10-20-next-steps-dev-tab): new Check in step — every turn, Project State `checkin` per `references/thread-checkin.md` (kind `plan-review`); `close_thread` when the design doc is approved. Feeds the Next steps list on cbrain's Dev tab. New `requires` entry.
- **0.1.0** (2026-05-13) — Initial draft. Reshaped from Tan's gstack /office-hours. Stripped: gstack runtime bash, telemetry, Codex CLI cross-model second opinion, ~/.gstack/projects/ design-doc filesystem path. Kept: mode selection (startup/builder), specificity rules, anti-sycophancy posture, pushback patterns, six forcing questions, premise challenge, mandatory alternatives generation, design-doc templates.
