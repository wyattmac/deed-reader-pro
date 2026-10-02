# Prompts to paste into Cursor

Model for every agent: Grok 4.7, effort high. Use a higher effort for 01-engine.

The app already exists. Do not recreate it. Read `AGENTS.md`, `docs/CONTRACTS.md`, `docs/RECONCILE.md`, and `docs/REQUESTS.md` before editing.

## Worker prompt (one per task)

Replace `<TASK>` with the task id, for example `01-engine`, and `<FILE>` with its phase file.

```
You are the agent for task <TASK>.

Read AGENTS.md, docs/CONTRACTS.md, docs/RECONCILE.md, docs/REQUESTS.md,
and the <TASK> section of docs/tasks/<FILE>.
Build only the remaining bullets in that section, only in the paths it owns.
The existing Flask and React app stays. Do not add pnpm, Next.js, Prisma,
Clerk, Stripe, or a packages/ tree.
Do not edit docs/CONTRACTS.md. If you need a shape change, add a row to
docs/REQUESTS.md, stub locally, and keep going.
Do not rewrite existing routes, parsers, or test_*.py scripts.

Work until every remaining bullet has a pytest or Jest assertion and the
definition of done in AGENTS.md is met. From deed-reader-web/backend run
python lint.py. From deed-reader-web/frontend run npm run lint and
npx tsc --noEmit. Do not stop to ask questions; record them in
docs/REQUESTS.md.

When done: update your row in docs/BOARD.md, open a pull request, and list
anything you left out and why.
```

## Review prompt (after each pull request)

```
Review the pull request for task <TASK> against its section in
docs/tasks/<FILE>, the hard rules in AGENTS.md, and the open rows in
docs/REQUESTS.md. List every remaining bullet that has no pytest or Jest
assertion, every hard rule broken, and any file changed outside the paths
the task owns. Do not fix anything; report only.
```

## Integration prompt (after a phase's pull requests are merged)

```
All Phase <N> tasks that are ready are merged to main. Install with pip and
npm as AGENTS.md describes. Run python lint.py, npm run lint, npx tsc --noEmit,
and the new pytest and Jest tests. Run tests/golden against the deterministic
solver in deed-reader-web/backend/core. Fix integration failures without
changing docs/CONTRACTS.md or existing field names. Then apply each open item
in docs/REQUESTS.md that has an answer, and report the items still open.
```

## Next-phase prompt

```
Phase <N> remaining work is merged and green. You are the agent for the first
task of Phase <N+1> in docs/tasks/phase-<N+1>.md. Read the merged code and
docs/RECONCILE.md. Update docs/CONTRACTS.md only for that phase's additions,
keeping every existing field name. Open a pull request. Change nothing else.
```
