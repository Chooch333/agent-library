---
title: "Crayon (prompt-to-game builder)"
reviewed: 2026-10-11
tools: [crayon]
draft: false
---

## What it is

Crayon (usecrayon.ai, by Crayon Labs Inc.) turns a plain-English idea into a playable 2D or 3D game that runs in a web browser. ✓ About three months public, in open beta, pre-seed funded. ✓

## Verdict by tool

| Tool | Verdict | Why | The one fact that would change it |
| --- | --- | --- | --- |
| Crayon | Never | Claude cannot drive it: no API (a way for programs to talk to it), connector or command line. ✓ The goal is to rebuild its process, not rent it. ✓ | Crayon opens an API or connector |

## Where it fits

Digital hands layer; pipeline steps 6 (make it on screen) and 7 (check it). Blocks 7 (game art), 8 (screen eyes), 16 (one skill per tool pack), 17 (rubric per domain). ✓ It serves no listed speed run; a kids'-games speed run is possible but not launched. ✓

## What we could use it for

- **Now:** the reference design for our own describe-it browser game builder.
- **Later:** nothing as a tool.
- **Cannot:** plug it into the harness or run it without a screen.

## What we checked

Crayon's homepage, app page, terms and privacy policy (both dated 30 Sep 2026), a co-founder interview, the founder's X posts (search snippets only; X blocks automated reading of the post), Tripo pricing and free art licences. ✓ No hands-on test: Charles waived it, since the finding is a design to copy, not a tool to adopt. ✓

## What else does this job

Our own harness, built from parts that exist:

- Claude writes the game; Three.js (free) draws it. ✓
- Free art: Quaternius, KayKit (rigged, animated characters) and Kenney (props), all CC0, meaning free for any use. ✓
- Custom art: Tripo, about $0.40–$0.50 per model plus $0.25 to add a skeleton. ✓ Walk, run and jump motions unconfirmed. ~
- Not opened: Rosebud AI, Makko AI, Phaser's Claude Code connector. ~

**Crayon's pipeline to copy** (✓ interview and terms): clarifying questions (6–8 per round) → a full plan before building (Pro mode adds a design document and reference pictures) → about 15 studio-style steps shown as 4 → specialist helpers (an artist with colour, shape, texture and material sub-helpers) → a shared parts library → editors (chat, assets, levels, textures, code view, version history) → export rewritten for each game site.

**Crayon's outside parts:** Anthropic and Google AI, picked per step for cost vs quality ✓; Three.js ✓ (founder's posts); Tripo for a few assets, partnership "in talks" ✓; Amazon S3 storage ✓; PostHog usage tracking ✓; Stripe payments ✓; website probably Next.js ~. Sound, animation, error fixing and playtesting: not disclosed.

## Requirements check

The only listed speed run is arch-renders. Conventions, storyboard, motion menu and graphics quality: all "not this tool's job". ✓

## Risks and cover

- **Closed internals.** Crayon does not say how it does sound, animation, error fixing or playtesting. ✓ Cover: design those parts in the Total Harness.
- **Moving characters are the hard part.** ~ Cover: start with free rigged characters; review Tripo separately.
- **Copying the pipeline does not guarantee good art.** Crayon's own founders say visuals are "not 100% there". ✓

## If adopted

Not adopted. Instead, the pipeline is handed to the Total Harness as the reference design for a possible kids'-games speed run, designed there. Dollars, hours and proof of done are set there if it launches.

## Sources

- Crayon homepage: https://usecrayon.ai
- Crayon terms: https://usecrayon.ai/terms
- Crayon privacy policy: https://usecrayon.ai/privacy
- Inside Crayon, interview with co-founder Aniket Jatav: https://vibecode.game/blog/inside-crayon-a-conversation-with-co-founder-aniket-jatav
- Aniket J on X: https://x.com/aniketjart
- Tripo API and pricing: https://www.tripo3d.ai/blog/what-3d-model-generation-api-can-convert-images-or-text-into
- Free 3D model sites guide: https://app.cinevva.com/guides/free-3d-model-sites
- Working document: https://claude.ai/code/artifact/230e5383-e327-4580-93f9-3139b1a994f3
