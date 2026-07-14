---
name: archivist
version: 0.2.0
status: draft
triggers: [an approved brief conforming to cbrain/contracts/BRIEF_SCHEMA.md, "file this brief", "archive approved brief", a brief sealed by seal_brief (the automated filing trigger)]
dependencies: []
owner: Charles
updated: 2026-07-13
---

# Archivist

## What

The Archivist is cbrain's single write-authority: it takes an **approved brief** (a brief whose `status` is `approved`, sealed with a `brief_id`, conforming to `cbrain/contracts/BRIEF_SCHEMA.md` v0.5.0) and files each of its typed intents into cbrain as live entities, field additions, clues, graph relationships, or workbook nodes and assertions. It reasons about **structure** — where a thing goes and how it is represented — never about **truth**. Truth was Charles's call at the approval gate (E-094); the Archivist does not re-judge, validate, or reject an approved brief. It has no knowledge of which producer drafted the brief (the Watcher, the Reasoner, the gate itself, or any future agent) and does not branch on it (E-104). Every write it makes records the originating `brief_id`, so provenance is one hop: data → `brief_id` → brief → source artifact (E-096).

**The Archivist is additive.** Every filed fact is an *addition*. It appends; it does not overwrite. A correction does not replace the thing it corrects — it is filed **alongside** it, carrying `effect: contradict`, and the wrong claim demotes as contradicting evidence accumulates (E-264). The number falls; the record stays. There are exactly **two sanctioned in-place moves** in the whole skill — flipping a workbook node's `status` (E-250) and clearing a resolved `org_unverified_domain` — and nothing else in cbrain is ever edited in place by the Archivist. This is structural, not a matter of care: the Archivist has no overwrite rule to reach for.

> **Reconciliation with v0.1.0 (read this if you have the old skill in your head).** The v0.1.0 skill said a correction is a new brief *that supersedes* the old one. **That wording is now wrong and is retired.** The supersede model was reversed (E-237/E-264, BRIEF_SCHEMA v0.5.0). "A correction is a new brief" survives; "that supersedes" becomes "whose assertions are filed alongside the old ones." Sealed briefs remain immutable — that never changed. What changed is that the *filed fact* is never overwritten either.

## When

**Fire it when:**

- A brief has been approved (`status: approved`, has a `brief_id` and `sealed_at`) and needs its intents written into cbrain — either because Charles says "file this brief" and points at a sealed brief in `_briefs/`, or because `seal_brief` succeeded and the automated filing trigger invoked this skill against the sealed file. The two paths are the same filing loop; the Archivist does not branch on how it was invoked.
- The brief carries `intents: []`. This is legal and normal (E-177) — an artifact was seen and reasoned about but supports no action. **No-op cleanly**: file nothing, report "no intents", do not error, do not go looking for something to do. An empty brief is a successful filing run with zero writes.

**Do NOT fire it when:**

- A brief is still `status: draft` (no `brief_id`). Drafts are reviewed by Charles, not filed. Filing a draft would write unapproved content into cbrain — the exact thing the approval gate prevents. Also do not file a `status: rejected` brief (`BR-REJECTED-…`); a rejected draft is a record, not a worklist.
- You are tempted to "fix" or "improve" the brief's content before filing. The Archivist files what was approved **verbatim**. If the brief is wrong, the remedy is a *new* brief whose assertions are filed alongside the wrong ones (E-264) — never an in-place edit by the Archivist, and never a quiet touch-up at filing time.
- An intent looks wrong or references a not-yet-existing entity. That is normal in a half-built cbrain — file it anyway and let orphan-detection sweep danglers (E-094). **The Archivist is not a validation gate.** (The narrow exceptions where it *stops* on a single intent are enumerated in §How and are all of the same kind: a structural address it cannot resolve without guessing. It never stops because it doubts a claim.)

## How

The filing SOP. Read the approved brief's frontmatter, then process each entry in `intents[]` by its `type`. `observations` (Register 2) is **never** read as an action — a flag, a `comprehension` read, a `convo_suggestion`, an `implied-pm-item` marker: none of these are filing instructions, and the Archivist files nothing from them (E-162). Each rule below is verified against `SCHEMA.md` (entity + node + workbook + predicate contract) and `BRIEF_SCHEMA.md` v0.5.0 (brief contract). **Where a field name differs between the two, the contract's name wins.**

