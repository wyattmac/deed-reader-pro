# Start here

The planning kit has been reconciled with the existing Deed Reader Pro app. Read `docs/RECONCILE.md` before starting a phase. The stack, folders, and field names in the app stay. `AGENTS.md` is the working instruction file.

## One-time setup that is still open

1. Answer the blank rows in `docs/REQUESTS.md` before tasks that depend on them (database, auth, billing, AI geometry).
2. Put public-record deeds in `tests/deeds/` if you want reading tests against real scans. `samples/sample_simple_deed.txt` is the synthetic sample already in the repo. Do not commit customer files.
3. For each hand-checked deed, add calls, closure, and area under `tests/golden/`. `tests/golden/engine-fixtures.json` holds synthetic figures and is not executed yet.
4. `deed-reader-web/frontend/public` is gitignored, so Create React App has no committed `index.html`. Task 00 owns that gap.
5. Turn on branch protection for `main` when CI from task 00 exists. There is no GitHub Actions workflow today.

Launch the app with `scripts/RUN_APP.bat` on Windows, or the Linux commands in `AGENTS.md`. Frontend port 3000. Flask port 5000.

## Each phase, in order

1. **Open task.** Start one agent with the worker prompt for the phase's first task (00, then 06 for Phase 2). Review and merge its pull request.
2. **Parallel tasks.** Start one agent per remaining task in that phase. Phase 1 tasks 01 to 05 can run together only after 00 merges. They must stay inside the paths in `AGENTS.md`. Task 05 is blocked on the auth and billing rows in `docs/REQUESTS.md`.
3. **Review.** For each pull request, run the review prompt in a fresh agent, then merge.
4. **Integrate.** Run the integration prompt on `main`.
5. **Gate.** Check the phase gate at the bottom of the phase file. Answer anything new in `docs/REQUESTS.md`.
6. **Next phase.** Run the next-phase prompt.

Prompts are in `docs/prompts.md`. Progress is in `docs/BOARD.md`.

## What still needs a person

- Answering `docs/REQUESTS.md`
- Merging pull requests and checking each phase gate
- An Anthropic API key in `deed-reader-web/backend/.env`
- Accounts and keys for any provider chosen in `docs/REQUESTS.md` (database, billing, map tiles)
- For Phase 2, if the CAD row is answered yes: a Windows machine with AutoCAD or Civil 3D, and an Autodesk developer account
