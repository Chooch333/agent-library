---
name: design-consultation
version: 0.1.0
status: draft
triggers:
  - "design consultation"
  - "design the design system"
  - "create a DESIGN.md"
  - "what should this look like"
  - "design from scratch"
  - "design system kickoff"
dependencies: []
owner: Charles
updated: 2026-05-13
source: Adapted from Garry Tan's gstack /design-consultation (https://github.com/garrytan/gstack/blob/main/design-consultation/SKILL.md). Stripped: gstack runtime bash, gstack designer binary (visual mockup generation), browse binary (competitive research screenshots), taste profile persistence to ~/.gstack/, Phase 5 design preview page generation. Kept: Phase 1 product context + memorable-thing question, Phase 2 three-layer research synthesis, Phase 3 complete proposal with SAFE/RISK breakdown, design knowledge library, AI slop anti-patterns, coherence validation, Phase 6 DESIGN.md output.
---

# Design Consultation

## What

Build a complete design system from scratch through a structured conversation. Output is a `DESIGN.md` file (or equivalent) that downstream design-reviewer can calibrate against. Covers aesthetic, decoration, layout, color, typography, spacing, motion — as one coherent package, not piecemeal. Includes deliberate SAFE/RISK breakdown so the user understands which choices play to category convention and which choices are where the product earns its own face.

## When

**Fire this skill when:**
- A new project or product needs a design direction from scratch
- The user says "design consultation," "create a DESIGN.md," "design the design system," "what should this look like"
- A design review surfaces that no design system exists and one is needed
- Existing UI feels piecemeal and needs a unifying direction

