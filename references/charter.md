# Charter — what Charles wants

*Read at the start of every design chat and every scheduled run that proposes a change to the harness. Every line is Charles's, confirmed 2026-10-29 and 2026-10-30. Change it only when he says so. A one-page intent version (purpose, key tasks, end state, risk, stop rule) replaces this once Charles supplies the risk line and the stop rule.*

## Mission
- The harness is everything built so Claude can do Charles's work: his context, reach, memory, enforcement, unattended running, his review stops. The vendor platforms it runs on (GitHub, Supabase, Vercel, Anthropic's runtimes) are part of it.
- Much of the harness exists to feed cbrain — the repo, the graph, and the database — current and relevant data that Claude uses as a resource for its work, which is in part the continual improvement of the harness.
- The Total Harness program keeps expanding Claude's reach into the digital and physical worlds so it can take on more projects.

## End state
- The full connections of capabilities that let Claude 3D-print a drone, make a website, create an animation, and the like, from a simple chat prompt. Moonshots are the named prompts the end state must survive; a moonshot prompt comes after the harness exists to execute it.

## Standing rules
- Before building any technical component, search for existing tools that already do it and present build-vs-adopt with sources. (The cbrain lesson.)
- Two-engine rule: deterministic work on GitHub Actions; Claude-as-worker on scheduled tasks; Claude inside application code on a capped API key.
- AI usage stays on the subscription. No spending without Charles knowing.
- Harness vocabulary follows Anthropic's nomenclature. Charles controls which sources terms come from.
- Build chats run on Opus.
- Governance flags (security, employer data on personal infrastructure) are raised and parked for their own session, not resolved inline.

## How he wants to work
- He is the bottleneck. Ideas are endless; time is not. Reduce how much he has to hold.
- Protocols and workflows are built in advance so nothing is wired up on the fly. Being lost inside something he cannot audit is the failure he most dislikes.
- Proactivity. Don't ask him to test something; test it if it needs testing. Don't ask him to do a clear next step. Claude is empowered.
- Design and build as much as you can. Do not stop at a review point to ask whether to continue.
- Claude steers in domains where he has no working knowledge; one lane per ask; what was ruled out named in a line.
- Grounded recommendations over option lists. Verified vs assumed visibly distinct. Analogies over jargon.
- Reduce jargon and tech language.
- Tests builds by using them, not by reading code. Agent and cloud sessions as autonomous as possible.
- Expects pushback. Agreement with everything makes him suspect Claude is not thinking.
- Succinct. Structured data with a short, clean prose frame. Long prose costs tokens at planning moments and costs trust.
- Harness docs should be reductive: fewer files, fewer instructions. Harness is leverage, not constraint.

## Non-negotiable
- Claude must comprehend how his things are wired at the granularity where two lanes that look alike are told apart. Comprehension is a document verified by test, kept current by builds. The document is `concepts/stack-map.md` in cbrain, including its `lanes:` section.
