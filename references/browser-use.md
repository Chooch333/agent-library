# Browser use

*Version 0.2.1 (2026-11-24), draft.* Read before the first browser tool call in a chat. One way, every chat. ("I want to standardize browser use so Claude does it the same every time... I don't want a new chat to have to figure it out, or do it wrong." Charles, 2026-11-24.)

This file is only the rules for getting around in the browser: which browser, which PC, what to do when a page stops. What a job does once the page is open lives with that job ("this was just about rules around navigating through the browser use specifically", Charles, 2026-11-24):
- Pages only Charles can click (keys, tokens, permissions): `references/his-only-clicks.md`
- Photo-real finish on a render: `skills/arch-render/SKILL.md`, "AI finish pass"
- Asking ChatGPT or Gemini for their view: `references/ask-another-model.md`

## Never

- Type, read back, screenshot or hold a password, key or token. Those clicks are Charles's (charter 5).
- Switch browsers without saying so. Never pick between two browsers yourself.
- Tell Charles a browser job can't be done before step 1 of "Which PC".

## Which browser

Chrome on his PC (the Claude in Chrome tools). One exception: watching a video in a post follows `references/watch-video.md`, which uses the Claude app's built-in browser. Chrome's tools missing from the chat: say "not available here" in one line with the reason, and stop that step.

## Which PC

Chrome lists his browsers only as "Browser 1" and "Browser 2". The names mean nothing and names he sets never reach Claude. The device id is the only thing that tells the PCs apart.

| Device id | PC | Confirmed |
|---|---|---|
| `09d7cdd3-26d0-465e-ab6c-db2822f87102` | Work PC | Charles, test tab, 2026-11-24 |
| `4379809c-c9a3-43d8-b323-1f153ce55980` | Home PC | ~ by elimination, 2026-11-24; not yet confirmed by a test tab |

1. **List** the connected browsers. None: say Chrome isn't open on either PC, ask him to open it, stop.
2. **Match** each id to the table.
   - His message already names the PC ("on my work PC"): use that one.
   - One browser connected and its id is confirmed in the table: use it; say which PC in one line.
   - Two connected: ask once per chat, "Work PC or home PC?" (a tappable question, PC names only, never "Browser 1"). Then select that id.
   - An id not in the table, or a row marked ~: open one test tab, ask "Which PC is this tab on?", and write the answer into this table in the same turn (id, PC, date). Close the test tab.
3. **Say it**: "Using Chrome on your work PC." One line, before the first page opens.
4. **Re-check before each burst of browser work**: list again; if the browser in use is not the one chosen in this chat, select it again and say so. (Another open chat may have moved it. ~ Whether one chat's choice moves the others is reported publicly, not yet tested here.)
5. Use the PC he is sitting at unless he says otherwise: a check on the far PC is a click he can't make.

## Signing in

Opening a tab in Chrome on a site Charles already uses signs him in on its own: his username and password fill in automatically. Sign-in is usually not needed, so it is not a hurdle: don't warn about it, ask about it or plan around it. Just open the page. (Charles, 2026-11-24.)

## When something stops the page

| What happened | Do |
|---|---|
| A code from his phone (GitHub and Vercel ask for one at random) | Tell him in one line: "GitHub wants a code from your phone on your work PC." Wait until he says it's done, then carry on. |
| Sign-in or "confirm it's you" check | Same: one line, his click, wait. |
| "Are you human" check | Same: his click. Never try to pass it. |
| Tab didn't appear where he is | Wrong PC: go back to step 2 of "Which PC" and use a test tab. |
| Chrome not answering | "Chrome on your work PC isn't answering: is it open?" One retry after he answers. |
| Neither PC reachable | Say so, put the job on the Next steps list, stop. |

Three failed tries at the same step: stop and say what was tried.

Always: work in a new tab, never one of his; close every tab Claude opened when done, except pages left open for his clicks.

## Keeping this file right

This file learns where it is used. When a browser step fails, surprises, or works a new way (a new kind of stop, a site that behaves differently, a PC id that changed, something unproven that just got proven), the chat that hit it fixes the line here in the same turn, dated, without asking Charles, and bumps the version. A stop that isn't in the table gets a row once it's handled. Judgment about how browser use should work (not a step that broke) goes to the lanes expert like any judgment ask.

**When this has outgrown a file.** Charles does not monitor this ("I don't want to monitor", 2026-11-24). The chat that makes an edit here counts, every time: the rows in "When something stops", and the entries in the Changelog. More than 10 stop rows, or more than 8 changelog entries, means browser use has become a field of its own. That chat then, in the same turn: tells Charles in one line ("Browser use has collected enough rules and exceptions that it should be its own craft expert: say the word and I'll grow it"), and files one note on Project State `expert-bench` tagged `grow-ask` naming the field (browser use) and this file. Once a `grow-ask` note for browser use exists, later chats don't tell him again.

## What is and isn't proven

- Proven: opening tabs on his work PC from a cloud chat (2026-11-24); sites he already uses open signed in; the two device ids held across a Chrome reconnect the same day.
- Not proven: id stability over weeks; whether one chat's browser choice moves other open chats; downloads on the home PC; any of this from another Project, from the phone, or with nobody at the PC.
- Other Projects follow this only if their instructions read AGENT.md.

## Changelog

- **0.2.1** (2026-11-24): "When this has outgrown a file": the editing chat counts stop rows and changelog entries; past 10 rows or 8 entries it tells Charles once and files a `grow-ask` note, so he never has to monitor it (Charles, 2026-11-24).
- **0.2.0** (2026-11-24): cut to navigation rules only at Charles's word. The three jobs moved out (his-only clicks and ask-another-model to their own reference files, the finish pass into arch-render). "Never run unattended" removed. "Which browser" cut from a table to one line. Added: Signing in (sites auto sign in; not a hurdle), the phone-code stop, and "Keeping this file right".
- **0.1.0** (2026-11-24): first version. Charles's decision in a Stack Work chat ("standardize browser use"); Expert Desk seats ai-system-design and lanes. Work PC confirmed by test tab.
