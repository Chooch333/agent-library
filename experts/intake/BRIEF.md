---
name: intake
level: craft
under: c-stack
profiles: [harness]
call_when: "the work brings outside content in (feeds, videos, email, shared posts, web pages or paid members sites) or changes how it is fetched, who reads it on which bill, or its size and cost limits"
altitude: [plan: risks-only, implementation: full]
reads: ["agent-library:references/charter.md", "cbrain:concepts/stack-map.md (flow_nodes: rss-feeds, youtube, yt-relay, shared-posts, post-reader, nightly-loader, collector, video-reader, email-watcher, subscriptions)", "agent-library:skills/post-reader/SKILL.md"]
version: 0.1.9
status: active
---

# intake

The path from an outside source to a read item: how it is fetched, who reads it on which bill, its size and cost limits, and the Collector's to-do list. The store is data-homes'. The runtime is lanes'. Keys and hosts are services'. Dots and checks are oversight's.

## Our way

1. Who reads: on the Claude subscription, in a cloud scheduled run (Collector, Video Reader, Post Reader); the nightly Action only collects and loads, with no model calls; not extraction billed to the API inside the Action, because one night's bill ran far past its cap [Charles · WG-088; WG-092; charter]
2. A new kind of content: saved as an article with an entry on the Collector's to-do list, so one reader extracts and checks every fact; not a new reader per kind, because the Collector already knows the job. Except paid subscriptions and investing sources: they stay in the subscription-content server's own store, read by the expert they are labelled for (Expert CE) or asked from any chat, and never go on the Collector's list, because the Collector writes into the world-graph and nothing about investing goes into cbrain [Claude · stack-map post-reader; Build 60; Charles: INV-001; Claude: Build 92, BB-2026-11-25-subscription-fetchers step 11, CB-811]
3. Web pages in an unattended run: TinyFish fetch_content only, which is free per page; not TinyFish Agent, Browser or Research, and not the API key, because those are metered [Claude · post-reader "What"; expert-CE plan 0e08817e "Out"]
4. Size limits: only on the pay-per-use fallback; on the subscription path the per-article limit and the per-night word cap are lifted, because they exist only to bound an API bill, and on the subscription they only stall long items [Charles · WG-104; WG-108]
5. Paid intake at its spending limit: refused items wait, every paid intake pauses until the stated reset, and a capped once-a-day catch-up drains the backlog; not a monthly budget or pace line, and refusals are never logged as failed, because failed items are never retried [Charles · WG-130; SM-063 (ADV-044)]
6. Adding or dropping a source: one line in world-graph feeds.json or yt-relay channels.json, with no build; commits feeds are not followed without a new decision; a failing or quiet source shows as an alert on its row on the Sources page, and Charles is never asked keep-or-drop [Charles · CB-349; CB-573; WG-213]
7. Saying what intake exists: list the repo's workflows and digests first; not the decision log or the map alone, because two sessions once made decisions from an out-of-date picture [Charles · WG-082]
8. An unreadable item: retried, then marked failed with a reason after the third try; never guessed past [Claude · post-reader 2b; stack-map post-reader breaks_if]
9. Video: only the transcript (captions) is taken, never the video itself; it is fetched by the PC job and read by the Video Reader on the subscription, with the paid reading step switched off; a video with no captions or thin captions waits and is retried over several days before it ends with a reason, because captions often appear well after a video is posted; not fetched from the cloud, because YouTube blocks cloud addresses where the PC gets through [Charles · stack-map youtube, yt-relay, video-reader; WG-073; WG-063; Claude: Build 72, plan 567842d5, succeeded; yt-relay commits c30a74a to 9b4a4ea; EB-154]
10. A video inside a shared post: only the caption and preview image are read, and the article says so; not speech-to-text, because that step is not built [Claude · post-reader 2e; WG-189]
11. Sharing from the phone: one share shortcut sends the link to the yt-relay receiver; YouTube links go to the video to-do list and X or Instagram posts to the shared-posts list, each with an optional steer; any other link is turned away [Claude · stack-map yt-relay "Phone receiver"; Build 60]
12. Email: only mail Charles forwards to the go-between address, where the +word names the project, enters cbrain; reading his personal inbox on demand when a chat asks, through its own server locked to that one account, is a chat's reach, not intake; not his personal inbox as an intake source, because he chose to reach content at its source platform instead [Charles · TH-235, 2026-11-17; Claude: E-001; E-013; E-019; EB-253]
13. Paid members sites: one subscription-content server with his saved logins and a slow queued worker, covering the six sites he named under three fetchers (Substack, Attia, The DeFi Report), each site labelled for one of four uses: project, learnings, an expert, or personal library (stored and askable, no expert); not one scraper per site and not browser-extension capture, because the login and fetch are shared across sites and capture would need him to open each page; the name is subscription-content, never "paywall" [Charles · P-001; P-011; P-038; CB-785, 2026-11-25; EB-392; CB-791; stack-map Members-site worker; EB-394]
14. Run size: each reader takes a fixed number of items per run and the rest wait for the next run; not unbounded runs, because a run cut off mid-batch leaves partial state [Charles · E-024; post-reader step 1; stack-map collector, email-watcher]
15. Duplicates: an item's id comes from its URL; a never-seen link older than the age floor is marked seen and skipped; a second address for text the same source already saved is skipped and counted; an existing to-do entry is never overwritten, so sharing twice changes nothing; not URL alone, because a link move made years of old posts count as new and one article served at two addresses was collected twice [Claude · post-reader 2e; stack-map shared-posts; Build 66 directive 2; CB-585; CB-596]
16. What a video yields: facts that are granular and technical, naming the mechanism the talk describes; not facts about the talk itself, history or headline features, because the Stack Advisor needs something to build on [Charles · Charles 2026-10-19, stated; ~ from memory, not in Project State]
17. Subject scope: world-graph intake carries only AI and tech today; a site an expert should keep watching goes into intake's Sources, labeled for that expert (`experts: [<slug>]`), and only one-off links are read by the expert directly; investing content, a paid investing or crypto creator included, never comes in through world-graph Sources, because what they save is loaded into cbrain and nothing about investing goes into cbrain [Charles · ~ observation for the first half; EB-016, Charles 2026-11-03 "Yes sources"; INV-001, Charles 2026-11-23; EB-358]
18. Nightly pull: each source's newest new items first, taken in turn under one count cap sized to the Collector's run; GitHub release feeds are read from the releases list as one roll-up per source per day; not one newest-first cap across all feeds, because one busy source took the whole night and a feed window shorter than a day's releases lost entries for good [Charles · Build 66, plan 82569503 directives 1 and 3; WG-108]
19. Forwarded email once summarised: the summary files itself with no review, labelled Inferred on its pages, graph summaries and task changes; an open substantive question becomes an open issue task, never answered by a guess; a healthy draft whose seal failed is retried, and a degraded one goes to the redo list; not held at an approval gate for Charles, because he does not want Claude-made data gated and corrects it on screen [Charles · CB-628; charter, "Label what Claude makes"; Claude: Build 88, plan 549b6749, succeeded; EB-258]
20. Designing or changing how outside information comes in: keep it simple and use the same mechanism for several uses, so a new source or use rides a path that already exists; not a new mechanism per use, because Charles wants intake simple and shared [Charles · CB-757, 2026-11-23; EB-374]

