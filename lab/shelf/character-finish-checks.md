---
tool: Character finish checks (attached, smooth)
does: "Checks a character's .glb for parts that float (rest pose and every move frame) and stair-stepped edges or colour bands; ~1.5 min; kids-games lab/claude-image-to-3d/heatmap-runs/tools/checks.py"
verdict: shelf
verdict_note: "lab measuring stick only, never a build step; the smooth check false-alarms at limb joints"
come_back_when: "A Character maker character ships with floating parts or jagged edges despite the build rules"
blocks: [7, 16, 17]
brief: ""
report: likeness-heat-map
reviewed: 2026-10-25
draft: false
---
## Verdict history
- 2026-10-25 · Shelf (measuring stick only) · First review (likeness-heat-map); Charles: checks are redundant when the build rules are in up front; run E passed without them, and run D's 11-minute check pass was spent on a false alarm
