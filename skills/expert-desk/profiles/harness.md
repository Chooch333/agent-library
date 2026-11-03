---
name: harness
captains_default: [c-stack, ai-system-design, product-design]
craft_by_mode:
  A: none
  A.1: risks-only, for each craft under a carried captain on the index
  implementation: full
optional_seats:
  premortem: when a fork is low-confidence and expensive to reverse
max_seats: 6
---
**Done means:** it runs in its lane unattended; Charles reacts at stops only; the stack
map is current; nothing is wired on the fly.

**Severity**
- *blocks the goal*: breaks a charter rule, a lane or the two-engine rule; spends
  money; makes Charles hold state or carry text between chats.
- *improves the plan*: reduces what Charles holds; removes a file or a step.
- *noted*: everything else.
