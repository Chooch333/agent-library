# Browser use

*Version 0.1.0 (2026-11-24), draft.* Read before the first browser tool call in a chat, and before telling Charles a step is his to click. One way, every chat. ("I want to standardize browser use so Claude does it the same every time... I don't want a new chat to have to figure it out, or do it wrong." Charles, 2026-11-24.)

Lane facts (what each place can reach) live in cbrain `concepts/stack-map.md` `lanes:`; this file holds the steps and the browser table.

## Never

- Type, read back, screenshot or hold a password, key or token. Those clicks are Charles's (charter 5).
- Switch browsers without saying so. Never pick between two browsers yourself.
- Run any of this unattended. Every job here needs Charles reachable: a sign-in check stops the page and only he can click it.
- Tell Charles a browser job can't be done before step 1 below.

## Which browser for which job

| Job | Browser | Why |
|---|---|---|
| His-only clicks; downloads; driving ChatGPT or Gemini; any site that needs his sign-in | **Chrome on his PC** (Claude in Chrome tools) | His real sign-ins; Claude handles the save step itself |
| Watching a video in a post | The Claude app's built-in browser, per `references/watch-video.md` | Proven there; Chrome untested for it |
| A public page that needs no sign-in | Web fetch from the chat; no PC browser | No PC needed |

A browser's tools missing from the chat: say "not available here" in one line with the reason, and stop that step.

## Which PC (Chrome)

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
5. For his-only clicks, always the PC he is sitting at. For the other jobs, the PC he is at unless he says otherwise: a sign-in check on the far PC is a click he can't make.

## When something stops the page

| What happened | Say, in one line |
|---|---|
| Sign-in or "confirm it's you" check | "GitHub wants a sign-in check on your work PC: one click, then tell me." Wait. |
| "Are you human" check | Same: his click. Never try to pass it. |
| Tab didn't appear where he is | Wrong PC: go back to step 2 and use a test tab. |
| Chrome not answering | "Chrome on your work PC isn't answering: is it open?" One retry after he answers. |
| Neither PC reachable | Say so, put the job on the Next steps list, stop. |

Three failed tries at the same step: stop and say what was tried.

Always: work in a new tab, never one of his; close every tab Claude opened when done, except pages left open for his clicks.

## Job 1: his-only clicks (keys, tokens, permissions, sharing) — proven

Proven 2026-11-23 (personal Gmail setup) in Chrome with Charles present.

1. First check whether the step can be done with no click of his at all: keys passed machine to machine (`skills/wire-new-app`), or a connector that already has the access. Only what's left comes here.
2. Work out the full list of pages before opening any: every place a key, token or permission is created, shared and saved (GitHub, Google, Vercel, Supabase and so on).
3. Open them all, one tab each, in the order he'll use them, on the PC he's at.
4. Give him one card: a numbered list, one line per tab, the exact click and the exact name to type or pick. Say where each value goes next ("copy it; tab 3 is where it's pasted"). Never ask him to paste a value into the chat.
5. Stop looking: once a page may show a secret value, take no screenshot and read no page text until he says he's done.
6. When he says done, check the result by name only (the secret's name exists, the permission shows, the run goes green), never by value. Then close the tabs.

## Job 2: photo-real finish pass on a render — draft, not yet run by Claude

Charles did this by hand with ChatGPT and judged it very successful (a plaza model with photo-wrapped buildings; ChatGPT cleaned the whole image to read as a photo). On his subscriptions it costs nothing extra. Stays draft until one real run.

1. Make the render and file it where renders live (`skills/arch-render`).
2. Open ChatGPT or Gemini in a new tab. Gemini is his pick for images when both would do.
3. Get the render to the model. Two routes, both unproven; the first real run tries A, then B, and this file keeps the one that works:
   - **A. Claude carries it**: upload the render into the chat page (the upload tool takes 3.8 MB a call; shrink or split above that), ask for the finish, download the result through Chrome, bring it back over the PC link and file it beside the render.
   - **B. The model fetches and saves back** through its own connection to his GitHub (his decision of 2026-11-20 for Gemini). Unproven for image files.
4. The ask to the model: keep the geometry, camera, buildings and signage exactly; change only what reads as computer-made (surfaces, light, plants, people, sky). One image per render.
5. Check the result against the render before Charles sees it: same building, same camera, nothing added or removed. A changed design is a fail, not a nicer picture.
6. File both; label the finished one "Inferred · finish pass by <model>".

Needs before the first run: the PC link up on the PC being driven (route A's return leg rides it).

## Job 3: ask another model for its view — draft, not yet run

Same steps as job 2 without the file. Stays draft until one real run.

1. Write the question so it stands alone: the other model has none of this chat. Include the material it needs; never a key, and nothing Charles has marked withheld.
2. One new chat in ChatGPT or Gemini, one question, read the whole answer.
3. Bring it back as "<Model>'s view", labelled Inferred, in your own words and short. Its claims count only once checked against the source they cite; say which were checked.
4. Where it disagrees with Claude, say so plainly and say which Claude thinks is right and why. Don't blend the two into one answer.

## What is and isn't proven

- Proven: opening tabs on his work PC from a cloud chat (2026-11-24); the two device ids held across a Chrome reconnect the same day; job 1 (2026-11-23).
- Not proven: id stability over weeks; whether one chat's browser choice moves other open chats; both return routes in job 2; the save step on the home PC; any of this from another Project or from the phone.
- Other Projects follow this only if their instructions read AGENT.md.

## Changelog

- **0.1.0** (2026-11-24): first version. Charles's decision in a Stack Work chat ("standardize browser use"); Expert Desk seats ai-system-design and lanes. Work PC confirmed by test tab.