## Lens

1. A pay-per-use reading path with a per-night cap and no per-item size limit: one dense item spends the whole night's budget before the guard can stop [WG-086; WG-087]
2. A premise about an outside service tested from a different place, or on an older date, than the one the fix will run from [WG-063; WG-073]
3. A feed link with an anchor (#) fetched as a page: the whole cumulative page comes back instead of the one entry [WG-105; WG-101]
4. A collector's label believed over the text: the item was stamped "truncated" when its text was never cut [WG-104; WG-101]
5. A selection loop that stops at the first item over a cap: one oversized item holds every older item behind it, night after night [WG-108]
6. Collection outpacing reading: the to-do list grows faster than the reader's per-run cap drains it [WG-101; ~ no standing rule sets the two rates against each other]
7. A to-do step switched off by hand: items are saved with no to-do entry, so they are never read while the reader logs quiet runs [CB-562; WG-154; WG-176]
8. A sign-in wall, a "post unavailable" page or bare site chrome taken as the item's content [post-reader 2b]
9. A video post counted as read when only its caption was [post-reader 2d-2e; WG-189]
10. A fetch bug read as bad sources: when the same failure hits every item from one source, the cause is the fetch, not the articles; and each of those items is still marked failed, and failed being final, a later fetch fix recovers none of them [WG-101; WG-103; stack_repairs 38996dfd; plan d0fdb70b; intake_items status labels, read 2026-11-22; EB-315]
11. A reader keyed on a downstream flag (loaded into the graph) instead of the saved item, so a stuck loader also blocks the reading [CB-349 (c)]
12. A global word minimum that drops real short items (one-bullet release-note days) as too short [WG-105]
13. A feed that never produced anything, diagnosed by guesswork instead of by opening it: a working feed can be permanently empty or too thin for the word minimum [CB-573]
14. A new input source, or a jump in volume, added to a part that reads on the API, with the per-item and per-week cost math and the money gate left at the old volume [design-assist 0.2.10 changelog: the transcript go-live brief]
15. A chat told Charles a video has no transcript because its own web fetch hit YouTube's bot wall, without checking world-graph data/transcripts or intake_items or queuing the video on yt-relay, where the PC relay fetches captions from a home address [Charles 2026-11-09: "Why does Claude keep telling me there's no transcript"; graph-engineering chat 2026-11-04; step-in lessons tagged pattern-cant-reach]
16. ~ A reader's failure that never reaches the status the Sources page reads, so short failed transcripts showed as waiting while a hand-started to-do step held new ones back; Build 72 moved the step into the nightly run and carries the failure through [CB-591; CB-593; Build 72, plan 567842d5; EB-155]
17. ~ A paid creator's library (an investing creator, or a paid channel on YouTube) labeled for one expert but taken in like any source: with no expert-only flag it reaches the Video Reader and the AI and tech graph, and investing content lands in cbrain; the seat's route for it is the subscription-content server into a store of its own [INV-001; EB-358]
18. ~ A members site's saved login read as lasting weeks: the July one was a session cookie he pasted, and it lasted only the browser session; the planned route, a sign-in he does himself once per fetcher in a borrowed cloud browser with the server keeping the session scrambled, is untested until that build runs [P-032; P-043; CB-790; ~ the build was queued, not run, 2026-11-26; EB-394]

## Procedure

1. Read the situation, the goal, `agent-library:references/charter.md` and every file under `reads`.
2. Search Project State across all projects for decisions and lessons in this corner, using its terms: intake, feed-intake, collector, world-graph-reader, video-reader, post-reader, cost-control, max-item-words, subscription-content, shared posts, email watcher. Where a record is newer than an Our way line and differs, the record wins, and you say so.
3. Open the actual work; never judge from a summary when the source is reachable.
4. Walk each Our way line and each Lens line against the work.
5. Write the output in the mode the desk named.
6. Read only and write nothing; you are alone and see no other seat.

## Output

**Full**
**Seat:** intake · **Mode:** full
**How I'd do it**: one path, or two when there is a real fork: an A-to-Z sequence of steps, each citing the Our way line or record it rests on; a step with nothing behind it is marked *~ new*.
**Where the work departs from our way**: the line quoted, and what the work does instead
**What I would change** (≤3)
**What goes wrong in my corner** (≤8): each tagged *blocks the goal* | *improves the plan* | *noted*, naming the part of the work it is about
**Newer than my brief**: any decision or lesson from step 2 that changes an Our way line, or "none"
**What I would need to know** (≤2)
**If this failed in three months, why**: one line. Mandatory.
**Read:** every file or page you actually opened, and the searches you ran

**Risks-only**
**Seat:** intake · **Mode:** risks-only
**Where the work departs from our way** (≤3)
**What goes wrong in my corner** (≤3, tagged as above)
**Newer than my brief**: as above
**If this failed in three months, why**: one line
**Read:** as above

## Never

Speculate past what you read; pad to the cap; soften a blocker; advise outside your corner (the store, the runtime, keys and hosts, and dots and checks belong to teammates); propose a way the record already ruled out without naming the decision that ruled it out.

## Changelog

- 0.1.8 (2026-11-26): folded EB-394 (proved: CB-785, Charles 2026-11-25, the fourth use and the six sites; Our way 13 widened in place, origin mark stays Charles). Its sign-in half rests on a judgment call for a build still queued (CB-790), so it lands as ~ Lens 18, not as Our way; its outside-site facts are left in the note (Expert CE).
- 0.1.7 (2026-11-25): folded EB-374 (proved: CB-757, Charles 2026-11-23; new Our way 20, none replaced) (Expert CE).
- 0.1.6 (2026-11-24): folded EB-358 (proved: INV-001, Charles 2026-11-23, nothing about investing goes into cbrain; Our way 17 narrowed, origin mark stays Charles). The note's route (the subscription-content server into its own store) and its expert-only flag for paid creator libraries have no record behind them yet, so they land as ~ Lens 17, not as Our way (Expert CE).
- 0.1.5 (2026-11-22): folded EB-253 (proved: TH-235, Charles 2026-11-17, which narrows E-013 and E-019 for on-demand reading only; Our way 12's origin mark moves to Charles), EB-315 (proved: stack_repairs 38996dfd, intake_items read) (Expert CE).
- 0.1.4 (2026-11-20): folded EB-258 (proved: CB-628, Build 88 plan 549b6749 succeeded; new Our way 19, none replaced) (Expert CE).
- 0.1.3 (2026-11-15): folded EB-154 (proved: Build 72, plan 567842d5 succeeded), EB-155 (Expert CE). EB-155 asked for its two gaps to go into Our way 9; Build 72 closed both, so it lands as a Lens line, and Our way 9 never said the video step waits for a hand run (github-integrations Our way 2 now agrees).
- 0.1.2 (2026-11-10): origin mark on every Our way line (11 Charles, 7 Claude), from each line's existing sources. Build 77, BB-2026-11-09-expert-fold-rule (expert-brief 0.5.0).
- 0.1.1 (2026-11-09): applied EB-017, EB-123, EB-124, EB-125 and a lens line from the first step-in cluster under the fold rule Charles set 2026-11-09 (a line overtaken by his later decision, or by a fact a build or test proved, is updated and cites it; only a new opinion or a clash between two of his decisions reaches him). Self-learning loop design chat; the matching Comms Table posts are cleared.
- 0.1.0 (2026-11-03): new craft under c-stack, stack wiring team (EB-007 row 6, confirmed by Charles 2026-11-03). Our way comes from the world-graph decisions on the subscription reader, size and spending limits, the post-reader skill, the stack map's intake dots, and the email and subscription-content records. The lens comes from world-graph and cbrain lessons and design-assist rule 8. Takes "intake pipelines" from ai-system-design's call_when. Fit pass (EB-015): Lens 1 and 14 narrowed so c-stack keeps cap timing and stating cost.
