---
title: "Circuit Board Designer - heypcb"
type: discovery-brief
discovered: 2026-10-15
tools: [heypcb]
brief_url: "https://claude.ai/artifact/2EVamG2k1t4gzxzskTTdUP"
draft: false
---
# Circuit Board Designer - heypcb

Discovery Brief · 2026-10-15

From [heypcb.ai/explore](https://heypcb.ai/explore). Tags: Published = checked at the maker's site or a source today. Assumed = our judgment. Nothing here is tested.

**Verdict · Shelf.** Come back when: **block 10, the Electronics bench**, is being scoped. Low priority. It serves no active speed run, and Claude-with-KiCad is the lead lane for that block; heypcb ranks behind it, mainly as a starting-board library.

## What it is

A website where you describe a circuit board in plain English and an AI helper ("Inky") draws it: the wiring diagram, the board layout, and the files a factory needs to make it. (Published) The files are in KiCad format, the free industry-standard board design program, so you own them and can open them elsewhere. (Published)

The page you linked is almost certainly **Circuit World**, its free-to-browse library of 11,000+ open-source boards that you can copy ("fork") and modify. (Assumed) The /explore page itself blocks automated reading, so I could not open it; the home page shows the same library. It also sells the boards: order from the editor and a factory in China makes and ships them. (Published)

## Verdict by tool

| Tool | Verdict | Come back when |
|---|---|---|
| heypcb editor + Inky | Shelf | Block 10 scoping |
| Circuit World library | Shelf (same row) | Block 10, or any board project |

## Where it fits

- Layer: Physical hands. Pipeline steps 6 (make it on screen) and 8 (make it physical, via board ordering). (Assumed)
- Block 10, Electronics bench, and block 14, Fabrication and parts accounts. Phase: Physical ladder, which sits after the Money stop. (Assumed)
- It would replace: the blank-page part of board design inside block 10. It would not replace the board loading and read-back that block 10 also needs.

## What we could use it for

- **Now:** nothing in the active work. Arch renders and the family arcade involve no circuit boards. (Assumed)
- **Later:** gadget, robot and drone boards for the Physical ladder; starting from a Circuit World board instead of a blank one; a fun one-off with the boys (heypcb's own sample boards include a plant-thirst sensor, a pomodoro timer and a phone-stand robot). (Published for the samples, Assumed for the fit.)
- **Cannot:** let Claude run it cleanly. I found no API, connector or command line. (Assumed; absence after searching; the terms mention "APIs" in passing but nothing is documented.) It is a website, not a desktop app, so desktop computer use does not apply. (Published) Claude could click through it in a browser after you sign in, but that is slow, fragile and screen-bound. (Assumed)

## What we checked

| Fact | Finding | |
|---|---|---|
| Maker | heypcb, a small California company; founders Inky Ganbold and Justin Kim | Published |
| Age | Very new. Circuit World launched Sept 23, 2026; live multiplayer Sept 26; terms dated Oct 10, 2026 | Published |
| Price | Free trial (one board). Starter $20/mo, Pro $60, Max $200, Ultra $500 | Published |
| Company use | Allowed. You own your designs. Circuit World boards carry each author's own license, and some forbid commercial use | Published |
| Claude can run it with no screen | No route found: no API docs, no connector, no MCP | Assumed |
| Quality | Maker says it checks real parts and factory rules. Its own terms say output is not production-ready without an engineer's review | Published |

## What else does this job

- **Claude + KiCad directly.** Several free, open-source connectors (MCP servers) let Claude draw schematics and boards in KiCad itself, run the rule checks and export factory files. This is the lane Claude can drive, and it already fits block 10's "free tools" line. (Published that they exist; Assumed on quality.)
- **DeepPCB.** AI that only does the layout and wiring step, but has a real API. (Published)
- Ruled out: comparing these properly. That is the separate overarching review, best done when block 10 opens.

## Requirements check

Against arch renders (the only speed run with written requirements): conventions, storyboard, motion menu, graphics quality are all **not this tool's job**. Against the family arcade draft: also not its job. (Assumed)

## Risks and cover

- Brand-new startup; features and prices may shift. Cover: the KiCad files are portable, so nothing is locked in.
- Hand-driven website, so it breaks the "Claude works while you are away" pattern. Cover: use it as a starting-board library and let Claude edit the KiCad files directly.
- License mix in Circuit World. Cover: check each board's license before copying or ordering.
- Ordering boards spends money. Cover: money always stops.

## If adopted

- What gets built: nothing in the harness; an account and a short skill note on when to use it versus Claude-with-KiCad.
- Dollars: $20/mo Starter, plus board orders. Your hours: about one to set up and try a board. (Assumed)
- Proof of done: one board designed from a plain sentence, opened in KiCad, passing its rule checks.

## Test run, if we do one

- Test problem: one small real board, for example a soil-moisture sensor that lights an LED.
- Input: one plain sentence.
- Variants: heypcb's Inky versus Claude driving KiCad through a free connector.
- Only a test can settle: does Inky's board pass KiCad's own checks untouched; how much hand-fixing each route needs; whether heypcb has any hidden way for Claude to drive it.

## Sources

- [heypcb home and pricing](https://heypcb.ai/) · [heypcb terms](https://heypcb.ai/terms) · [heypcb challenge](https://heypcb.ai/challenge)
- [RuntimeWire: Circuit World launch](https://runtimewire.com/article/heypcb-circuit-world-open-hardware-designs) · [RuntimeWire: multiplayer](https://runtimewire.com/article/heypcb-multiplayer-hardware-design)
- [KiCad MCP Pro](https://github.com/oaslananka/kicad-mcp-pro) · [KiCAD-MCP-Server](https://github.com/mixelpixx/KiCAD-MCP-Server) · [DeepPCB help](https://deeppcb.ai/help/)
