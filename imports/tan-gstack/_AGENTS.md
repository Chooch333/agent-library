# gstack — AI Engineering Workflow

> **Imported from https://github.com/garrytan/gstack (MIT License). Preserved for reference.**
> This is Tan's original routing file. Do not modify in place — if you adapt, copy to `roles/`.

gstack is a collection of SKILL.md files that give AI agents structured roles for
software development. Each skill is a specialist: CEO reviewer, eng manager,
designer, QA lead, release engineer, debugger, and more.

## Status Legend (Charles's reshape decisions)

- ✅ **Reshaped** — adapted into `roles/` for Charles's stack
- ⏭️ **Skipped** — not portable to claude.ai or not relevant to Charles's workflow (reason noted)
- ◯ **Available** — not yet reshaped, worth doing later

## Available skills

Skills live in `.agents/skills/` (or `~/.claude/skills/gstack/` on Claude Code).
Invoke them by name (e.g., `/office-hours`).

### Plan-mode reviews

| Status | Skill | What it does | Notes |
|---|-------|-------------|-------|
| ✅ | `/office-hours` | Start here. Reframes your product idea before you write code. | Reshaped → `roles/office-hours/` |
| ✅ | `/plan-ceo-review` | CEO-level review: find the 10-star product in the request. | Reshaped → `roles/ceo-reviewer/` |
| ✅ | `/plan-eng-review` | Lock architecture, data flow, edge cases, and tests. | Reshaped → `roles/eng-reviewer/` |
| ✅ | `/plan-design-review` | Rate each design dimension 0-10, explain what a 10 looks like. | Reshaped → `roles/design-reviewer/` |
| ✅ | `/plan-devex-review` | DX-mode review: TTHW, magical moments, friction points, persona traces. | Reshaped → `roles/devex-reviewer/` |
| ⏭️ | `/plan-tune` | Self-tune AskUserQuestion sensitivity per question. | Skipped — meta-tunes gstack's own runtime config, not relevant to Charles's stack |
| ✅ | `/autoplan` | One command runs CEO → design → eng → DX review. | Reshaped → `roles/autoplan/` |
| ✅ | `/design-consultation` | Build a complete design system from scratch. | Reshaped → `roles/design-consultation/` |

### Implementation + review

| Status | Skill | What it does | Notes |
|---|-------|-------------|-------|
| ✅ | `/review` | Pre-landing PR review. Finds bugs that pass CI but break in prod. | Reshaped → `roles/pr-reviewer/` (git ops adapted to Custom GitHub MCP) |
| ⏭️ | `/codex` | Second opinion via OpenAI Codex. Review, challenge, or consult modes. | Skipped — requires OpenAI Codex CLI, not in Charles's stack |
| ✅ | `/investigate` | Systematic root-cause debugging. No fixes without investigation. | Reshaped → `roles/investigate/` |
| ⏭️ | `/design-review` | Live-site visual audit + fix loop with atomic commits. | Skipped — requires Playwright + browse daemon for live site interaction; static review handled by `roles/design-reviewer/` instead |
| ✅ | `/design-shotgun` | Generate multiple AI design variants, comparison board, iterate. | Reshaped → `roles/design-shotgun/` (text descriptions instead of PNG generation — gstack designer binary unavailable) |
| ✅ | `/design-html` | Generate production-quality Pretext-native HTML/CSS. | Reshaped → `roles/design-html/` (adapted to Next.js + Tailwind; Pretext API tier-routing dropped) |
| ⏭️ | `/devex-review` | Live developer experience audit (TTHW measured against the real flow). | Skipped — requires live runtime to measure TTHW. Plan-mode DX review handled by `roles/devex-reviewer/` |
| ⏭️ | `/qa` | Open a real browser, find bugs, fix them, re-verify. | Skipped — requires Playwright runtime |
| ⏭️ | `/qa-only` | Same methodology as /qa but report only — no code changes. | Skipped — requires Playwright runtime |
| ⏭️ | `/scrape` | Pull data from a web page. First call prototypes; codified call runs in ~200ms. | Skipped — requires gstack browse daemon (Charles has Article Scraper MCP for scraping) |
| ⏭️ | `/skillify` | Codify the most recent successful `/scrape` flow into a permanent browser-skill. | Skipped — depends on /scrape and gstack runtime |

### Release + deploy

