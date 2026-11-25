# Browser use

*Version 0.3.0 (2026-11-25), draft.* Read before the first browser tool call in a chat. One way, every chat. ("I want to standardize browser use so Claude does it the same every time... I don't want a new chat to have to figure it out, or do it wrong." Charles, 2026-11-24.)

This file is only the rules for getting around in the browser: which browser, which PC, what to do when a page stops. What a job does once the page is open lives with that job ("this was just about rules around navigating through the browser use specifically", Charles, 2026-11-24):
- Pages only Charles can click (keys, tokens, permissions): `references/his-only-clicks.md`
- Photo-real finish on a render: `skills/arch-render/SKILL.md`, "AI finish pass"
- Asking ChatGPT or Gemini for their view: `references/ask-another-model.md`

## Never

- Type, read back, screenshot or hold a password, key or token. Those clicks are Charles's (charter 5).
- Switch browsers without saying so. Never pick between browsers yourself.
- Tell Charles a browser job can't be done before step 1 of "Which PC".

## Which browser

Chrome on his PC (the Claude in Chrome tools). One exception: watching a video in a post follows `references/watch-video.md`, which uses the Claude app's built-in browser. Chrome's tools missing from the chat: say "not available here" in one line with the reason, and stop that step.

## Which PC

Chrome lists his browsers only as "Browser 1", "Browser 2", "Browser 3" and so on. The names mean nothing and names he sets never reach Claude. **Three or four browsers may be connected at any time** (Charles, 2026-11-25), not only two. The device id is the only thing that tells them apart, and an id matched to a PC one day did not hold the next (2026-11-25, below), so the table is a hint, never proof.

| Device id | PC | Confirmed |
|---|---|---|
| `4379809c-c9a3-43d8-b323-1f153ce55980` | Work PC | Charles, three-site sweep, 2026-11-25 (he saw Weather.gov) |
| `09d7cdd3-26d0-465e-ab6c-db2822f87102` | Unknown | Matched to the work PC by a test tab on 2026-11-24, but on 2026-11-25 Charles at his work PC did not see its tab. Not his work PC that day |
| `1257f9d2-0e31-4b05-a6da-dfc3f91f43ca` | Unknown | First seen 2026-11-25; its tab was not on the work PC |

1. **List** the connected browsers. None: say Chrome isn't open on any PC, ask him to open it, stop.
2. **One browser connected**: use it; say which PC the table hints in one line. If the page doesn't appear in front of him, go to step 3.
3. **More than one connected: the three-site sweep**, once per chat, before the first real page. (Charles, 2026-11-25: "I like this method.")
   - Open one new tab in each connected browser, each on a different site, in list order:
     1. Wikipedia (`https://www.wikipedia.org`)
     2. Weather.gov (`https://www.weather.gov`)
     3. NASA (`https://www.nasa.gov`)
     4. Library of Congress (`https://www.loc.gov`), when a fourth is connected
   - Ask one tappable question: "Which site do you see?" with the site names as choices plus "None of them". Never "Browser 1".
   - The browser whose site he sees is the PC he's at. Use that tab for the job (navigate it), close the sweep tabs in the others, and write the result into the table in the same turn (id, PC, date).
   - "None of them": Chrome on the PC he's at isn't connected. Say so in one line and ask him to open the Claude extension there.
   - His message already names a PC ("on my work PC") does not skip the sweep when several are connected: the name tells you which row to write, the sweep tells you which id it is.
