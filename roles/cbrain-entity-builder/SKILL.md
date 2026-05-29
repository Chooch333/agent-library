---
name: cbrain-entity-builder
version: 0.2.0
status: draft
triggers:
  - "add to cbrain"
  - "build out cbrain"
  - "let's capture"
  - "I want to record"
  - "create an entity for"
  - "event: a person, org, or project not yet in cbrain is named during a chat that is clearly about knowledge capture"
dependencies: []
owner: Charles
updated: 2026-05-29
---

# cbrain Entity Builder

## What

Builds and updates knowledge entities in cbrain — people, organizations, projects, frameworks, concepts, and places. It is the first cbrain-focused skill in the library; the rest are software-development shaped. Given a capture request, it identifies the entity type, asks the questions SCHEMA.md requires for that type, surfaces follow-on entities the new one implies (a person implies their org; a project implies its client and delivering orgs), proposes each entity as a reviewable artifact, and — after approval — commits it to the cbrain repo at the correct path and patches the `related_to` of any existing entity that should now point at the new one. It enforces the SCHEMA.md contract; it never invents data.

## When

**Fire this skill when:**
- Charles says "add to cbrain," "build out cbrain," "let's capture," "I want to record," or "create an entity for."
- Charles names a person, organization, or project that does not yet exist in cbrain **during a chat that is clearly about knowledge capture** (filing facts, building out the knowledge base, recording what's known).
- A prior cbrain entity references — via `related_to` or body prose — an entity that doesn't exist yet, and Charles confirms he wants it built out.

**Do NOT fire this skill when:**
- A person, org, or project name comes up during a build, coding, planning, or debugging chat. A name mentioned in passing is not a capture request. Stay asleep.
- The chat is about *using* cbrain knowledge — looking something up, traversing the graph, answering a question — rather than *adding* to it. (That's read-side work, not this skill.)
- Firing would interrupt active work to ask "want me to capture this?" Wait until the chat is unambiguously about knowledge capture.
- The request is to create a *new entity type* beyond the six in SCHEMA.md. That requires a schema change first (see Pitfalls / How step 1).
- The content belongs in Project State (decisions, next steps, status) rather than cbrain (durable knowledge about entities). Those are different systems; this skill never writes to Project State.
- The file is an email-thread file under `projects/<slug>/threads/`. Those are owned by the email watcher, not this skill.

## How

This skill reads cbrain contract and reference files as inputs. It does **not** chain to another skill. The files it relies on:

- `cbrain/SCHEMA.md` — the entity contract this skill enforces (required/recommended/type-specific fields, body sections, slug rules, cross-reference rules).
- Existing entities under `cbrain/<type>/` — to check what already exists, mirror house style, and find entities whose `related_to` may need patching.

Numbered SOP:

1. **Confirm entity type.** Determine which of the six types Charles wants: `person`, `organization`, `project`, `framework`, `concept`, `place`. If the request implies a type not in this list, STOP — do not invent a type. Surface it as a Needs-from-you item: a new type requires a SCHEMA.md change through a separate flow first.

2. **Read the contract.** Fetch `cbrain/SCHEMA.md` via Custom GitHub MCP `get_file_contents` (owner=Chooch333, repo=cbrain, path=SCHEMA.md). Identify, for the chosen type: the five required fields (`slug`, `type`, `created`, `updated`, `summary`), the recommended fields (`tags`, `related_to`, `sources`), and the type-specific optional fields.

3. **Check for collision.** List the target directory (`get_file_contents`, owner=Chooch333, repo=cbrain, path=`<type>` — e.g. `people`). If an entity with the proposed slug already exists, this is an *update*, not a create: read the existing file and carry its content forward rather than overwriting it.

4. **Derive the slug.** Lowercase, hyphen-separated, no dates, no numeric suffix unless needed to disambiguate, stable. The slug must match the eventual filename without `.md`.

5. **Ask the right questions — one batch, plain English.** Cover *every* required field at minimum. Opportunistically gather recommended and type-specific fields. Ask only for what isn't already evident from the chat. For any required field that's genuinely unknown, do not guess — leave it blank and record a TODO in the body's "Open questions" section.

6. **Surface follow-on entities.** Based on type:
   - **person** → ask about their organization. If the org isn't in cbrain, propose it as a follow-on entity.
   - **project** → ask about `client_org` and `delivering_org`. Propose any missing ones.
   - **organization** → if key people are named, flag each as a potential follow-on person entity.
   Surface follow-ons as Needs-from-you items, not automatic creates. Charles decides which to build.

7. **Propose the entity as an artifact.** One artifact per entity. Show the full file — YAML frontmatter *and* markdown body, both visible — in plain English. Use the SCHEMA.md body section order: Summary, What we know, Open questions, Sources. Per PROTOCOL.md, the artifact is the ticket; discussion stays in chat.

8. **Commit after approval.** On Charles's approval, commit via Custom GitHub MCP `create_or_update_file` (owner=Chooch333, repo=cbrain) to path `<type>/<slug>.md`. For an update (step 3), include the current blob `sha`.

9. **Declare relationships as graph tuples.** Distinct from `related_to` (which is an undirected "these are connected" link), the `relationships` frontmatter field holds typed, directed graph tuples — subject → predicate → object — extracted into the tuples table by `services/lib/extract.ts`. For each meaningful relationship the entity has to another entity:
   - Check the predicate registry (the `PREDICATE_REGISTRY` in `services/lib/extract.ts`) for a predicate that fits. If one fits, declare it in the `relationships` field (e.g. `worked_with`, `went_to_college_with`).
   - If a real, stated relationship does **not** fit any registered predicate, **proactively propose a new predicate by name** as a Needs-from-you item — do not silently bury the relationship in body prose only. This is required initiative, not optional: the moment a relationship has no home predicate, surfacing a candidate is part of the job. Likely examples as the network grows: `introduced_me_to`, `former_colleague_at`, `reports_to`, `referred_by`, `mentored_by`.
   - Predicates are **demand-driven**: propose one whenever a genuine, stated relationship needs it, but never invent speculative predicates for relationships that aren't actually present. The test is "does a real relationship exist that no predicate captures?" — if yes, propose; if no, do nothing.
   - Adding a predicate is a code edit (one line in `PREDICATE_REGISTRY`, with its symmetry flag) plus declaring the tuple in the `relationships` field of both entities. Only registered predicates are extracted; unknown ones are skipped with a warning, so the registry edit must land before the tuple is meaningful.

10. **Patch related entities.** After committing, check whether the new entity should appear in another entity's `related_to`. Example: a new person joining an existing org — that org's file should list the person. Propose each such update as its *own* artifact, get approval, then commit (with `sha`).

11. **Hook check at close (`should-distill`).** Ask: did anything emerge worth capturing as a schema improvement, an alias/slug convention, a **new relationship predicate**, or a workflow note? A relationship that surfaced during this capture and had no fitting predicate is an explicit distill trigger — flag it. If yes, surface it as a Needs-from-you item. If no, do nothing — that's the correct outcome most of the time.

## Examples

### Example 1: New person, implies an org already in cbrain

**Input:** "Let's capture Reece Chapman — he's a project engineer at Wilhelm on the C92 job."

**Output:**
- Type: `person`. Slug: `reece-chapman`.
- Required fields gathered; `org: f-a-wilhelm-construction` (already exists — no follow-on needed), `role: Project Engineer`, `related_to: [f-a-wilhelm-construction, elanco-c92-2025]`.
- Email/phone unknown → left blank, noted in Open questions.
- Proposes `people/reece-chapman.md` as an artifact. After approval, commits.
- Patches `organizations/f-a-wilhelm-construction.md` and `projects/elanco-c92-2025.md` to add `reece-chapman` to their `related_to` — each as its own artifact, each committed after approval.
- Hook check: notes that C92's body already lists Reece in prose; flags whether prose mentions should be reconciled with `related_to` going forward. Surfaces as a Needs-from-you.

### Example 2: New project, implies a missing client org

**Input:** "Create an entity for the Ridgeworks Maple Street duplex — it's a Ridgeworks deal, no outside client."

**Output:**
- Type: `project`. Slug: `ridgeworks-maple-street`.
- `delivering_org: ridgeworks`. Checks cbrain — `ridgeworks` org doesn't exist yet → surfaces it as a follow-on entity (Needs-from-you: build the Ridgeworks org now, or leave the reference dangling for the orphan-detection cron to flag?).
- `client_org` left blank (self-delivered deal), noted in Open questions.
- Proposes the project artifact; if Charles approves building Ridgeworks too, proposes that as a second artifact.

### Example 3: Request for an unsupported entity type

**Input:** "Add an entity for the C92 weekly meeting — it's a recurring event."

**Output:**
- SCHEMA.md has no `event` type. STOP. Does not invent one.
- Surfaces as Needs-from-you: a new type requires a SCHEMA.md change first. Offers the nearest supported fit (capture the recurring meeting as facts in the body of `projects/elanco-c92-2025.md` instead), and asks which Charles wants.

### Example 4: A relationship surfaces with no fitting predicate

**Input:** "Jared and I went to college together." (while capturing Jared, a new person)

**Output:**
- The relationship is real and stated, but the only registered predicate is `worked_with`, which means *delivered project work* — college friendship doesn't fit it.
- Does NOT bury the relationship in prose only. Proactively proposes a new predicate by name: `went_to_college_with` (symmetric), as a Needs-from-you item, with the first tuple `charles-courtney → went_to_college_with → jared-natalino`.
- On approval: adds the predicate to `PREDICATE_REGISTRY` in `services/lib/extract.ts` (one line, symmetry flag), then declares the tuple in the `relationships` field of both people's entities.
- Keeps `worked_with` clean by giving the personal tie its own predicate rather than stretching the professional one.

## Pitfalls

> Every pitfall must come from a real trace. No fabrications.

No traces yet; pitfalls will populate as the skill runs in production.

## Changelog

- **0.1.0** (2026-05-28) — Initial draft. First cbrain-focused skill in the library. Enforces SCHEMA.md contract for the six entity types; surfaces follow-on entities; patches `related_to` on related entities post-commit; `should-distill` hook at close. Does not write to Project State, does not create new entity types, does not touch watcher-owned email-thread files.