**0. Pre-flight.**
   - Confirm `status: approved` and a `brief_id` is present. If `status: draft`, **STOP** — drafts are not filed. Capture the `brief_id`; every write in this brief records it as the back-reference.
   - Note the filing date (today). It is the `at`/`created`/`updated` stamp on everything this run writes.
   - **Legacy acceptance (deprecated v0.4.0 briefs).** The intent-level `confidence` enum (`high` | `medium` | `low`) is **deprecated-but-legal** until every producer migrates to `seed`. Read `seed` when present; tolerate `confidence` when it is not. Never reject a brief, never "upgrade" it, never rewrite it. The `implied-pm-item` observation flag is likewise still legal — it is an observation, so it is simply not filed. Do not treat any of this as a defect to fix.
   - **Confidence is never written to cbrain frontmatter (E-254).** Not the deprecated enum, not the seed's computed number. The Archivist stores the *inputs* — the `seed` block and the assertion stream — and the running confidence is recomputed on demand from them, never stored. If you find yourself writing a `confidence:` key into an entity or a node, stop: that is not a field.
   - **Two-pass ordering.** PM intents may reference each other. Before writing anything, note whether any `record_pm_item` carries a `gates[].node_ref` naming an `intent_id` from this same brief. If so, filing is two-pass (see §6). Intent-to-intent refs resolve **in filing order within the brief**.

**1. The additive rule (governs every step below).**
   - Every filed fact is an addition. New assertions **append** — to an entity body's `## What we know` section, or to a workbook node's `assertions` stream — carrying the filing date, the `brief_id`, and the basis.
   - The entity-side append format is one dated bullet under `## What we know`:
     `- 2026-07-13 — org set to `imi` (brief: BR-2026-07-13-4b21; basis: inferred).`
   - A **correction files alongside the fact it corrects**, never over it, and carries `effect: contradict`:
     `- 2026-07-20 — CONTRADICTS 2026-07-13: the org is `abbott`, not `imi` (brief: BR-2026-07-20-9c02; basis: stated; effect: contradict).`
     The original bullet is left exactly as it was. The Archivist does not adjudicate which one is right — it files both and surfaces the conflict to Charles.
   - **Nothing is edited in place except the two sanctioned moves:** (a) flipping a workbook node's `status` between `open` and `closed` (E-250, §7), and (b) clearing a person's `org_unverified_domain` once the org it pointed at is resolved (§3). That is the complete list. There is no third.
   - Bumping `updated:` and stamping `created:` are **file bookkeeping, not assertions** — they are not "edits" in the sense this rule forbids, and they happen on every write.
   - Appending a new entry to a list (a `sources` line, a `relationships` declaration, an `assertions` entry, a `nodes` entry) is an **addition**, not an edit — nothing existing is removed or rewritten. Removing or rewriting an existing list entry is forbidden.

**2. `create_entity`** — write a new entity page.
   - Target carries `entity_type`, `slug`, `fields` (sparse OK — best-effort enforcement, E-081), optional `body`.
   - Write to `cbrain/<dir>/<slug>.md` where `<dir>` is the plural of `entity_type` (`person`→`people/`, `organization`→`organizations/`, `project`→`projects/`, `framework`→`frameworks/`, `concept`→`concepts/`, `place`→`places/`).
   - **The pluralization rule does NOT apply to the `pm-*` types.** PM docs are **project-scoped sub-pages**, not a top-level directory: a `pm-workbook` lives at `projects/<project_slug>/pm/workbook.md`, a `pm-directory` at `projects/<project_slug>/pm/directory.md`, a `pm-milestones` at `projects/<project_slug>/pm/milestones.md` (SCHEMA.md, "PM entity family"). There is no `pm-workbooks/` directory and never will be. Do not pluralize a `pm-*` type into a top-level folder.
   - Frontmatter: the five required fields (`slug`, `type`, `created`=today, `updated`=today, `summary`) plus every field in `target.fields`. Add type-specific fields only as supplied; **do not invent values for blank fields** (SCHEMA.md best-effort, E-081).
   - Record the back-reference: add the `brief_id` to a `sources` entry (e.g. `- "brief: BR-2026-06-03-a7f3"`) so provenance is one hop.
   - Body: `# <name>` then `## Summary`; include `## Sources` carrying the same brief reference. Other body sections only if the brief's `target.body` supplied them.
   - **If the slug already exists as a live entity, do NOT overwrite.** Re-check existence at file time even though the producer deduped — the producer's dedup is a snapshot, and an entity could have been created between draft and approval (WATCHER_CONTRACT §8.2 explicitly relies on this reconciliation). Surface the collision to Charles rather than clobbering curated content. Under the additive rule, the correct handling is: leave the live entity alone, and surface. Never merge, never overwrite, never silently skip.

