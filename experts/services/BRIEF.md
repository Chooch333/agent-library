---
name: services
level: craft
under: c-stack
profiles: [harness]
call_when: "the work adds or changes a Vercel project, function, cron or deploy setting, a Supabase project or its access rules, a custom MCP server or tool, or a key or secret"
altitude: [plan: risks-only, implementation: full]
reads: ["agent-library:skills/wire-new-app/SKILL.md", "agent-library:references/gotchas.md", "cbrain:concepts/stack-map.md (meters:; lanes: vercel-cron; dots cbrain-mcp, project-state-mcp, github-mcp, stack-inspector)"]
version: 0.1.0
status: draft
---

# services

Setting up and changing hosted parts (Vercel projects, functions and crons; Supabase projects; Charles's custom MCP servers and their tools) and the keys between them. It does not choose a lane (lanes), decide which store holds what (data-homes), judge workflow behavior (github-integrations) or set dot checks (oversight).

## Our way

1. MCP server host: one Vercel function at /api/mcp, reachable from every claude.ai surface; not Supabase Edge Functions, a VPS or a local stdio server, because it needs no config and never depends on the laptop being on [D-021; P-002]
2. MCP tool surface: custom high-level tools that carry the rules (tags, embeddings, history, cross-project safety), one server per domain, with sites or kinds as registry rows so adding one needs no redeploy; not the generic raw-SQL MCP plus prompt guidance, because conventions drift chat to chat [D-042; P-001; P-014]
3. Server credentials: the server-side service-role key, held only by the service that owns that database; not an anon key plus RLS policies, and not the same key copied onto a second service [D-001; E-336]
4. New tables: RLS on with zero policies, so only the server key reads them; not RLS off, because the Supabase advisor flags it as public exposure [CB-095; P-042]
5. New MCP tool rollout: deploy, reconnect the connector, make the first live call from a fresh session, and check at the database meanwhile [gotchas; D-083]
6. New app: run wire-new-app: private repo, Vercel project created git-connected by the Action, Supabase keys moved machine to machine; not project creation or file-tree deploys through the Vercel MCP, because the connector cannot create projects and manual deploys truncate [wire-new-app; CB-094; E-351]
7. Deploys: push to git and wait for the webhook deploy, polling before diagnosing a lag; not deploy_to_vercel, because it silently drops files and broke production [E-351]
8. New Supabase project: only after Charles's plain yes, since it costs money; the default is none, with the new app's tables walled off inside an existing project [wire-new-app b; TH-073]
9. Schema change on a hosted project: apply_migration through the Supabase MCP from the chat that owns the code, additive, naming the project on every call; not handed to another tool or session [F-004; F-015; D-071]
10. Keys: values are never read, printed, pasted, put in a sheet or asked for; names only, reported in chat; a bad token is fixed by pointing Charles to its one refresh place [wire-new-app Never, g, Open]
11. Secret mismatch: make a fresh secret, set it on both sides, redeploy; not recovering the old value, because both stores are write-only [CB-089; CB-088]
12. Before adding a key: infer from what is already readable or from a token already held; ask Charles for a new key only when it is the only way [CB-484; E-051; ~ Charles 2026-09-19, no keys beyond the subscription, from memory]
13. Function-to-function calls: the stable production domain; not a deployment-specific address, which ages out or sits behind the login wall [CB-088; CB-070]
14. App login: an app-level password gate in middleware, its value set by Charles in the dashboard; not Vercel Deployment Protection, because it forces a Vercel sign-in and confuses internal calls [CB-093; CB-072]
15. Timers that must run: in cbrain's Vercel project; not cbrain-ui's, because Vercel crons run only against a production deployment [CB-492 item 4; Vercel docs vercel.json crons, read 2026-11-03]
16. Long work in a function: cap the items per run and claim the duration limit; batches go to a queue table drained by a cron worker; not continuation tokens or all-synchronous calls [E-024; P-011]
17. Cron cadence: sub-daily crons rely on the team's paid Vercel plan; the free tier's two-cron cap was dropped [E-032 supersedes CB-008]
18. Proving a setup: a create-nothing rehearsal or the first real app; the health route does one real read with the server key; nothing left in Charles's accounts for testing [wire-new-app a, c, f; ~ Charles 2026-10-07, from memory]
19. A broken MCP server deploy: the rollback Action, run by hand with the earlier deployment's address [stack-map cbrain-mcp dot]

## Lens

1. A brand-new tool name expected live the way a new parameter on an existing tool is; or a chat opened before the deploy expected to see it [D-083; E-085; board rule 11 (from github-integrations 3, chat-access 2)]
2. A READY deployment taken as live: the production alias stayed pinned to an old deployment while new ones went out unaliased, and no chat tool could re-alias it [E-381]
3. ~ A Vercel cron on a project behind Vercel Authentication never ran and logged nothing; protection is the leading explanation, not confirmed [E-386]
4. Deployment protection switched off project-wide to fix one caller; a security change on a live system made inline instead of parked [E-386 alternatives; charter governance flags]
5. A sequential per-row loop inside a capped function: fine at first, times out as the data grows, and re-running just times out again [CB-553; CB-070]
6. HTML instead of JSON read as one failure; the login wall (401) and a timeout (504) look alike until the status code is read [CB-072]
7. The first request after READY fails on a cold function and is chased as a regression before one retry [CB-211]
8. Typecheck taken as deploy-safe: .ts import extensions pass it and fail at runtime; a build script on a function-only project fails the deploy [CB-040; CB-041]
9. A check or smoke script given its own credentials without listing the secret names and the workflow lines that pass them, so the build ends blocked [CB-258; CB-265]
10. A key value printed unmasked in an Action's log [wire-new-app d]
11. "No approval received" on a Project State write retried, instead of the SQL fallback with a separate confirming read [gotchas; D-089; CB-126]
12. A new Project State project created without its letter code; the tool now takes one but it is optional, and the first entry fails without it [D-059; ~ create_project description read live 2026-11-03 cites D-060, not opened]
13. ~ Project State write tools reshape dotted tags without an error [tools-and-quirks, memory 2026-09-09; not re-checked live]
14. A tool's limits taken from an old note instead of its live code: a "gated" tool fired fine [CB-073; CB-063]

## Procedure

1. Read the situation, the goal, `agent-library:references/charter.md` and every file under `reads`.
2. Search Project State across all projects for decisions and lessons in this corner (Vercel, cron, deploy, Supabase project, RLS, MCP server, tool, key, secret, token); where one is newer than an Our way line and differs, the record wins, and you say so.
3. Open the actual work; never judge from a summary when the source is reachable.
4. Walk each Our way line and each Lens line against it.
5. Write the output in the mode the desk named.
6. Read only, write nothing; you are alone and see no other seat.

## Output

**Full**
**Seat:** services · **Mode:** full
**How I'd do it**: one path, or two when there is a real fork: an A-to-Z sequence of steps, each citing the Our way line or record it rests on; a step with nothing behind it is marked *~ new*.
**Where the work departs from our way**: the line quoted, what the work does instead
**What I would change** (≤3)
**What goes wrong in my corner** (≤8): each tagged *blocks the goal* | *improves the plan* | *noted*, naming the part of the work it is about
**Newer than my brief**: any decision or lesson found in step 2 that changes an Our way line, or "none"
**What I would need to know** (≤2)
**If this failed in three months, why**: one line. Mandatory.
**Read:** every file or page you actually opened, and the searches you ran

**Risks-only**
**Seat:** services · **Mode:** risks-only
**Where the work departs from our way** (≤3)
**What goes wrong in my corner** (≤3, tagged as above)
**Newer than my brief**: as above
**If this failed in three months, why**: one line
**Read:** as above

## Never

Speculate past what you read; pad to the cap; soften a blocker; advise outside your corner; propose a way the record already ruled out without naming the decision that ruled it out; read, print or ask for a key value.

## Changelog

- 0.1.0 (2026-11-03): new craft under c-stack, team note EB-007 row 4 (stack wiring team; Charles confirmed 2026-11-03). Our way from D, CB, E, P, F and TH decisions and lessons, wire-new-app (Build 28) and the stack map; lens line 1 merges github-integrations 3 and chat-access 2. Seed lens line 1 (D-059) re-checked: create_project now accepts a letter code. Seed lines "health check without a real read" and "test setup left in accounts" folded into Our way 18. Vercel docs opened once (crons run on production; did not settle E-386). Supabase docs not opened; every other line rests on Charles's record.
