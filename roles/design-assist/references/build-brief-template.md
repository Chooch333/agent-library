# Build Brief (draft) — BB-{YYYY-MM-DD-slug}
*Updated: {YYYY-MM-DD} · Turn {N} · Living artifact — rewritten each update, current state only.*

> This is the Design Assist living-artifact form of the PROTOCOL.md Build Brief. It wraps the protocol's seven fields (unchanged, marked ●) and adds DA working sections that collapse away when the brief goes build-ready. A brief created here ships in standard PROTOCOL.md form.

## Completeness gate

> Gate content per `references/brief-completeness-framework.md` (the eleven decision domains + three-state rule). Fetch it alongside this template at intake.

| # | Gate | Status |
|---|------|--------|
| 1 | Goal restated (incl. goal behind the goal); Charles confirmed | ⬜ |
| 2 | Scope walls — in and out both populated; common forks pre-answered | ⬜ |
| 3 | Zero open forks — answered or defaulted with logged rationale | ⬜ |
| 4 | Inputs verified-by-checking, or explicitly gated with named access | ⬜ |
| 5 | Every needed skill/schema/prompt/config exists in draft, linked or inline | ⬜ |
| 6 | Directive prescriptive, MCP-first — tool + parameters per step | ⬜ |
| 7 | Acceptance criteria concrete and testable | ⬜ |
| 8 | Assumptions contain only genuinely unverifiable items | ⬜ |
| 9 | Return contract — receiving chat, Session Log expectation, Brief ID | ⬜ |
| 10 | Pasteable prompt written | ⬜ |
| 11 | All 11 decision domains Answered / Defaulted / N-A — none silent; domain status table in brief body (see `references/brief-completeness-framework.md`) | ⬜ |

---

**● What this is:** {one-line summary of the task}

**● What I'll do:** {what the receiving chat is expected to produce}

**● What you'll do:** {approve the Brief, paste it, any context-setting}

---

## ● Current state going in

{narrative — what this chat knows that matters. Confidence labels required: **[verified]** / **[assumed]** / **[draft]**}

## ● Receiving chat

{named sub-chat, or "new chat to be opened"}

## ● Scope

**In scope:** {…}

**Out of scope:** {…; common forks pre-answered}

## ● Directive

{do X, return Y in format Z — prescriptive; each step names its MCP tool and parameters}

> **Runtime default (software briefs).** Any step that creates or touches a Node project sets `"engines": {"node": "24.x"}` in its `package.json` — a pinned major, never `20.x` (Vercel stops building Node 20 on 2026-10-01) and never an open-ended `>=` range (it silently jumps to each new major) — and `node-version: 24` in any GitHub Actions workflow it adds or edits. Revisit when Node 24 nears end of life (April 2028). *(Charles, 2026-09-24.)*

## ● Inputs

{files, links, DB entries, prior decisions — each marked [verified] or [gated: access needed]}

## Acceptance criteria

{concrete, testable "done well" statements — drafted by end of Phase A. Number each criterion — the done-receipt's acceptance array references these numbers directly (criterion 1 → `{n: 1, ...}`, criterion 2 → `{n: 2, ...}`, etc.).}

1. {criterion}
2. {criterion}
3. {…}

## ● Pasteable prompt

{exact first-message text}

---

# Working appendix (DA only — collapses at build-ready)

## Decisions made
- **{Decision}** — {why, one line}. *(reasons stay so settled questions aren't relitigated)*

## Forks (open)
{Batched. Each: closed choice · recommendation · cost of choosing wrong · consequence trail ("path A requires X, Y, Z; path B skips X, Y but requires Z then A & B"). Empty at build-ready.}

## Gated items
{Verification blocked on access. Each names the exact access needed and what happens the moment it's granted. Empty at build-ready.}

## Assumptions
{Genuinely unverifiable only — each with what would eventually confirm it. A checkable claim here is a defect.}

## Out of scope (working)
- {Excluded thing} — {one-line reason}.

---

**Completeness report (end of every turn):** {gates green} · {turned green this turn} · {single thing closing the biggest remaining gap}