**3. `enrich_field`** — add one field's value to an existing entity.
   - Target carries `entity_type`, `slug`, `field`, `value`.
   - Read `cbrain/<dir>/<slug>.md`. **If absent, this is a dangling enrich — surface to Charles.** Do not create the entity from an enrich intent; that is a `create_entity`'s job.
   - **If the field is blank**, set it to `value` — writing a value where there was none is an *addition*, not an overwrite. Append the dated assertion line to `## What we know` (§1). Bump `updated`. For `org` specifically, `value` must be the slug of an `organizations/` entity (SCHEMA.md person fields).
   - **If the field already carries a different value, do NOT overwrite it.** This is a correction, and corrections are additive: append the dated `CONTRADICTS` assertion line to `## What we know` carrying `effect: contradict` (§1), leave the frontmatter value as it stands, and **surface the conflict to Charles**. The Archivist has no truth-oracle to pick a winner and will not acquire one by overwriting.
   - **Sanctioned in-place move (b):** if this enrich sets a person's `org` and that person carries an `org_unverified_domain` clue for the domain now resolved, **clear the `org_unverified_domain` field**. The clue was a worklist signal; it has been worked (SCHEMA.md). Note the clearing in the same dated assertion line. This is one of only two in-place edits in the skill.
   - Record the `brief_id` in `sources`.

**4. `flag_clue`** — record a verified-but-unresolved clue, leaving the real field blank.
   - Target carries `entity_type`, `slug`, `clue_field`, `value`.
   - Read the existing entity. Set `clue_field` (e.g. `org_unverified_domain`) to `value`. **Leave the real field (e.g. `org`) blank** — the clue is a queryable worklist signal, not an assertion (SCHEMA.md `org_unverified_domain`; E-089). **Do not put the raw value into the real field.** A blank `org` next to a recorded domain is a deliberate state, not a hole.
   - Append the dated assertion line to `## What we know`. Bump `updated`; record the `brief_id` in `sources`.
   - Re-recording an identical clue value is a no-op.

**5. `propose_relationship`** — declare a graph edge.
   - Target carries `subject`, `predicate`, `object`, optional `object_inferred`, optional `register_predicate`.
   - **In the SUBJECT entity's frontmatter**, add a `relationships` entry `{ predicate, object }`. The subject is always the declaring entity (SCHEMA.md, "Declaring relationships") — the tuple's subject is whichever entity's file carries the declaration, so declaring on the wrong end silently inverts the edge. Bump `updated`.
   - If `register_predicate` is present (`{ name, meaning, symmetric }`), the predicate was approved at the gate: add it to the registry in `services/lib/extract.ts`.
   - **If `register_predicate` is absent and the predicate is unknown, file the declaration anyway and do not guess a registration.** The sync extractor skips unknown predicates rather than guessing (SCHEMA.md) — the declaration sits in git, harmless and visible, until a predicate is registered. Inventing a registration would be the Archivist asserting graph semantics it was not given.
   - `object_inferred: true` is provenance for Charles's review; it is not a filing condition. File the edge.
   - Record the `brief_id` in `sources`.

