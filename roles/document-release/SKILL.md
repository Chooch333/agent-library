---
name: document-release
version: 0.1.0
status: draft
triggers:
  - "document this release"
  - "update the docs"
  - "documentation sweep"
  - "doc sync"
  - "update docs for what shipped"
dependencies: []
owner: Charles
updated: 2026-05-13
source: Adapted from Garry Tan's gstack /document-release (https://github.com/garrytan/gstack/blob/main/document-release/SKILL.md). Stripped: gstack runtime bash, telemetry, ~/.gstack/ filesystem ops, automatic git diff via shell, doc-discovery via find. Kept: 9-step audit process, auto-update vs ask-user classification, never-auto-update list, file-type heuristics, voice polish for CHANGELOG.
---

# Document Release

## What

Updates all documentation to match what shipped. Audits README, ARCHITECTURE, CONTRIBUTING, CLAUDE.md, and any other markdown files for drift against the diff, applies safe auto-updates, and asks before making narrative-level changes. The goal is documentation that matches reality — not documentation that *almost* matches.

In Charles's environment, doc fetch and update happens through Custom GitHub MCP. The role doesn't open the IDE — it reads and writes files directly.

## When

**Fire this skill when:**
- A PR has merged and docs need to catch up
- The user says "update the docs," "documentation sweep," "doc sync"
- A user-visible change shipped but README/ARCHITECTURE wasn't touched

**Do NOT fire this skill when:**
- The change had zero user-visible surface (pure internal refactor with no doc impact)
- Docs were already updated as part of the original PR
- The user wants to write *new* docs from scratch (different task — design or planning)

## How

### Step 1: Pre-flight & diff analysis

Confirm the work has been merged or is about to be. Gather context:

1. The diff (from PR or commit range) — Custom GitHub MCP `list_pr_files` or `list_commits`
2. The merge commit SHA if applicable
3. List of all documentation files in the repo — `search_code` for `*.md`

Classify changes into doc-relevant categories:
- **New features** — new files, endpoints, commands, capabilities
- **Changed behavior** — modified services, updated APIs, config changes
- **Removed functionality** — deleted files, removed commands
- **Infrastructure** — build system, tests, CI, deploy

Output: "Analyzing N files changed across M commits. Found K documentation files to review."

### Step 2: Per-file audit

Read each doc file. Cross-reference against the diff.

**README.md:**
- Does it describe all features and capabilities visible in the diff?
- Are install/setup instructions still consistent?
- Are examples, demos, usage descriptions still valid?
- Are troubleshooting steps still accurate?

**ARCHITECTURE.md** (if present):
- Do ASCII diagrams and component descriptions match the current code?
- Are design decisions and "why" explanations still accurate?
- Be conservative — only update things clearly contradicted by the diff.

**CONTRIBUTING.md** — new-contributor smoke test:
- Walk through setup instructions as if you're a brand new contributor.
- Are listed commands accurate? Would each step succeed?
- Do test descriptions match current infrastructure?
- Flag anything that would fail or confuse.

**CLAUDE.md / project instructions** (if present):
- Does the project structure section match the actual file tree?
- Are listed commands and scripts accurate?
- Do build/test instructions match package.json?

**Other markdown files:**
- Read the file, determine its purpose and audience.
- Cross-reference against the diff. Does it contradict anything?

For each file, classify needed updates as:

- **Auto-update** — factual corrections clearly warranted by the diff. Examples: adding an item to a table, updating a file path, fixing a count ("N skills" → "N+1 skills"), updating a project-structure tree.
- **Ask user** — narrative changes, section removal, security model changes, large rewrites (>10 lines in one section), ambiguous relevance, adding entirely new sections.

### Step 3: Apply auto-updates

Make all clear, factual updates via Custom GitHub MCP `replace_in_file`.

For each file modified, output one line: **what specifically changed** — not "Updated README.md" but "README.md: added cash-out-refi to feature list, updated table count from 8 to 9 calculators."

**Never auto-update:**
- README introduction or project positioning
- ARCHITECTURE philosophy or design rationale
- Security model descriptions
- Do not remove entire sections from any document

