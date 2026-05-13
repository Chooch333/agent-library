---
name: design-html
version: 0.1.0
status: draft
triggers:
  - "generate HTML"
  - "generate the HTML for"
  - "implement this design"
  - "write the HTML"
  - "code this design"
  - "design to HTML"
dependencies: [design-consultation, design-shotgun]
owner: Charles
updated: 2026-05-13
source: Adapted from Garry Tan's gstack /design-html (https://github.com/garrytan/gstack/blob/main/design-html/SKILL.md). Major adaptation: Tan's original is Pretext-native (a custom layout engine he uses) and includes a Pretext API tier-routing step (prepare / prepareWithSegments / etc). Charles's stack uses Next.js + Tailwind, so the Pretext routing is replaced with standard React + Tailwind generation. The judgment frame, design analysis, and framework detection ports cleanly.
---

# Design HTML

## What

Generate production-quality HTML/CSS (or React component) code from an approved design spec. Takes a design brief — colors, typography, layout, motion — and produces clean, semantic, accessible markup. Built to avoid AI-slop output (no purple gradients, no system-ui fonts, no centered-everything).

## When

**Fire this skill when:**
- A design direction has been chosen (from design-consultation, design-shotgun, or manual brief)
- The user asks to "generate HTML," "implement this design," "write the markup"
- A UI component or page needs to move from spec to code

**Do NOT fire this skill when:**
- The design isn't locked in yet (use design-consultation or design-shotgun first)
- The user needs design judgment, not implementation (use design-reviewer)
- The code already exists and the question is about modification (use pr-reviewer or investigate)

## How

### Step 1: Design analysis

Gather the implementation spec. Sources:

1. **Approved design brief** — from design-consultation or design-shotgun output
2. **DESIGN.md** if one exists — its tokens override any locally-specified values
3. **Plan or design doc** — if no formal design exists, extract intent from the plan's prose
4. **Freeform** — if nothing exists yet, ask the user one question covering: purpose/audience, visual feel (dark/light, playful/serious, dense/spacious), content structure (hero, features, pricing, etc.), and any reference sites they like

Output an **Implementation spec** summary:
- Colors (hex)
- Fonts (family + weights)
- Spacing scale (base unit + multipliers)
- Component list
- Layout type (grid, asymmetric, single-column, etc.)
- Motion (entrance, hover, scroll-linked, etc.)

### Step 2: Framework detection

Determine output format. For Charles's stack the answer is almost always Next.js + React + Tailwind, but ask if the project context is unclear:

- **React component** (`.tsx`) — default for Family Trip App, Property Analyzer, future apps
- **Vanilla HTML** — for standalone artifacts, landing pages, simple previews
- **Other** (Svelte, Vue) — only if explicitly asked

For React, follow:
- TypeScript with proper types on props
- Functional components + hooks
- Tailwind classes for styling (no inline styles unless dynamic)
- No external CSS files unless the project already has one
- Accessibility-first markup (semantic HTML, ARIA where appropriate, keyboard nav)

### Step 3: Generate the markup

Apply the design knowledge library (see `design-consultation/SKILL.md`) and these rules:

**Universal generation rules:**
- Use CSS variables for color tokens (`--color-bg`, `--color-fg`, etc.) — both in vanilla HTML and Tailwind config
- Real font families. Never `system-ui` or `-apple-system` as primary. Use Google Fonts or a self-hosted font from the design spec.
- Real content. Never lorem ipsum. Generate realistic content based on the plan or user description.
- Semantic HTML: `<header>`, `<nav>`, `<main>`, `<section>`, `<article>`, `<aside>`, `<footer>`.
- Accessibility: visible focus states, ≥16px body text, ≥4.5:1 contrast on body, 44px touch targets on interactive elements, alt text on images.
- Responsive by default. Mobile-first if the design is mobile-primary; otherwise desktop-first with explicit mobile breakpoints.

**AI slop prohibitions** (do NOT generate any of these):
1. Purple/violet/indigo gradient backgrounds
2. 3-column feature grid (icon-in-colored-circle + bold title + 2-line description × 3 symmetric)
3. Icons in colored circles as section decoration
4. Centered everything (`text-align: center` on all headings/descriptions/cards)
5. Uniform bubbly border-radius on every element
6. Decorative blobs, floating circles, wavy SVG dividers
7. Emoji as design elements (rockets in headings, emoji bullet points)
8. Colored left-border on cards (`border-left: 3px solid <accent>`)
9. Generic hero copy ("Welcome to [X]", "Unlock the power of...", "Your all-in-one solution for...")
10. Cookie-cutter section rhythm (hero → 3 features → testimonials → pricing → CTA)
11. `system-ui` / `-apple-system` as primary display/body font

### Step 4: Refinement loop

After initial generation, ask the user one question:

> "Initial generation done. Want to see: (A) the full output, (B) a specific section's code, or (C) refine a specific area?"

For refinement: drill into the area, regenerate just that section with the changes, keep the rest stable.

### Step 5: Hand off

Final output options:

- **Vanilla HTML** — single self-contained file, ready to open in browser
- **React component** — written to a file via Custom GitHub MCP (`create_or_update_file`)
- **Inline preview** — if the artifact is small enough, render directly in chat for inspection

Include a short note on what's next: integrate into the app, write tests, run accessibility audit.

## Examples

### Example 1: "Generate HTML for the Property Analyzer dashboard header"

→ Step 1: design spec from earlier design-consultation — Industrial/Utilitarian, Geist + JetBrains Mono, deep green accent
→ Step 2: React component (Property Analyzer is Next.js)
→ Step 3: generate header with semantic `<header>`, real navigation labels ("Properties", "Analysis", "Settings"), keyboard-accessible nav, no icons-in-circles, dense but readable spacing
→ Step 4: ask Charles to refine the property-count badge area
→ Step 5: write to `src/components/dashboard-header.tsx` via Custom GitHub MCP

### Example 2: "Write the HTML for a hype slide in the Family Trip App"

→ Step 1: design spec from design-shotgun — Cinematic Photo direction, full-bleed image, minimal overlay text
→ Step 2: React component
→ Step 3: full-viewport image with absolutely-positioned text, semantic `<figure>` + `<figcaption>`, accessible alt text generated from trip data, mobile-first
→ Step 5: write to `src/components/trip-tour/hype-slide.tsx`

## Pitfalls

> Pitfalls come from real traces.

(Draft. Tan's biggest pitfall is generating "AI design" — clean code, but the visual output is one of the 11 slop patterns. The blacklist exists for that reason. In Charles's environment with no visual preview, the temptation is even higher because the slop isn't visible until rendered. Defense: enforce the slop list at generation time, not after.)

## Changelog

- **0.1.0** (2026-05-13) — Initial draft. Reshaped from Tan's gstack /design-html. Major adaptation: replaced Pretext-native API routing (prepare / prepareWithSegments / walkLineRanges) with standard React + Tailwind generation suited to Charles's Next.js stack. Stripped: gstack designer binary (PNG analysis), browse binary (live preview server), Pretext source embedding, Pretext tier classification. Kept: design analysis step, framework detection (default React + Tailwind for Charles), generation rules, AI slop prohibitions, accessibility requirements.
