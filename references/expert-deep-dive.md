# Expert deep dive (0.1.0, draft)

The procedure a deep-dive helper follows when the desk grows a new expert, and the
deliverable it returns. One procedure for every expert, scoped to the subject:
a field for a captain (A/E delivery, property development, project management), a
technique for a craft (Target Value Delivery, BRRRR underwriting, BD cadence, GitHub
Actions). Only when the subject is software that can be run does the helper add the
tech-review test step and cite what the run showed.

## Inputs
The confirmed reframe note (name, level, under, call_when, seed lens, documents).

## Steps (the Domain Expansion method, compressed)
1. Map the subject: its parts, the practices people use, the roles involved, where it
   touches Charles's own work. Charles's own jobs, projects and records (cbrain,
   Project State, FAW jobs) are read first; the field's standard references second.
2. Vocabulary: the terms a practitioner uses, each in one line, kept as
   `references/vocabulary.md` in the expert's folder if longer than ten lines.
3. Practices: the two to four established ways work in this subject is done, and
   what each is for.
4. Traps: how work in this subject goes wrong, from real cases. Each becomes a Lens
   line with its source. Confirm, cut or add to the seed lens; never keep an
   unsourced line without marking it ~; never keep a figure, keep the pointer.
5. Software subjects only: run it, as tech-review does, and cite the run.
6. Overlap: read every brief on the bench; a line another expert already owns is
   cut here, not after.
7. Write the whole BRIEF.md per `references/expert-brief.md`: call_when (sharpened),
   reads (only documents actually opened and that exist), the lens (10–20 sourced
   lines), the boilerplate procedure and output sections, a changelog line.
8. Commit to `experts/<slug>/BRIEF.md` with `status: draft` and report the commit
   SHA. Nothing is returned as an attachment or as chat text only.
9. If the subject turns out larger than a craft or smaller than a captain, say so and
   stop; the desk re-runs roster-builder.