### Step 4: Ask about risky/questionable changes

For each risky update identified in Step 2, ask:

> Context: [project, branch, doc file, what's being reviewed]
> [The specific documentation decision]
> Recommendation: [X] because [reason]
> A) [X]
> B) [alternative]
> C) Skip — leave as-is

Apply approved changes immediately after each answer.

### Step 5: CHANGELOG voice polish

If CHANGELOG.md exists, sweep the latest entry. Apply voice rules:
- Plain English, not jargon ("Added cash-out refinance calculator" not "Implemented CORefiCalc module")
- User-visible framing, not internal ("Fixed slideshow duplicate photos" not "Resolved RNG state bleed in tour-tour.tsx")
- Imperative voice ("Add" not "Added") — match the existing CHANGELOG voice if it's consistent
- Cut redundant words. If "Refactored auth module to use new pattern" can be "Refactored auth module," cut it.

### Step 6: Cross-doc consistency & discoverability check

After all per-file updates:
- Is the new feature mentioned in both README and CHANGELOG?
- If there's a documentation TOC or index file, does it reference any new doc files?
- Are version numbers consistent across README badges, CHANGELOG, package.json?
- If a major feature shipped, is it discoverable from the README (not buried in a sub-doc)?

### Step 7: TODOS.md cleanup (if present)

- Remove TODOs this release completed
- Add TODOs surfaced during the doc sweep (e.g., "README screenshot is stale, regenerate")

### Step 8: VERSION bump question

If VERSION wasn't bumped during ship/, ask now:
- Was this release supposed to bump? (Some doc-only updates legitimately don't bump.)
- If yes: patch / minor / major?

### Step 9: Commit & output

Commit the doc updates via Custom GitHub MCP. Commit message:

```
docs: update for [release version or description]

- [file 1]: [what changed]
- [file 2]: [what changed]
```

Final output: summary of what was updated, what was asked, what was skipped. If there are any remaining doc gaps the role couldn't address (e.g., "Architecture diagram needs to be regenerated — too complex for auto-update"), flag them as follow-up TODOs.

## Examples

### Example 1: "Document the release for the cash-out refi calculator"

→ Step 1: diff has 8 files changed, README + ARCHITECTURE + a new docs/analyzer.md
→ Step 2 audit: README needs feature added, ARCHITECTURE diagram still accurate, docs/analyzer.md needs a refi section
→ Step 3 auto-updates: add refi to README feature table
→ Step 4 ask: should we add a full refi math section to docs/analyzer.md, or keep the README description and skip the deep doc?
→ Step 5 CHANGELOG: polish to "Added cash-out refinance calculator with LTV cap and DSCR feasibility check"
→ Step 9: commit "docs: update for refi calculator release"

### Example 2: "Document the slideshow dedup fix"

→ Step 1: small diff, 1 file changed
→ Step 2 audit: README mentions slideshow but doesn't claim any specific behavior worth correcting; CHANGELOG needs entry
→ Step 3 auto-updates: none needed in README
→ Step 5 CHANGELOG: "Fixed slideshow showing duplicate photos across slides"
→ Step 8 VERSION: patch
→ Step 9: commit "docs: changelog for v0.4.1"

## Pitfalls

> Pitfalls come from real traces.

(Draft. Tan's biggest documented pitfall: auto-updating narrative content. The model sees "the README has outdated framing of what the product is for" and rewrites it. That's not a fix, that's a unilateral product positioning change. The never-auto-update list exists for that reason. Defense: when tempted to rewrite narrative, surface it as an ask-user question, not an auto-update.)

## Changelog

- **0.1.0** (2026-05-13) — Initial draft. Reshaped from Tan's gstack /document-release. Stripped: gstack runtime bash, telemetry, ~/.gstack/ filesystem ops, shell-based git diff and doc-file discovery, persistent metrics. Adapted: file read/edit/commit operations route through Custom GitHub MCP. Kept: 9-step audit, auto-update vs ask-user classification, never-auto-update list, per-file-type heuristics (README, ARCHITECTURE, CONTRIBUTING, CLAUDE.md, others), CHANGELOG voice polish rules, cross-doc consistency check.
