---
name: wire-new-app
version: 0.1.0
status: draft
triggers:
  - "wire up"
owner: Charles
updated: 2026-10-08
source: Designed in DA chat DA-1007-wire-new-app (2026-10-07); built in Build 28 (BB-2026-10-07-wire-new-app). Key passing runs in Chooch333/cbrain .github/workflows/wire-new-app.yml.
wiring:
  runs: with-you
  starts: "\"wire up <name>\""
  runs_in: claude-chat
  reads: [github, supabase, vercel]
  writes: [github-repo, supabase-project, vercel-project, vercel-env-names]
  origin: yours
  label: Wire New App
---

# Wire New App

## What

Charles says "wire up <name>". Claude creates the app's GitHub repo, its Supabase database and its Vercel project, and moves the keys between them **machine to machine** — a GitHub Action fetches the Supabase keys and writes them into Vercel. No person, and no chat, ever sees or copies a key.

This is a skill, not an agent: Charles starts it, and it stops for his "yes" before spending money.

## Never

- Read, print, paste or ask for a key value — not in chat, not in a doc, not in a sheet. Names only. (A-027)
- Ask Charles to paste a key into chat. If a token is bad, point him at the one place to refresh it (step g).
- Recover an old secret. On a mismatch, make a fresh one. (CB-089)
- Create the Supabase project without Charles's plain "yes" in this chat.
- Touch `sync-secrets.yml`.

## Steps

**a. Repo.** Custom GitHub `create_repo` — owner Chooch333, name `<name>`, **private**. Then commit a minimal Next.js starter with `create_or_update_file` (one file per commit, branch `main`):
- `package.json` — `next`, `react`, `react-dom`, `@supabase/supabase-js`; scripts `dev`/`build`/`start`; `"engines": {"node": "24.x"}`.
- `app/layout.tsx`, `app/page.tsx` — a one-line page with the app's name.
- `app/api/health/route.ts` — does **one real read** with the server-side key, and returns 200 only if it worked:
  ```ts
  import { createClient } from "@supabase/supabase-js";
  export const dynamic = "force-dynamic";
  export async function GET() {
    const sb = createClient(process.env.SUPABASE_URL!, process.env.SUPABASE_SECRET_KEY!, { auth: { persistSession: false } });
    const { error } = await sb.storage.listBuckets();
    return Response.json({ ok: !error }, { status: error ? 500 : 200 });
  }
  ```
  (`listBuckets` needs no table to exist, and only succeeds with a real secret key.)
- `.gitignore` — `node_modules`, `.next`, `.env*`.

**b. Database — real money check.** Ask in plain words: **"New Supabase database, about $10/month — yes?"** Wait for the answer.
- On yes: Supabase MCP `create_project` (if the MCP offers `get_cost`/`confirm_cost`, call them first) in org `jltnoausribdvmjeedlx`, name `<name>`, region `us-east-2`. Poll `get_project` until status `ACTIVE_HEALTHY`.
- If Charles names an existing Supabase project instead, use its ref. No money question.
- On no: stop and say what exists so far (the repo).

**c. Pass the keys.** Custom GitHub `run_workflow`: owner `Chooch333`, repo `cbrain`, workflow_file `wire-new-app.yml`, ref `main`, inputs:
`{ "repo": "Chooch333/<name>", "supabase_ref": "<ref>", "vercel_name": "<name>", "rehearsal": "false" }`.
`rehearsal` defaults to `"true"` (read-only plan); only `"false"` creates anything. If unsure, run a rehearsal first — it creates and changes nothing.

The workflow, in order: checks `SUPABASE_ACCESS_TOKEN`; fetches the keys and masks every value; checks `VERCEL_TOKEN`; creates the Vercel project linked to the repo if missing; writes `SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY` and `SUPABASE_SECRET_KEY` (Sensitive) on production + preview; deploys; calls `/api/health` from inside Actions (CB-286).

**d. Verify — names only.**
- `list_workflow_runs` (workflow_file `wire-new-app.yml`) then `get_workflow_run` — conclusion `success`. Don't trust silence: if no run appears within ~2 min, say so.
- Vercel `filter_project_envs` on `<name>` (team `team_8nMi0Bd6orQHGeTrMZYWCamm`) — the four names are there. Read only the `key` and `target` fields; never decrypt.
- Vercel `list_deployments` for the project — newest production deployment `READY`.
- `get_job_logs` with search `sb_secret_|sb_publishable_|eyJ` — nothing but masked `***`.

**e. Tell Charles**, in plain words:
- What exists now: the repo link, the Supabase project name, the Vercel project name and its address.
- The key **names** and where they live ("4 keys in Vercel → <name> → Settings → Environment Variables: …"). Never a value.
- Keys from other sites (Google, Anthropic, etc.) are his to add in Vercel himself when the app needs them.

**f. First-real-use checklist** (the Build 28 rehearsal could not prove these — it created nothing). On the **first** live run only, check and log a Session Log on Project State `agent-build-out` referencing BB-2026-10-07-wire-new-app:
1. Workflow run green — tokens valid, keys fetched with every value masked.
2. Vercel project created and linked to the repo; four key names present on production + preview; `SUPABASE_SECRET_KEY` marked Sensitive.
3. Health check green from inside Actions (real read with the secret key).
4. The run log has no key value — search for `sb_secret_`, `sb_publishable_`, `eyJ` and find nothing unmasked.
Then complete the next move "First real 'wire up'" (tags `build-28`, `wire-new-app`).

**g. If the run fails on a token**, say which one and where to refresh it — never ask for the value:
- `SUPABASE_ACCESS_TOKEN`: Supabase → Account → Access Tokens → make a new token; then GitHub → Chooch333/cbrain → Settings → Secrets and variables → Actions → `SUPABASE_ACCESS_TOKEN` → Update.
- `VERCEL_TOKEN`: Vercel → Account Settings → Tokens → make a new token for the team; then the same GitHub page → `VERCEL_TOKEN` → Update.
Then re-run step c.

If Vercel refuses to link the repo (Vercel's GitHub app has no access to it): tell Charles to open Vercel → Account Settings → Git → GitHub → Configure, and add `<name>` to the repos it can see. Then re-run step c.

## Open (left open by Charles, 2026-10-07)

Whether key values may ever go in a spreadsheet, and where a long-term labeled list of key names lives. Until he decides: no sheet, and names are reported in chat only.

## Changelog

- **0.1.0** (2026-10-08) — Initial draft. Build 28 (BB-2026-10-07-wire-new-app). Proven by a rehearsal run only; first real use is the final proof (step f).