**Do NOT fire this skill when:**
- A DESIGN.md / design system already exists (review or extend it, don't redo it)
- The user wants a single visual decision (font, color), not a whole system
- The product has no visual surface

## How

### Phase 1: Product Context

Ask a single question that covers what's needed. Pre-fill anything inferable from the codebase or prior context:

1. Confirm what the product is, who it's for, what space/industry
2. What project type — web app, dashboard, marketing site, editorial, internal tool
3. Should you research what top products in this space are doing, or work from your design knowledge?
4. Explicit nudge: "At any point you can drop into chat and we'll talk through anything — this isn't a rigid form, it's a conversation."

**Memorable-thing forcing question.** Before moving on, ask:

> "What's the one thing you want someone to remember after they see this product for the first time?"

One sentence answer. Could be a feeling ("this is serious software for serious work"), a visual ("the blue that's almost black"), a claim ("faster than anything else"), or a posture ("for builders, not managers"). Write it down. Every subsequent design decision should serve this memorable thing. Design that tries to be memorable for everything is memorable for nothing.

### Phase 2: Research (only if user said yes)

If competitive research is wanted, use web search to find 5-10 products in the space. Search:
- `[product category] website design`
- `[product category] best websites 2026`
- `best [industry] web apps`

**Three-layer synthesis:**
- **Layer 1 (tried and true):** What design patterns does every product in this category share? Table stakes — users expect them.
- **Layer 2 (new and popular):** What's trending? What new patterns are emerging?
- **Layer 3 (first principles):** Given what we know about THIS product's users and positioning — is there a reason the conventional design approach is wrong? Where should we deliberately break category norms?

**Eureka check:** If Layer 3 reveals a genuine design insight — a reason the category's visual language fails THIS product — name it:
> "EUREKA: Every [category] product does X because they assume [assumption]. But this product's users [evidence] — so we should do Y instead."

Summarize conversationally:
> "I looked at what's out there. They converge on [patterns]. Most feel [observation]. The opportunity to stand out is [gap]. Here's where I'd play it safe and where I'd take a risk..."

If the user said no research, skip Phase 2 entirely and use built-in design knowledge.

### Phase 3: The Complete Proposal

This is the soul of the skill. Propose EVERYTHING as one coherent package with SAFE/RISK breakdown:

```
Based on [product context] and [research / design knowledge]:

AESTHETIC: [direction] — [one-line rationale]
DECORATION: [level] — [why this pairs with the aesthetic]
LAYOUT: [approach] — [why this fits the product type]
COLOR: [approach] + proposed palette (hex values) — [rationale]
TYPOGRAPHY: [3 font recommendations with roles] — [why these fonts]
SPACING: [base unit + density] — [rationale]
MOTION: [approach] — [rationale]

This system is coherent because [explain how choices reinforce each other].

SAFE CHOICES (category baseline — your users expect these):
  - [2-3 decisions that match conventions, with rationale for playing safe]

RISKS (where your product gets its own face):
  - [2-3 deliberate departures from convention]
  - For each risk: what it is, why it works, what you gain, what it costs

The safe choices keep you literate in your category. The risks are where your
product becomes memorable. Which risks appeal? Want different ones? Adjust
anything else?
```

The SAFE/RISK breakdown is critical. Coherence is table stakes — every product in a category can be coherent and look identical. The real question is: where do you take creative risks?

**Options:** (A) Looks great → write DESIGN.md, (B) Adjust [section], (C) Different risks — show wilder, (D) Start over, (E) Just write DESIGN.md.

### Design knowledge library (use to inform proposals)

**Aesthetic directions:**
- Brutally Minimal — Type and whitespace only. No decoration. Modernist.
- Maximalist Chaos — Dense, layered, pattern-heavy. Y2K meets contemporary.
- Retro-Futuristic — Vintage tech nostalgia. CRT glow, pixel grids, warm monospace.
- Luxury/Refined — Serifs, high contrast, generous whitespace.
- Playful/Toy-like — Rounded, bouncy, bold primaries.
- Editorial/Magazine — Strong typographic hierarchy, asymmetric grids, pull quotes.
- Brutalist/Raw — Exposed structure, system fonts, visible grid, no polish.
- Art Deco — Geometric precision, metallic accents, symmetry.
- Organic/Natural — Earth tones, rounded forms, hand-drawn texture, grain.
- Industrial/Utilitarian — Function-first, data-dense, monospace accents.

**Decoration levels:** minimal / intentional (subtle texture, grain) / expressive (full creative direction, layered depth, patterns).

**Layout approaches:** grid-disciplined / creative-editorial (asymmetry, grid-breaking) / hybrid (grid for app, creative for marketing).

**Color approaches:** restrained (1 accent + neutrals) / balanced (primary + secondary + semantic) / expressive (color as primary design tool).

**Motion approaches:** minimal-functional / intentional (subtle entrances, meaningful state transitions) / expressive (full choreography, scroll-driven).

**Font recommendations by purpose:**
- Display/Hero: Satoshi, General Sans, Instrument Serif, Fraunces, Clash Grotesk, Cabinet Grotesk
- Body: Instrument Sans, DM Sans, Source Sans 3, Geist, Plus Jakarta Sans, Outfit
- Data/Tables: Geist (tabular-nums), DM Sans (tabular-nums), JetBrains Mono, IBM Plex Mono
- Code: JetBrains Mono, Fira Code, Berkeley Mono, Geist Mono

**Font blacklist** (never recommend): Papyrus, Comic Sans, Lobster, Impact, Jokerman, Bleeding Cowboys, Permanent Marker, Bradley Hand, Brush Script, Hobo, Trajan, Raleway, Clash Display, Courier New (body).

**Overused fonts** (never recommend as primary unless user asks): Inter, Roboto, Arial, Helvetica, Open Sans, Lato, Montserrat, Poppins, Space Grotesk. Space Grotesk is specifically on this list because every AI design tool converges on it as "the safe alternative to Inter" — that's the convergence trap.

**AI slop anti-patterns** (never include):
- Purple/violet gradients as default accent
- 3-column feature grid with icons in colored circles
- Centered everything with uniform spacing
- Uniform bubbly border-radius on all elements
- Gradient buttons as primary CTA
- Generic stock-photo hero sections
- system-ui / -apple-system as primary display/body font
- "Built for X" / "Designed for Y" marketing copy patterns

**Anti-convergence directive:** Across multiple generations in the same project, VARY light/dark, fonts, aesthetic directions. Never propose the same choices twice without explicit justification. Convergence across generations is slop.

### Phase 4: Drill-downs (only if user requests adjustments)

When the user wants to change a specific section, go deep:
- **Fonts:** 3-5 specific candidates, rationale, what each evokes
- **Colors:** 2-3 palette options with hex values, color theory reasoning
- **Aesthetic:** Walk through which directions fit and why
- **Layout/Spacing/Motion:** Approaches with concrete tradeoffs

After each drill-down, re-check coherence.

### Coherence validation

When the user overrides one section, check if the rest still coheres. Flag mismatches as a gentle nudge — never block:

- Brutalist/Minimal + expressive motion → "Brutalist usually pairs with minimal motion. Your combo is unusual — fine if intentional. Want me to suggest motion that fits, or keep it?"
- Expressive color + restrained decoration → "Bold palette with minimal decoration can work, but the colors will carry a lot of weight..."
- Creative-editorial layout + data-heavy product → "Editorial layouts can fight data density. Want a hybrid approach?"

Always accept the user's final choice. Never refuse to proceed.

### Phase 6: Write DESIGN.md & Confirm

After all choices are locked, write the design system to a markdown file. Template:

```markdown
# Design System: {Product Name}

Generated by design-consultation on {date}
Status: APPROVED

## Memorable Thing
{one-line answer from Phase 1}

## Aesthetic
{direction + rationale}

## Decoration
{level + rationale}

## Layout
{approach + rationale}

## Color
{palette with hex values + rationale}

## Typography
{display / body / data / code fonts + rationale}

## Spacing
{base unit + density + scale}

## Motion
{approach + key principles}

## Safe Choices
{the category-baseline decisions and why}

## Risks
{the deliberate departures, what they buy, what they cost}

## Anti-Patterns (forbidden in this product)
{specific things to never do — usually a subset of the AI slop blacklist}
```

In Charles's environment, write DESIGN.md to the project's docs directory via Custom GitHub MCP.

## Examples

### Example 1: "Design consultation for the Property Analyzer"

→ Phase 1: app for real estate investors analyzing Indianapolis multifamily; memorable thing = "the spreadsheet replacement that doesn't feel like a spreadsheet"
→ Phase 2 (with research): comparable tools converge on "blue-and-white SaaS dashboard"; eureka = the user is staring at numbers all day, dense-but-calm app UI matters more than landing-page polish
→ Phase 3 proposal: Industrial/Utilitarian aesthetic, minimal decoration, grid-disciplined layout, restrained color (1 deep-green accent), typography = Geist + JetBrains Mono for tables, spacing dense (4px base), minimal-functional motion. Safe: green is on-brand for property/finance. Risk: monospace for tables instead of the standard sans-serif everyone else uses.

### Example 2: "Design consultation for the Family Trip App"

→ Phase 1: personal/family use, kids will see it; memorable thing = "feels like a road-trip movie, not a spreadsheet"
→ Phase 3 proposal: Organic/Natural aesthetic, expressive decoration (texture, photos), creative-editorial layout, expressive color (warm earth tones), typography = Fraunces serif + DM Sans, generous spacing, intentional motion (gentle entrances). Safe: photo-driven (every trip app does this). Risk: editorial layout for what's usually a list-driven category.

## Pitfalls

> Pitfalls come from real traces.

(Draft. Tan notes the most common pitfall: proposing safe choices only, no risks. Coherent + safe = forgettable. The SAFE/RISK breakdown forces the deliberate distinction. Another pitfall: drifting back to overused fonts (Inter, Space Grotesk) when the user pushes back — these are on the blacklist for a reason and should be defended.)

## Changelog

- **0.1.0** (2026-05-13) — Initial draft. Reshaped from Tan's gstack /design-consultation. Stripped: gstack runtime bash, designer binary integration (visual mockup generation), browse binary (competitive screenshots), taste profile persistence (~/.gstack/projects/$SLUG/taste-profile.json), legacy approved.json migration, Phase 5 design-preview page generation. Kept: Phase 1 product context + memorable-thing forcing question, Phase 2 three-layer research synthesis with eureka check, Phase 3 complete proposal with SAFE/RISK, design knowledge library (aesthetics, fonts, colors), AI slop anti-patterns, anti-convergence directive, coherence validation, Phase 6 DESIGN.md output.
