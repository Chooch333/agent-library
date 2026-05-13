---
name: devex-reviewer
version: 0.1.0
status: draft
triggers:
  - "devex review"
  - "DX review"
  - "developer experience review"
  - "review the dev experience"
  - "TTHW review"
dependencies: []
owner: Charles
updated: 2026-05-13
source: Adapted from Garry Tan's gstack /plan-devex-review (https://github.com/garrytan/gstack/blob/main/plan-devex-review/SKILL.md). Stripped: gstack runtime bash, telemetry, ~/.gstack/ filesystem ops, dx-hall-of-fame.md auto-load (the original loaded a separate reference file per pass — preserved as inline notes here). Kept: DX first principles, seven DX characteristics, cognitive patterns, TTHW benchmarks, 0-10 rating method, Step 0 investigation (persona / benchmark / magical moment / friction trace), 8 review passes.
---

# DevEx Reviewer

## What

Plan-mode developer experience review. Evaluates whether the planned tool, API, SDK, CLI, or platform will be a joy or a chore for developers to use. Rates on the 7 DX Characteristics (Usable, Credible, Findable, Useful, Valuable, Accessible, Desirable), measures time-to-Hello-World, and runs 8 review passes covering everything from install friction to migration paths.

Most relevant for: APIs (Property Analyzer's analyze endpoint), MCPs (Custom GitHub, Article Scraper), shared libraries (Family Trip App's tool-use patterns), or any system another developer (including future-you) will integrate with.

## When

**Fire this skill when:**
- The plan involves a tool, API, SDK, CLI, or platform that other developers will use
- The "user" of the thing being built is a developer (or a future Claude session)
- You're considering DX trade-offs (default behaviors, escape hatches, error messages)

**Do NOT fire this skill when:**
- The plan is for end-user product (use design-reviewer instead)
- The plan has no developer interface (pure internal logic with no API surface)
- The change is a tactical fix with no DX surface

## How

### DX first principles (apply throughout)

1. **Zero friction at T0.** First five minutes decide everything. One click to start. Hello world without reading docs. No credit card. No demo call.
2. **Incremental steps.** Never force developers to understand the whole system before getting value from one part.
3. **Learn by doing.** Playgrounds, sandboxes, copy-paste code that works in context.
4. **Decide for me, let me override.** Opinionated defaults are features. Escape hatches are requirements. Strong opinions, loosely held.
5. **Fight uncertainty.** Developers need: what to do next, whether it worked, how to fix it. Every error = problem + cause + fix.
6. **Show code in context.** Hello world is a lie. Show real auth, real error handling, real deployment.
7. **Speed is a feature.** Iteration speed, response times, build times, lines of code to accomplish a task.
8. **Create magical moments.** What would feel like magic? Stripe's instant API response. Vercel's push-to-deploy. Find yours and make it the first thing developers experience.

### The seven DX characteristics

| # | Characteristic | Means | Gold Standard |
|---|---|---|---|
| 1 | **Usable** | Simple install/setup. Intuitive APIs. Fast feedback. | Stripe: one key, one curl, money moves |
| 2 | **Credible** | Reliable, predictable, consistent. Clear deprecation. Secure. | TypeScript: gradual adoption, never breaks JS |
| 3 | **Findable** | Easy to discover AND find help within. Strong community. | React: every question answered on SO |
| 4 | **Useful** | Solves real problems. Features match actual use cases. | Tailwind: covers 95% of CSS needs |
| 5 | **Valuable** | Reduces friction measurably. Saves time. | Next.js: SSR, routing, bundling, deploy in one |
| 6 | **Accessible** | Works across roles, environments, preferences. CLI + GUI. | VS Code: junior to principal |
| 7 | **Desirable** | Best-in-class tech. Reasonable pricing. Community momentum. | Vercel: devs WANT to use it |

### Cognitive patterns

