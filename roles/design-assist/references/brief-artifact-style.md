# Brief artifact style

*Referenced by `SKILL.md`'s "The living artifact" section and doctrine rule 11 (Confidence labeled). Governs how the draft or final Build Brief is rendered when shown to Charles in chat — not the brief's content, which stays governed by `build-brief-template.md` and PROTOCOL.md.*

Charles reads DA output as a published HTML artifact, not a markdown wall in chat. This file is the one visual system every DA session reuses, so briefs look and feel the same across sessions — Charles should never have to re-learn how to read one.

## When to render this way

Any turn that presents the living artifact for Charles's review: every phase boundary (end of Orient, end of Constrain, convergence milestones), every batched-fork turn (doctrine rule 5), and the exit/handoff turn. Load `artifact-design` and `artifact-diagramming` before writing the file — this reference layers on top of those, it doesn't replace them.

Lighter chat turns (a quick clarifying exchange, a one-line status check) don't need a full re-publish — use judgment. When in doubt, publish; a re-published artifact reaches Charles's already-open tab automatically.

## Confidence badges

Doctrine rule 11 requires verified-by-checking, assumed, and drafted-unreviewed to be *visibly* distinct — not just worded differently. Four pill classes, used consistently:

- **`verified`** (green) — checked directly this session: read the source, ran the query, dispatched the workflow. Carry a one-line "Checked:" note under the claim.
- **`assumed`** (amber) — genuinely unverifiable (future behavior, third-party intent, unreleased pricing) per doctrine rule 2. A checkable claim badged `assumed` is a defect — check it or badge it `drafted`.
- **`drafted`** (violet) — a draft artifact per doctrine rule 3 (skill file, schema, prompt, template, config) that exists in the brief but hasn't been reviewed/exercised yet. Distinct from `assumed`: this is unreviewed work, not an unverifiable fact.
- **`correction`** (rust) — something the prior brief, task, or Charles's own framing assumed that turned out wrong once checked. These are the highest-signal cards in any findings section — never bury them among `verified` cards.

Never badge something `verified` on a search returning zero results — absence needs a direct check (list the directory, read the file) before it's asserted either way.

## Readable size (mandatory)

Charles must be able to read every word without squinting. Added 2026-09-24 after a Mermaid diagram shipped with labels around 8px once it was scaled to fit the page.

- **Text floor: 14px as it appears on screen.** This covers body text, captions, sources, table cells, legends, and every label inside a diagram. Short badges such as pills may go down to 12px. Measure what the reader sees, not what the file says: a 16px label in a 1900px-wide SVG that is scaled into a 900px column is really about 7.5px.
- **Any diagram too big to fit at the floor gets a zoom viewer.** It opens at readable size, not shrunk to fit. It has zoom-in and zoom-out buttons, a "Whole picture" (fit) button, a "Readable size" (100%) button, and full screen. Scrolling or pinching zooms toward the pointer, dragging pans, and arrow keys and +/− work too.
- **Every diagram also ships as a download.** Render it to a standalone SVG plus a 2× PNG in the sandbox (headless Chromium is available), and present both files in chat alongside the artifact.
- **Prefer hand-laid SVG over auto-layout for diagrams with more than about 12 nodes.** Mermaid's automatic layout lets subgraphs overlap and doesn't control label size. Draw the SVG at a fixed size with 15px or larger labels, then screenshot it and check it before publishing.

## Section structure

**Working-draft turns (Phase A–C, brief not yet build-ready):**

