# Build Brief — BB-2026-10-14-skills-folder-merge

**Build:** 38
**Brief:** BB-2026-10-14-skills-folder-merge
**Git home:** owner=Chooch333, repo=agent-library, path=docs/design/BB-2026-10-14-skills-folder-merge.md
**Project State:** agent-build-out · tags build-brief, build-38, agent-library, skills-merge
**Overnight:** yes · **target_repo:** Chooch333/agent-library · **after:** none
**skills:** orchestrate-build
**Stack Flow:** text-only path edits in cbrain concepts/stack-map.md; no dots or lines change
**Authored:** 2026-10-14, harness review chat (Charles + Claude). Approved by Charles 2026-10-14: stubs, project home agent-build-out.

**What this is:** Move every folder under `agent-library/roles/` into `agent-library/skills/`, byte-identical, leave 30-day stubs at the old paths, and update every live reference so the word "role" stops naming a kind of file.

**What I'll do:** Copy 27 folders (SKILL.md plus any sibling files) to `skills/`; replace each old SKILL.md with a three-line stub; delete moved sibling files from `roles/` (git history keeps them); update `roles/` → `skills/` in AGENT.md, every live SKILL.md and reference, cbrain's `concepts/stack-map.md` text, and any cbrain workflow that fetches a `roles/` path; retitle AGENT.md's section headers and column labels; try to update the three scheduled-task prompts; prove it with a repo-wide search and sha comparison; close with a Session Log and disclosures.

**What you'll do:** Nothing before the build. After it: if the build could not reach the scheduled tasks, change three prompt paths (listed in its disclosure). After 2026-11-14, approve removing the stubs (a one-line follow-up).

---

## Current state going in

- [verified] 27 folders in `roles/`, 12 in `skills/`; AGENT.md 13 KB (sha ea490e9) with "Active roles" headers and a "Role" column; `roles/stack-manager` is deprecated per the 2026-09-22 changelog.
- [verified] The Cowork preference block already names `skills/<name>/SKILL.md`; it needs no change.
- [assumed] cbrain `concepts/stack-map.md` cites `roles/` paths in its side-panel text; cbrain `.github/workflows/repair.yml` may fetch `roles/repairer`. The build searches both repos rather than trusting this list.
- [assumed] Historical briefs under `docs/design/` in several repos cite `roles/`. They are records and are not edited.

## Why (design decision, 2026-10-14)

The repo's `roles/` vs `skills/` split had no criterion behind it: no runtime difference (a file read stays in context either way), no exclusivity (AGENT.md chains roles in one chat), no consistent placement (`night-run` is a whole session and lives in `skills/`; `investigate` is one task and lives in `roles/`). Anthropic's Agent Skills standard uses one word. Charles decided 2026-10-14 to retire "role" and match Anthropic's vocabulary.

---

## Receiving chat

Night runner, 15 Oct 2026, ~1 am Indianapolis. Project State project `agent-build-out`. Target repo `Chooch333/agent-library`.

---

## Scope

**In scope:**
- `agent-library`: `roles/*` → `skills/*`; stubs; AGENT.md text; live cross-references in `skills/`, `references/`, `README.md`, `CONVENTIONS.md` if present.
- `cbrain`: live path text in `concepts/stack-map.md`; any workflow step that fetches a `roles/` path. Stack Flow: text-only path edits; no dots or lines change.
- Scheduled-task prompts via `claude-code-remote` tools, if available in the session.

**Out of scope:**
- Any change to a skill's content. Byte-identical moves only; `name:` fields unchanged.
- PROTOCOL.md and its content (Build 39).
- Historical briefs, `imports/`, the plugin skill in Charles's claude.ai account, project instructions.
- Deleting `roles/stack-manager` outright; it moves like the rest and keeps its deprecated marker.

---

## Directive

