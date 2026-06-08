# chat-capture.md — Drafting a cbrain brief from chat

**Status:** v0.1.0 — reference, not a skill. No write-authority.
**Owner:** Charles
**Read this when:** Charles asks to capture a person / organization / project / framework / concept / place into cbrain *from chat* ("add to cbrain," "let's capture," "create an entity for," or names an entity not yet in cbrain during a clear knowledge-capture chat).

---

## What this is

This is **drafting guidance**, not a write-authority. It is the chat equivalent of the email Watcher: it turns a capture request into a well-formed **brief**, which Charles approves in chat, and which the **Archivist** (the single write-authority) then files. It holds no commit logic of its own.

The chat path:

1. Charles prompts a capture ("capture Reece — project engineer at Wilhelm on C92").
2. Claude, following this reference, asks the SCHEMA questions, derives slugs, surfaces follow-on entities and relationships, and **assembles a brief** conforming to `cbrain/contracts/BRIEF_SCHEMA.md` (v0.2.0).
3. Claude shows the brief as an artifact and prompts for approval.
4. Charles replies **"approved"** in chat. Only then is the brief sealed (assigned `brief_id` + `sealed_at`).
5. The **Archivist** files the sealed brief's intents into cbrain.

**Claude does not commit anything to cbrain from the chat path.** Drafting produces a brief; the Archivist writes. This is what keeps cbrain's single-write-authority + one-hop-provenance model intact (E-094, E-096): the human approval gate sits cleanly between drafting and filing.

## The one structural rule: intents-only

`BRIEF_SCHEMA.md` v0.2.0 has two registers:

- **Register 1 — `intents`** — the typed worklist the Archivist files.
- **Register 2 — `observations`** — a producer's *reasoning pass* output (prose comprehension, conflict flags, conversation suggestion).

A chat capture has **no reasoning pass** — that is the Watcher's Layer-2 job on unattended email. So **a chat-drafted brief carries `intents` only; the `observations` register is absent** (the schema marks it "absent when the producer ran no reasoning pass"). Do **not** populate `comprehension`, `flags`, or `convo_suggestion` from the chat path. If a possible duplicate or merge is noticed while drafting, raise it in chat as a Needs-from-you item for Charles to resolve *before* sealing — not as a brief flag.

## The brief a capture produces

**One capture = one brief**, bundling every intent the capture implies (E-096): the entity itself, any follow-on entities, any relationship edges, any enrichment of existing entities. Three intent types cover everything this path produces (targets per `BRIEF_SCHEMA.md`):

| What the capture needs | Intent type | `target` shape |
|---|---|---|
| A new entity | `create_entity` | `{ entity_type, slug, fields, body }` |
| A field set on an entity that already exists | `enrich_field` | `{ entity_type, slug, field, value }` |
| A graph edge between two entities (optionally a new predicate) | `propose_relationship` | `{ subject, predicate, object, register_predicate? }` |

`flag_clue` and `record_pm_item` exist in the vocabulary but are not typically produced by a chat capture (the first is a watcher tier-2 case; the second is reserved).

---

## Drafting SOP

1. **Confirm entity type.** One of the six: `person`, `organization`, `project`, `framework`, `concept`, `place`. If the request implies a type not in this list, STOP — do not invent a type. Surface it as a Needs-from-you item: a new type requires a `SCHEMA.md` change through a separate flow first.

2. **Read the contract.** Fetch `cbrain/contracts/SCHEMA.md` via Custom GitHub MCP `get_file_contents` (owner=Chooch333, repo=cbrain, path=`contracts/SCHEMA.md`). Identify, for the chosen type: the five required fields (`slug`, `type`, `created`, `updated`, `summary`), the recommended fields (`tags`, `related_to`, `sources`), and the type-specific optional fields. *(The entity contract lives at `contracts/SCHEMA.md`, not the repo root.)*

3. **Check for collision.** List the target directory (`get_file_contents`, owner=Chooch333, repo=cbrain, path=`<type>` — e.g. `people`). If an entity with the proposed slug already exists, this capture **enriches** an existing entity rather than creating one: the intent is `enrich_field` on that slug, not a second `create_entity`. (The Archivist refuses to overwrite a live entity from a `create_entity` intent, so drafting must catch this and route to `enrich_field`.)

4. **Derive the slug.** Lowercase, hyphen-separated, no dates, no numeric suffix unless needed to disambiguate, stable. The slug matches the eventual filename without `.md`.

5. **Ask the right questions — one batch, plain English.** Cover *every* required field at minimum. Opportunistically gather recommended and type-specific fields. Ask only for what isn't already evident from the chat. For any required field that's genuinely unknown, do **not** guess — leave it blank in `target.fields` (sparse fields are acceptable, best-effort, E-081) and note the gap in the brief body so Charles sees it at the gate.

