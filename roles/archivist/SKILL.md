---
name: archivist
version: 0.1.0
status: draft
triggers: [an approved brief conforming to cbrain/contracts/BRIEF_SCHEMA.md, "file this brief", "archive approved brief"]
dependencies: []
owner: Charles
updated: 2026-06-03
---

# Archivist

## What

The Archivist is cbrain's single write-authority: it takes an **approved brief** (a brief whose `status` is `approved`, sealed with a `brief_id`, conforming to `cbrain/contracts/BRIEF_SCHEMA.md`) and files each of its typed intents into cbrain as live entities, field edits, clues, or graph relationships. It reasons about **structure** — where a thing goes and how it is represented — never about **truth**. Truth was Charles's call at the approval gate (E-094); the Archivist does not re-judge, validate, or reject an approved brief. It has no knowledge of which producer drafted the brief (the Watcher or any future agent) and does not branch on it (E-104). Every write it makes records the originating `brief_id`, so provenance is one hop: data → `brief_id` → brief → source artifact (E-096).

## When

**Fire it when:**

- A brief has been approved in chat (`status: approved`, has a `brief_id` and `sealed_at`) and needs its intents written into cbrain.
- Charles says "file this brief" / "archive the approved brief" and points at a sealed brief in `_briefs/`.

**Do NOT fire it when:**

- A brief is still `status: draft` (no `brief_id`). Drafts are reviewed by Charles, not filed. Filing a draft would write unapproved content into cbrain — the exact thing the approval gate prevents.
- You are tempted to "fix" or "improve" the brief's content before filing. The Archivist files what was approved verbatim; a correction is a *new* brief that supersedes (E-096), never an in-place edit by the Archivist.
- An intent looks wrong or references a not-yet-existing entity. That is normal in a half-built cbrain — file it anyway and let orphan-detection sweep danglers (E-094). The Archivist is not a validation gate.

## How

The filing SOP. Read the approved brief's frontmatter, then process each entry in `intents[]` by its `type`. Each rule below is verified against `SCHEMA.md` (entity contract) and `BRIEF_SCHEMA.md` (brief contract).

**0. Pre-flight.** Confirm `status: approved` and a `brief_id` is present. If `status: draft`, STOP — drafts are not filed. Capture the `brief_id`; every write in this brief records it as the back-reference.

**1. `create_entity`** — write a new entity page.
   - Target carries `entity_type`, `slug`, `fields` (sparse OK — best-effort enforcement, E-081), optional `body`.
   - Write to `cbrain/<dir>/<slug>.md` where `<dir>` is the plural of `entity_type` (`person`→`people/`, `organization`→`organizations/`, `project`→`projects/`, `framework`→`frameworks/`, `concept`→`concepts/`, `place`→`places/`).
   - Frontmatter: the five required fields (`slug`, `type`, `created`=today, `updated`=today, `summary`) plus every field in `target.fields`. Add type-specific fields only as supplied; do not invent values for blank fields (SCHEMA.md best-effort).
   - Record the back-reference: add the `brief_id` to a `sources` entry (e.g. `- "brief: BR-2026-06-03-a7f3"`) so provenance is one hop.
   - Body: `# <name>` then `## Summary`; include `## Sources` carrying the same brief reference. Other body sections only if the brief's `target.body` supplied them.
   - If the slug already exists as a live entity, do NOT overwrite. This is a producer-side dedup miss; surface it to Charles rather than clobbering curated content.

