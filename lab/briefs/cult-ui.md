---
title: "Animated Web Components for Our Sites — Cult UI"
type: discovery-brief
discovered: 2026-10-19
tools: [cult-ui]
brief_url: https://claude.ai/artifact/BM8evenMruUcnMDT2mDcfU
draft: false
---

# Animated Web Components for Our Sites — Cult UI

Discovery Brief · 2026-10-19

Evidence marks: **Published** = checked at the source today. **Assumed** = our judgment.

## What it is

A free library of about 150 ready-made, animated pieces for websites: buttons, cards, tabs, scoreboards, carousels, device mockups, backgrounds. *Published.* You don't install it like an app. A one-line command copies each piece's source code into your own website, so you own it and can change it. *Published.*

It only works inside a React website styled with Tailwind (the same kind of site as cbrain-ui and the planned family arcade). It does not make images, video or 3D models. *Published.*

## Verdict by tool

**Shelf** — Cult UI. Trigger: **the family arcade site exists (Build 42 done) and its shelf page gets a look pass.** Next step then is a test run, not adoption.

Why not Never: it is free, MIT licensed, actively maintained, and fits our site stack exactly. Why not more: no listed speed run needs it, and Claude already writes this kind of animated UI by hand. It saves time and raises polish; it does not unlock anything the harness can't do today. *Assumed.*

## Where it fits

- **Layer:** Digital hands (making things on screen). **Pipeline step:** 6, "I make it on screen". *Assumed.*
- **Block:** 16, one skill per tool pack (a "web UI pack" note in the game-maker or build skills). Touches 17 only if we write a "looks right" rubric for site screens. *Assumed.*
- **Replaces in the blueprint:** nothing. It would replace part of what Claude hand-writes today for cbrain-ui and the arcade site. *Assumed.*

## What we could use it for

### Now (after Build 42 lands)

- **Family arcade shelf.** The brief asks for "a toy arcade the boys want to open, not an admin panel — big buttons, phone first." Matching pieces exist: 3D Carousel (spin through games), Texture and Neumorph Buttons (chunky, pressable), Lightboard (LED scrolling sign), Rolling Number (score counters), Pixel Heading (arcade lettering). *Published* that they exist; *Assumed* that they suit the boys.
- **cbrain-ui polish.** Kanban Board, Halo tabs/inputs/toasts, Timer, Copy Button, Analytics Chart could replace plainer hand-built parts of the Harness and Workflows screens. *Assumed.*

### Later

- Pursuit or project microsites for FA Wilhelm (hero sections, device mockups to frame renders). *Assumed.*
- The real-estate holding company's public site. *Assumed.*

### Cannot

- Arch-render stills or clips, motion graphics in video, game art, 3D characters. Not what it is. *Published.*
- Drop straight into a Claude chat artifact (artifacts are single HTML files with no build step; these are React source files that need one). A piece could be hand-ported, but then the library isn't doing the work. *Assumed.*

## What we checked

| Fact | Finding | Mark |
|---|---|---|
| Maker | Nolly Studio (Nolan Sym). Funded by their paid side products (AI SDK Agents, Newcopy). | Published |
| Age / activity | Started May 2024; last code push 2026-10-14; 6,612 stars, 350 forks, 16 open issues. | Published |
| Version | No numbered releases; dated drops. Latest: September 2026, 58 new components and a rename of one set to "Halo". | Published |
| Price | $0. A separate paid "Cult UI Pro" (blocks and templates) exists; the new September pieces' image folder is named `cult-pro-component-images`, so some Pro pieces likely moved to free. | Published / Assumed on the move |
| Company use | MIT license: yes, including commercial. | Published |
| Claude, no screen | Yes in principle: a command-line install, a markdown copy of every docs page, an `llms.txt` index, and the shadcn connector for coding agents. | Published |
| Our stack match | cbrain-ui already runs Next 15, React 19, Tailwind 4, Motion, Radix and the same helper libraries. It has no `components.json` (the setup file the one-line install expects), so first use needs a one-time setup or the manual route. | Published (read today) |
| Extra pieces some need | Halo set uses Base UI; shader pieces use Paper Design WebGL; drawers use Vaul; carousels use Embla. Each adds a small library. | Published |

## What else does this job

- **Claude by hand (today).** cbrain-ui's buttons, tabs and cards are hand-written in the same style. Works; slower and plainer for showpiece effects. *Published* (repo read).
- **shadcn/ui itself** — the plain base Cult UI builds on. *Published.*
- **Magic UI, Aceternity UI** — the other two main animated libraries in the same family. Not reviewed. *Published* that they exist.
- **Claude Design canvas** — for mockups to react to, not for production site code. *Assumed.*

## Requirements check

**arch-renders** (the only speed run listed in the lab's speed-run brief at discovery time): **not this tool's job** on all four requirements (conventions, storyboard, motion pieces, graphics quality). Its one touchpoint would be the Workflows screens in cbrain-ui, which are tooling, not the clip. *Assumed.*

**family arcade** (active in Total Harness, plan 5eb4d7db, but not yet listed in `lab/speed-run.md` at discovery time): yes for the site's look, because the shelf and login pages are a React + Tailwind site and the brief's design intent asks for toy-like, phone-first screens. Not this tool's job for the games themselves, which are Three.js. *Assumed.*

## Risks and cover

- **Maker drift or abandonment.** Cover: the code is copied into our repo, so nothing breaks if they stop. *Published.*
- **Heavy effects on kids' tablets** (WebGL shaders, many springs). Cover: pick CSS/SVG pieces for the arcade; test on a real tablet. *Assumed.*
- **Cloud shell may not reach cult-ui.com** (our workspace allowlist is mostly npm and GitHub). Cover: pull the same source from the GitHub repo's `registry` folder through the GitHub connector. *Assumed.*
- **Look sprawl** — mixing five button styles. Cover: pick one family per site and write it into the site's skill. *Assumed.*

## If adopted

- **What gets built:** a one-time setup file in each site, a short "web UI pack" section in the game-maker / build skills naming the chosen pieces.
- **Dollars:** $0.
- **Your hours:** about 15 minutes to react to a before/after of the arcade shelf.
- **Proof of done:** the arcade shelf ships with the chosen pieces, loads smoothly on the boys' tablet, and the boys pick it over the plain version.

All *Assumed.*

## Test run, if we do one

- **Test problem:** restyle the family arcade's game shelf.
- **Input:** the live shelf page from Build 42 with three test games.
- **Variants:** (A) Build 42's plain version; (B) 3D Carousel + Texture Buttons + Pixel Heading; (C) Lightboard sign + Neumorph Buttons + Rolling Number for scores.
- **Questions only a test can settle:** Can the cloud session install pieces directly or only via GitHub? Do they run smoothly on the boys' actual tablet? Does Claude use them correctly from the docs alone, without fixes? Do the boys care?

## Sources

- https://github.com/nolly-studio/cult-ui — repo facts, README, license
- https://www.cult-ui.com/llms.txt — full component list, install rules
- https://www.cult-ui.com/docs/changelog — release history
- https://www.cult-ui.com/docs/mcp-server — agent install route
- Chooch333/cbrain-ui `package.json`, `components/ui`; Chooch333/family-arcade Build 42 brief; agent-library `lab/`; Total Harness state (read 2026-10-19)
