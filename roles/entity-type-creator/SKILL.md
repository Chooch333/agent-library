---
name: entity-type-creator
version: 0.1.0
status: draft
triggers: ["define a new entity type", "new entity type", "add an entity type", "cbrain needs a new type", "add a type to the schema", "create a new KIND of entity", a request to define a new KIND of thing that has no type in SCHEMA.md yet]
dependencies: [cbrain/contracts/SCHEMA.md]
owner: Charles
updated: 2026-06-09
---

# Entity-Type Creator

## What

The Entity-Type Creator is the single-approval path for adding a **new entity TYPE** to cbrain — a new KIND of thing, not a new instance of an existing kind. It runs one guided pass to gather the type's `meaning`, `propose_when` triggers, and `key_fields`, bundles those into the exact `SCHEMA.md` additions (the type-enum entry, the type-specific fields section, and the machine-readable per-type guidance stanza), presents the bundle for Charles's single "approved", and on approval commits the `SCHEMA.md` change.

Because the email watcher reads its entity-type vocabulary AND its per-type guidance from `SCHEMA.md` at runtime (E-185, `email-watcher/lib/reasoning.ts` → `resolveEntityTypes`), that one commit AUTO-DEPLOYS the new type to the watcher with no watcher code change and no separate "teach the watcher" step. **Approving the schema addition IS deploying to the watcher.** This is the whole reason the skill exists: it collapses "define a type" + "teach the watcher" into one act.

This skill writes ONLY to `SCHEMA.md`. It is not a write-authority for entity instances — those go through the chat-capture → Archivist path. It does not touch the watcher, Project State, or any entity file.

## When

**Fire it when:**

