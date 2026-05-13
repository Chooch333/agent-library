# agent-library

Personal markdown role/skill library for agentic AI infrastructure.

## What this is

A collection of role files, skill definitions, and routing schemas used across the four-layer agentic chassis (Instructions / Reasoning / Tools / Memory). Files here are fetched at runtime via the Custom GitHub MCP and loaded as instructions into Claude sessions.

## Layout

```
agent-library/
├── README.md              # This file
├── AGENT.md               # Routing schema — thin, no domain knowledge
├── CONVENTIONS.md         # Rules for the library (Cheung-style)
├── SKILL_TEMPLATE.md      # Contract template for new skills
├── docs/
│   └── IMPORTS.md         # Notes on imported/cloned material
├── imports/               # Reference imports from other stacks
│   ├── tan-gstack/        # Garry Tan's gstack (cloned for reference)
│   └── tan-gbrain/        # Garry Tan's gbrain schema
└── roles/                 # Charles's own role definitions
    └── (built over time)
```

## Conventions at a glance

- **Schema (`AGENT.md`)** is routing only. No domain knowledge.
- **Skill files** follow the Cheung contract: front-matter + What / When / How / Examples / Pitfalls / Changelog.
- **No SKILL.md over 500 lines.** Spill to `references/` under the skill directory.
- **Pitfalls must come from real traces.** No fabrications.
- **Imports stay in `imports/`** as reference. Reshape into `roles/` when you actually use one.

## Influences

- **Garry Tan** — gstack (specialist worker roles, slash-command pattern), gbrain (entity-memory routing)
- **Andrej Karpathy** — LLM-Wiki (human-curator vs LLM-maintainer split, the Linter)
- **hanyuancheung** — `llm-skill` (Execute/Distill/Guide meta-skills with exclusive write rights, contract template)
- **Patrick Debois** — CDLC (Generate / Test / Distribute / Observe lifecycle, the Context Engineer role)