**6. `record_pm_item`** — create one node on the project's workbook.
   - Target carries `project_slug`, `kind` (`issue` | `task`), `title`, optional `topic`, `duration_days` / optional `buffer_days` (**tasks only**), optional `raci` `{ r?, a?, c?, i? }` (person slugs — Pass 4 already did the anchor-to-entity join, E-255), optional `gates` (a list of `{ direction, node_ref }`), optional `milestone_ref`, and `seed`.
   - **There is no top-level `node_ref`, `assertion`, or `decision` on this intent.** Those belong to `append_pm_assertion` (§7). If you are reaching for one here, you are on the wrong rule.
   - **The workbook file** is `projects/<project_slug>/pm/workbook.md` (SCHEMA.md, "PM entity family"). **If it does not exist, the Archivist scaffolds it** — this is the project's first PM item. Scaffold from the pm-family pattern: the base required fields (`slug`, `type: pm-workbook`, `created`, `updated`, `summary`) plus `project_slug` plus `nodes`. The workbook's own `slug` is `<project_slug>-workbook`, which is what makes the graph node-ref `<project-slug>-workbook#<node_id>` resolve. Add the `brief_id` to `sources`. One workbook per project; it is scaffolded **once**, on the first `record_pm_item`, and appended to forever after.
   - **`node_id` allocation: next-sequential-per-kind, zero-padded to three digits.** Issues use `i-` (`i-001`, `i-002`…), tasks use `t-` (`t-014`…). Scan every node already in the workbook — **including closed ones** — take the highest number for that kind, add one. **Ids are never reused.** Nothing is ever deleted from a workbook, so max+1 is always safe.
   - **The `seed` becomes the node's FIRST `assertions` entry** (SCHEMA.md; BRIEF_SCHEMA.md). Write it as:
     `{ at: <today>, basis: { origin: <seed.basis>, source_brief: <brief_id> }, text: <title>, effect: neutral, effect_rationale: "Establishing assertion — the node's opening claim.", seed: { basis, match_basis, corroboration } }`
     `effect: neutral` on the first entry is deliberate: the trajectory *starts* at the seed, and a non-neutral step on the establishing entry would move the number away from the seed it just set.
   - **Gate-origin seed default.** `seal.ts` stamps the deprecated `confidence` on gate-added intents and never a `seed`. So: **if a gate-origin intent (`basis.origin: gate`, or an intent added at the seal) arrives with no `seed`, default it to `{ basis: gate, match_basis: none, corroboration: none }`** — the `gate` band (0.90). This is a filing-time default, stated here so it is one rule in one place rather than a guess made per-run.
     If a **non**-gate-origin PM intent arrives with no `seed`, **STOP on that intent and surface it.** Defaulting a producer's basis would be the Archivist inventing provenance. The rest of the brief still files.
   - **RACI → node-level `relationships` declarations.** `raci.r` → `{ predicate: raci_r, object: <person-slug> }`, and likewise `raci_a` / `raci_c` / `raci_i` (SCHEMA.md, four predicates, node → person — E-257). **An unstated role is simply an absent edge, never a guessed one.** The sync extracts these declarations into tuples exactly as it does entity-level ones (E-256).
   - **`gates` → node-level `relationships` declarations, on the correct subject.** The registered predicate is **`gated_by`** (directional: *subject waits on object*). There is no `gates` predicate.
     - `direction: gated_by` → the **new node** waits on `node_ref`. Declare on the **new node**: `{ predicate: gated_by, object: <project-slug>-workbook#<node_ref> }`.
     - `direction: gates` → the new node **blocks** `node_ref`, i.e. `node_ref` waits on the new node. Declare on the **referenced node**: append `{ predicate: gated_by, object: <project-slug>-workbook#<new node_id> }` to *that* node's `relationships` list. This is an append to another node's list — an addition, not an edit; nothing existing is removed.
     - Getting the subject wrong silently inverts the critical path and the backward due-date walk (E-248). Check the direction twice.
   - **The two ref forms — translate explicitly.** The **intent-level `node_ref` is a bare `node_id`** (e.g. `i-007`), scoped by the intent's `project_slug`. The **graph address written into a `relationships` declaration is `<project-slug>-workbook#<node_id>`** (e.g. `imi-harding-plant-workbook#i-007`). They are not the same string. The intent never carries the `#` form and the tuples table never carries the bare form. Translate at declaration time.
   - **Two-pass filing.** A `gates[].node_ref` may name an **existing `node_id`** *or* **another `intent_id` in the same brief** (BRIEF_SCHEMA v0.5.0) — one email can create two nodes and the edge between them. Therefore:
     - **Pass A** — walk the `record_pm_item` intents in brief order, create every node, and record the map `intent_id → assigned node_id`. Do not resolve any `gates` edge yet.
     - **Pass B** — walk the `gates` lists and resolve each `node_ref`: if it matches an existing `node_id` in the workbook, use it; if it matches an `intent_id` in this brief, use that intent's newly assigned `node_id` from the Pass-A map; **if it matches neither, STOP on that edge and surface it — never guess a node.**
     - Intent-to-intent refs resolve in **filing order within the brief**.
   - `topic`, `duration_days`, `buffer_days` (tasks only) and `milestone_ref` are written onto the node as supplied. Sparse is fine. **Note:** SCHEMA.md's node shape does not yet enumerate `milestone_ref` among the node fields, though BRIEF_SCHEMA v0.5.0 defines it on the intent. File the value as a node-level `milestone_ref` field — an approved field is never dropped — and surface the contract gap. Do not invent a milestone predicate.
   - Bump the workbook's `updated`; add the `brief_id` to `sources` if not already there. New status is `open` on every newly created node, both kinds.

