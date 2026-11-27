# Gaming Lab audit — November 2026

Audit chat: https://claude.ai/code/session_01KaPN8HrYCRcdUxHw6MQzGE (run 2026-11-27)
Scope: the 18 most recently updated chats in the Gaming Lab Project, excluding the audit chat. Audit only — nothing else was changed.
Method: each chat read with read_conversation; claims checked against GitHub (files + commits), Vercel, Supabase and Project State. Labels: **Verified** (what was checked), **Contradicted** (what was found), **Unchecked** (why).

## Chat list (newest first)

| # | Title | Last updated | Link |
|---|---|---|---|
| 1 | F1 car 3D game | 2026-11-27 | https://claude.ai/chat/7b8edc6e-89b1-4e20-8609-39f683510558 |
| 2 | Needoh unboxing game | 2026-11-27 | https://claude.ai/chat/0db91ed9-b76e-4bed-ae01-e593f4a9e66b |
| 3 | Baby Claude rap game | 2026-11-27 | https://claude.ai/chat/4dbe611c-9aaf-4909-8b5a-d5c787edaae4 |
| 4 | Tesla Roadster jump game | 2026-11-26 | https://claude.ai/chat/7ce8a7ea-9d7f-49fe-9006-4ccab18e5bf0 |
| 5 | Pokémon-style card game | 2026-11-26 | https://claude.ai/chat/cc30a93d-9915-4303-9f64-0b50c5eee47c |
| 6 | Minigame-based attack game design (Rage Bait Bots) | 2026-11-26 | https://claude.ai/chat/09019579-c925-4efb-876f-08a283cd289e |
| 7 | Fun video game (Backroad Bonk / Cubicle Clash) | 2026-11-25 | https://claude.ai/chat/7bcba705-4708-4881-9408-2acc6098313e |
| 8 | Squishy clicker game (Squish Club) | 2026-11-25 | https://claude.ai/chat/4e914afe-ab7c-436f-9b2e-609d4a54a6fa |
| 9 | Prankster game concept (Prank City) | 2026-11-25 | https://claude.ai/chat/9dd08244-0780-47e0-8b20-44f7b037c86d |
| 10 | card (Dino Mech, Neon Rush, Dunk Brawl, Rift Packs) | 2026-11-25 | https://claude.ai/chat/e2871c02-7313-4250-a93a-c179362171fe |
| 11 | Haunted house game design | 2026-11-25 | https://claude.ai/chat/c7e01b7a-4665-4a57-a3fb-5fc271bb0b8a |
| 12 | truck (Skull Cove, Monster Truck, Elliott's arcade) | 2026-11-22 | https://claude.ai/chat/7f595a88-0202-4881-9537-9fc9a85235a9 |
| 13 | gold medal (Avalanche Escape, Downhill Gold) | 2026-11-22 | https://claude.ai/chat/a4e80b49-d05f-4e8d-86af-ef07f34e5125 |
| 14 | Steal a Brainrot game (Giggle Grab) | 2026-11-21 | https://claude.ai/chat/7744b1f4-c72a-4cd8-8d87-28de8418f96f |
| 15 | jelly | 2026-11-21 | https://claude.ai/chat/e0ac1f96-37df-4d65-890a-45807e15fcb5 |
| 16 | 3D character from image (ninja) | 2026-11-20 | https://claude.ai/chat/afe94094-77ff-4a1a-a4ac-6d3785ad2aab |
| 17 | Ninja 3D viewer | 2026-11-15 | https://claude.ai/chat/cbb61f08-212d-40d0-a734-ecd1cb825405 |
| 18 | Ninja character sword redesign (Blue Ninja) | 2026-11-15 | https://claude.ai/chat/9507cae4-8e1a-450a-8d1b-69aa5393f411 |

## Per-chat findings

### 1. F1 car 3D game → "Slipstream" (Elliott)
Link: https://claude.ai/chat/7b8edc6e-89b1-4e20-8609-39f683510558 · 165 turns, read in full · Nov 25–27

**What it became:** a browser racing game that grew into a Godot (game engine) banger/supercar racer with many tracks, 37+ cars, replay, cockpit view, and a Windows app.

**Tech used**
| Tech | For | How | Worked? / broke / workaround |
|---|---|---|---|
| Three.js + Rapier physics + esbuild | v1/v2 browser racer | bundled into one script, published as artifact "Slipstream: Monza" | Worked; kid said "graphics suck" → abandoned for Godot |
| @pmndrs/assets (Poly Haven sky, CC0) | sky/reflections in v2 | npm install, embedded | Worked; ambient-occlusion pass made streaks → switched off |
| Godot 4.5.1 (desktop + web export) | main game from turn 11 on | headless Godot + xvfb software graphics in sandbox; web export packed as gzip+base64 JS pieces unzipped by fflate | Worked. Broke: artifact host refuses files >20 MiB → split into game-pck-1…12.js; browser cached old pieces → "invalid/literal" error → fixed by adding a build stamp (?v=) to every piece |
| HTTP range requests into Godot's 1.3 GB templates file | get only the web / Windows export template | python range reader / remotezip | Worked (good trick) |
| Claude in Chrome (Charles's real Chrome) | search Meshy account, run TRELLIS, read models from blocked sites, check the live game, debug in Elliott's tab | navigate/screenshot/JS injection | Worked; Chrome disconnected once, switched device with select_browser |
| Meshy (via kids-games `meshy.yml` workflow) | credit check | run_workflow `credit-check` (run 45674834427) | Worked: 6 credits left; no Meshy spend in this chat |
| Hugging Face TRELLIS (free picture-to-3D) | car models from Elliott's pictures | JS injected into the HF page in Chrome | Dead end: free daily GPU quota used up after 1 test car; sandbox can't reach huggingface.co |
| RunPod | rent a GPU for TRELLIS | checked balance ($7.76) | Not used — Claude asked for a parent's OK (money gate respected); kid said free only |
| TripoSR on GitHub Actions (CPU) | picture → 3D car, free | new workflow `kids-games/.github/workflows/triposr.yml`, one job per picture, bot commits `out/triposr/<car>/mesh.glb` | Worked after one fix (missing xatlas). One job hung → cancelled with `gh` CLI, added 12-min time limit |
| trimesh + pymeshlab + photo projection (proc2.py, sandbox only) | clean up TripoSR meshes, paint Elliott's photo onto them | python | Worked technically but Elliott called results "lumpy / fake / bad" over several rounds → all photo cars deleted at his request |
| Kenney Car Kit (CC0) via a third-party GitHub mirror | flying debris parts | git clone Arslan12216775/kenney_car-kit | Worked; kenney.nl not reachable from sandbox |
| gltf-transform CLI, meshoptimizer | shrink downloaded car/track models | npm | Worked |
| Free car models (GitHub Vivekkk-1/3D-Models, Nissmo89/Supercar-Vault-3D, three.js Ferrari, Sketchfab CC-BY via GitHub copies) | the garage cars | raw.githubusercontent downloads; git LFS | Worked. Licensing checked unevenly (see below) |
| Objaverse (allenai) on Hugging Face | 21 more cars, Indy track scan | sandbox can't download → built "Add car files" bulk importer + drop box so Elliott loads files in his browser | Partly: those cars live only in Elliott's browser storage; a GitHub copy of the Indy scan (Amogha027/Car-Racing-Game, licence file checked) was baked into the game |
| Device bridge + computer use on Charles's laptop | put Slipstream.exe and a shortcut on the Desktop; look at the screen | device_request_folder_access, device_commit_files to `C:\Users\cecou\Desktop` and `…\OneDrive\Desktop`; computer_screenshot | Files landed. The kid was actually on a different, unconnected computer; Claude never ran the .exe |
| Project doc `claude/slipstream-godot-handoff.md` | handoff notes | project_write, rewritten ~10 times | Exists |

**Built / where it lives now**
- Live game artifact "Slipstream: Banger Racing" — https://claude.ai/artifact/2PntVtTizPezHZAHh5pZWC (slug 0b47c7f1…). **Verified**: get_artifact returns it, version 1795807858-de9d, private.
- Older artifact "Slipstream: Monza" (Three.js) — https://claude.ai/artifact/Dq4HMafeWeuSZWEAMpAuR7. **Verified** exists.
- Slipstream.zip and Slipstream.exe (225 MB, unsigned) — only as chat attachments and on Charles's laptop Desktop. **Unchecked**: can't see the laptop from here.
- **The Godot source code is not saved in any repo.** It lived only in that chat's sandbox (`/home/claude/godot`) and inside the zip/artifact. The handoff doc itself says the build script is "gone when the session ends".
- kids-games repo: `triposr.yml`, `drawings/bangers`, `bangers2`, `supercars`, `supercars_retry`, TripoSR outputs. **Verified**: files present; Claude commits 674427e, 789e615, 89e1786, b94faa6, 673a9c6 plus 4 bot commits; workflow runs 1 failed, 3 succeeded, 1 cancelled — matches the chat.
- No family-arcade repo, Supabase or Project State work in this chat. **Verified** by reading every turn.

**Claims checked**
- "Handoff notes saved to claude/slipstream-handoff.md" (turn 3) — **Contradicted**: the Project only has `claude/slipstream-godot-handoff.md`.
- "Cars sit on the road now" (turn 92) — **Contradicted by Elliott** ("you didn't fix it"); second fix tested on one car, one track.
- "Replay works" (turn 88) — Elliott said it didn't; rewired in turn 90. **Unchecked** with a real player since.
- "Glitching fixed" (turn 112) — Elliott meant the main screen; that glitch was never reproduced or fixed.
- "Speedway Figure 8 matches your photo" (turn 163) — **Unchecked** on the laptop (Claude said so).
- Every "checked on my computer" = headless software-render tests in the sandbox. Real-device feel, speed and sound were never tested; Claude said so each time.

**Decisions**
- Three.js instead of the Godot Elliott asked for (Claude) → back to Godot (Elliott: "still doesn't look good").
- Wild crash physics kept as a feature (Elliott, reversing Claude's fix).
- F1 → bangers → photo cars → supercars → "delete every car except the Ferrari" → garage of real models (all Elliott).
- Copying the Wreckfest stadium refused twice (Claude). In the last turns Claude matched the stadium to "the empty figure-eight speedway picture" Elliott relayed, calling it generic — worth a look, since earlier turns said a Wreckfest screenshot would only be used "for ideas".
- Unsigned .exe on the laptop: Claude asked for a grown-up's yes; the yes came typed by the kid ("the grown up said yes").
- Many prompts were long specs written by another AI and pasted by the kid (one says "Attach this picture to your Slipstream chat in Claude, then paste…").

**Money:** none spent. RunPod proposed and not used. Meshy credits unchanged. Paid/login model sites skipped.

**Licences:** checked for the Sketchfab CC-BY cars, Porsche (CC BY-NC-SA), Indy scan (CC-BY), EB110 (no-edits → user-loaded). Not checked for the Vivekkk-1 cars ("your game is private, so that's fine for now" — an assumption) or the 21 Objaverse cars ("I didn't check the license").

### 2. Needoh unboxing game → "Squish Box"
Link: https://claude.ai/chat/0db91ed9-b76e-4bed-ae01-e593f4a9e66b · 8 turns, read in full · Nov 27

**Tech used**
| Tech | For | How | Worked? |
|---|---|---|---|
| AGENT.md → charter → game-maker skill (GitHub connector) | setup | read at start | Worked |
| family-arcade repo (git clone + add_repo + register_repo_root) | the arcade kit: `kit/arcade-kit.js`, template, cabinet kit, `tools/inline-kit.mjs`, `tools/check-game.mjs` | cloned read-only; game built in `/home/claude/squish` (shell.html + game.js → inline-kit → check-game) | Worked |
| Three.js (kit, three@0.160.0 from jsdelivr) | the 3D game | single HTML file | Worked |
| Playwright + headless Chrome (software graphics) | test runs: start, 20 fast taps, background screenshot | `/opt/npm-tools` playwright-core, local http.server, CDN rewritten to local three | Worked; local test server died once → restarted |
| Artifacts | game + cabinet preview | publish_files, then republished twice to the same slug | Worked |
| Project State checkin | progress card | `game-maker:squish-box`, once after round 1 | Worked, but see below |

**Built / where it lives**
- "Squish Box" artifact — https://claude.ai/artifact/NimJHq4Wextv54VAvM4EF9 (slug afe4b4c3…). **Verified** exists (version 1795801154-8f44), private.
- "Squish Box Cabinet" preview artifact (link in the Project State card). **Unchecked** directly; card link present.
- Nothing committed to family-arcade; not launched. **Verified**: no Squish Box commit appears in the session's work; card still says "say Launch".
- Rounds: 1) 4 boxes, 96 squishies, 12 rarities; 2) "spam squish" (every tap pays); 3) neon party room + confetti.