- **Chef-for-chefs.** Your users build products for a living. The bar is high; they notice everything.
- **First five minutes obsession.** Can a new dev hello-world without docs, sales, or credit card?
- **Error message empathy.** Every error: identifies the problem, explains the cause, shows the fix, links to docs.
- **Escape hatch awareness.** No escape hatch = no trust = no adoption at scale.
- **Journey wholeness.** DX is discover → evaluate → install → hello world → integrate → debug → upgrade → scale → migrate. Every gap = a lost dev.
- **Context switching cost.** Every time a dev leaves your tool, you lose them for 10-20 minutes.
- **Upgrade fear.** Clear changelogs, migration guides, codemods, deprecation warnings. Upgrades should be boring.
- **Pit of Success** (Rico Mariani) — make the right thing easy, the wrong thing hard.
- **Progressive disclosure.** Simple case is production-ready. Complex case uses the same API.

### TTHW (Time to Hello World) benchmarks

| Tier | Time | Adoption impact |
|---|---|---|
| Champion | < 2 min | 3-4× higher adoption |
| Competitive | 2-5 min | Baseline |
| Needs Work | 5-10 min | Significant drop-off |
| Red Flag | > 10 min | 50-70% abandon |

### 0-10 scoring rubric

| Score | Meaning |
|---|---|
| 9-10 | Best-in-class. Stripe/Vercel tier. Devs rave about it. |
| 7-8 | Good. Devs can use without frustration. Minor gaps. |
| 5-6 | Acceptable. Works but with friction. Devs tolerate it. |
| 3-4 | Poor. Devs complain. Adoption suffers. |
| 1-2 | Broken. Devs abandon after first attempt. |
| 0 | Not addressed. |

The gap method: For each score, explain what a 10 looks like for THIS product. Then fix toward 10.

### Step 0: DX investigation (before any scoring)

**0A. Developer Persona.** Who is the developer? Name role, company, what they're trying to do today. ("YC founder building MVP" vs "platform engineer at a 500-person company integrating a service mesh.")

**0B. Empathy narrative.** Write a 3-paragraph story: developer arrives at zero knowledge. Walks through install, hello world, first real use. Where do they get stuck?

**0C. Competitive benchmark.** Pick 2-3 competitor or comparable tools. What's their TTHW? Where is the target — Champion, Competitive, Needs Work?

**0D. Magical moment design.** What's the single moment that would make the persona say "whoa, this is great"? When does it happen in the journey? Is the plan delivering it in the first 5 minutes?

**0E. Mode selection** — DX EXPANSION (push every dimension toward 10), DX POLISH (fix every gap, no shortcuts), DX TRIAGE (only flag adoption-blockers, skip nice-to-haves).

**0F. Developer journey trace.** Walk through every step from discover → migrate. Flag friction points.

STOP. Present Step 0 findings. Wait for response.

### Pass 1: Getting Started Experience (Zero Friction)

Rate 0-10: Can a developer go from zero to hello world in under 5 minutes?

Evaluate: installation (one command?), first run (visible meaningful output?), sandbox/playground (try before install?), free tier (no credit card?), quick start guide (copy-paste complete?), auth/credential bootstrapping (how many steps?), magical moment delivery (is the vehicle from 0D in the plan?), competitive gap (how far from target tier?).

Stripe test: Can [persona from 0A] go from "never heard of this" to "it worked" in one terminal session?

Fix to 10. STOP after the pass.

### Pass 2: API/CLI/SDK Design (Usable + Useful)

Rate 0-10: Intuitive, consistent, complete?

Evaluate: naming (guessable without docs?), defaults (every parameter has a sensible default?), consistency (same patterns across surface?), completeness (or do devs drop to raw HTTP?), discoverability (CLI/playground exploration?), reliability/trust (latency, retries, rate limits, idempotency), progressive disclosure (simple case production-ready, complexity revealed gradually).

Test: Can [persona] use this API correctly after seeing one example?

STOP.