1. Custom GitHub `get_file_contents`: list `roles/`; for each folder, list it recursively and read every file. Record each file's sha.
2. For each file, `create_or_update_file` the identical content at `skills/<name>/<same relative path>`. Commit message: `Build 38: move roles/<name> → skills/<name>`.
3. Replace each `roles/<name>/SKILL.md` (with its sha) with: `Moved to skills/<name>/SKILL.md on 2026-10-14 (Build 38). Read that file. This stub is removed after 2026-11-14.` Delete every other file under `roles/<name>/` with `delete_file`.
4. `search_code` in `Chooch333/agent-library` for `roles/`. For every hit outside `roles/`, `docs/design/` and `imports/`, change the path to `skills/` with `replace_in_file`. Read each file back.
5. AGENT.md: "Active roles" → "Active skills"; table header "Role" → "Skill"; "Activation pattern" text `roles/<name>` → `skills/<name>`; "Disambiguation rules" wording "role" → "skill"; add a changelog line. Do not touch the Build row's target (Build 39 does).
6. `search_code` in `Chooch333/cbrain` for `agent-library/roles/` and `roles/`. Update live paths in `concepts/stack-map.md` and any `.github/workflows/*.yml`; read back. Then cbrain `rebuild_index` so `get_entity('stack-map')` reflects the text.
7. ToolSearch for `mcp__claude-code-remote__list_triggers` and `update_trigger`. If present: list; for each prompt containing `roles/`, update the path. If absent: record the three task names and the exact replacement in the closing disclosure (`action_needed = true`).
8. Verify: `search_code` `roles/` in agent-library returns hits only in `roles/*/SKILL.md` stubs, `docs/design/`, `imports/`; `get_file_contents` on `skills/` lists 39 folders; read back three moved skills (`design-assist`, `inspector`, `ceo-reviewer`) and compare their sha to the originals captured in step 1.
9. Close per project-state conventions: one Session Log on `agent-build-out`, `post_judgment_call` for every fork, `update_plan_status` succeeded with a done receipt covering acceptance 1–6.

---

## Acceptance

1. `skills/` lists 39 folders; each moved SKILL.md's sha equals the original's (three spot-checked, listed in the receipt).
2. Every `roles/<name>/SKILL.md` is a stub under 200 bytes; no other files remain under `roles/`.
3. Repo-wide search for `roles/` in agent-library hits only stubs, `docs/design/`, `imports/`.
4. AGENT.md contains no heading or column labelled "role"/"Role".
5. cbrain `concepts/stack-map.md` contains no `roles/` path; `get_entity('stack-map')` returns the updated text.
6. Scheduled-task prompts updated, or the three replacements named in a disclosure with `action_needed = true`.

Verification is code and data only. Effort: M. Real-money cost: $0.

---

## Inputs

- [verified] `agent-library/AGENT.md` sha ea490e9; `roles/` and `skills/` listings as of 2026-10-14.
- [verified] Design intent narrative below.
- [assumed] cbrain `concepts/stack-map.md` and `.github/workflows/repair.yml` as the cross-repo hits.

---

## Design intent narrative

This is a rename, not a redesign. The repo's own split between `roles/` and `skills/` never had a criterion behind it, and Anthropic's Agent Skills standard uses one word. Prefer the dullest move: copy bytes, leave stubs, fix paths. If a file under `roles/` turns out to have a counterpart already in `skills/` with the same name, keep the `skills/` one, stub the `roles/` one pointing at it, and disclose. If a reference is in a historical brief, leave it. If a cross-repo workflow is already failing for an unrelated reason, fix the path anyway and disclose the pre-existing failure; do not try to repair the workflow. Never alter a skill's words. When in doubt between editing and leaving, leave and disclose.

---

## Eleven domains

| Domain | State | Where |
|---|---|---|
| 1 Purpose & users | Answered | What this is; Charles and every chat that routes through AGENT.md |
| 2 Acceptance | Answered | §Acceptance, 6 checks, code and data only |
| 3 Runtime | Defaulted | Night runner on claude-code-cloud; Custom GitHub MCP; no third-party cost |
| 4 Data schema | N/A | No database change |
| 5 Storage & recall | Defaulted | GitHub markdown; exact path lookup |
| 6 Interconnectivity | Answered | agent-library, cbrain (stack-map, workflows), scheduled-task prompts; §Directive 6–7 |
| 7 Access & hard gates | Answered | Two repos named; no credentials needed; no money; git deletions are recoverable, so no gate expected |
| 8 Skills & tools | Answered | skills: orchestrate-build; tools named per step |
| 9 Sequence | Answered | No upstream; Build 39 depends on this |
| 10 Assumptions & risks | Answered | §Current state (two assumed items); risk: a stale path in a scheduled prompt, covered by stubs |
| 11 Design intent | Answered | §Design intent narrative |

---

## Pasteable prompt

```
Build 38 — execute Build Brief BB-2026-10-14-skills-folder-merge.
Fetch the brief from Chooch333/agent-library at docs/design/BB-2026-10-14-skills-folder-merge.md (Custom GitHub get_file_contents); do not trust pasted text. Fetch skills/orchestrate-build/SKILL.md (or roles/orchestrate-build if skills/ does not have it yet) and follow it. Reconcile the brief against live repo state before acting. Autonomous build: decide forks from the design intent narrative, log each one, stop only at a hard gate. Close with one Session Log on agent-build-out, disclosures on the Comms Table, and a done receipt.
```