6. **Surface follow-on entities.** Based on type:
   - **person** → ask about their organization. If the org isn't in cbrain, propose it as a follow-on `create_entity` intent **in the same brief**.
   - **project** → ask about `client_org` and `delivering_org`. Propose any missing ones as follow-on `create_entity` intents in the same brief.
   - **organization** → if key people are named, flag each as a potential follow-on person.
   Surface follow-ons as Needs-from-you items — Charles decides which to include. Those he approves become additional `create_entity` intents bundled into the one brief.

7. **Model relationships as `propose_relationship` intents.** For each meaningful, *stated* relationship the entity has to another entity:
   - Check the predicate registry (`PREDICATE_REGISTRY` in `cbrain/services/lib/extract.ts`) for a fitting predicate. If one fits (e.g. `worked_with`), emit a `propose_relationship` intent with that predicate.
   - If a real, stated relationship fits **no** registered predicate, **proactively propose a new predicate by name** as a Needs-from-you item — never bury it in prose. On Charles's approval, the intent carries `register_predicate: { name, meaning, symmetric }`; the **Archivist** performs the registry edit and tuple declaration at filing time. Drafting proposes the predicate; the Archivist registers it.
   - Predicates are **demand-driven**: propose one only when a genuine stated relationship needs it; never invent speculative predicates. Test: "does a real relationship exist that no predicate captures?" — if yes, propose; if no, do nothing.

8. **Assemble the brief as an artifact.** One brief, all approved intents bundled, `intents` register only (no `observations`). Show the full brief — frontmatter and body — in plain English. Per PROTOCOL.md the artifact is the ticket; discussion stays in chat.

9. **Prompt for approval / sealing.** Ask Charles to approve. On "approved," the brief is sealed (assigned `brief_id` + `sealed_at`, `status: approved`) and handed to the Archivist to file. A draft brief (no `brief_id`) is never filed.

10. **Hook check at close (`should-distill`).** Did anything emerge worth capturing — a schema improvement, an alias/slug convention, a new relationship predicate, a workflow note? A relationship that surfaced with no fitting predicate is an explicit distill trigger. If yes, surface as a Needs-from-you item. If no, do nothing — the usual outcome.

---

## Examples

### Example 1 — New person, org already in cbrain
"Let's capture Reece Chapman — project engineer at Wilhelm on the C92 job."
- Type `person`, slug `reece-chapman`. `org: f-a-wilhelm-construction` (exists — no follow-on), `role: Project Engineer`.
- Email/phone unknown → left blank in `target.fields`, gap noted in brief body.
- Brief carries: one `create_entity` (the person) + `propose_relationship` edges to the Wilhelm org and the C92 project (predicates checked against the registry). One brief, intents only.
- Charles approves → sealed → Archivist files.

### Example 2 — New project, implies a missing client org
"Create an entity for the Ridgeworks Maple Street duplex — a Ridgeworks deal, no outside client."
- Type `project`, slug `ridgeworks-maple-street`. `delivering_org: ridgeworks`.
- `ridgeworks` org not in cbrain → surface as a Needs-from-you follow-on. If approved, a second `create_entity` for the org joins the same brief.
- `client_org` blank (self-delivered), noted in body.

### Example 3 — Unsupported entity type
"Add an entity for the C92 weekly meeting — a recurring event."
- `SCHEMA.md` has no `event` type. STOP; do not invent one.
- Needs-from-you: a new type requires a `SCHEMA.md` change first. Offer the nearest fit (capture the meeting as facts in the body of `projects/elanco-c92-2025.md`) and ask which Charles wants.

### Example 4 — A relationship with no fitting predicate
"Jared and I went to college together." (while capturing Jared)
- Real, stated relationship; only `worked_with` is registered, which means delivered project work — college friendship doesn't fit.
- Do not bury in prose. Propose a new predicate `went_to_college_with` (symmetric) as a Needs-from-you, first tuple `charles-courtney → went_to_college_with → jared-natalino`.
- On approval the `propose_relationship` intent carries `register_predicate: { name: went_to_college_with, meaning: "attended the same college", symmetric: true }`. The **Archivist** adds it to `PREDICATE_REGISTRY` and declares the tuple at filing — not this drafting step.

---

## Changelog

- **v0.1.0 (2026-06-08)** — Created from the retired `roles/cbrain-entity-builder/SKILL.md`. Converged the chat path onto the producer → approve → Archivist brief model (E-096): the chat path no longer commits to cbrain; it drafts an intents-only brief (no `observations` register — no reasoning pass on a chat capture) that Charles seals and the Archivist files. Preserved the entity-builder's interview content (type questions, slug rules, follow-on-entity logic, relationship/predicate proposal) as drafting guidance; dropped its commit/patch SOP steps (the Archivist owns writing). Corrected the entity-contract path to `cbrain/contracts/SCHEMA.md`.
