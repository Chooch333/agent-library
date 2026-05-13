---
name: design-shotgun
version: 0.1.0
status: draft
triggers:
  - "design shotgun"
  - "design variants"
  - "show me different design directions"
  - "give me design options"
  - "design options for"
dependencies: [design-consultation]
owner: Charles
updated: 2026-05-13
source: Adapted from Garry Tan's gstack /design-shotgun (https://github.com/garrytan/gstack/blob/main/design-shotgun/SKILL.md). Major adaptation: the gstack designer binary (which actually generates PNG mockups via image-gen API) is unavailable in claude.ai. Without it, this skill becomes a structured exercise in *describing* distinct design directions instead of *generating* them. The judgment frame and anti-convergence rules port; the image generation does not.
---

# Design Shotgun

## What

Explore multiple distinct design directions for a screen, page, or component before committing to one. Forces deliberate variation — different fonts, colors, layouts — so the comparison reveals which direction fits the product, not which direction is the safest interpretation of a vague brief.

**Important runtime note:** Tan's original generates actual PNG mockups via the gstack designer binary. In Charles's claude.ai environment, that runtime is unavailable. This reshape produces **detailed text descriptions** of variants — each with specific fonts, hex colors, layout grids, and motion choices — so Charles can imagine the directions concretely. If actual visual mockups are needed, this role hands off to an external tool (Figma, v0.dev, or a local designer).

## When

**Fire this skill when:**
- A design direction is being chosen and one option isn't enough
- The user asks for "design variants," "different directions," "design options"
- A design feels generic and needs deliberate exploration before locking in

**Do NOT fire this skill when:**
- The design system is already established (DESIGN.md exists, just follow it)
- The user wants final implementation, not exploration
- The change is too tactical to warrant multiple directions

## How

### Step 0: Context gathering

Read what exists. Pull from:
- DESIGN.md if one exists
- The product description and user persona
- Any constraints (target platform, accessibility, brand)

Ask one question if needed: "How many variants do you want — 2, 3, or 4?" Default to 3.

### Step 1: Concept generation

Generate N text concepts. Each is a distinct creative direction, not a minor variation.

```
I'll explore 3 directions:

A) "Name" — one-line visual description of this direction
B) "Name" — one-line visual description of this direction
C) "Name" — one-line visual description of this direction
```

Draw on the design knowledge library (see `design-consultation/SKILL.md`) and the user's brief to make each concept distinct.

**Anti-convergence directive (hard requirement):** Each variant MUST use a different font family, color palette, and layout approach. If two variants look like siblings — same typographic feel, overlapping color temperature, comparable layout rhythm — one of them failed. Regenerate the weaker one with a deliberately different direction.

Concrete test: if someone could swap the headline text between two variants without noticing, they're too similar. Variants should feel like they came from three different design teams, not the same team at three different coffee levels.

### Step 2: Concept confirmation

Present the N directions. Ask: "Generate detailed descriptions of these, or want to swap one out first?"

### Step 3: Generate detailed variants

For each approved concept, produce a structured description:

```
VARIANT A: <Name>
  Aesthetic: <direction>
  Decoration: <level>
  Layout: <approach + ASCII grid sketch>
  Color palette:
    - Background: #XXXXXX
    - Primary text: #XXXXXX
    - Accent: #XXXXXX
    - Supporting: #XXXXXX
  Typography:
    - Display: <font name + weight + size>
    - Body: <font name + weight + size>
    - Data (if applicable): <font name + weight + size>
  Spacing: <base unit + density rule>
  Motion: <approach + 2-3 specific moments>
  The feeling: <one sentence on what this evokes>
```

Use the design knowledge library's font/color/aesthetic options. Apply AI slop blacklist — no purple gradients, no 3-column feature grids, no system-ui as primary font.

### Step 4: Comparison

Present all variants side-by-side in a table summarizing the key differences:

```
              | Variant A    | Variant B     | Variant C
--------------|--------------|---------------|------------------
Aesthetic     | Minimal      | Editorial     | Brutalist
Display font  | Fraunces     | Cabinet G.    | JetBrains Mono
Accent color  | Deep green   | Burnt orange  | Yellow
Layout        | Grid 12-col  | Asymmetric    | Single column
Feeling       | Calm/serious | Curated/print | Raw/direct
```

### Step 5: Pick + refine

Ask: "Which variant do you want to refine?" Then drill down: tweak fonts, adjust palette, refine spacing. Output the refined variant ready for handoff to design-html or to an external implementation tool.

## Examples

### Example 1: "Design shotgun for the Property Analyzer dashboard"

→ 3 concepts: (A) "Calm Industrial" — Geist + dense data tables; (B) "Editorial Finance" — Fraunces serif + magazine-style layout; (C) "Brutal Direct" — JetBrains Mono everywhere, no decoration
→ Each generated with specific fonts, hex colors, layout, motion
→ Comparison table side-by-side
→ Charles picks (A), drills into specific palette refinement

### Example 2: "Show me design directions for the Family Trip App hype slides"

→ 3 concepts: (A) "Cinematic Photo" — full-bleed image + minimal overlay; (B) "Storybook" — illustrated frame around photo; (C) "Polaroid Stack" — overlapping photo cards with handwritten captions
→ Each described in full detail
→ Charles picks (A) for hype slides specifically; might use (C) for memory archive later

## Pitfalls

> Pitfalls come from real traces.

(Draft. Tan's biggest pitfall: convergence across variants — generating three "different" directions that all use Inter + a card grid + center-aligned headers. The anti-convergence directive exists for that reason. In Charles's environment without visual generation, an additional pitfall is vague text descriptions — "minimal modern feel" — which fail the specificity rule from design-reviewer. Name the font, the hex code, the layout grid.)

## Changelog

- **0.1.0** (2026-05-13) — Initial draft. Reshaped from Tan's gstack /design-shotgun. Major adaptation: the gstack designer binary (image generation) is unavailable; this skill now produces detailed text descriptions of variants instead of actual PNG mockups. Stripped: $D variants/iterate/compare commands, comparison-board HTML generation, $B browser preview, taste memory persistence to ~/.gstack/. Kept: concept generation, anti-convergence directive, specificity rules, comparison table format.
