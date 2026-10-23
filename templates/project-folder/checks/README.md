# checks

Checker verdict files, one per feature per attempt: `<feature-id>-<n>.md`, with `PASS`, `FAIL` or `CAN'T CHECK` on the first line, then what the checker ran, what it saw and, for a FAIL, the gap and a one-line fix hint. Only the checker (agent-library `skills/checker`) writes here; the builder never does. A feature can be `passes: true` only when its newest verdict here is a PASS, and `check_folder.py` refuses the folder otherwise.
