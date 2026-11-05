---
name: coding
level: craft
under: c-stack
profiles: [harness, construction]
call_when: "the work writes, restructures or reviews code in any of Charles's repos, whatever it is for (harness services and MCP servers, cbrain-ui, family apps and games, real-estate and work tools; TypeScript, Python or a one-file HTML game): how the code is split into files, its types and the contracts it reads, its tests, its libraries and their versions, a rename or reshuffle across files, or which checks and coding tools (typecheck, tests, style checker, language server) are used where Claude writes it, and why"
altitude: [plan: risks-only, implementation: full]
reads: ["agent-library:references/charter.md", "agent-library:skills/build/SKILL.md (Build execution — tool-first)", "agent-library:skills/orchestrate-build/SKILL.md (step 6; Standing rules: No browser tests)", "agent-library:skills/execute-build-task/SKILL.md (Worker rules)", "agent-library:skills/game-maker/SKILL.md (sections 1–2, 9.1–9.2)", "cbrain:services/package.json", "cbrain:services/tsconfig.json", "cbrain:.github/workflows/services-test.yml", "cbrain-ui:package.json (ref review)", "family-arcade:package.json", "family-arcade:kit/README.md", "world-graph:requirements.txt", "https://code.claude.com/docs/en/plugins/code-intelligence"]
version: 0.1.0
status: active
---

# coding

How Charles's code is written and kept so a later change is safe and cheap, in every repo whatever it is for: harness services and MCP servers, cbrain-ui, the family apps and the arcade games, the real-estate analyzer, and work pipelines. It covers how code is split into files and modules, its types and the contracts it reads, its tests, its libraries and their versions, renames and reshuffles across files, and which checks and coding tools Claude uses in each place it writes code, and why.

Outside this corner: hosting, deploy settings and keys (services); how a commit or edit lands through GitHub, and commit order (github-integrations); where a job runs (lanes); dots and checks on running parts (oversight); where data lives (data-homes); what a graph means and how agent steps are laid out (graph-engineering); SKILL.md files (skill-authoring); what a screen looks like (product-design); 3D scene and model craft (the three-js stub).

## Our way

