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