4. **Say it**: "Using Chrome on your work PC." One line, before the first real page opens.
5. **Re-check before each burst of browser work**: list again; if the browser in use is not the one chosen in this chat, select it again and say so. (Another open chat may have moved it. ~ Whether one chat's choice moves the others is reported publicly, not yet tested here.)
6. Use the PC he is sitting at unless he says otherwise: a check on the far PC is a click he can't make.

## Signing in

Opening a tab in Chrome on a site Charles already uses signs him in on its own: his username and password fill in automatically. Sign-in is usually not needed, so it is not a hurdle: don't warn about it, ask about it or plan around it. Just open the page. (Charles, 2026-11-24.) A sign-in page usually means the tab opened on the wrong PC: run the sweep before telling him to sign in (2026-11-25: Vercel asked for sign-in on one browser and opened signed in on the PC he was at).

## When something stops the page

| What happened | Do |
|---|---|
| A code from his phone (GitHub and Vercel ask for one at random) | Tell him in one line: "GitHub wants a code from your phone on your work PC." Wait until he says it's done, then carry on. |
| Sign-in or "confirm it's you" check | First make sure it's the right PC (sweep). Then: one line, his click, wait. |
| "Are you human" check | Same: his click. Never try to pass it. |
| Tab didn't appear where he is | Wrong PC: run the three-site sweep (Which PC, step 3). |
| Chrome not answering | "Chrome on your work PC isn't answering: is it open?" One retry after he answers. |
| No PC reachable | Say so, put the job on the Next steps list, stop. |

Three failed tries at the same step: stop and say what was tried.

Always: work in a new tab, never one of his; close every tab Claude opened when done, except pages left open for his clicks.

## Keeping this file right

This file learns where it is used. When a browser step fails, surprises, or works a new way (a new kind of stop, a site that behaves differently, a PC id that changed, something unproven that just got proven), the chat that hit it fixes the line here in the same turn, dated, without asking Charles, and bumps the version. A stop that isn't in the table gets a row once it's handled. Judgment about how browser use should work (not a step that broke) goes to the lanes expert like any judgment ask.

**When this has outgrown a file.** Charles does not monitor this ("I don't want to monitor", 2026-11-24). The chat that makes an edit here counts, every time: the rows in "When something stops", and the entries in the Changelog. More than 10 stop rows, or more than 8 changelog entries, means browser use has become a field of its own. That chat then, in the same turn: tells Charles in one line ("Browser use has collected enough rules and exceptions that it should be its own craft expert: say the word and I'll grow it"), and files one note on Project State `expert-bench` tagged `grow-ask` naming the field (browser use) and this file. Once a `grow-ask` note for browser use exists, later chats don't tell him again. (Count at 0.3.0: 6 stop rows, 4 changelog entries.)

## What is and isn't proven

- Proven: opening tabs on his PCs from a cloud chat (2026-11-24); sites he already uses open signed in on the PC he's at; the three-site sweep finds the right PC in one question (2026-11-25, three browsers connected).
- Disproven: that a device id stays matched to the same PC from one day to the next (2026-11-25). That's why the sweep runs every chat with more than one browser.
- Not proven: whether one chat's browser choice moves other open chats; downloads on the home PC; which PC the other two ids are; any of this from another Project, from the phone, or with nobody at the PC.
- Other Projects follow this only if their instructions read AGENT.md.

## Changelog

- **0.3.0** (2026-11-25): the three-site sweep replaces "ask Work PC or home PC" and the single test tab: one tab per connected browser on Wikipedia, Weather.gov, NASA (Library of Congress for a fourth), and Charles says which site he sees (Charles: "I like this method. Make this a learning"). Three or four browsers may be connected at once. Yesterday's work-PC match did not hold: the work PC is now a different id, the old one is unknown, and a third id appeared. A sign-in page now means "check the PC first".
- **0.2.1** (2026-11-24): "When this has outgrown a file": the editing chat counts stop rows and changelog entries; past 10 rows or 8 entries it tells Charles once and files a `grow-ask` note, so he never has to monitor it (Charles, 2026-11-24).
- **0.2.0** (2026-11-24): cut to navigation rules only at Charles's word. The three jobs moved out (his-only clicks and ask-another-model to their own reference files, the finish pass into arch-render). "Never run unattended" removed. "Which browser" cut from a table to one line. Added: Signing in (sites auto sign in; not a hurdle), the phone-code stop, and "Keeping this file right".
- **0.1.0** (2026-11-24): first version. Charles's decision in a Stack Work chat ("standardize browser use"); Expert Desk seats ai-system-design and lanes. Work PC confirmed by test tab.