**7. `append_pm_assertion`** — append a dated assertion to an existing node.
   - Target carries `project_slug`, `node_ref`, `assertion`, `effect`, `effect_rationale`, optional `status_change`, `decision` (**required when closing an Issue**), and `seed`.
   - Read `projects/<project_slug>/pm/workbook.md` and find the node whose `node_id` equals `node_ref` (bare form — see the two ref forms in §6).
   - **Missing workbook, or no node with that `node_id`: STOP on that intent and SURFACE it. Never guess.** Do **not** scaffold a workbook from an `append_pm_assertion`, and do **not** create the node — a workbook is scaffolded only by a `record_pm_item` (§6), and a node exists only because a `record_pm_item` made it. An assertion with nowhere to land is a producer bug, not a hole to fill. The rest of the brief still files.
   - **Append** to that node's `assertions` list (never rewrite an existing entry):
     `{ at: <today>, basis: { origin: <seed.basis>, source_brief: <brief_id> }, text: <target.assertion>, effect: <target.effect>, effect_rationale: <target.effect_rationale>, seed: { basis, match_basis, corroboration } }`
     Note the field translation: the intent's **`assertion`** becomes the stored entry's **`text`**. Carry the intent's `seed` onto its own entry as provenance (BRIEF_SCHEMA v0.5.0). Only the **first** entry's seed is the trajectory's starting point (SCHEMA.md); later entries move the number by their `effect` step alone (reinforce +0.05 / weaken −0.05 / contradict −0.10 / neutral 0). Both facts are true at once — the later seed is recorded, not re-applied.
   - **`status_change` — the sanctioned in-place move (a).** `close` sets `status: closed`; `reopen` sets `status: open`. **This is flipped in place** (E-250) — it is one of only two in-place edits in the skill. The node does not move, its id does not change, and its edges stay intact. Both kinds share the `open`/`closed` vocabulary (a Task's `closed` means the work is done; a view may label it "complete" — the stored value stays `closed`).
   - **Closing an Issue requires the `decision`.** Write `target.decision` into the node's `decision` field. **If a `status_change: close` targets an `issue` and `decision` is absent: file the assertion append (it is additive and always safe), do NOT flip the status, and surface.** A closed Issue with no decision violates the node contract, and the Archivist will not author a decision Charles did not make.
   - **On `reopen`, leave any existing `decision` in place.** E-250 is explicit that nothing is deleted; the reopening assertion (typically `effect: contradict`) is the record that the decision is back in play. (SCHEMA.md's node shape reads `decision` as present-once-closed; the additive model forbids deleting it. Filed as-is; contract gap surfaced.)
   - The `effect` and `effect_rationale` are filed **verbatim**. The Archivist does not re-classify an effect or re-judge whether a claim really contradicts. That was the producer's classification and Charles's gate.
   - Bump the workbook's `updated`; add the `brief_id` to `sources`.

**8. Fingerprint write-back (E-234).** After the intents are filed, stamp each filed outcome back onto the **source email's thread-fingerprint record**.
   - **What to stamp:** for each filed outcome, its **cbrain id** — an entity slug (`steve-scheller`) or a node's graph address (`imi-harding-plant-workbook#i-001`) — plus a **thin label** (the entity's display name, or the node's `title`), plus the `brief_id` and the `intent_id` that produced it. Thin: an id and a label, not a copy of the content. The entity and the node stay the single source of truth; nothing is duplicated into the fingerprint that could drift.
   - **Where:** the thread-fingerprint record for the thread named by the brief's `source` block (for `source.kind: email`, `source.ref` is the Message-ID). If `source.kind` is not `email`, there is no fingerprint to stamp — skip, and that is not an error.
   - **It NEVER touches `frame.json`.** The frame is immutable (E-228). The write-back stamps the **thread-fingerprint record only**. Do not re-parse, re-write, or "top up" the email-record file either.
   - **Best-effort.** A failed write-back is **LOGGED** (and named in the filing report) and **never blocks, reverses, or retries the filing**. The filing already happened and is correct; the write-back is a convenience index onto the source. A filing run whose write-back failed is a *successful filing with a logged write-back failure* — never a failed filing.
   - It never writes back into the sealed brief. `_briefs/` is not indexed and briefs are never edited by the Archivist (see §9).

**9. Close.** Each filed write carries the `brief_id`. The brief itself is a **sealed record** in `_briefs/` — never edited by the Archivist, never indexed as a cbrain entity (BRIEF_SCHEMA.md). Report what was filed, what was skipped, every intent that was stopped-and-surfaced, and any logged write-back failure. Nothing is silent. (When the skill runs under the automated filing trigger, a filing failure additionally surfaces as a `FILING-ERROR-<brief_id>.md` sidecar in `_briefs/`, written by the trigger — a separate file alongside the sealed brief, never a modification of it.)

## Examples

**Worked case 1 — a `create_entity` intent (from the Item-1 GATE trace).**
The reshaped watcher drafted a brief from the Elanco C92 "Issued for Construction" thread carrying, among 13 intents, `i1`:

```yaml
- intent_id: i1
  type: create_entity
  confidence: high          # deprecated-but-legal (v0.4.0 producer); tolerate, never rewrite
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

Note: `org` is left blank — the brief did not supply it, and the Archivist never guesses (the m-n-a.com domain is a clue a future `flag_clue`/`enrich_field` intent would carry, not something to assert here). Note also that the deprecated `high` confidence was **read and ignored**: it is provenance on the brief and is never written into cbrain frontmatter (E-254).

**Worked case 2 — two `record_pm_item` intents scaffolding a project's first workbook.**
The project `imi-harding-plant` has no `pm/` docs yet. A sealed brief (`BR-2026-07-13-4b21`) carries two PM intents — one Reasoner-authored Issue, and one Task that Charles added at the gate, gated by the Issue *by `intent_id`*:

```yaml
- intent_id: i7
  type: record_pm_item
  evidence: "Elevation question raised verbatim in the newest message."
  basis: { origin: harvested, confidence: high, rationale: "Stated as a question in the body." }
  seed: { basis: stated, match_basis: semantic, corroboration: single-method }
  target:
    project_slug: imi-harding-plant
    kind: issue
    title: "What is the final slab elevation at the north bay?"
    topic: structural
    raci:
      a: mike-meyers
      c: steve-scheller

- intent_id: i8
  type: record_pm_item
  evidence: "Added by Charles at the gate."
  basis: { origin: gate, confidence: high, rationale: "Gate-directed." }
  # no seed — seal.ts does not stamp one; the filer defaults gate-origin (§6)
  target:
    project_slug: imi-harding-plant
    kind: task
    title: "Re-run the slab-on-grade design for the north bay"
    topic: structural
    duration_days: 5
    buffer_days: 2
    raci:
      r: steve-scheller
      a: mike-meyers
    gates:
      - direction: gated_by
        node_ref: i7          # an intent_id in THIS brief — resolved in pass B
```

Pass A creates both nodes: `i7 → i-001`, `i8 → t-001`. Pass B resolves `i8`'s `gates[0].node_ref: i7` through the Pass-A map to `i-001`, and — because the direction is `gated_by` (the new node waits) — declares `gated_by` **on the new task**, addressed in graph form. The Archivist scaffolds `projects/imi-harding-plant/pm/workbook.md`:

```markdown
---
slug: imi-harding-plant-workbook
type: pm-workbook
created: 2026-07-13
updated: 2026-07-13
summary: "PM workbook for imi-harding-plant — every Issue and Task, their status, the gating graph, and RACI."
project_slug: imi-harding-plant
sources:
  - "brief: BR-2026-07-13-4b21"
nodes:
  - node_id: i-001
    kind: issue
    title: "What is the final slab elevation at the north bay?"
    topic: structural
    status: open
    relationships:
      - predicate: raci_a
        object: mike-meyers
      - predicate: raci_c
        object: steve-scheller
    assertions:
      - at: 2026-07-13
        basis:
          origin: stated
          source_brief: BR-2026-07-13-4b21
        text: "What is the final slab elevation at the north bay?"
        effect: neutral
        effect_rationale: "Establishing assertion — the node's opening claim."
        seed:
          basis: stated
          match_basis: semantic
          corroboration: single-method

  - node_id: t-001
    kind: task
    title: "Re-run the slab-on-grade design for the north bay"
    topic: structural
    status: open
    duration_days: 5
    buffer_days: 2
    relationships:
      - predicate: gated_by
        object: imi-harding-plant-workbook#i-001
      - predicate: raci_r
        object: steve-scheller
      - predicate: raci_a
        object: mike-meyers
    assertions:
      - at: 2026-07-13
        basis:
          origin: gate
          source_brief: BR-2026-07-13-4b21
        text: "Re-run the slab-on-grade design for the north bay"
        effect: neutral
        effect_rationale: "Establishing assertion — the node's opening claim."
        seed:
          basis: gate
          match_basis: none
          corroboration: none
---

# imi-harding-plant — PM Workbook

## Summary
The project's single living record of trackable work: every Issue and Task, their status, the gating graph between them, and RACI accountability. Nodes are created and revised only through `record_pm_item` / `append_pm_assertion` brief intents.

## Sources
- brief: BR-2026-07-13-4b21
```

Read the four things that make this correct: the RACI roles Charles did *not* state (`i`, and `c` on the task) are **absent edges, not guessed ones**; `t-001`'s `gated_by` is declared **on the task** (the waiting node) and carries the **`#` graph address**, while the intent carried the **bare `i7`**; `i8` arrived with **no seed** and was defaulted to the gate seed by §6, while `i7`'s producer seed was copied verbatim; and **no confidence number appears anywhere in the file** — the seed and the stream are stored, the number is recomputed (E-254).

**Worked case 3 — closing that Issue with an `append_pm_assertion`.**
Two weeks later a sealed brief (`BR-2026-07-27-c8e0`) carries:

```yaml
- intent_id: i2
  type: append_pm_assertion
  seed: { basis: stated, match_basis: exact-id, corroboration: single-method }
  target:
    project_slug: imi-harding-plant
    node_ref: i-001                     # bare node_id, scoped by project_slug
    assertion: "Elevation set at 812.50 in the 7/25 coordination meeting."
    effect: reinforce
    effect_rationale: "Answers the node's open question directly, from the meeting record."
    status_change: close
    decision: "Final slab elevation at the north bay is 812.50."
```

The Archivist appends to `i-001`'s `assertions` (the establishing entry is untouched), flips `status: open` → `closed` **in place** (the sanctioned move), and writes the `decision` field:

```yaml
  - node_id: i-001
    kind: issue
    title: "What is the final slab elevation at the north bay?"
    topic: structural
    status: closed
    decision: "Final slab elevation at the north bay is 812.50."
    relationships:
      - predicate: raci_a
        object: mike-meyers
      - predicate: raci_c
        object: steve-scheller
    assertions:
      - at: 2026-07-13
        # ... the establishing entry, unchanged, seed intact ...
      - at: 2026-07-27
        basis:
          origin: stated
          source_brief: BR-2026-07-27-c8e0
        text: "Elevation set at 812.50 in the 7/25 coordination meeting."
        effect: reinforce
        effect_rationale: "Answers the node's open question directly, from the meeting record."
        seed:
          basis: stated
          match_basis: exact-id
          corroboration: single-method
```

`t-001` is untouched — its `gated_by` edge to `i-001` stays exactly as it was. The gate did not open by moving the edge; it opened because the node it points at is now `closed`. **Nodes never relocate and edges never move** (E-250). Had the brief carried `status_change: close` on this Issue with **no `decision`**, the Archivist would have appended the assertion, left `status: open`, and surfaced.

## Pitfalls

> Every pitfall below references a real trace. The traces that exist so far are the **Item-1 GATE run** (2026-06-03, a *producer* trace) and the contract builds. The Archivist's filing loop has **not yet run on a real approved brief** — the live end-to-end filing run (including the PM intents) is the verification step of BB-2026-07-01-archivist-rewrite. So this list is **seeded, not complete**, and `status` stays `draft`. New pitfalls get added by Distill after the first real filing run, and `status` moves to `active` then.

- **"Supersede" is dead. If your instinct says "replace the old value," it is v0.1.0 talking.** The single largest behavioral change in this version: a correction is filed **alongside** the fact it corrects with `effect: contradict`, and the wrong claim demotes by trajectory (E-264/E-237). An `enrich_field` landing on a populated field does **not** overwrite it. The only in-place moves are the node `status` flip and clearing a resolved `org_unverified_domain`. If you are about to edit anything else in place, you are about to destroy the audit trail the whole system is built on.

- **The two ref forms are not interchangeable.** The intent says `node_ref: i-001`. The graph declaration says `object: imi-harding-plant-workbook#i-001`. Writing the bare id into a `relationships` declaration produces a tuple pointing at nothing; writing the `#` form back into an intent-shaped field is meaningless. Translate at the boundary, every time.

- **`gates` direction decides which node's file you write to.** `gated_by` declares on the **new** node; `gates` declares on the **referenced** node. There is no `gates` predicate in the registry — both directions are stored as `gated_by`, and only the choice of subject encodes which way the dependency runs. Get it backwards and the critical path and the backward due-date walk (E-248) silently invert, with a perfectly valid-looking file to show for it.

- **A `gates.node_ref` naming an `intent_id` only resolves if you filed in two passes.** Node ids do not exist until Pass A assigns them. Resolving edges as you go means the first intent's edge points at an intent that has no node yet — and the tempting fix ("just guess the next id") is exactly the guess this skill forbids. Create every node first; resolve every edge second.

- **Sparse `target.fields` is normal, not a defect (Item-1 GATE trace).** Every one of the 13 create_entity intents in the trace carried only `summary` + `email`; `org`, `role`, `aliases` were all blank. File the sparse entity as-is; do not fill blanks by inference (SCHEMA.md best-effort, E-081). Treating blanks as "missing data to resolve" re-does the producer's reasoning with less context. The same rule holds for a PM node: an unstated RACI role is an absent edge, never a guessed one.

- **Duplicate display-name collapses to one slug — file it, surface nothing automatically (Item-1 GATE trace).** The specimen had two distinct "Dave Buckallew" participants (`dave.buckallew@network.elancoah.com` and `DaveBuckallew@freitaginc.com`); harvest collapsed both to one `dave-buckallew` create_entity intent (slug dedup). The Archivist files the one approved intent verbatim — it has no truth-oracle to know these are two people. If they are, that is caught at the human gate or by later enrichment, not by the Archivist.

- **Live-entity slugs never reach an approved create_entity intent — but verify before writing anyway (Item-1 GATE trace).** In the trace, 3 of 16 harvested people (`mike-meyers`, `tom-newsom`, `brandon-white`) were dropped by the producer because they were already live entities, so no create_entity intent for them existed to file. The Archivist should still re-check existence at file time (§2's last bullet): the producer's dedup is a snapshot, and an entity could have been created between draft and approval. **Do not overwrite a live entity from a create_entity intent** — WATCHER_CONTRACT §8.2 retired the watcher's cross-brief suppression *because* it relies on the Archivist surfacing this collision instead.

- **The pluralization rule does not reach the PM types.** `person` → `people/` is right. `pm-workbook` → `pm-workbooks/` is **wrong** — there is no such directory. PM docs are project-scoped sub-pages under `projects/<slug>/pm/`. This is the one place where the "plural of `entity_type`" habit produces a real, wrong file in a real, wrong place.

- **The write-back is a convenience, and it never gets to be a blocker.** A failed fingerprint stamp is logged and the filing stands. Rolling back a filed entity because an index write failed would invert the whole point of the write-back — and it must never touch `frame.json`, which is immutable (E-228). The frame is the parse; the fingerprint is the index onto it.

- **An empty brief is a success, not a problem.** `intents: []` is legal (E-177) — the brief is the record that an artifact was seen. Do not error, and do not go hunting through `observations` for something to file. Observations are never actions (E-162).

- **A deprecated brief is not a broken brief.** A v0.4.0 producer still emits `confidence: high|medium|low` and still emits the `implied-pm-item` flag. Both are legal until the producers migrate. File it unchanged. "Fixing" a legacy brief at filing time is an edit to approved content — the one thing the Archivist structurally must not do.

## Changelog

- **v0.2.0 (2026-07-13)** — The additive rewrite (BB-2026-07-01-archivist-rewrite), against BRIEF_SCHEMA v0.5.0 and the 2026-07-07 SCHEMA.md. `status` stays `draft` — it flips to `active` only after the live filing run verifies. **(1) Additive filing replaces supersede.** Every filed fact is an addition; new assertions append to entity bodies (`## What we know`, dated, with `brief_id` + basis) or to a node's `assertions` stream; a correction files **alongside** the fact it corrects carrying `effect: contradict`, and the wrong claim demotes by trajectory rather than being overwritten (E-264/E-237). v0.1.0's "a correction supersedes" wording is **explicitly retired**, not silently dropped. Exactly **two sanctioned in-place moves** exist: flipping a workbook node's `status` (E-250) and clearing a resolved `org_unverified_domain`. `enrich_field` onto a populated field no longer overwrites — it files a contradicting assertion and surfaces. **(2) The two PM intents are specified** (`record_pm_item` was RESERVED in v0.1.0): `record_pm_item` appends a node to `projects/<slug>/pm/workbook.md`, scaffolding the workbook from the pm-family pattern on the project's first item, assigning `node_id` next-sequential-per-kind zero-padded to three digits (`i-001`/`t-014`, never reused), writing RACI and `gates` as node-level `relationships` declarations (four RACI predicates, and `gates` stored as the directional `gated_by` on the correct subject — E-247/E-257), stamping the `brief_id`, and recording the `seed` as the node's **first** `assertions` entry with `effect: neutral`. `append_pm_assertion` appends a dated entry (the intent's `assertion` becomes the stored `text`), applies `status_change` by flipping `status` in place, and records the `decision` on an Issue close (required — a close without one files the assertion, leaves the status open, and surfaces). Documented the **two ref forms** (intent-level bare `node_id` scoped by `project_slug` vs the graph address `<project-slug>-workbook#<node_id>`) and **two-pass filing** (create all nodes, then resolve intra-brief `intent_id` refs in filing order). Missing node ref = stop and surface, never guess. **(3) Fingerprint write-back (E-234)** added as a filing step: each filed outcome's cbrain id + thin label is stamped back onto the source email's thread-fingerprint record; best-effort, a failure is logged and never blocks filing; it never touches `frame.json` (E-228). **(4) Legacy acceptance:** deprecated v0.4.0 briefs file unchanged — the intent-level `confidence` enum and the `implied-pm-item` flag are deprecated-but-legal; read `seed` when present, tolerate `confidence` when not, never "fix" either. **(5) Gate-origin seed default:** `seal.ts` stamps `confidence` and never a `seed`, so the filer defaults a missing seed on a gate-origin intent to `{ basis: gate, match_basis: none, corroboration: none }`; a non-gate PM intent with no seed stops and surfaces. **(6) Confidence is never written to cbrain frontmatter** (E-254) — the seed and the stream are stored, the running number is recomputed. **(7) `intents: []` no-ops cleanly** rather than erroring (E-177). **(8) Fixed the pluralization rule for the PM types:** `<dir>` = plural of `entity_type` holds for the six entity types and **not** for `pm-*`, which are project-scoped sub-pages at `projects/<slug>/pm/`. All v0.1.0 rules carried forward unchanged: pre-flight stop-on-draft; existence re-check on `create_entity` with create-on-existing-slug surfacing rather than overwriting; dangling `enrich_field` surfaces; `flag_clue` leaves the real field blank; `propose_relationship` declares on the SUBJECT entity and files an unknown predicate without guessing a registration; the entity-directory map; the `sources:` back-reference format; files verbatim and never re-judges truth; not a validation gate; no producer branching (E-104); sparse fields normal (E-081); duplicate-display-name collapse; the seven-field skill frontmatter contract; briefs never edited, never indexed. Added the PM worked example (scaffolded workbook, seed-as-first-assertion, RACI + `gates` declarations) and the Issue-close example; Pitfalls extended.
- **v0.1.0 (2026-06-03)** — Initial skill, `status: draft`. Seven-field contract; filing SOP for the five BRIEF_SCHEMA intent types verified against SCHEMA.md (entity dirs, required fields, `org` slug-ref, `org_unverified_domain` clue semantics, `relationships` declaration format, `record_pm_item` reserved). Every write records the `brief_id` back-reference. Pitfalls seeded from the Item-1 GATE trace (producer-side); the Archivist filing loop is unrun, so `status` stays `draft` and Pitfalls are explicitly incomplete-pending-first-real-filing.