**2. `enrich_field`** — set one field on an existing entity.
   - Target carries `entity_type`, `slug`, `field`, `value`.
   - Read `cbrain/<dir>/<slug>.md`. If absent, this is a dangling enrich — surface to Charles (do not create the entity from an enrich intent; that is a `create_entity`'s job).
   - Set the named `field` to `value`, bump `updated` to today. For `org` specifically, `value` must be the slug of an `organizations/` entity (SCHEMA.md person fields).
   - Record the `brief_id` in `sources`.

**3. `flag_clue`** — record a verified-but-unresolved clue, leaving the real field blank.
   - Target carries `entity_type`, `slug`, `clue_field`, `value`.
   - Read the existing entity. Set `clue_field` (e.g. `org_unverified_domain`) to `value`. Leave the real field (e.g. `org`) **blank** — the clue is a queryable worklist signal, not an assertion (SCHEMA.md `org_unverified_domain`; E-089). Do not put the raw value into the real field.
   - Bump `updated`; record the `brief_id` in `sources`.

**4. `propose_relationship`** — declare a graph edge.
   - Target carries `subject`, `predicate`, `object`, optional `register_predicate`.
   - In the **subject** entity's frontmatter, add a `relationships` entry `{ predicate, object }` (subject is always the declaring entity — SCHEMA.md "Declaring relationships"). Bump `updated`.
   - If `register_predicate` is present (`{ name, meaning, symmetric }`), the predicate was approved at the gate: add it to the registry in `services/lib/extract.ts`. If absent and the predicate is unknown, the sync extractor will skip the unknown predicate (SCHEMA.md) — file the declaration anyway; do not guess a registration.
   - Record the `brief_id` in `sources`.

**5. `record_pm_item`** — RESERVED. Not yet specified (`BRIEF_SCHEMA.md`; E-060, E-056). If an approved brief carries this type, do not invent a filing rule — surface it to Charles and stop on that intent. The other intents in the brief still file normally.

**6. Close.** Each filed write carries the `brief_id`. The brief itself is a sealed record in `_briefs/` and is never edited by the Archivist and never indexed as a cbrain entity (BRIEF_SCHEMA.md).

## Examples

**Worked case — a `create_entity` intent (from the Item-1 GATE trace).**
The reshaped watcher drafted a brief from the Elanco C92 "Issued for Construction" thread carrying, among 13 intents, `i1`:

```yaml
- intent_id: i1
  type: create_entity
  confidence: high
  evidence: "Named in forwarded thread \"Fw: Elanco C92 Lab Addition...\" routed to elanco-c92-2025."
  target:
    entity_type: person
    slug: steve-scheller
    fields:
      summary: "Steve Scheller — drafted from email, awaiting review."
      email: "sscheller@m-n-a.com"
```

After Charles approves and the brief is sealed (say `BR-2026-06-03-a7f3`), the Archivist files `i1` as `cbrain/people/steve-scheller.md`:

```markdown
---
slug: steve-scheller
type: person
created: 2026-06-03
updated: 2026-06-03
summary: "Steve Scheller — drafted from email, awaiting review."
email: "sscheller@m-n-a.com"
sources:
  - "brief: BR-2026-06-03-a7f3"
---

# Steve Scheller

## Summary
Steve Scheller — drafted from email, awaiting review.

## Sources
- brief: BR-2026-06-03-a7f3
```

Note: `org` is left blank — the brief did not supply it, and the Archivist never guesses (the m-n-a.com domain is a clue a future `flag_clue`/`enrich_field` intent would carry, not something to assert here).

## Pitfalls

> Every pitfall below references a real trace. The only trace that exists so far is the **Item-1 GATE run** (2026-06-03): the reshaped watcher drafting one brief from the real Elanco C92 specimen. That is a *producer* trace — the Archivist's filing loop has **not yet run on a real approved brief**, so this list is seeded, not complete. New pitfalls get added by Distill after the first real filing run, and `status` moves to `active` then.

- **Sparse `target.fields` is normal, not a defect (Item-1 GATE trace).** Every one of the 13 create_entity intents in the trace carried only `summary` + `email`; `org`, `role`, `aliases` were all blank. The Archivist must file the sparse entity as-is and must not fill blanks by inference (SCHEMA.md best-effort, E-081). Treating blanks as "missing data to resolve" would re-do the producer's reasoning with less context.

- **Duplicate display-name collapses to one slug — file it, surface nothing automatically (Item-1 GATE trace).** The specimen had two distinct "Dave Buckallew" participants (`dave.buckallew@network.elancoah.com` and `DaveBuckallew@freitaginc.com`); harvest collapsed both to one `dave-buckallew` create_entity intent (slug dedup). The Archivist files the one approved intent verbatim — it has no truth-oracle to know these are two people. If they are, that is caught at the human gate or by later enrichment, not by the Archivist. (Logged in the session as a producer-side alias/identity candidate.)

- **Live-entity slugs never reach an approved create_entity intent — but verify before writing anyway (Item-1 GATE trace).** In the trace, 3 of 16 harvested people (`mike-meyers`, `tom-newsom`, `brandon-white`) were dropped by the producer because they were already live entities, so no create_entity intent for them existed to file. The Archivist should still re-check existence at file time (step 1's last bullet): the producer's dedup is a snapshot and an entity could have been created between draft and approval. Do not overwrite a live entity from a create_entity intent.

## Changelog

- **v0.1.0 (2026-06-03)** — Initial skill, `status: draft`. Seven-field contract; filing SOP for the five BRIEF_SCHEMA intent types verified against SCHEMA.md (entity dirs, required fields, `org` slug-ref, `org_unverified_domain` clue semantics, `relationships` declaration format, `record_pm_item` reserved). Every write records the `brief_id` back-reference. Pitfalls seeded from the Item-1 GATE trace (producer-side); the Archivist filing loop is unrun, so `status` stays `draft` and Pitfalls are explicitly incomplete-pending-first-real-filing.
