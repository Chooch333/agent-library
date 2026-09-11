# Build Brief — BB-2026-09-11-investment-review-role

**Git home:** Chooch333/agent-library · `docs/design/BB-2026-09-11-investment-review-role.md`
**Project State plan:** `0aaa7de0-05fa-4d28-8d10-f8cd5d6d64cc` on `misc-builds`

**What this is:** Add an "Investment Review" role to agent-library. A chat opening with **"This is an investment review"** produces one of three standardized outputs — **Theme**, **Fund**, or **Study** — as an HTML artifact in the chat, built from a fixed template, checked against an output completeness framework, and applied to Charles's six-sleeve book.

**What I'll do (receiving chat):** Commit the role skill, three templates, the output completeness framework, and an HTML shell to agent-library; add the AGENT.md routing row; prove the role with one live Fund review delivered as a chat artifact.

**What you'll do:** Paste the handoff prompt into a new build chat. Separately (not a build gate): add the PROTOCOL.md line to the Invest project's instructions.

---

## Current state going in
*Labels: **[verified]** checked 2026-09-11 · **[notes]** from Invest project memory notes, not re-checked*

- **[verified]** No investment role in agent-library (`roles/` has 19 roles, none investment); AGENT.md has no investment trigger.
- **[verified]** `agent-library/docs/design/` exists and holds prior role briefs (stack-advisor, advisor-response-loop).
- **[verified]** Design Assist pattern to copy: `roles/design-assist/SKILL.md` + `references/` with a completeness framework using the three-state rule.
- **[verified]** Claude memory notes are readable account-wide in claude.ai chats; the Invest project's notes (`portfolio-framework`, `principles-and-learnings`, `ways-of-working`) were read from a different project. Build chats in Claude Code cannot read them — conventions are reproduced in Draft A.
- **[verified]** SEC raw 13F filings on sec.gov/Archives are fetchable via web_fetch when a web search surfaces the URL.
- **[verified]** 13F aggregators disagree on the same filer (Atreides: reported AUM and "latest filing" quarter differed across sites) — SEC filing must win for totals.
- **[verified]** stockzoa fund pages are live and search-indexed.
- **[notes]** Conventions the role inherits are written into Draft A (standing rules) and the templates.

## Receiving chat
New build chat (to be opened).

## Scope

**In scope**
- `roles/investment-review/SKILL.md` (Draft A) — S, $0
- `roles/investment-review/references/theme-template.md` (Draft B), `fund-template.md` (Draft C), `study-template.md` (Draft D), `output-completeness.md` (Draft E), `html-shell.html` — S, $0
- AGENT.md: new "Investment" section + routing row + changelog line — S, $0
- One verification run (Fund review, chat artifact) — M, $0