- Charles is defining a brand-new KIND of thing that has no `type` in `SCHEMA.md` yet (e.g., the PM family's `pm-directory`/`pm-milestones` were such additions).
- Charles says "define a new entity type", "cbrain needs a type for X", "add a type to the schema", or describes a recurring kind of thing that does not fit any existing type.

**Do NOT fire it when:**

- Charles wants to create a new INSTANCE of an existing type (a new person, org, project). That is the chat-capture → Archivist path (`references/chat-capture.md` → `roles/archivist/SKILL.md`). A new person is not a new type.
- The thing fits an existing type with maybe a new optional FIELD. Adding a field to an existing type is a smaller schema edit, not a new type — do that directly, do not spin up a type.
- Charles is only asking what types exist. Answer from `SCHEMA.md`; do not propose a change.

The dividing test: **is there no `type` value in `SCHEMA.md` that this thing could carry?** If an existing type fits, it is an instance or a field, not a new type.

## How

The SOP. One guided pass, one approval, one commit.

**0. Confirm it is genuinely a new type.** Read the current `type` enum in `SCHEMA.md`. If any existing type fits the thing Charles is describing, stop and say so — steer him to instance-creation (chat-capture) or a field addition instead. Only proceed if no existing type fits.

**1. Gather the three things in ONE pass.** Ask Charles, together, not in a back-and-forth:
   - **meaning** — one line: what this type IS.
   - **propose_when** — one line: when an agent (the watcher's reasoning pass) should propose this type.
   - **key_fields** — the handful of fields that matter most for it (these become the type-specific fields section and the stanza's `key_fields`).
   Offer a recommended draft of all three from what Charles already said, so he can approve or tweak in one reply rather than author from scratch. Also propose the **type name** (slug-style, lowercase-hyphenated, matching the existing naming — e.g. `pm-directory`).

**2. Bundle the three SCHEMA.md additions.** Assemble, as one reviewable block:
   - **Type-enum entry** — add the new type name to the `type` required-field enum row ("One of: ...").
   - **Type-specific fields section** — a `**`type: <name>`**` subsection under "Type-specific optional fields" (or the relevant family section), listing the key fields with one-line descriptions, mirroring how existing types are documented.
   - **Per-type guidance stanza** — the machine-readable block the watcher parses, in the "Per-type guidance (machine-readable)" section:
     ```
     <!-- guidance:<name> -->
     meaning: <one line>
     propose_when: <one line>
     key_fields: <comma-separated>
     <!-- /guidance:<name> -->
     ```
   - A one-line **changelog entry** dated today, describing the new type.

**3. Present for a single approval.** Show Charles the assembled bundle (the exact text that will go into `SCHEMA.md`) and ask for one "approved" — the same gate model as Project State logs and briefs. He approves, tweaks, or declines. Do not commit anything before "approved".

**4. On approval, commit `SCHEMA.md`.** Re-fetch the current `SCHEMA.md` blob SHA immediately before writing (staleness rule — a SHA captured earlier in the session can be stale). Apply the three additions plus the changelog entry. Verify the file after the write (re-read; confirm the enum row, the fields section, and the stanza all landed and the file is intact — no duplicated or truncated content). Prefer a whole-section insert anchored on a unique heading over a regex-heavy find-replace; surgical find-replace with special characters has corrupted this file class before.

**5. Note what auto-deploys, honestly (E-142).** Tell Charles the commit makes the type valid in the watcher on its next run (it reads `SCHEMA.md` fresh each run — no cache, no redeploy). State the honest status: the type is **wired** into the schema and will be **accepted** by the watcher, but it is **not verified** until a real email actually surfaces an entity of the new type and it appears correctly in a draft brief. Do not claim verified.

## Examples

**Worked case — the PM family (the additions that motivated this skill).** On 2026-06-08 Charles added two new KINDS of thing: a project's contact roster and a project's milestone schedule. Neither fit `person`/`organization`/`project`/etc. Run through this skill, that is:

- type names: `pm-directory`, `pm-milestones`
- `pm-milestones` gathered in one pass:
  - meaning: "A project's time-based schedule — dated milestones with status, each carrying the real-world date it was established."
  - propose_when: "An email or steer establishes or moves a dated project milestone."
  - key_fields: `milestones, project_slug, established`
- bundle: enum row gains `pm-milestones`; a `**`type: pm-milestones`**` fields section is added; and the stanza:
  ```
  <!-- guidance:pm-milestones -->
  meaning: A project's time-based schedule of milestones.
  propose_when: An email or steer establishes or moves a dated project milestone.
  key_fields: milestones, project_slug, established
  <!-- /guidance:pm-milestones -->
  ```
- one "approved" → one `SCHEMA.md` commit → the watcher accepts `pm-milestones` on its next run, no code change.

(Historical note: the PM family was actually added by hand before this skill existed; it is the canonical example of the shape this skill produces.)

## Pitfalls

> **`status: draft`.** This skill has not yet been run on a real new-type definition by Charles. Its SOP is verified against the `SCHEMA.md` structure as it stands 2026-06-09 (the type enum, the type-specific fields sections, and the "Per-type guidance (machine-readable)" section all exist and parse). But the live run — Charles defining a genuinely new type through this skill end to end — has not happened, so Pitfalls are seeded, not complete. Flip to `active` after the first real run, adding any pitfalls it surfaces.

- **New type vs new instance is the whole job (seeded).** The most likely misfire is treating a new person/org/project as a new type. A new instance of an existing type is NOT this skill — it is chat-capture → Archivist. Always run step 0 (does an existing type fit?) before gathering anything.

- **New type vs new field (seeded).** If the thing fits an existing type but wants one more optional field, that is a field addition, not a type. Do not create a type to hold a single new field.

- **Keep the three SCHEMA.md surfaces in sync (seeded).** A new type touches three places in `SCHEMA.md`: the enum row, the fields section, and the guidance stanza. Adding the enum name without the stanza means the watcher accepts the type but proposes it without guidance (degraded); adding the stanza without the enum name means the watcher's name-gate rejects it. The bundle in step 2 exists so all three move together in one commit.

- **The commit deploys; verify needs a real email (seeded, E-142).** Because the watcher reads `SCHEMA.md` at runtime, the commit makes the type live with no redeploy — which can read as "done". It is not verified until a real email surfaces the type in a draft brief. Say wired, not verified.

## Changelog

- **v0.1.0 (2026-06-09)** — Initial skill, `status: draft`. Created alongside the schema-driven entity-type work (E-185): the watcher now reads type names + per-type guidance from `SCHEMA.md` at runtime, which is what makes a single schema commit auto-deploy a new type to the watcher. SOP: confirm new-type (not instance/field) → gather meaning/propose_when/key_fields in one pass → bundle the three SCHEMA.md additions (enum entry, fields section, guidance stanza) + changelog → single "approved" gate → commit with SHA re-fetch and post-write verify. Replaces no prior skill (the retired `cbrain-entity-builder`, E-172/E-173, handled instances, not types). Pitfalls seeded from the SCHEMA.md structure; unrun, so `status` stays `draft` until Charles defines a real new type through it.