1. Before writing: read the live code, its caller and every file the behaviour spans, not only the file the brief names; not a design stacked on an assumed behaviour, because named file scope hid changes in other files, and every live file read in one session corrected an assumption [E-295; E-306; CB-081]
2. Library facts: current docs from Context7 before writing code against a library; when Context7 is over quota, the npm registry; not memory [skills/build "Build execution — tool-first" 2; CB-162]
3. Picking a library: one that ships its own types and is still maintained, with a small in-house hook in place of a stale or untyped wrapper; not a deprecated `@types` stub (whether to build or adopt a whole part is c-stack's Our way 1) [CB-160]
4. Versions: an exact pin wherever a new release could break the thing. cbrain-ui and family-arcade pin exactly. Every game and character uses the arcade kit's one fixed Three.js version. The Node `engines` line names the version Vercel runs. A version held back carries its reason in a comment beside it. Not open-ended ranges, because an open floor floats to the newest major release, and an unpinned Anthropic library broke every world-graph write [family-arcade kit/README; game-maker 9.2; world-graph requirements.txt; PP-033]
5. What proves code works: it compiles or the deploy is READY, unit tests cover the logic, files are read back and data is checked by SQL or API; Charles tests what he sees from a What to check list. The arcade's robot check after Launch is the one standing exception. Not browser tests, because CB-441 retired them (how a cloud lane sees a screen is lanes' Our way 10) [orchestrate-build "No browser tests" (CB-441); TH-075]
6. The typecheck covers the whole project and stays green: old errors it finds are fixed when they are few, not scoped out of the check [CB-582 (2)]
7. Tests and typecheck run together: node's test runner strips types without checking them, so a test run is never taken as a typecheck [cbrain services-test.yml, BB-2026-11-04-stack-fix-stack-inspector]
8. A shape another service reads: tests pin it to its exact keys, and a type gap is closed on the reading side (an optional field) rather than by changing what the other service receives, unless the brief asks for it [CB-582 (4)]
9. Contracts lead code: the contract changes first and the code catches up, with the commit saying so (where the contract lives is data-homes' Our way 11) [E-297; E-309]
10. Logic that can be tested: kept in its own small module with a test beside it (family-arcade `lib/floor.ts` with `npm test`; cbrain `services/lib` with `services/test`), not buried in screen code [family-arcade README "What's here"; cbrain services/test; ~ drawn from two repos, not a decision]
11. A family game: one `index.html` on the arcade kit, the kit pasted unchanged, only the kit's Three.js, no other libraries and no build step, and `check-game` prints OK before Launch; not another engine, because browser Three.js replaced Godot, Unity and Roblox Studio [family-arcade kit/README "Rules"; game-maker §2; TH-072]
12. Shared code: changed only at its source (the kit in `kit/arcade-kit.js`, the 2D-3D Maker tool in its repo folder), never patched inside one game or during a run [kit/README "Never edit the kit inside a game"; game-maker 9.1]
13. Code meant to be tweaked later: colours and sizes as named constants at the top, clearly named parts, and every tunable number in `settings`, so a change is a line edit [game-maker 9.2; kit/README "Tuning lives in settings"]
14. Repo checks: every TypeScript repo has a `typecheck` script (`tsc --noEmit`) over the whole project, beside its tests (how the script is named on a function-only Vercel project is services' lens 8) [cbrain services/package.json; ~ new for project-state-mcp, Family-Trip-App and Chooch-Property-Analyzer, which have none]
15. Coding tools in a claude.ai build or design chat (proposed call): no language server and no style checker. Typecheck the changed file in the chat's own workspace before committing where one is available, and treat the deploy reaching READY as the check that the files fit together. Not a language server, because code-intelligence plugins are a Claude Code feature and these chats edit through the GitHub connector with no copy of the repo. Not a hand-made copy of a neighbouring file taken as proof [code-intelligence page; skills/build "Build execution — tool-first"; E-189; E-168; ~ that claude.ai chats load no such plugin is inferred, since the page covers Claude Code only]
16. Coding tools in a Claude Code cloud session (build lead and workers, night builds) (proposed call): no language server. Run the repo's own `typecheck` and `test` scripts before committing, and `lint` where the repo already has one (cbrain-ui, Family-Trip-App, Chooch-Property-Analyzer). Not a language server, because cloud sessions start none. Not a new style checker added, because no miss in the record traces to style and harness tooling stays lean [code-intelligence page, cloud note; CB-582; orchestrate-build step 6; charter "fewer files, fewer instructions"; ~ the lint half has no record]
17. Coding tools in a Claude Code terminal session on the PC (proposed call): none set up, because no code work runs there and nothing is parked on the PC. If code work ever moves there, add the TypeScript language-server plugin at that time (free, one install) for its error report after each edit and its find-every-use [lanes Our way 3; code-intelligence page; charter "agent and cloud sessions as autonomous as possible"]
18. Coding tools in GitHub Actions (proposed call): typecheck and unit tests in a workflow run by hand (cbrain's `services-test.yml`), with no language server and no style checker. Not on every push, because Actions triggers are off since 2026-10-12 to save minutes (c-stack Our way 6). Not a language server, because it helps only something that is editing code, and an Action runs fixed steps [services-test.yml; CB-562; charter, two-engine rule]

## Lens

1. A coding tool assumed present because another place has it: a language server expected in a cloud session or a claude.ai chat, where none runs [code-intelligence page]
2. A typecheck left failing for good, so a new error hides among the old one [E-395]
3. Files typechecked one at a time against hand-made copies of their neighbours: each passes while the real pieces don't fit [E-168]
4. A passing typecheck taken to mean the code runs: `.ts` import endings pass `tsc` and fail at Vercel runtime [CB-040; moved from services lens 8]
5. A test run read as a type check: the test runner strips types without checking them, and five type errors sat in cbrain services until a typecheck step was added [services-test.yml comment; CB-582 (2)]
6. Live output that looks right but whose values were never checked against the contract that defines them; a parser anchored to the first loose match instead of the exact table row [E-210]
7. Screen code bugs a typecheck cannot see: a handler reads a stale value, a URL-driven checkbox flips back on fast clicks, and one passing run is taken as proof against a timing bug [CB-208; CB-182]
8. A canvas or 3D scene whose checks only count things (layout done, counts match): every check passes on a canvas drawn at zero size [CB-170; ~ its browser-gate fix was retired by CB-441; the arcade's live check after Launch is what remains (TH-075)]
9. ~ Logic left inside screen code where no unit test can reach it, so Charles clicking is its only check [orchestrate-build "No browser tests" (CB-441); ~ inferred, no single trace]
10. Checks left to the deploy when the session could have run them first: a local `tsc` caught a corrupted file sooner than the deploy did [E-189 corollary]
11. ~ A rename or move across files done by searching text, with nothing that finds every use and no typecheck after [code-intelligence page; ~ no failure in Charles's record]
12. A file grown so large that briefs mark it don't-touch and commits of it time out; splitting it is this corner's job, and how the edit lands is github-integrations' Our way 10 [CB-291; E-196]
13. A test with hard-coded expectations (a milestone's status, a header's wording, an element id) turns red when real progress or a wording change happens: expected values should come from the data, and every test file is searched for the old literal when a screen's words change [CB-191; CB-245; CB-382; CB-402; moved from product-design lens 15]
14. ~ Clean-up never scheduled: build workers may not touch code next to their task, so known problems sit open as next moves with no build to clear them [execute-build-task worker rule 1; E-395; ~ the link is inferred]
15. A runtime version set in the dashboard while `package.json` pins another: the file wins without a word, and the dashboard's upgrade button does not touch it [PP-033]
16. ~ Repos with no typecheck or test at all (project-state-mcp; Family-Trip-App and Chooch-Property-Analyzer have a style checker only), so only using the app catches a break [those repos' package.json; ~ what the files show, no failure traced]
17. ~ Each repo keeps its code its own way (exact pins plus a test and a checker in family-arcade, ranges plus typecheck and tests in cbrain services, a style checker only in the trip app), so a lesson learned in one never reaches the others [the package.json files under reads; ~ inferred]

## Procedure

1. Read the situation, the goal, `agent-library:references/charter.md` and every file under `reads`.
2. Search Project State across all projects for decisions and lessons in this corner, using its terms (typecheck, tsc, unit test, node:test, lint, eslint, language server, LSP, refactor, rename, pin, version, dependency, Context7, contract, stub, deploy READY, kit, character.js). Where one is newer than an Our way line and differs, the record wins, and you say so.
3. Open the actual work (the repo's package.json, tsconfig and the files being changed); never judge from a summary when the source is reachable.
4. Walk each Our way line and each Lens line against it.
5. Write the output in the mode the desk named.
6. Read only, write nothing; you are alone and see no other seat.

## Output

**Full**
**Seat:** coding · **Mode:** full
**How I'd do it**: one path, or two when there is a real fork: an A-to-Z sequence of steps, each citing the Our way line or record it rests on; a step with nothing behind it is marked *~ new*.
**Where the work departs from our way**: the line quoted, and what the work does instead
**What I would change** (≤3)
**What goes wrong in my corner** (≤8): each tagged *blocks the goal* | *improves the plan* | *noted*, naming the part of the work it is about
**Newer than my brief**: any decision or lesson from step 2 that changes an Our way line, or "none"
**What I would need to know** (≤2)
**If this failed in three months, why**: one line. Mandatory.
**Read:** every file or page you actually opened, and the searches you ran

**Risks-only**
**Seat:** coding · **Mode:** risks-only
**Where the work departs from our way** (≤3)
**What goes wrong in my corner** (≤3, tagged as above)
**Newer than my brief**: as above
**If this failed in three months, why**: one line
**Read:** as above

## Never

Speculate past what you read; pad to the cap; soften a blocker; advise outside your corner (hosting, deploy settings and keys are services'; how an edit or commit lands is github-integrations'; where a job runs is lanes'; checks on running parts are oversight's; where data lives is data-homes'; what a screen looks like is product-design's); propose a way the record already ruled out without naming the decision that ruled it out; push a coding tool for its own sake when the per-place call says no and nothing new has changed it.

## Changelog

- 0.1.0 (2026-11-05): new craft under c-stack (proposal EB-063, superseding EB-062; Charles "go"). The corner spans all of Charles's repos, not only the harness (Charles, 2026-11-05). Our way comes from Charles's record (CB-162, CB-160, PP-033, CB-441, TH-075, CB-582, E-297, E-309, TH-072, the build, orchestrate-build and game-maker skills, family-arcade kit/README, cbrain services-test.yml, world-graph requirements.txt). Our way 15–18 are proposed per-place calls on language server, typecheck and style checker; no tool is adopted (Charles: "I don't have to have LSP capability. I just want it to be clear why or why not"). Lens 4 moved from services lens 8 (first half); Lens 13 takes product-design lens 15. Left to their owners: E-133 (ai-system-design), E-359 (graph-engineering), CB-081's transaction claim (data-homes lens 9), CB-148 (lanes lens 10), large-file edit method and commit order (github-integrations Our way 10–11). pm-app (README only) and moonshot-demo (planning folder) hold no code. Tool facts on where each coding tool runs belong on a cbrain concepts/ page that does not exist yet, so it is not listed under reads. Nothing from memory.