1. Header — `<h1>` design goal in plain language, one-sentence lede, `<div class="meta">` (Project / Turn / Reads).
2. Completeness gate — the 11-gate table from `brief-completeness-framework.md`, rendered with the standard `table`/`th`/`td` classes; a ✓/⬜ column plus which gates turned green this turn (doctrine rule 9's completeness report, visually).
3. "What I verified, and where I was wrong" — one `.finding` card per checked claim this turn, badged per above.
4. Decisions made — compact list, one line each (`**Decision** — reason`), decider marker **[Charles]** / **[Claude-per-doctrine]**.
5. Forks (open) — `ol.needs`, one `.rec` recommendation per fork, consequence trail folded into the item body per doctrine rule 5. Empty at build-ready by definition — omit the section entirely once it's empty rather than showing "none."
6. Gated items — same list styling as Forks but no `.rec` (nothing to recommend until access exists); state the exact access needed.
7. Assumptions — plain list, each with what would eventually confirm it.

**Handoff turn (build-ready):**

1. Header + TOC (`nav.toc`).
2. Mechanism diagram (inline SVG per `artifact-diagramming`) when the design has a real multi-stage or before/after shape worth drawing — skip it otherwise.
3. "What I verified, and where I was wrong" — carried forward from the working draft, final state.
4. One `.brief` card per Build Brief, fields exactly as `build-brief-template.md`'s ● fields (What this is / What I'll do / What you'll do / Current state going in / Receiving chat / Scope in/out / Directive / Inputs / Acceptance criteria / Pasteable prompt) — no invented fields, none dropped.
5. Needs from you — only if something genuinely still needs Charles's word beyond brief approval itself (rare at handoff; gate 3 requires zero open forks). Omit if empty.
6. Footline — what happens once Charles approves: commit to git, `write_plan`/`update_plan_content`, set `queued`, Handoff Reference block per `handoff-reference-template.md`.

## CSS (reuse verbatim; only `--accent*` may vary by subject)

```html
<style>
  @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Serif:ital,wght@0,400;0,500;0,600;1,400&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap');

  :root{
    --bg:#f5f7f9; --surface:#ffffff; --surface-2:#eef1f4;
    --ink:#1b2430; --ink-soft:#4b5768; --border:#dde3ea;
    --accent:#2f6b8f; --accent-ink:#1c4a63; --accent-soft:#e7eef3;
    --verified:#2f7d5c; --verified-bg:#e6f3ec; --verified-bd:#bfe0cd;
    --assumed:#a3661f; --assumed-bg:#faf1e3; --assumed-bd:#eecfa0;
    --drafted:#6b5b95; --drafted-bg:#f0edf7; --drafted-bd:#d9d0ea;
    --gap:#a8432f; --gap-bg:#fbe9e5; --gap-bd:#f0c3b7;
    --mono-bg:#eef1f4; --shadow: 0 1px 2px rgba(20,30,40,.06);
  }
  @media (prefers-color-scheme: dark){
    :root:not([data-theme="light"]){
      --bg:#11151b; --surface:#171d25; --surface-2:#1e2530;
      --ink:#e7ecf1; --ink-soft:#a2aebd; --border:#2b3441;
      --accent:#7fb8dc; --accent-ink:#bfe0f5; --accent-soft:#1c2b35;
      --verified:#74c39c; --verified-bg:#152920; --verified-bd:#295c44;
      --assumed:#e0ac66; --assumed-bg:#2f2415; --assumed-bd:#5c481f;
      --drafted:#b3a3d9; --drafted-bg:#241f30; --drafted-bd:#4a3f63;
      --gap:#e2937f; --gap-bg:#331f19; --gap-bd:#5c3327;
      --mono-bg:#1e2530; --shadow: 0 1px 2px rgba(0,0,0,.4);
    }
  }
  :root[data-theme="dark"]{
    --bg:#11151b; --surface:#171d25; --surface-2:#1e2530;
    --ink:#e7ecf1; --ink-soft:#a2aebd; --border:#2b3441;
    --accent:#7fb8dc; --accent-ink:#bfe0f5; --accent-soft:#1c2b35;
    --verified:#74c39c; --verified-bg:#152920; --verified-bd:#295c44;
    --assumed:#e0ac66; --assumed-bg:#2f2415; --assumed-bd:#5c481f;
    --drafted:#b3a3d9; --drafted-bg:#241f30; --drafted-bd:#4a3f63;
    --gap:#e2937f; --gap-bg:#331f19; --gap-bd:#5c3327;
    --mono-bg:#1e2530; --shadow: 0 1px 2px rgba(0,0,0,.4);
  }

  *{box-sizing:border-box;}
  body{background:var(--bg); color:var(--ink); font-family:'IBM Plex Sans', system-ui, sans-serif; font-size:16px; line-height:1.6; padding:0 20px;}
  .wrap{max-width:780px; margin:0 auto; padding-block:48px 80px;}
  h1,h2,h3{font-family:'IBM Plex Serif', Georgia, serif; font-weight:600; text-wrap:balance; color:var(--ink);}
  h1{font-size:2rem; line-height:1.15; margin:0 0 6px;}
  h2{font-size:1.4rem; margin:2.6em 0 .6em; padding-top:.4em; border-top:1px solid var(--border);}
  h3{font-size:1.12rem; margin:1.6em 0 .5em; color:var(--accent-ink);}
  p{margin:0 0 1em; max-width:66ch;}
  .lede{color:var(--ink-soft); font-size:1.02rem; max-width:62ch;}
  code, .mono{font-family:'IBM Plex Mono', ui-monospace, monospace; font-size:.88em;}
  code{background:var(--mono-bg); padding:.12em .38em; border-radius:4px;}
  a{color:var(--accent-ink); text-decoration-color:var(--border);}

  .meta{display:flex; flex-wrap:wrap; gap:.5em 1.4em; margin:1.2em 0 0; font-size:.9rem; color:var(--ink-soft);}
  .meta b{color:var(--ink); font-weight:600;}

  nav.toc{margin:2em 0; padding:14px 18px; background:var(--surface); border:1px solid var(--border); border-radius:10px; box-shadow:var(--shadow);}
  nav.toc div{font-size:.72rem; text-transform:uppercase; letter-spacing:.08em; color:var(--ink-soft); margin-bottom:.6em;}
  nav.toc ol{margin:0; padding-left:1.2em; display:grid; gap:.35em; font-size:.92rem;}
  nav.toc a{color:var(--ink); text-decoration:none;}
  nav.toc a:hover{color:var(--accent-ink);}

  .pill{display:inline-flex; align-items:center; gap:.4em; font-size:.72rem; font-weight:600; letter-spacing:.02em; padding:.22em .62em; border-radius:99px; white-space:nowrap; border:1px solid transparent; font-family:'IBM Plex Sans',sans-serif;}
  .pill.verified{background:var(--verified-bg); color:var(--verified); border-color:var(--verified-bd);}
  .pill.assumed{background:var(--assumed-bg); color:var(--assumed); border-color:var(--assumed-bd);}
  .pill.drafted{background:var(--drafted-bg); color:var(--drafted); border-color:var(--drafted-bd);}
  .pill.gap{background:var(--gap-bg); color:var(--gap); border-color:var(--gap-bd);}
  .pill.dot::before{content:"\25CF"; font-size:.7em;}

  .finding{display:grid; grid-template-columns:auto 1fr; gap:.15em 1em; padding:14px 16px; margin:10px 0; background:var(--surface); border:1px solid var(--border); border-left:3px solid var(--border); border-radius:8px; box-shadow:var(--shadow);}
  .finding.v{border-left-color:var(--verified);}
  .finding.a{border-left-color:var(--assumed);}
  .finding.d{border-left-color:var(--drafted);}
  .finding.g{border-left-color:var(--gap);}
  .finding .pill{grid-row:1; align-self:start; margin-top:.15em;}
  .finding .body{grid-column:2;}
  .finding .body p{margin:0 0 .4em; font-size:.95rem;}
  .finding .body p:last-child{margin-bottom:0;}
  .finding .body .src{color:var(--ink-soft); font-size:.875rem;}

  figure{margin:1.8em 0; padding:16px; background:var(--surface); border:1px solid var(--border); border-radius:10px; box-shadow:var(--shadow);}
  figure svg{max-width:100%; height:auto; display:block; margin:0 auto;} /* only when labels stay >=14px at this width; otherwise use the zoom viewer (Readable size, above) */
  figcaption{font-size:.9rem; color:var(--ink-soft); margin-top:.8em; text-align:center;}

  .brief{margin:1.6em 0; background:var(--surface); border:1px solid var(--border); border-radius:12px; box-shadow:var(--shadow); overflow:hidden;}
  .brief > .head{padding:16px 22px; background:var(--accent-soft); border-bottom:1px solid var(--border);}
  .brief > .head .tag{font-size:.72rem; text-transform:uppercase; letter-spacing:.08em; color:var(--accent-ink); font-weight:600;}
  .brief > .head h3{margin:.15em 0 0; color:var(--ink); font-size:1.2rem;}
  .brief .field{padding:14px 22px; border-bottom:1px solid var(--border);}
  .brief .field:last-child{border-bottom:none;}
  .brief .field .label{font-size:.72rem; text-transform:uppercase; letter-spacing:.07em; color:var(--ink-soft); margin-bottom:.4em; font-weight:600;}
  .brief .field p, .brief .field li{font-size:.94rem;}
  .brief .field ul, .brief .field ol{margin:.2em 0 0; padding-left:1.3em;}
  .brief .field li{margin-bottom:.45em;}
  .scope-grid{display:grid; grid-template-columns:1fr 1fr; gap:0 20px;}
  @media (max-width:560px){.scope-grid{grid-template-columns:1fr;}}
  .scope-grid .in b, .scope-grid .out b{font-size:.72rem; text-transform:uppercase; letter-spacing:.06em; color:var(--ink-soft); display:block; margin-bottom:.4em;}
  .prompt{background:var(--mono-bg); border:1px solid var(--border); border-radius:8px; padding:14px 16px; font-family:'IBM Plex Mono',monospace; font-size:.875rem; line-height:1.55; white-space:pre-wrap; overflow-x:auto; color:var(--ink);}

  table{width:100%; border-collapse:collapse; font-size:.9rem; margin:.5em 0;}
  th{text-align:left; font-size:.72rem; text-transform:uppercase; letter-spacing:.05em; color:var(--ink-soft); padding:6px 10px; border-bottom:1px solid var(--border);}
  td{padding:8px 10px; border-bottom:1px solid var(--border); vertical-align:top;}
  tr:last-child td{border-bottom:none;}
  .num{font-variant-numeric:tabular-nums; text-align:right;}
  .tbl-wrap{overflow-x:auto;}

  ol.needs{padding-left:1.4em; margin-top:.6em;}
  ol.needs > li{margin-bottom:1.3em; font-size:.97rem;}
  ol.needs .rec{display:block; margin-top:.4em; padding:8px 12px; background:var(--verified-bg); border:1px solid var(--verified-bd); border-radius:7px; font-size:.9rem; color:var(--ink);}
  ol.needs .rec b{color:var(--verified);}

  .footline{margin-top:3em; padding-top:1.2em; border-top:1px solid var(--border); color:var(--ink-soft); font-size:.9rem;}
</style>
```

## Mechanics

- Write the body content to a file (no `<!DOCTYPE>`/`<html>`/`<head>`/`<body>` — just the `<style>` block and the `<div class="wrap">…</div>` content) and publish with the Artifact tool.
- Title the artifact after the design goal in plain language (2–4 words) — not "Build Brief" and not a BB-code. Charles reads plain titles per PROTOCOL.md's naming rule; the same discipline applies to the artifact's own title.
- Redeploy (same file path / same artifact URL) rather than publishing a new one each turn within one DA session — Charles should have one artifact per design thread that updates in place, not a new card every phase boundary.
- The artifact is presentation only. Nothing in it commits anything — git commits, `write_plan`/`update_plan_content`, and `update_plan_status` all happen only after Charles reviews and answers, per PROTOCOL.md's Review → Execute workflow.

## Provenance

Added 2026-09-14 at Charles's request, generalizing the ad-hoc styling used in a world-graph feed-reader design session that day (verification-findings cards + Build Brief cards + Needs-from-you list, published as one HTML artifact). That session's specific artifact wasn't drafted from any existing template — this file is what makes the pattern reusable and gives it a canonical home next to `build-brief-template.md`.
