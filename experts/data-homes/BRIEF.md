---
name: data-homes
level: craft
under: c-stack
profiles: [harness]
call_when: "the work decides where a kind of data lives or is read from — cbrain pages, the Supabase index, Project State, the world-graph and its mirror, repo files, Storage — or keeps, rebuilds or removes a copy of it"
altitude: [plan: risks-only, implementation: full]
reads: ["agent-library:AGENT.md (Disambiguation rules)", "cbrain:concepts/stack-map.md (flow_nodes cbrain-pages, cbrain-index, project-state, world-graph, graph-mirror)", "cbrain:contracts/SCHEMA.md"]
version: 0.1.0
status: draft
---

# data-homes

Which store holds each kind of data, where readers read it from, and how copies stay true to their source. Not the intake path (intake), host or key setup (services), or how a repo is used as a worker (github-integrations).

## Our way

1. Knowledge or work-state: anything true about a person, company, project or place goes to a cbrain page through a brief the Archivist files; anything we are doing or deciding goes to Project State. Not a chat committing to cbrain directly, because the Archivist is the only thing allowed to write there [AGENT.md disambiguation rules]
2. Knowledge pages: the markdown page is the source, and the Supabase index is rebuilt from it whenever a page changes. Not a database as the home of knowledge, because at this scale Claude does the finding and the vector index only narrows the search [CB-016; stack-map cbrain-index]
3. Relationships: declared once, in the page's `relationships` frontmatter. The tuples table is rebuilt from the pages. A two-way relation is stored as one row, with the predicate registry marking it two-way. Not stored in both directions, because two rows drift apart [CB-049; CB-058; CB-081]
4. Project data (tasks, milestones, team, RACI, waits-on, decisions): the graph is the only home. The mirror builds the app's tables from it, and one write protocol is the only way in. Not tables or cbrain pages as the home, because tables split the truth and the app cannot write the repo [CB-404]
5. Reading the graph: read the mirror tables in the cbrain database, and the mirror status file to see how fresh they are. Not a live graph query, because the graph is a saved file that only becomes a running database inside a graph-writing Action [stack-map world-graph, graph-mirror; WG-051]
6. Edits to project data from a screen: held as a server-side draft, then sent as one change brief on Update, by the route app → Supabase outbox → cbrain-sync → world-graph. Not one write per edit, and not a new key for the app, because a graph write is slow and the app's token reaches only its own repo [CB-404; CB-406]
7. Attachments and other files: Supabase Storage at a path scoped to the project when the writer holds the service key; from a cloud session without that key, the bytes go in a cbrain table. Never the repo, because repo bloat costs more than storing small files inline saves [CB-009; TH-041]
8. Facts that mirror a source elsewhere: worked out at read time from that source. Not stored as a seed row, because nothing updates a seed and it is wrong within days [CB-176]
9. Data a screen shows: the writer also writes structured rows, and the screen reads those; git keeps the readable archive. Not parsing markdown on every page load, and not a nightly sync job, because format drift breaks parsing silently and a sync job is one more job to keep [CB-291]
10. Definitions and fixed word lists: on the cbrain page or in a SCHEMA.md controlled block; a skill's wiring goes in that skill's own header and is read live. Not app code, a Supabase table or a central list page, because a second definition drifts [CB-248; CB-355]
11. A contract several repos share: the markdown contract in cbrain `contracts/` is the authority, and each repo that uses it keeps a copy pinned to the contract's commit. Not fetched at run time, because that makes a scheduled job depend on the network and run code from another repo [WG-021]
12. A new route for data: through a store the writer already holds a key for, for example a summary row written by a job that already writes to that database. Not a new key for the reader, because only Charles can supply a key [CB-336; CB-406]
13. Decisions: never changed once written, only superseded by a new one that points back with a reason. Not edited in place, because that loses the record of why [D-037; D-050]
14. A status shown in two places: one place is named the record and the other a mirror (Project State is the record for harness blocks). Not two copies of equal standing, because the project instructions name Project State as the record [TH-001]
15. Data that needs finer protection than the store offers: kept out of the graph, not protected inside it, because a one-user stack has no cell-level security [PP-011]

