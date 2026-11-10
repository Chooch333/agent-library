# Expert deep dive (0.3.2, draft)

The procedure the roster-builder follows, seated as a research helper, when the desk
grows a new expert, and the deliverable it returns. One procedure for every expert,
scoped to the subject: a field for a captain (A/E delivery, property development,
project management), a technique for a craft (Target Value Delivery, BRRRR
underwriting, BD cadence, GitHub Actions). Only when the subject is software that can
be run does the helper add the tech-review test step and cite what the run showed.

The helper writes nothing. It returns text; the desk files it; `skills/team-builder`
writes the files.

## Inputs
The confirmed proposal note (name, level, under, call_when, seed lens, documents,
deep-dive scope) and, for a craft, the captain's brief.

## Steps (the Domain Expansion method, compressed)
1. Map the subject: its parts, the practices people use, the roles involved, where it
   touches Charles's own work. Charles's own jobs, projects and records (cbrain,
   Project State, FAW jobs) are read first; the field's standard references second.
2. Vocabulary: the terms a practitioner uses, each in one line; if longer than ten
   lines, return it as a second file text for `experts/<slug>/references/vocabulary.md`.
3. Practices: the two to four established ways work in this subject is done, and
   what each is for.
3a. Our way: Charles's record first, before the field. Read `references/charter.md`;
   search Project State across all projects (`search_state`, decisions and lessons,
   using the subject's terms, several queries); read the build briefs and cbrain
   notes those results point to. For each job that keeps coming up in this corner,
   write one Our way line per `references/expert-brief.md`: how we do it, what was
   dropped and why, with the decision, lesson, build or charter line as its source.
   Where two records disagree, the newer wins and the older is named as dropped. Only
   where his record is silent may a field default stand. Every line's bracket starts
   with its origin mark, `Charles ·`, `Claude ·` or `field ·` (expert-brief 0.5.0).
   A craft with fewer than five Our way lines after this step says so and lists the
   jobs it found no record for. No client, job or employer specifics (the repo is
   public); point to the record instead.
4. Traps: how work in this subject goes wrong, from real cases. Each becomes a Lens
   line with its source. Confirm, cut or add to the seed lens; never keep an
   unsourced line without marking it ~; never keep a figure, keep the pointer.
5. Software subjects only: run it, as tech-review does, and cite the run.
6. Overlap: read every brief on the bench. A line another expert already owns is cut
   here. A line the captain owns that belongs at the craft's altitude moves down: it
   leaves the captain's brief and joins this one, and that move is listed under the
   captain's revisions.
7. Write the whole BRIEF.md per `references/expert-brief.md`: call_when (sharpened),
   reads (only documents actually opened and that exist), Our way (from step 3a), the
   lens (at least 10 sourced lines, most important first; no upper limit, so never merge or cut a sourced line for length), the boilerplate procedure and output sections, a changelog line.
8. Write the captain's revisions: the lens lines that move (quoted), any change to the
   captain's call_when, and nothing else.
9. Return both as text in the roster-builder's Research shape: `### BRIEF`, then
   `### Captain revisions`, then `**Read:**`. Nothing is committed, filed or attached
   by the helper.
10. If the subject turns out larger than a craft or smaller than a captain, say so and
    stop; the desk re-runs the proposal at the new level.