**Out of scope (pre-answered forks)**
- New repo, saved output files, `book.md`, `watchlist.md` — v1 is chat artifacts only.
- cbrain storage and UX viewing of reviews — later build.
- Calendar events or Project State next steps for checkpoints — checkpoints are listed inside the output only.
- Sleeve weights — Book Impact uses holdings and sleeves without weights.
- Trade execution, broker connection, scheduled scanning (Dislocation Scanner's future job), wealth planning, tax, real estate, paid data feeds, automated bull/bear agent panels.
- Any edit to Design Assist, PROTOCOL.md, or other roles ("extend, never modify").
- Editing claude.ai project instructions — only Charles can.

## Directive
1. **Reconcile.** Read live `Chooch333/agent-library` `AGENT.md` and `roles/` (Custom GitHub `get_file_contents`). If `roles/investment-review/` already exists, compare against Drafts A–E and adopt if faithful (lesson C-061); otherwise proceed.
2. **Commit role files** — Custom GitHub `create_or_update_file`, owner `Chooch333`, repo `agent-library`, branch `main`:
   - `roles/investment-review/SKILL.md` ← Draft A verbatim (code block contents)
   - `roles/investment-review/references/theme-template.md` ← Draft B, as a markdown doc with a title and the table
   - `roles/investment-review/references/fund-template.md` ← Draft C including the full F3 spec and illustrative layout
   - `roles/investment-review/references/study-template.md` ← Draft D
   - `roles/investment-review/references/output-completeness.md` ← Draft E
   - `roles/investment-review/references/html-shell.html` ← build it: `<meta name="color-scheme" content="dark">`; background `#131210` hard-coded on `html`, `body`, and the main container, each with `!important`; Fraunces for headings, Inter Tight for body, JetBrains Mono for all numbers and tables (Google Fonts link); amber/cream accent palette; styles for the confidence labels (Verified / Interpretive / Estimated / Inferred as visually distinct badges), status-grouped tables with subtotal rows, a completeness table, and the footer line. Placeholder comments mark where each template section goes.
   - Read every file back and confirm content landed.
3. **Routing row** — Custom GitHub `replace_in_file` on `AGENT.md`: add, under "Active roles" after the "Design shaping" section, a new `### Investment` section with table row: trigger `` `this is an investment review` (case-insensitive, must be in the very first message — mentioning an investment review mid-chat is not an invocation) `` → `roles/investment-review/SKILL.md`. Add a Changelog entry dated 2026-09-11 citing this Brief ID. Read back.
4. **Verification run** — in the build chat, follow the committed `SKILL.md` exactly for: `This is an investment review — fund: Atreides Management, Q2 2026 vs Q1 2026`. Use the source ladder; deliver one HTML artifact built on `html-shell.html`. Check it against every acceptance criterion below and record pass/fail per criterion.
5. **Close** — Session Log on `misc-builds` referencing this Brief ID (include per-criterion results); post each judgment call to the Comms Table (`post_judgment_call`, project `misc-builds`, plan_id of this brief). Do not review your own plan.

## Inputs
- This brief (Project State plan above; git copy above) **[verified]**
- `agent-library/roles/design-assist/references/brief-completeness-framework.md` — pattern reference **[verified]**
- Book context at review run time: Invest memory note `portfolio-framework` (claude.ai chats only) **[verified readable]**

## Acceptance criteria
1. `AGENT.md` row reads back correctly and its path resolves to the committed `SKILL.md`.
2. Per the skill, "This is an investment review" with no type → exactly one closed question (Theme / Fund / Study).
3. The verification output follows the Fund template section-for-section; its completeness table marks every domain Answered, N-A (with reason), or Gated (source tried). None silent.
4. The Before/After table places every position in exactly one status group — New, Exited, Increased, Decreased, Unchanged — with before and after share counts, values, and portfolio weights side by side; status set by share count only.
5. Every number carries one of the four confidence labels; summary-strip totals cite the SEC cover pages.
6. Book Impact names overlapping holdings and their sleeves (or is marked Gated if memory notes are unreadable in the build environment).
7. HTML renders with the dark background (hard-coded rules present); checkpoints appear as a dated list; no calendar, file, or database writes from the review itself.

## Fork handling and hard gates
Answer forks autonomously using the design intent narrative; log each as a judgment call. Hard gates: **none in this brief** — no credentials beyond existing GitHub MCP access, no real money, no destructive changes.

## Domain status

| Domain | State | Where |
|---|---|---|
| 1 Purpose & users | Answered — personal tool, Charles only | What this is |
| 2 Acceptance criteria | Answered | §Acceptance |
| 3 Runtime | Defaulted — claude.ai chat, on demand, no infra | §Scope |
| 4 Data — schema | Answered — output templates | Drafts B–E |
| 5 Storage & recall | Answered — no storage; prior reviews recalled via past-chat search | Draft A |
| 6 Interconnectivity | Answered — GitHub (skill fetch), web, memory notes read-only | §Directive |
| 7 Access & hard gates | Answered — none | §Fork handling |
| 8 Skills & tools | Answered — Custom GitHub MCP, web_search/web_fetch | §Directive |
| 9 Build sequence | Answered — reconcile → files → routing → verify → close | §Directive |
| 10 Assumptions & risks | Answered | §Assumptions |
| 11 Design intent | Answered | below |

## Design intent narrative
This is Charles's investment discipline in a box, not a sell-side report generator. Prefer fewer names with a full rubric over long candidate lists; never ship a verdict without a falsifiable claim and kill evidence; cluster risk is the sizing constraint; label every number; a missing data point is written as Gated with the source tried, never smoothed over. For Fund reviews the Before/After comparison is the centerpiece — status comes from share counts, never dollar values, because value moves with price. Outputs are chat artifacts for now; don't build storage. Plain English, dense tables, no filler. Charles is not technical — the output must read cleanly to him.

**Decisions behind the shape (reasons kept so they aren't relitigated):**
- Study = focused question ending in a position decision on specific names or a setup — keeps the template tight. [Charles]
- Chat artifacts only; cbrain + UX viewing later. [Charles]
- Checkpoints listed only — no events or database writes. [Charles]
- No sleeve weights. [Charles]
- Fund reviews built around a Before/After table grouped New / Exited / Increased / Decreased / Unchanged. [Charles]
- Unchanged positions capped to After top 20 for filers with 50+ positions; options on their own rows; holdings read from Invest memory notes. [Charles-approved]
- Status from share count, split-adjusted. [Claude-per-doctrine]
- Prior-review comparison via past-chat search (only recall path without storage). [Claude-per-doctrine]
- Three types share the ending: Book Impact, Rubric, Checkpoints. [Claude-per-doctrine]
- SEC filing primary for Fund totals; aggregators verified to disagree. [Claude-per-doctrine]
- Analysis-not-advice footer. [Claude-per-doctrine]

## Assumptions
- Invest memory notes reflect current holdings — only Charles's broker screen confirms.
- Past-chat search is enabled where reviews run — confirmed the first time a review runs there.
- stockzoa and search-surfaced SEC URLs stay reachable — checked each run by the source ladder.

---

# Drafts

## Draft A — `roles/investment-review/SKILL.md`

```markdown
---
name: investment-review
version: 0.1.0
status: draft
triggers:
  - "this is an investment review"
owner: Charles
updated: 2026-09-11
source: Designed in a Design Assist chat 2026-09-11 (BB-2026-09-11-investment-review-role).
---

# Investment Review

## What
Produces one standardized investment output — Theme, Fund, or Study — as an
HTML artifact in the chat, applying Charles's six-sleeve framework and standing
rules, and ending in a decision against his book.

## When
Fire when the first message contains "this is an investment review"
(case-insensitive). Mentioning an investment review mid-chat is not an invocation.

## Output types
- **Theme** — a structural shift and how to express it.
  Template: references/theme-template.md
- **Fund** — one 13F filer, current quarter vs prior quarter (or two quarters
  Charles names). Template: references/fund-template.md
- **Study** — a focused question that ends in a position decision on specific
  names or a setup (single name, pair comparison, sleeve rubric check).
  Template: references/study-template.md

## Run sequence
1. **Classify.** Read type + subject from the first message. If type is missing
   or ambiguous, ask ONE closed question (Theme / Fund / Study) and stop.
2. **Load context.** Read the Invest memory notes (portfolio-framework,
   principles-and-learnings) for holdings, sleeves, and rules — label them
   [notes]. Search past chats for a prior review of this subject; if found,
   state what changed. If none found or search unavailable, mark
   "what changed" N-A with the reason.
3. **Research.** Use the type's source ladder. Every figure gets a date and
   one confidence label.
4. **Draft** section-for-section from the template. No sections added or
   dropped — non-applicable sections are written N-A with a reason.
5. **Completeness check** against references/output-completeness.md. Fix gaps;
   anything still missing is Gated with the source tried.
6. **Deliver** one HTML artifact built on references/html-shell.html.
   Checkpoints are listed in the output only — no calendar events, no
   database writes, no files saved.

## Source ladders
- **Fund:** SEC filing via a search-surfaced sec.gov/Archives URL for both
  quarters (cover page totals + entry count authoritative) → stockzoa full
  table → 13f.info / chartinsight top-10 cross-check. Filings about two weeks
  old or newer may not be syndicated yet. When sources disagree, the SEC
  filing wins; say so.
- **Theme:** company filings and earnings materials, industry data, credible
  press; tracked-filer positioning.
- **Study:** latest 10-Q/10-K and earnings call, valuation data, share count
  history, lockup/float events.
- **Price authority:** Charles's broker screen overrides all sources. When
  searching, use the freshest-dated source and state its date.

## Standing rules
1. Cluster ≠ diversification — names selling into the same budget line are one bet.
2. Sleeve 6 entries require all four: sector-wide drawdown; top-1-or-2
   fundamentals; written falsifiable claim with exit trigger; 12–18 month time
   stop. Single-name multiple compression does not qualify.
3. Every Act or Watch verdict carries a falsifiable claim + kill evidence.
4. 13F position status comes from share counts, never dollar value. Classify
   each change: real capital / price-only / disclosure artifact. Flag
   denominator distortion.
5. Wrapper risk: treasury-wrapper equities carry dilution and negligible
   operating revenue — say so when relevant.
6. Pyramiding vs averaging down depends on sleeve; check size vs sleeve cap
   before any add schedule.
7. Confidence labels: Verified / Interpretive / Estimated / Inferred.
8. Footer: "Analysis against Charles's own framework — not personalized
   financial advice. Broker screen governs prices; CPA governs tax."

## Pitfalls
- Aggregator staleness and disagreement (verified 2026-09-11 on Atreides).
- 13F value units differ across filing eras — read the unit on each filing.
- Stock splits between quarters make a flat position look like a huge add —
  split-adjust before assigning status.
- Theme reviews drifting into candidate lists with no rubric.

## Changelog
- **0.1.0** (2026-09-11) — Initial draft per BB-2026-09-11-investment-review-role.
```

## Draft B — `references/theme-template.md`

| § | Section | Content rule |
|---|---|---|
| T0 | Header | Theme · date · price as-of · prior review (if found) · confidence legend |
| T1 | Bottom line | ≤3 sentences: Build / Hold / Trim / Avoid the theme, which sleeve(s), what changed |
| T2 | The shift | One paragraph: what's structurally changing, why now |
| T3 | Bottleneck map | Table — chain layer · what's scarce · who controls it · pricing power (H/M/L) · public expressions |
| T4 | Timing | Adoption stage; catalyst calendar (date · event · confirms/kills); priced-in read (drawdown from highs, multiple vs 5-yr range) |
| T5 | Expressions | Table — ticker · layer · mkt cap · valuation metric · % off 52w high · exposure purity · sleeve fit · Act/Watch/Pass |
| T6 | Smart-money check | Which tracked filers are in or out |
| T7 | Book impact | Holdings already in theme; cluster overlap with other themes |
| T8 | Rubric | Per Act/Watch name: falsifiable claim · kill evidence · entry tranches · valuation exit · time stop |
| T9 | Anti-thesis | Strongest case against; what would change the call |
| T10 | Checkpoints | Dated list |
| T11 | Sources + completeness | |

## Draft C — `references/fund-template.md`

| § | Section | Content rule |
|---|---|---|
| F0 | Header | Filer · CIK · Before quarter → After quarter · filed dates · source ladder used |
| F1 | Bottom line | One paragraph: what the manager did and the read-through for Charles |
| F2 | Summary strip | Before vs After: reported value · position count · top-10 concentration. Counts: New · Exited · Increased · Decreased · Unchanged. Verified from SEC cover pages |
| F3 | Before / After comparison | The centerpiece table — spec below |
| F4 | Portfolio shape | Theme concentration before vs after; turnover estimate |
| F5 | Read-through | Themes leaning in/out; named confirmations or conflicts with Charles's theses |
| F6 | Book overlap | Shared names and their sleeves |
| F7 | Study candidates | Names worth a Study — no verdicts |
| F8 | 13F limits applied | Days of lag; long-only US; options shown as underlying; no cash, shorts, non-US, or directly held crypto |
| F9 | Checkpoints | Next filing due date; any 13D/G to watch |
| F10 | Sources + completeness | |

### F3 spec — Before / After comparison table

**Columns:** Ticker · Before shares · Before value · Before % of portfolio · After shares · After value · After % of portfolio · Share change · Signal

**Grouped by status, in this order, each with a subtotal row:**
1. **New** — zero shares before, shares after
2. **Exited** — shares before, zero after
3. **Increased** — more shares after
4. **Decreased** — fewer shares after
5. **Unchanged** — identical share count (value change is price-only). For filers with 50+ positions, show only unchanged positions in the After top 20 by value, plus a "+N other unchanged" line.

Within each group, sort by After value (Exited: by Before value).

**Rules**
- Status comes from share count only. Dollar value never sets status.
- Split-adjust Before shares when a split happened between quarters; note it in the Signal column.
- Options (PUT/CALL) get their own rows, labeled, never merged with common stock.
- Signal values: *Real capital* (share count moved) · *Price-only* (unchanged shares) · *Disclosure artifact* (position newly reportable — shown under New but flagged).
- If one large New position distorts After weights, flag "denominator distortion" on the summary strip and don't read weight changes as conviction changes.

**Illustrative layout (placeholder tickers, not real data)**

| Ticker | Before sh | Before $ | Before % | After sh | After $ | After % | Δ shares | Signal |
|---|---|---|---|---|---|---|---|---|
| **New** | | | | | | | | |
| AAA | — | — | — | 1.2M | $190M | 4.1% | new | Real capital |
| **Exited** | | | | | | | | |
| BBB | 800K | $95M | 2.3% | — | — | — | exited | Real capital |
| **Increased** | | | | | | | | |
| CCC | 500K | $60M | 1.5% | 900K | $120M | 2.6% | +80% | Real capital |
| **Decreased** | | | | | | | | |
| DDD | 3.0M | $410M | 10.0% | 1.1M | $170M | 3.7% | −63% | Real capital |
| **Unchanged** | | | | | | | | |
| EEE | 2.0M | $300M | 7.3% | 2.0M | $360M | 7.8% | 0% | Price-only |

## Draft D — `references/study-template.md`

| § | Section | Content rule |
|---|---|---|
| S0 | Header | Question verbatim · names · date · price as-of · prior review (if found) |
| S1 | Bottom line | Act / Watch / Pass · sleeve · one-sentence why |
| S2 | Business snapshot | What it sells, how it earns. Table — revenue growth · margin · FCF · net cash/debt · share count trend (3 yr) |
| S3 | Thesis & variant view | Market believes / we believe / why we could be right |
| S4 | Valuation | Multiple vs 5-yr range and peers; what's priced in; bear/base/bull table (key assumption · implied value) |
| S5 | Sleeve gate check | Target sleeve's entry rules, each pass/fail with evidence |
| S6 | Structure risks | Dilution · float events (lockups, in-kind distributions) · wrapper · capital stack · deal-break |
| S7 | Comparison | Side-by-side when 2+ names; otherwise N-A |
| S8 | Book impact | Sleeve fit; cluster overlap with current holdings |
| S9 | Rubric | Falsifiable claim · kill evidence = exit trigger · entry tranches · valuation exit · time stop |
| S10 | Counter-case | Best bear argument |
| S11 | Checkpoints | Dated list |
| S12 | Sources + completeness | |

## Draft E — `references/output-completeness.md`

Every output marks each domain **Answered**, **N-A** (one-line reason), or **Gated** (data unavailable — name the source tried). Silence is a defect.

| # | Domain | Theme | Fund | Study |
|---|---|---|---|---|
| 1 | Question, type, as-of date | T0 | F0 | S0 |
| 2 | Price & data freshness | T4/T5 | F2 | S4 |
| 3 | Facts with confidence labels | T3–T5 | F2–F3 | S2 |
| 4 | Thesis / read-through | T2 | F5 | S3 |
| 5 | Falsifiable claim + kill evidence | T8 | N-A unless F7 escalates | S9 |
| 6 | Valuation / what's priced in | T4 | N-A | S4 |
| 7 | Timing & catalysts | T4 | F9 | S11 |
| 8 | Structure risks | T5 | F8 | S6 |
| 9 | Book impact (sleeve, cluster) | T7 | F6 | S8 |
| 10 | Rubric (entry / exit / time stop) | T8 | N-A | S9 |
| 11 | Counter-case | T9 | F5 | S10 |
| 12 | Checkpoints listed + what changed since prior review | T10 | F9 | S11 |

## Pasteable prompt
> Execute Build Brief BB-2026-09-11-investment-review-role. Pull the plan from Project State (plan_id 0aaa7de0-05fa-4d28-8d10-f8cd5d6d64cc, project misc-builds, status queued — set it to running when you claim it). Git copy at Chooch333/agent-library/docs/design/BB-2026-09-11-investment-review-role.md. Follow the brief's fork-handling rules: answer forks autonomously with judgment-call tags; escalate only at hard gates (none in this brief). Do not edit Design Assist, PROTOCOL.md, or any other role.