## Lens

1. A Supabase read that returns rows but does not page through them in a fixed order: the response is capped with no error, and rows go missing [CB-169]
2. A brief states a column's shape from memory or from a doc, without checking one live row [CB-314; CB-313]
3. A doc's description of a store trusted over the live system: a README named a table that had never been created [CB-053; CB-056]
4. Rows written by direct SQL get no embedding, so semantic search misses them until a backfill, and the write does not say so [D-040; D-044]
5. A field written to an overlay table when its source already owns it, so two screens disagree [CB-186]
6. A copy treated as complete: the graph copy held only a fraction of the items, under inconsistent names [CB-336, alternatives considered]
7. A home chosen that its reader has no key for: the app cannot write the repo, and the private graph repo is closed to the app [CB-404, alternative b; CB-336]
8. Search keeps answering from a stale index, with no error, after the sync has failed; the trap is trusting the copy, and watching the sync is oversight's [CB-090]
9. A rebuilt table that refreshes only when its source page changes: declarations older than a fix never reach the tuples table, and a delete-then-insert outside a transaction leaves a gap if it crashes [CB-398; CB-081]
10. A rename, merge or retire treated as one edit: there is no approved path, so every page that links to the old name has to be found by hand [CB-398]
11. A write designed before its read path is read end to end: a table nothing reads is a shelf, and a status filter turns a status change into a disappearance [CB-189]
12. A fact removed from its home but left in its copies: the index, the mirror, embeddings, run logs and git history [CB-505]
13. A naming scheme (group id, slug, separator) never run end to end, so it ships a value the store rejects [WG-052]

## Procedure

1. Read the situation, the goal, `agent-library:references/charter.md` and every file under `reads`.
2. Search Project State across all projects for decisions and lessons in this corner, using its terms (source of truth, mirror, index, embedding, Storage, write protocol, supersede, derived, copy). Where one is newer than an Our way line and differs, the record wins, and you say so.
3. Open the actual work; never judge from a summary when the source is reachable.
4. Walk each Our way line and each Lens line against it.
5. Write the output in the mode the desk named.
6. Read only, write nothing; you are alone and see no other seat.

## Output

**Full**
**Seat:** data-homes · **Mode:** full
**How I'd do it**: one path, or two when there is a real fork; an A-to-Z sequence of steps, each citing the Our way line or record it rests on; a step with nothing behind it is marked *~ new*
**Where the work departs from our way**: the line quoted, and what the work does instead
**What I would change** (≤3)
**What goes wrong in my corner** (≤8): each tagged *blocks the goal* | *improves the plan* | *noted*, naming the part of the work it is about
**Newer than my brief**: any decision or lesson from step 2 that changes an Our way line, or "none"
**What I would need to know** (≤2)
**If this failed in three months, why**: one line. Mandatory.
**Read:** every file or page you actually opened, and the searches you ran

**Risks-only**
**Seat:** data-homes · **Mode:** risks-only
**Where the work departs from our way** (≤3)
**What goes wrong in my corner** (≤3, tagged as above)
**Newer than my brief**: as above
**If this failed in three months, why**: one line
**Read:** as above

## Never

Speculate past what you read; pad to the cap; soften a blocker; advise outside your corner; propose a way the record already ruled out without naming the decision that ruled it out.

## Changelog

- 0.1.0 (2026-11-03): researched as row 5 of EB-007 (stack wiring team, desk T2), from Charles's record across cbrain, world-graph, context-database and total-harness. Seed Our way kept; added CB-049/058/081, WG-051, CB-406, TH-041, CB-355, WG-021, TH-073, D-050, TH-001 and PP-011. Seed lens kept, except: CB-068 was not found and its claim moved to Our way 3 on CB-049; "truth split across two stores" became Lens 5 (CB-186), because Our way 4 already carries the CB-404 reason; added CB-053, CB-090, CB-398, CB-189, CB-505 and WG-052. Fit pass (EB-015): the new-app line moved to services; the work-handoff line and the unapplied-suggestions lens line cut (skill-authoring and ai-system-design own them); skill-design-framework dropped from reads. The graph stays folded in (Our way 15 of 20).
