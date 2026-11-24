# Operator mandate — template (0.1.0)

An **Operator** is, in Charles's words: "a broader scale, long duration goal that is achieved by judging how to use varied skills to perform varied tasks over a longer time horizon" (2026-11-23; the definition, CB-759). The goal may be broad. It has no "one subject" limit and no stated time span.

A **mandate** is the essence of one Operator: what it is for, what it may do alone, how we know it is working, and which skills it draws on. How to do any task stays in the skills. One mandate per Operator, at `operators/<slug>/MANDATE.md`. It is not a skill and is never routed to directly: `skills/operator-run/SKILL.md` runs every Operator from its mandate.

## Rules for writing one
- Under 60 lines. Tables, not prose. Sections in the order below, Authority first.
- No names of jobs, clients, people or companies: this repo is public. Say where the live list is read.
- Point at skills; never restate their steps. Point at the stack map's lane row; never copy lane facts.
- The Operator never checks its own goal. Name who does.
- A Bench row's "Use when" is a fact the run can see in the live data, never a mood ("when useful").

## Sections

```
# <Title> — mandate
slug · version · status (draft | active) · owner · updated

## Authority
| May, alone | Only on Charles's ask | Never |

## Goal
One or two sentences. Broad is fine.

## Standing check
What shows the goal is being met, read from live data; and who checks it (never this Operator).

## Scope
What it covers and where the live list and facts are read, each run.

## Bench
| Move | Use when (a fact in the live data) | File | Writes? |

## Starts
Who or what starts a run (Duet on demand or on a cadence; a plain ask in a chat), and the lane row on the stack map.

## Log
Which log it writes (default: cbrain `operator_log`), and anything that must never go in it.

## Report
Where the report goes and its parts.

## Each run reads
The few things a fresh session must read so nothing depends on memory of the last run.

## Run by
`skills/operator-run/SKILL.md`, or the Operator's own skill if it has one.

## Changelog
```

## Changelog
- 0.1.0 (2026-11-24): first version. Design chat on the Operator category; seats ai-system-design, c-stack, data-homes, lanes, oversight, skill-authoring (report CB-754). Charles's decisions CB-753, CB-759, CB-761.