### Pass 3: Error Messages & Debugging (Fight Uncertainty)

Rate 0-10: Does every error help the developer fix it?

Evaluate: do errors identify the problem, explain the cause, show the fix, link to docs? Is there a debug mode? Are stack traces actionable? Are logs structured?

STOP.

### Pass 4: Documentation & Learning (Findable + Learn by Doing)

Rate 0-10: Can a developer learn this primarily by doing, not reading?

Evaluate: quickstart leads to working code in 5 min, reference is searchable, examples cover the 80% case, conceptual docs exist for the why, recipes for common tasks, playground for experimentation.

STOP.

### Pass 5: Upgrade & Migration Path (Credible)

Rate 0-10: Is upgrading boring?

Evaluate: changelogs (clear breaking changes section?), migration guides for major versions, codemods for mechanical changes, deprecation warnings with timeline, semver discipline.

STOP.

### Pass 6: Developer Environment & Tooling (Valuable + Accessible)

Rate 0-10: Does the tool fit into developers' existing workflows?

Evaluate: IDE/editor integration, CLI ergonomics, CI/CD support, local dev story, offline capability, env-var conventions.

STOP.

### Pass 7: Community & Ecosystem (Findable + Desirable)

Rate 0-10: Is there an answer to every question within 30 seconds?

Evaluate: Stack Overflow presence, GitHub Discussions activity, Discord/Slack channels, plugin/extension ecosystem, third-party tutorials, blog post density.

For Charles's internal infrastructure (MCPs, agent-library), community is less relevant — but documentation depth and self-service answers still apply.

STOP.

### Pass 8: DX Measurement & Feedback Loops

Rate 0-10: Is DX being measured and improved?

Evaluate: instrumentation of TTHW, NPS/CSAT signals, error rate dashboards, developer survey cadence, feedback channels.

STOP.

## Examples

### Example 1: "DevEx review on the Custom GitHub MCP"

→ 0A persona: Charles in a fresh claude.ai chat, no prior knowledge of the server
→ 0B empathy: arrives at deployed URL, can't tell what endpoints exist, fumbles with tool_search to discover them
→ 0C benchmark: Anthropic's official MCPs are the comparison tier
→ 0D magical moment: "I asked Claude to fetch a file from a repo and it just worked"
→ Pass 1 TTHW: probably 2-3 minutes to first successful tool call after connection — Champion tier
→ Pass 3 errors: do tool failures explain themselves, or do they just say "Failed"?
→ Pass 8 measurement: is there logging on tool-call success/failure rates?

### Example 2: "Review the DX of the property-analyzer API"

→ 0A persona: future-Charles in another chat consuming the API
→ 0C benchmark: Rentometer, Mashvisor — simpler interfaces but worse data
→ 0D magical moment: "I paste an address, the analyzer returns IRR/DSCR/CoC in seconds"
→ Pass 1: is there a curl example in the README that returns a usable response?
→ Pass 2 API design: does the request/response shape match how Charles thinks about properties?
→ Pass 5 upgrade: when zoning ordinance is updated (January 2025 version → next), is the migration path clear?

## Pitfalls

> Pitfalls come from real traces.

(Draft. Tan documents one core pitfall: scoring the plan without doing Step 0 first — produces scores without anchoring evidence. The rule is every rating MUST reference findings from Step 0, e.g., "Getting Started: 4/10 because [persona] hits [friction point from 0F] at step 3.")

## Changelog

- **0.1.0** (2026-05-13) — Initial draft. Reshaped from Tan's gstack /plan-devex-review. Stripped: gstack runtime bash, telemetry, dx-hall-of-fame.md inline-load mechanism, ~/.gstack/ filesystem ops, persona-detection auto-detection scripts. Kept: 8 DX first principles, 7 DX characteristics, cognitive patterns, TTHW benchmarks, 0-10 scoring rubric, Step 0 (persona + empathy + benchmark + magical moment + journey + mode), 8 review passes.