**Claims checked**
- "Played it through, no errors" (round 1) and "20 fast taps earned 40 coins" (round 2) — **Unchecked** beyond the chat's own sandbox test output; nothing persistent to re-run.
- Project State card — **Verified** it exists (open, waiting on you), but **stale**: it still describes round 1; rounds 2 and 3 were never checked in.

**Decisions:** Claude named it "Squish Box" and left the NeeDoh brand off (Claude). Spam-squish and neon background were the kid's asks.

**Money:** none.

### 3. Baby Claude rap game
Chat 4dbe611c-9aaf-4909-8b5a-d5c787edaae4 · 11-26 to 11-27 · 22 turns, all read (pages t0–t21).

**Tech used**
- Claude artifacts with capabilities (describe_capabilities / declare_capabilities): the game page calls the real Claude (`window.claude.use("sample")`), Claude voices (`tts`, 4 voices: glassy/buttery/rounded/airy) and dictation. Worked in Claude's test with a pretend Claude; never tested against the real one by Claude.
- Web Audio (in-browser sound synthesis) for the beats (boom-bap, then trap with 808s), air horns, piano, effects. No audio files. Claude could not hear any of it.
- Browser speech synthesis (device voice) as fallback "Tiny Baby" voice and hype-man ad-libs.
- three.js 0.160 from jsdelivr CDN for the 3D room and town.
- Local tools in the sandbox clone of family-arcade: `tools/check-game.mjs` after every change; Playwright + headless Chrome (swiftshader) with a mocked `window.claude` for screenshots and scripted tests.
- Game-side "tools" Claude can call inside the game: start_rap, make_baby, remove_baby, build (3D thing from a fixed shape list, max 60 parts), set_world, give_power, go_play, buy_item, reset_room, draw_picture. Claude chose shape lists over letting the game run any code (stated reason: safety, can't break).
- publish_files to the artifact after each round; Project State checkin after each round.

**What was built, and where it lives**
- Rounds 2–9 on one game: real beat + rapping, voice picker, Trap Party style, extra Baby Claudes (up to 12), "anything mode" (build/weather/gravity/powers), playground (Baby Maker, hoop, trampoline, floor piano, ball pit), Babyville town with 4 paid jobs, Baby Mart (4 → 22 items), progress reset + Start over button, then a fix so raps start even when Claude doesn't use the rap tool.
- Lives in: the artifact only, plus the sandbox file `/home/claude/family-arcade/public/games/baby-claude/index.html` (gone when that sandbox ends).

**Decisions**
- Kid asked for a voice "like Travis Porter" → Claude refused (copying a real person's voice) and made a Trap Party style instead, with a prompt rule "never copy real songs or name real rappers". Claude's decision.
- "Reset the game" → Claude chose a one-time wipe via a save-version number (RESET_GEN=2) plus a Start over button; it offered to undo features if that's what was meant. Claude's interpretation, not confirmed.
- Open for Charles, raised every round: the arcade rulebook says "no chat"; this game is a talk-to-Claude game. Claude recommends allowing it. Not answered in the chat.
- Rap fix (turn 21) was based on a guess about the cause; Claude said so.

**Money / credits:** none seen. (Each kid question uses the real Claude through the artifact; cost of that is on the user's plan, not measured.)

**Claims checked**
- Artifact "Baby Claude" exists, latest version 1795797623-612b (newer than the last publish base 1795797503-e1d9, matches one more publish): **Verified** (get_artifact).
- Cabinet artifact 1WYVu9iRYYwfX4D4T9AYxG exists ("Baby Claude Cabinet"), last changed at version 1795707209 (round 1, not updated since): **Verified**.
- Project State card game-maker:baby-claude open, waiting on Charles, next step matches the turn-21 fix: **Verified**.
- Game is in the family-arcade repo: **Contradicted**. `public/games/baby-claude` returns 404; the repo's games folder holds only backroad-bonk, dino-mech, skull-cove-loot-rush, skull-cove-lv, test-probe, waddle-out, waddle-out-godot.
- "Raps work every time now": **Unchecked** (only tested with a pretend Claude and a stuck pretend voice; no report back from the kids in this chat).
- Sound quality, iPad smoothness with 12 babies: **Unchecked** (Claude said so itself).

### 4. Tesla Roadster jump game
Chat 7ce8a7ea-9d7f-49fe-9006-4ccab18e5bf0 · 11-26 · 14 turns, all read (pages t0–t13).

**Tech used**
- Start-of-chat routine worked: memory file family-arcade.md, AGENT.md, references/charter.md, skills/game-maker/SKILL.md, Project doc claude/roblox-mind.md.
- WebSearch for the twist (real Roadster thruster facts) and one-search "Roblox check" each round (Claude labelled it "one search, not a full sweep").
- Kid supplied model links (a ChatGPT-written box): Roadster GLB from GitHub Vivekkk-1/3D-Models; semi truck from tevy.dev.
- **tevy.dev was unreachable from the sandbox** (WebFetch and shell). Workaround: the arcade's existing `fetch-assets.yml` GitHub Action ("download robot") run with a URL list and `deploy:false`; it commits raw files to `assets-src/` in the private family-arcade repo; then Claude attached the repo (add_repo / register_repo_root) and git-pulled to get them. Worked three times (truck; tevy's full 1,655-model catalog + 30 city models; mech + props).
- Model processing in the sandbox: Roadster cut from 26.7 MB / ~609k triangles to 4 MB; textures shrunk; roof height maps measured from the building meshes (18 KB); mesh simplification of apartments/trees.
- Headless Chrome tests with a fast-forward hook ("runs the game logic at full speed") because the software renderer ran at a few frames per second. Soak tests (3-minute random driving, 35 runs, 2.9 km flight).
- **Artifact host would not serve .glb files as page files.** Workaround: declare_capabilities to turn on assets, then upload_asset for each model, then republish the page pointing at assets. Worked (pages published); whether models actually load on the real page was never confirmed.
- AskUserQuestion multiple-choice cards for the kids (3 rounds).
- Project State checkin on one card for all three games.

**What was built, and where it lives**
- Highway Hop (hop between moving semis, air tank, low bridges) + cabinet → artifacts. Kids: "its not fun" → dropped.
- Sky Derby proposed → kid: "nah".
- Thrust City (free-roam 7×7-block city, 31 models, ~3 million triangles, stunt park) + cabinet → artifacts. Rated "okay".
- Mech Breaker (ram glowing weak spots on walking 32 m mechs, waves) + cabinet → artifacts. Kid had no idea ("idk, something elser"), so Claude picked it.
- Raw downloads in family-arcade `assets-src/highway-hop`, `assets-src/tevy`, `assets-src/thrust-city`, `assets-src/mech`. Game code itself: sandbox only (`/home/claude/game`, `/home/claude/city`, `/home/claude/mech`), not in any repo.

**Decisions**
- Twist "Highway Hop" chosen by Claude, accepted by kid; then dropped after "not fun". Claude reasoned the kids had said before that jump-and-run games aren't fun (from memory/Project context).
- Mech Breaker idea picked by Claude when the kid had none.
- Roadster credit put on the start screen (Claude: "free licence requires credit").

**Money / credits:** none.

**Claims checked**
- Highway Hop, Thrust City, Mech Breaker, Mech Breaker Cabinet artifacts exist: **Verified** (get_artifact on YJLhVFi5…, CFFPmxQg…, 6Fu3kBxt…, 8yL3rYK2…).
- Download-robot commits: **Verified** — family-arcade commits 21b971a (11-26 01:39), 5b5c292 and e190d11 (11-26 14:36–14:39), 15b63c1 (11-26 21:08), all "fetch assets [wip]" by arcade-fetch-robot; the four assets-src folders exist.
- Project State card game-maker:highway-hop: **Verified** open, waiting on Charles, links Mech Breaker game/cabinet and Thrust City. It does not link Highway Hop or the Thrust City cabinet any more.
- "The Roadster model's free licence requires credit": **Contradicted / not supported.** The Vivekkk-1 repo LICENSE is a Boost software licence, and its README says the owner does not own the models (collected from Sketchfab) and to "verify the license of each model". No per-model licence for the Roadster was found in the chat or the repo. Also a real brand (Tesla) and car design.
- "Models load on the real Claude page": **Unchecked** (Claude flagged this itself every round; no kid report).
- Jump distances, soak tests: **Unchecked** beyond Claude's own test logs (sandbox gone).

### 5. Pokémon-style card game
Chat cc30a93d-9915-4303-9f64-0b50c5eee47c · 11-25 to 11-26 · 93 turns, all read (pages t0–t92). Game name: **Apex Summoners**. Player named in records: Elliott.

**Tech used**
- Start routine: memory family-arcade.md, AGENT.md, charter.md, game-maker SKILL.md; conversation_search for the earlier card game ("Rift Packs") to avoid repeating its mistakes; TaskCreate/TaskUpdate task list.
- family-arcade repo: `gh repo clone` did not work; add_repo + `git clone` did. Used kit, `tools/slim-model.mjs`, `tools/check-game.mjs`, `tools/fetch-assets.py` (read only).
- Models: sandbox could reach raw.githubusercontent.com and api.github.com (curl tested). Downloaded from GitHub `oosawak/cc0-monsters` (catalog.json; Grab3D, OpenGameArt sources) and `511action/descent-3d-assets` (Quaternius). No paid tool used ("didn't use any of Dad's Meshy credits").
- Model slimming in the sandbox: gltf-transform + meshoptimizer + sharp + draco3dgltf (Draco models needed a decoder added; then the Draco extension had to be removed before writing). First pass 16k triangles / 512 px textures; round 4 redid all 33 at 26k / 1024 px.
- Playwright + headless Chrome (swiftshader) for contact sheets of every monster, scripted pack openings, battles, login, knockouts. Many tests needed fast-forward hooks or forced states because the software renderer was too slow to finish a full battle (Claude said so in round 5).
- Artifact assets: declare_capabilities + upload_asset (26, then 7, then all 33 again, then 1); `modelmap.json` maps each model to its `/_blob/<id>` link baked into the page. Artifact "storage" (A.load/A.save) holds saves.
- **Claude in Chrome (Charles's own Chrome)** used once in round 1 to open the published artifact and screenshot it, so "monsters loaded on the real page" was checked live. Rounds 2–6 were not opened on the real page (Claude said so each time).
- Body animation done without rigs: vertex-shader bending of heads, jaws, legs, tails, wings, driven by measuring each model's points (feet clustering, snout finding). Web Audio for all sound (synth voices, compressor, reverb).
- Project State checkin each round.

**What was built, and where it lives**
- Six published rounds of one game: packs with 10 rarities and foils, collection, market, evolutions, Normal/EX/MEGA/Shiny versions, spells and traps, deck battles where 7 knockouts win, levels unlocking 5 arenas, rival ladder, 2-player on one device, hologram view, stadium with crowd, local player profiles with optional 4-digit code ("log in"), Lucky Wheel, arena events.
- Lives in: artifact "Apex Summoners" + cabinet artifact; source only in the sandbox (`/home/claude/apex/src/*.js`, build scripts). **Not in any repo.**
- 7 extra monsters were added in round 5, then removed as "broken"; only Puff Drake kept.

**Decisions**
- Every feature came from the kid's message stream (about 45 asks); Claude built each. Kid reversed himself once: "squad of 5" was built, then replaced by "a deck… kill seven creatures to win".
- Claude's own calls: mouths open only on long-snouted monsters (round 6); "log in" built as local profiles on the device, not real accounts; PIN stored as plain digits in the save.
- "Restart me": Claude added a ↺ start-over on the profile card rather than wiping saves.

**Money / credits:** none. Meshy credits explicitly not used.

**Claims checked**
- Artifact "Apex Summoners" exists, version 1795707485-7a3f: **Verified** (get_artifact).
- Cabinet artifact 88AKakeYp7wRQMhuj7rvYg exists, last changed at version 1795632243 (round 1): **Verified**.
- Project State card game-maker:apex-summoners: **Verified** open, next step matches round 6. Two oddities: `waiting_on` is "nobody" (set by Claude from round 4 on, though the game waits on the kids/Charles), and it now links only the game, not the cabinet.
- Models are CC0: **Verified as claimed by the source** — oosawak/cc0-monsters README says every item was checked as CC0 at its origin page. Not checked origin by origin.
- "Monsters loaded on the real game page" (round 1): **Verified at the time** by Claude in Charles's Chrome; not re-checkable now. Rounds 2–6 on the real page: **Unchecked**.
- "No errors / no glitches": **Unchecked** (sandbox tests only; full battle never completed in test).
- Game in the arcade repo: **Contradicted** — no `public/games/apex-summoners` folder in family-arcade.

### 6. Rage Bait Bots
Chat 09019579-c925-4efb-876f-08a283cd289e (listed title "Minigame-based attack game design") · 11-25 to 11-26 · 24 turns, all read (pages t0–t23).

**Tech used**
- Start routine: memory, AGENT.md, charter.md, game-maker SKILL.md, kit README/template/cabinet.md, references/thread-checkin.md. add_repo + register_repo_root for family-arcade (used `tools/check-game.mjs` after every change).
- Built from scratch in the sandbox (`/home/claude/rbb`: shell.html + game.js + a small `build.py` patcher that applies JSON find/replace lists). three.js from CDN; all graphics are code-drawn robots; Web Audio sounds.
- Headless Chrome (Playwright, swiftshader) with a "robot player" script that plays every minigame and blocker, on phone and desktop sizes; screenshot contact sheets checked by eye.
- Artifact save (localStorage key `arcade:rage-bait-bots`) for coins, pets, chat log, levels. Old-save migration written for each data change.
- publish_files to the same artifact each round; Project State checkin each round.

**What was built, and where it lives**
- 4 published versions: (1) tap-to-annoy clicker with upgrades, pets, eggs; (2) every bait is a minigame (10, then 20), 6 "blockers", suspicion meter that ends in a BAN, login, fake stream chat; (3) chat log instead of stream, 14 bots, PC Base room with 20 shop items, bots answer what you said; (4) a new bot every level (generated from a seed), boss every 5th level, Claude at level 35, endless mode after, glitch sweep.
- Lives in: artifact "Rage Bait Bots" + cabinet artifact. Source only in the sandbox. **Not in any repo.**

**Decisions**
- Kid asked for "bosses of major AIs": Claude used real product names as bosses — Siri, Alexa, Copilot, Gemini, Grok, ChatGPT, Claude — with its own robot designs ("not the real company logos"). Claude's call; not raised with Charles.
- Kid: "no upgrades just… mini games" → upgrades removed; coins only buy eggs (later also base items).
- Claude interpreted two vague asks and said how: "list of you messages" = saved chat log, not a stream; "new bots every level" = numbered levels with generated bots.
- Login = a username and face saved on the device (not a real account).

**Money / credits:** none.

**Claims checked**
- Artifact "Rage Bait Bots" exists, version 1795655936-ad08: **Verified**.
- Cabinet artifact Xi2S2mWh5ndMQH6UFuLU1Y exists ("Rage Bait Bots — Cabinet"), version 1795644723 (round 1): **Verified**.
- Project State card game-maker:rage-bait-bots: **Verified** open, waiting on Charles. Its next step was rewritten at 06:37 on 11-26, about 5 hours after this chat ended, with different wording ("Choose: Launch it and name whose arcade (recommended)…"). Something other than this chat changed it; not traced.
- "All 20 minigames winnable, no errors": **Unchecked** beyond Claude's sandbox robot (sandbox gone).
- Sound, full 35-level climb: **Unchecked** (Claude said so).
- Game in the arcade repo: **Contradicted** — no `public/games/rage-bait-bots`.

### 7. Fun video game
`7bcba705-4708-4881-9408-2acc6098313e` · 259 turns · read in full (turns 1–140 first, 141–259 after the hourly read limit reset). Turns 141–259 are summarised under "Turns 141–259" at the end of this section.

**Who and where.** Turns 1–138 are a kid making games, outside the Gaming Lab project at first (Claude's own search said it could only see chats outside projects; at turns 96–110 it read memory from a different project, `01a12d74-…`, files `topics/games.md` and `areas/demo-day-game.md`). No AGENT.md routine, no Game Maker skill, no Project State cards in that stretch. At turn 139 Charles says he is bringing this chat into a new game chat and asks to launch Backroad Bonk.

**Tech used**
- Single-file HTML games written in the sandbox, published with the Artifact tool. Checks: `node --check` syntax only early on; later a headless Chromium (Playwright, software 3D via SwiftShader) robot that plays the game and takes screenshots Claude looked at. Worked.
- Three.js r128 from cdnjs for 3D games (Backroad Bonk, Pinball Galaxy, Cubicle Clash), multi-file folders stitched by a `build.sh`.
- Artifact capabilities `db` + `user` for cloud saves (Backroad Bonk, Pinball Galaxy) and `room` for online matchmaking (Cubicle Clash).
- Breaks / workarounds: 12 assistant turns came back empty when the kid sent messages mid-build (31, 33, 35, 39, 85, 87, 90, 120, 122, 124, 130, 136); the work carried on in the next turn. Sound can't be heard in the sandbox and real-device speed can't be measured — Claude said so each time. A turkey animation crash froze Backroad Bonk ("laggy and glitchy"); fixed at turn 94 and the main loop wrapped so one bad frame can't freeze it.

**What was built (all artifacts unless noted)**
- Steel Stack, Orbit Hop, Flock & Fence, Lumen (puzzle generator tested: 200 → 540 generated puzzles all solvable), Mistlake → rebuilt as **Fathom** (deep-sea fishing, 57 species, phone apps), **Backroad Bonk** (truck/boat/plane, cabin hub, 26–27 hittable animals), Gust, Boomtown Pinball → replaced in place by **Pinball Galaxy** (`USzZMRWK2P4c9LQRWURND4`), **Cubicle Clash** office brawler v1–v3 (`Gf5ydFped7SDkXaqxCGF4d`, 22 fighters).
- Turn 140: Backroad Bonk launched to the family arcade (`family-arcade` repo `public/games/backroad-bonk/`, Supabase `arcade_games`, live-check workflow, Project State `game-maker:backroad-bonk`). Login screen removed (arcade account instead); coins reset to 0; run length set from the parent panel.

**Decisions and who made them**
- Kid asked for a "driving in my car right after a beer" meme game running over deer with the real song. Claude (not Charles) dropped the song (copyright) and the beer, kept hitting cartoon deer for points.
- Kid asked for logins; Claude chose local profiles with an optional 4-digit PIN stored as plain digits, and told the kid it "isn't real security."
- Kid asked to "get rid of" Boomtown; Claude overwrote it at the same link with Pinball Galaxy.
- Charles (turn 139): launch Backroad Bonk, skip the dev step.

**Money:** none seen in turns 1–140.

**Claims checked**
- Pinball Galaxy published at `USzZMRWK2P4c9LQRWURND4` — **Verified** (exists, private to owner, version `1792089372-8488`).
- Cubicle Clash "link is now set so anyone with it can open it" — **Verified**: artifact `read` is **public**. A kids' game with player names and online play is open to anyone with the link.
- Backroad Bonk launched live — **Verified**: repo folder exists; `arcade_games` row `backroad-bonk` status `live`, version 1, launched 2026-10-22 00:10 UTC.
- Project State `game-maker:backroad-bonk` closed — **Contradicted in part**: status is `done`, but its next step still says the robot check is running and it's waiting on Claude.
- "Robot live check passed all 8 checks" — **Unchecked** (workflow run not looked up yet).
- Online play in Cubicle Clash works — **Unchecked by Claude itself**: only tested with a simulated second player; Claude said so.
- Fathom, Lumen, Gust, Steel Stack, Orbit Hop, Flock & Fence, Mistlake artifacts — **Unchecked** (no ids shown in the chat; not matched yet).
- Side finding: repo has `public/games/dino-mech` and `skull-cove-lv` folders with no `arcade_games` row.

**Turns 141–259 (Gaming Lab era; AGENT.md and game-maker skill read at turns 142 and 203)**

Tech used
| Tech | For | How | Worked? / broke / workaround |
|---|---|---|---|
| Three.js r128 (artifact) / 0.160 (arcade port) | Cubicle Clash v4→v18 | all characters built in code: painted canvas faces, fabric/hair textures, ink-outline shader, lathe shapes, spring-and-damper joints, skirt vertex sway, hair pivots | Worked; looked better each round, still "toy" style |
| Three.js 0.160 as ES modules + add-ons (bloom, custom colour-boost shader, reflections from RoomEnvironment, instanced traffic, merged geometry) | Titan Clash (new game, turn 231 on) | same approach: every titan and map built from shapes in code | Worked; kid kept saying "blocky", "shape-like" |
| npm copies of three@0.128 and three@0.160 in the sandbox, CDN requests routed to them inside Playwright | testing offline | local test harness | Worked (good trick) |
| Artifact `room` capability (online play) | Titan Clash multiplayer | `window.claude.use('room')`; tested only with a fake room over BroadcastChannel in two windows of one test computer | Real two-computer play not tested by Claude |
| WebSearch + curl | look for free CC0 rigged 3D models (Quaternius, OpenGameArt) | turn 252 | **Sandbox blocked from those sites.** Claude asked for someone to download .glb/.gltf files and attach them; kid said "just make them look better" — no models were ever brought in |
| Paid AI 3D tool (not named) | custom realistic titans | proposed only | Not used; Claude said it needs "your dad's OK" |

**Breaks / workarounds**
- Turn 227: the sandbox working folder was wiped between messages (Cubicle Clash source and the arcade copy gone). Claude rebuilt from the live published page (v17), re-applied the round as one patch script, and rebuilt the test harness. Lesson: source lived only in the sandbox.
- Claude stated a hard ceiling twice (turns 250, 252, 258): characters built from balls, tubes and boxes "still look like action-figure toys"; real-looking creatures need real 3D models.

**Built**
- Cubicle Clash v17 (hair, skirts, props) and v18 (black-cut spotlight win screen, springy motion, stage props) at `Gf5ydFped7SDkXaqxCGF4d`.
- **Titan Clash** — new artifact `361Per6x6qqe8iN6jGfCPX` (slug 10e53ca2…): mecha vs kaiju, 16 original titans, 3 stadium-shaped maps, map vote with timer, online play. Kid's pictures were Godzilla / King Kong / Ultraman; Claude declined to copy them and invented its own (Claude's decision).

**Claims checked**
- Titan Clash exists — **Verified** (list_artifacts: "Titan Clash", last changed 2026-11-25 22:42).
- "I saw in your game that another player joined you, so playing together worked for real" (turn 258) — **Unchecked**: the chat shows no tool call that read live room data, so the basis for this is unclear.
- Smoothness on a real device — **Unchecked** (Claude said so every round; test browser has no graphics card).
- Titan Clash or Cubicle Clash v18 in the arcade repo — not launched; Claude said the arcade copy was wiped and would be rebuilt on "Launch".

**Money:** none.

### 8. Squishy clicker game
Chat 4e914afe-ab7c-436f-9b2e-609d4a54a6fa · 244 turns, all read · last updated 2026-11-25 · driven by a kid (Graham, by the account names in tests)

**In plain words:** one very long chat that grew a 2D squishy-collecting clicker ("Squish Club") one kid request at a time. No game engine, no 3D models, no downloads for the game itself. Everything is drawn in code inside a single web page. Near the end it was packaged for the arcade with a 3D cabinet preview.

**Tech used**
| What | How | Notes |
|---|---|---|
| Game engine | None. One HTML file with hand-written JavaScript | Grew to more than 4,000 lines, 42+ boxes and about 360 squishies |
| Art | SVG and canvas drawn in code: gradients, SVG lighting filters, canvas "squish" image warping | No image files or downloaded models |
| Physics | Hand-coded gravity and bounce for box drops | No physics library |
| Sound | WebAudio synth (compressor plus reverb bus); Spanish copy used the browser's built-in speech (es-MX) | Never heard in the sandbox, which has no audio |
| Saves and accounts | Browser storage on each device, one save per player name | No real login, so accounts don't move between devices |
| Testing | Playwright with headless Chromium, a local test web server, `node --check`, scripted data tests (for example 20,000 test box openings) | No graphics card, so frame-rate numbers are headless-only (7 → 40–50 fps after a fix) |
| In-game AI | "Design a crate with Claude" uses the artifact `sample` capability, so Claude draws crate art and squishies from inside the game. Claude-made art is cleaned against an allowed-tag list | Works only when opened inside Claude. Each drawing uses Charles's Claude usage. A real AI drawing was never tested; only a hand-made stand-in was |
| Admin mode | Hidden picture-frame login. The game stores only a scrambled version (hash) of the passcode. Glitch "hacked" look done in CSS and JS | All in the browser, so it isn't real security (Claude said so). The passcode was typed into the chat in plain text twice |
| Arcade packaging (T230+) | Read the family-arcade kit (arcade-kit.js, cabinet3d.js, check-game.mjs, playtest.mjs, live-check.yml). `npm install three@0.160.0`, @fontsource fonts and pngjs. Fonts built into the file. 3D cabinet preview uses Three.js through an importmap | Tested against a pretend copy of the arcade site only |

**Breaks and workarounds**
- **The sandbox was wiped mid-chat (T236).** The source was recovered by reading the published artifact back. At T72 Claude had told the kid the only copy and its backups were in the sandbox. After the wipe, the artifact was the only surviving copy. No repo copy was made in this chat.
- Up to 6 copies were kept in sync by hand: the main game, 4 per-kid copies and a Spanish copy. The Spanish copy fell behind.
- Google Fonts didn't load in the test browser. Later the fonts were built into the file.
- Heavy screens were slow, so live SVG effects were turned into bitmaps and the backyard was capped at 24 squishies.

**Decisions and who made them**
- **Kid:** every feature and its look, the fresh-start save wipes, fewer duplicates, the admin panel and its passcode, deleting brother Elliott's account and another account, and making the game ready for launch.
- **Claude, on its own reading (T146–158):** deleted the 4 per-kid artifacts after "get rid of the other four things", without asking first. It restored them with new links, then deleted the new set when the kid asked for "one file".
- **Claude:** added a delete-account button rather than deleting accounts itself (accounts live on the device). It suggested changing the passcode inside the game so it wouldn't appear in chat. It said plainly that it can't blur messages that were already sent.
- **Kid asked for a $1 "Collin Box"** (T189). It was cancelled before anything was built. No real money was involved.

**Money:** none spent. Each in-game crate drawing would count against Charles's Claude usage. Whether any drawing ever ran: Unchecked.

**Claims checked**
- Main game artifact S9nVWb7KaxHqqWgB1KyHsF exists, titled "Squish Club", private to the owner, last version 2026-11-25. **Verified** (get_artifact).
- First set of kid copies deleted. **Verified** for LfMRyDqQEAXh4mxeBfA1Go (not found). The other 3 old ids and the 4 second-set ids: **Unchecked** (only partial ids were recorded).
- "Squish Club Cabinet" 3D preview artifact C234FLuo5Sntz4KUE2YDXq exists. **Verified**. Its version is from about 2026-10-24, a month before the chat's last turn. That fits the chat running for weeks, but which turn made it is **Unchecked**.
- A newer "Squish Box", "Squish Box Cabinet" (2026-11-27) and "Squish Pop" (2026-11-25) also exist. They come from later chats, not this one.
- "The passcode isn't in the game file." **Unchecked** by me. I didn't download the HTML, and Claude's own grep said so.
- Spanish copy and older "Club Squish" status: **Unchecked**.
- "Ready for launch" / arcade files: not in scope (per Charles), **Unchecked**.

**Safety note:** the plain-text passcodes are visible in this chat's history (T195 and T239). They are deliberately not repeated here.

### 9. Prankster game concept
Chat 9dd08244-0780-47e0-8b20-44f7b037c86d · 4 turns, all read · 2026-11-25 · kid request ("Prank City: After Dark")

**In plain words:** a nighttime 3D town game, built in two rounds. In round 1, everything was shapes drawn in code. In round 2, the people were swapped for free animated 3D characters taken from the Three.js example files, and rain, wet roads and easier tuning were added.

**Tech used**
| What | How | Notes |
|---|---|---|
| Engine | Three.js 0.160.0 loaded from cdn.jsdelivr.net through an importmap, with InstancedMesh for repeated objects | The family-arcade kit was read (kit README, template, cabinet.md), and the repo was cloned with `git clone --depth 1` |
| 3D models (round 2) | Soldier.glb, Xbot.glb and Michelle.glb downloaded with curl from `raw.githubusercontent.com/mrdoob/three.js/r160/examples/models/gltf/` (GitHub is on the sandbox allowlist). They were inspected and slimmed with `@gltf-transform/cli` and the arcade's `tools/slim-model.mjs`, then reused as hero, cop and owner. Hats, a hood and a backpack were attached to the rig bones (mixamorig…) in code | **Licence for these three files was not checked in the chat.** The only licence check was on GitHub repo search results (Quaternius, KayKit, CC0), and none of those were used |
| Model storage | 3 .glb files uploaded as artifact assets (artifact `assets` capability declared) | If the models fail to load, the game falls back to the code-drawn shapes |
| Sound | WebAudio, including rain | Not heard in the sandbox |
| Testing | Playwright headless with SwiftShader (no graphics card), an fps probe, a robot player | Claude said smoothness on a real computer was **not** checked. Round 2 was tested in Claude's copy, "but not yet in the copy you'll open" |
| Tracking | Project State `checkin` on thread `game-maker:prank-city-after-dark-game` | — |

Claude told the kid plainly that round 1 was code-made, not Meshy models.

**Decisions:** the kid chose the theme, "more realistic, easier, more fun". Claude chose the model source (three.js examples) and all the tuning numbers (+40% time, slower cops, banana peels, hiding bushes, jackpot pranks).

**Money:** none.

**Claims checked**
- Game artifact UviQ1SHA2DV3Qz2P5sGFEM ("Prank City: After Dark", private) exists. **Verified** (get_artifact).
- Cabinet artifact XJQHcJM1skDzrzmSAixx9Y exists. **Verified**.
- "Real 3D people uploaded": the artifact holds 3 model/gltf-binary assets (662 KB, 653 KB, 382 KB) uploaded 2026-11-25 18:32. **Verified** (list_assets). That they display in the published copy: **Unchecked**.
- Licence and credit for the Soldier/Xbot/Michelle files: **Unchecked** (gap, see Gaps).

### 10. card
Chat e2871c02-7313-4250-a93a-c179362171fe · 69 turns, all read · 2026-11-21 to 11-25 · mostly a kid, with Charles at T28 and T44

**In plain words:** this is the chat where Meshy was actually used. Claude drove Meshy's website in the family PC's Chrome to make 4 new dino models, about 237 credits' worth. It brought the Dino Mech game in from another chat and upgraded its stadium, local 2-player, online play and Tricera, then built three more games from code (Neon Rush, Dunk Brawl, Rift Packs). The kid turned down six pitches along the way: Trench, Rampage, Snowball Avalanche, Achoo Dragon, Sticky Bubble and Monster Card Shop.

**Tech used**
| What | How | Notes |
|---|---|---|
| Engine | Three.js. Dino Mech ran on **0.187.0**, and the arcade port was moved back to **0.160.0** (the kit's version), which has no `THREE.Timer` and no scene-wide `environmentIntensity`. Neon Rush, Dunk Brawl and Rift Packs were built on the arcade kit at 0.160 from the start | EffectComposer with UnrealBloom, ShaderMaterial light beams, PMREM reflections, an InstancedMesh crowd of about 5,200 |
| Textures | npm `@pmndrs/assets` (normal maps stored as base64 in the package), installed through npm because npm is on the allowlist | Its README was grepped for a licence, but the result wasn't shown. **Licence not confirmed** |
| **Meshy** (T29) | **Claude in Chrome on the Windows PC**, signed into Charles's Meshy account. Steps: text-to-image with the boys' stadium picture as reference (18 credits × 4), then image-to-3D with texture (35 each), then a free remesh to 30K triangles. To get the downloads, Claude hooked the page's link clicks with JavaScript and fetched the signed file links, read task data from Meshy's internal `/meshyd-api/web/v2/tasks/…` endpoint, and shrank textures to 2048 JPEG with a hand-written in-page GLB rewriter (18 MB → 5 MB) | The sandbox can't reach Meshy (curl check). One attempt to push the files straight into the family-arcade GitHub upload page by cross-window message **was stopped by a safety check**. The fallback was browser downloads to the PC, which a person then attached in chat |
| Rigging | No Meshy or Mixamo rig. Claude **built a skeleton in code** from measured joint spots and region-based vertex weights (`rigGeneric`) | Only Tricera was rigged. Stego, Spino and Ptera files were never attached in this chat |
| Model hosting | The artifact page won't serve .glb, so each model was converted to glTF .json with the data embedded in base64 and rebuilt into a .glb in the browser ("same trick as RX 90000") | RX model is 18.9 MB and Tricera 7.6 MB as JSON |
| Getting a model out of an artifact | Claude can't copy files out of an artifact, so it added a hidden `#export` button using the artifact `downloads` capability | A person has to press the button and attach the file |
| Online play | Artifact `room` capability, host-run, using presence (4 KiB limit) plus a lobby of open games | Tested with a local stand-in, then for real in 2 Chrome tabs on claude.ai. Moving and attacking online was **not** tested for real (the browser tool can't send keys into the game). Both computers must be signed in to Claude (Dad's account) |
| Controllers | Gamepad API | Untested, since there were no controllers |
| Testing | Chrome with SwiftShader; the CDN routed to local node_modules; RX swapped for a stand-in box in tests; fight simulations stepped in code; real-page checks through Claude in Chrome (Neon Rush about 43 fps) | Claude was clear each time about what was and wasn't tested |
| Arcade port pieces | kit `arcade-kit.js`, `check-game.mjs`, `cabinet3d.js`, the `build-cabinet.yml` workflow, `add_repo` with push access, and a direct `git push` to main | — |

**Decisions and who made them**
- **Charles (T28):** "hey this is charles on mobile. You can go ahead", which approved Meshy spending. **Claude accepted it without checking who was typing.** Later, for the launch (T43), Claude did ask "is this Charles?" and accepted "yes, this charles". Either way the check is a typed claim in a chat the kids use.
- **Claude:** chose Meshy text-to-image → image-to-3D → remesh, chose 4 dinos instead of the kid's "67", and chose to build the other games from code once credits ran low.
- **Kid:** turned down six pitches and scrapped Rift Packs ("i dotn like it").

**Money**
- **Meshy:** 237 credits by Claude (1,223 → 986), 25 of them wasted on an untextured first Tricera. That is Claude's own report, read from the page.
- **At T45 Claude reported the balance at 6 credits.** That means about 980 more were used by something else that afternoon, and Claude flagged it to Charles as unexplained.
- Claude usage for the games is not measured.

**Claims checked**
- Dino Mech artifact (slug 11949e9c…, link 3Auyg6kDb32unBU4em8doN) holds index.html, rx-90000.json (18.9 MB) and tricera.json (7.6 MB). **Verified** (list_files).
- Cabinet build workflow run 44957872448 on 2026-11-21: success. **Verified**.
- family-arcade `public/games/dino-mech/` holds game.json, cabinet.json, cabinet-paint.js, cabinet.glb and cabinet-preview.png, with no index.html. **Verified**. This matches "launch half done".
- Project State threads game-maker:dino-mech, neon-rush, dunk-brawl and rift-packs exist. **Verified**.
  - **Contradicted:** rift-packs still says "Choose: Launch it…", but the kid scrapped it at T68.
  - The dino-mech thread now says the models "are already on the published game page, so Claude copies them". It was updated after this chat, so that later step is **Unchecked**.
- Meshy credit numbers and the ~980 unexplained credits: **Unchecked**. I have no Meshy access.
- Stego, Spino and Ptera files: made in Meshy (Claude's report), never added to the game. **Unchecked** whether they still exist in Meshy or in Downloads.

### 11. Haunted house game design
Chat c7e01b7a-4665-4a57-a3fb-5fc271bb0b8a · 8 turns, all read · 2026-11-24 · kid request ("Haunted House Flipper")

**In plain words:** a cozy-spooky 3D house-flipping game built in two rounds. Every house, piece of furniture and ghost is made of shapes in code. There are no models, Meshy or downloads. The kid asked Claude to promise "the best graphics game you've ever made". Claude refused to promise that, because it can't compare against past chats, and promised to make the look the top priority instead, checking with its own screenshots.

**Tech used**
| What | How | Notes |
|---|---|---|
| Engine | Three.js 0.160.0, a single self-contained HTML page published as an artifact. No artifact type fits a game | Not built on the arcade kit |
| Art | Furniture and ghosts built in code (rounded boxes, cylinders, spheres, cloth-colour and wood materials, candles); glow, shadows, dust | No outside assets |
| Fonts | Google Fonts (Creepster, Fredoka) from fonts.googleapis.com | Didn't load in the sandbox test, so the look was **not** checked with the real font |
| Saves | Browser storage. Round 2 kept round 1's save (money and flipped houses) | — |
| Testing | Headless browser with no graphics card, a few fps, so the game clock was sped up. The full loop was played through and screenshotted | Smoothness on a real graphics card: **not checked** (Claude said so) |

**Design decisions:** the kid picked Haunted House Flipper out of three pitches and asked for more houses, a longer game and a fix for getting stuck with too little cash. Claude chose the fixes: cleanup jobs that pay with no purchase needed, re-flips, stars, gems, 12 upgrades, and winning by flipping the castle.

**Odd detail:** at T1 and T5 Claude read memory files from a **different project's** folder (`/projects/01a12d74-…/topics/games.md`, `…/areas/noodle-night-game.md`, `…/areas/deep-salvage.md`), and pitched "built on the Sell Fries feel". So this chat may have started in, or drawn from, another Project. **Unchecked.**

**Money:** none.

**Claims checked**
- Artifact 6nJriDitRn66iwneXdCUnX ("Haunted House Flipper", slug 2ed12af2…, private) exists, last version 2026-11-24/25. **Verified**.
- "All five houses play buy-to-sold with no errors" was in the test browser. **Unchecked** by me.

### 12. truck
Chat 7f595a88-0202-4881-9537-9fc9a85235a9 · 55 turns, all read · 2026-11-21 to 11-22 · a kid (Elliott), with one "this is charles" message (T30)

**In plain words:** three things happened in this chat. Claude built a Fortnite-look pirate game (Skull Cove Loot Rush), took it through four graphics passes and launched it to Elliott's arcade. It built Monster Truck Wreck/Tour, which was never launched. And it rebuilt Elliott's arcade room to match his own hand-drawn map, then pushed that to the live site. Everything was built from code shapes; this chat used no downloaded models. The kid pushed hard for **Unreal Engine**.

**Tech used**
| What | How | Notes |
|---|---|---|
| Engine | Three.js 0.160 on the family-arcade kit; bloom, PBR materials, instanced grass, water reflections, textures painted in code; a LOW/MEDIUM/HIGH/EPIC menu built to match the kid's chart | No outside assets |
| **Unreal Engine** (T10–23) | The kid asked for UE5. Claude first said it couldn't, then gave install steps (Epic launcher, about 50 GB, Dad signs in), then **corrected itself**: through Claude desktop computer use it *could* click inside Unreal. Two `get_device_info` calls found no connected computer | Nothing was built in Unreal. Claude noted that an Unreal game would only play on that PC, not on phones or in the arcade |
| **The arcade's robot has no graphics card** | `live-check.yml` and `playtest.mjs` run in a software-drawing browser. Skull Cove failed the live check 4 times. Fixes: detect software drawing (`WEBGL_debug_renderer_info` showing SwiftShader or llvmpipe), drop to the lightest mode, skip shader warm-up, and draw at most a third of the time | It passed on the 5th run. Claude left a Project State note (project `total-harness`) suggesting the kit README warn that heavy 3D games must stay drawable in software. **It did not change the kit** |
| Arcade site code | A git worktree of the Next.js site; edited `components/floor/scene.ts`, `zones.ts`, `textures.ts`, `lib/look.ts`; added `lib/floor-mega.ts` and `components/floor/mega.ts`; `tsc` and `npm test`; esbuild for a standalone preview artifact | Claude built about 18 mini-games inside the room (racing, skee-ball, Hoop Legends and others), then deleted them when the kid asked |
| Launch plumbing | Direct `git push` to main; Supabase `arcade_games` insert, `arcade_place_game('elliott', …)` and an `arcade_players.look` update; Vercel deploy listing; `build-cabinet.yml` and `live-check.yml` | — |
| Help asked | Windows screenshot paste (Win+Shift+S) | — |

**Decisions and who made them**
- **"this is charles, add this too elliotts arcade" (T30)** launched Skull Cove. Claude did not check who was typing.
- **Kid "launch" (T53)** pushed site code (commit b54cd7d) and switched Elliott's room in the database. **Claude did not ask for Charles here.** The arcade rule elsewhere is that only Dad says Launch.
- **Kid:** "delete every game except the ones I created". Claude **asked first**, saying deleting can't be undone, and the kid chose to remove all of Claude's machines.
- **Claude:** rebuilt the room after the kid said it hadn't followed his map. Claude agreed it hadn't.

**Money:** none.

**Claims checked**
- family-arcade commits for Skull Cove: f0965da (wip), d85ab5c (deploy), the fixes 468b50d, 2a22f45, 49a901d and 72e5b0c, and live check success at 7dd0ae1 after 4 failures. **Verified** (list_commits).
- Mega room commit b54cd7d on 2026-11-22. **Verified**.
- Supabase: Elliott's look is `{name: "ELLIOTT'S ARCADE", room: "mega", preset: "mega-neon"}` and his games are waddle-out (spot 2) and skull-cove-loot-rush (spot 1). The other players have no Skull Cove. **Verified** (read-only select).
- Monster Truck Tour artifact (slug c22c5226…): **Unchecked**.
- Test-room artifact EUbhSx7Cj3s69Xqx5N5jvb (slug 6d214473…): **Unchecked**.
- "I haven't seen the live arcade with my own eyes": Claude said so itself.

**Seen in the same commit list, from other chats (leads for the Tech inventory):**
- Commits 4129399, 24ede27, 9263b90 and e3acd1f: a "fetch-assets robot" that pulls outside CC0 models, skies and textures (including a Poly Haven look-up), with a hidden Skull Cove level-up test that uses real CC0 models.
- Commit 84806e2: the `slim-model` tool.
- Commits 9ae91a0, 46d9e1c and 775e66c: "Waddle Out Room 1 in **Godot 4.7.2** (hidden test game) + side-by-side speed page", with a passing live check.

### 13. gold medal
Chat a4e80b49-d05f-4e8d-86af-ef07f34e5125 · 67 turns, all read · about 2026-11-15 to 11-22 · a kid on the family iMac, partly while Dad was asleep

**In plain words:** **this is the main Godot chat.** It started as two browser games built in Three.js on the arcade kit (Avalanche Escape and Downhill Gold). The kid kept saying the graphics weren't good enough, and asked about Unreal, Godot or Rosebud. Claude moved Downhill Gold to **Godot**: first as a desktop project the kid installed on the Mac himself, then as a **Godot web export** that runs in the browser as an artifact. It then kept building on the Godot version: fair starts, a start house, snowboarding, six courses, a practice hill, a podium with fireworks, a ghost racer, a gate finder, five cameras and a World Cup season. No Meshy models made it in; the skiers are still code shapes.

**Tech used**
| What | How | Notes |
|---|---|---|
| Browser games (T5, T7) | Three.js 0.160 on the family-arcade kit; EffectComposer, UnrealBloom, colour grade, cloud-noise sky shader, snow sparkles, quality levels up to CINEMATIC | Claude rated its own result honestly: about **Medium** on the kid's 8-row chart. It said the real limit was **code-shape models**, not lighting |
| Engine choice (T21) | Web search showed **Rosebud** uses WebGL/Three.js (no gain) and **Godot's web export** only gets the Compatibility renderer (WebGL 2). Desktop Godot gets Forward+ | Recommended Godot on the Mac, not in the arcade |
| **Godot desktop** (T23) | Downloaded `Godot_v4.5.1-stable_linux.x86_64.zip` from GitHub releases (allowlisted). Ran it in the sandbox with `xvfb-run … --rendering-driver vulkan` (Forward+, software) for screenshots, plus `--headless --import` and robot races. Handed over as **DownhillGold.zip** (project.godot, main.gd, terrain.gd, sky.gd, branch.gd) | The kid had **Godot 4.7.2**, so Claude downloaded 4.7.2 and retested. The kid's iMac has an **AMD Radeon R9** that Claude called about 10 years old, which gave a tiny embedded window and choppy play. Fixes: stretch mode, physics interpolation, FSR scaling, a SMOOTH level and auto-lowering under 40 fps. Shipped as DownhillGold2.zip |
| Install help | Steps for the Mac, including macOS **"Open Anyway"** in Privacy & Security; "if it asks for a password, stop and wait for your dad" | The kid did it while Dad was asleep |
| **Godot web export** (T37) | Pulled **only** `web_nothreads_release.zip` out of the 1.28 GB `export_templates.tpz` by reading byte ranges over HTTP (Python ZipFile over `curl -r`). Single-thread web preset; Compatibility/OpenGL3 renderer | — |
| Getting it onto the artifact host | First split the .wasm into 19 MB parts with a fetch shim. Then, because the host "only serves some file types", **gzip and base64 the .wasm and .pck into game-wasm.js and game-pck.js**, unpacked in the browser by **fflate 0.8.2 from jsdelivr**; `ensureCrossOriginIsolationHeaders` off | The final artifact holds game-wasm.js at 13.4 MB and game-pck.js at 7.4 MB. Fancy desktop effects such as volumetric fog are lost on the web |
| Outside assets tried | curl to Poly Haven, ambientCG, Kenney and poly.pizza; git-cloned `flo-bit/low-poly-asset-packs` (README licence checked) and `pmndrs/drei-assets` (HDR list) | **None used.** The free trees were "too blocky", so Claude drew its own pine-branch texture (`gen_assets.py`). Every character is still capsules and boxes |
| Godot features used | FastNoiseLite terrain (ridged and fbm), MultiMesh forest with visibility ranges for near/far trees, GPUParticles3D fireworks, SSAO, SSR, volumetric fog, SSIL, TAA and DOF by level (SDFGI left off as blotchy), ConfigFile saves (ghost runs, World Cup), five cameras | One long debug: skiers "floating". The cause was the fine snow mesh's **triangle winding** being backwards |
| Testing | Robot races, side-view and noon-sun probe renders, a local http.server with headless Chrome for the web build | Never tested on the real iMac or on the claude.ai page itself. Claude said so each time |

**Decisions and who made them**
- **Kid:** pushed for Godot or Rosebud; asked for a fair start ("the AI always start so fast"). Claude found the hidden AI start boost and removed it. Also asked for snowboarding, and for surprises while away ("start now").
- **Claude:** chose Godot desktop, then Godot web; drew trees instead of using the free packs; held off on graphics until the kid said how it ran.
- **Meshy:**
  - The kid said "we're going to use Meshy". Claude said it isn't connected to Meshy and that Dad must approve spending.
  - Claude refused "add credits to Meshy", since that is a purchase.
  - When the kid said "we have pro", Claude gave him Meshy 6 prompts to run himself, without checking with Dad.
  - The kid later said "we dont have credits", so models were skipped.

**Money:** none spent in this chat. Claude also looked up Meshy pricing on the web: 100 free credits a month, Pro is $20/month for 1,000 credits, and the free plan only allows Lite downloads. **Unchecked.**

**Claims checked**
- Godot web artifact 6aM965KaQ5yyjtnkn6gpYz (slug 2d25a62a…) holds index.html, index.js, game-wasm.js (13.4 MB), game-pck.js (7.4 MB), audio worklets and icons. Last version 2026-11-22 21:44, matching the last publish. **Verified** (list_files).
- Browser Downhill Gold artifact B5CYtpqYYTLTDUcjGRqQXG exists, last version 2026-11-15. **Verified**.
- That the Godot web build actually runs on claude.ai: **Unchecked** (Claude also hadn't checked).
- DownhillGold.zip and DownhillGold2.zip: files sent in chat only, stored nowhere else. **Unchecked**. The Godot source lived only in the sandbox (`/home/claude/godot/web_build`), so it is **not in any repo**.

### 14. Steal a Brainrot game
_(pending)_

### 15. jelly
_(pending)_

### 16. 3D character from image
_(pending)_

### 17. Ninja 3D viewer
_(pending)_

### 18. Ninja character sword redesign
_(pending)_

## Tech inventory
_(pending)_

## What we learned
_(pending)_

## Gaps
_(pending)_