| Status | Skill | What it does | Notes |
|---|-------|-------------|-------|
| ✅ | `/ship` | Run tests, review, push, open PR. Workspace-aware version queue. | Reshaped → `roles/ship/` (git ops via Custom GitHub MCP; tests run by Charles locally) |
| ✅ | `/land-and-deploy` | Merge the PR, wait for CI and deploy, verify production health. | Reshaped → `roles/land-and-deploy/` (merge via Custom GitHub MCP, deploy status via Vercel MCP; multi-platform support dropped) |
| ⏭️ | `/canary` | Post-deploy monitoring loop using the browse daemon. | Skipped — requires browse daemon. Lightweight health check is in `roles/land-and-deploy/` Step 7 |
| ⏭️ | `/landing-report` | Read-only dashboard for the workspace-aware ship queue. | Skipped — gstack-specific workspace queue not applicable |
| ✅ | `/document-release` | Update all docs to match what you just shipped. | Reshaped → `roles/document-release/` |
| ⏭️ | `/setup-deploy` | One-time deploy config detection (Fly.io, Render, Vercel, etc.). | Skipped — Charles's deploys are already Vercel-configured |
| ⏭️ | `/gstack-upgrade` | Update gstack to the latest version. | Skipped — N/A, agent-library has its own update model |

### Operational + memory

| Status | Skill | What it does | Notes |
|---|-------|-------------|-------|
| ◯ | `/context-save` | Save working context (git state, decisions, remaining work). | Available — Charles's Project State MCP handles most of this; reshape if a session-level snapshot is wanted |
| ◯ | `/context-restore` | Resume from a saved context, even across Conductor workspaces. | Available — sister to /context-save |
| ⏭️ | `/learn` | Manage what gstack learned across sessions. | Skipped — gstack-specific learnings store; Cheung's Distill meta-skill is the analog Charles will adopt |
| ◯ | `/retro` | Weekly retro with per-person breakdowns and shipping streaks. | Available — strong judgment frame, worth reshaping when wanted |
| ⏭️ | `/health` | Code quality dashboard (type checker, linter, tests, dead code). | Skipped — requires runtime tools |
| ⏭️ | `/benchmark` | Performance regression detection (page load, Core Web Vitals). | Skipped — requires runtime |
| ⏭️ | `/benchmark-models` | Cross-model benchmark for skills (Claude, GPT, Gemini side-by-side). | Skipped — needs multi-model runtime |
| ◯ | `/cso` | OWASP Top 10 + STRIDE security audit. | Available — strong judgment frame, worth reshaping when security work picks up |
| ⏭️ | `/setup-gbrain` | Set up gbrain for cross-machine session memory sync. | Skipped — requires Postgres + pgvector gbrain backend |
| ⏭️ | `/sync-gbrain` | Keep gbrain current with this repo's code; refresh agent search guidance in CLAUDE.md. | Skipped — same as above |

### Browser + agent integration

| Status | Skill | What it does | Notes |
|---|-------|-------------|-------|
| ⏭️ | `/browse` | Headless browser — real Chromium, real clicks, ~100ms/command. | Skipped — requires browse daemon |
| ⏭️ | `/open-gstack-browser` | Launch the visible GStack Browser with sidebar + stealth. | Skipped — same |
| ⏭️ | `/setup-browser-cookies` | Import cookies from your real browser for authenticated testing. | Skipped — same |
| ⏭️ | `/pair-agent` | Pair a remote AI agent (OpenClaw, Codex, etc.) with your browser. | Skipped — same |

### Safety + scoping

| Status | Skill | What it does | Notes |
|---|-------|-------------|-------|
| ⏭️ | `/careful` | Warn before destructive commands (rm -rf, DROP TABLE, force-push). | Skipped — wraps local shell; Charles has no local shell in claude.ai |
| ⏭️ | `/freeze` | Lock edits to one directory. Hard block, not just a warning. | Skipped — local filesystem mechanism |
| ⏭️ | `/guard` | Activate both careful + freeze at once. | Skipped — depends on /careful + /freeze |
| ⏭️ | `/unfreeze` | Remove directory edit restrictions. | Skipped — depends on /freeze |
| ◯ | `/make-pdf` | Turn any markdown file into a publication-quality PDF. | Available — Charles has the PDF skill in claude.ai; reshape only if integrating with PR workflow |

## Reshape summary

- **13 reshaped** — plan-mode reviews (6), implementation/review (4), release/deploy (3)
- **5 available** — `/context-save`, `/context-restore`, `/retro`, `/cso`, `/make-pdf` — worth reshaping if/when needed
- **30 skipped** — mostly runtime-dependent (Playwright, browse daemon, gbrain backend, Codex CLI) or gstack-specific config tooling
