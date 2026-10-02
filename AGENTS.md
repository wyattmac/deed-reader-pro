# Agent instructions

Deed Reader Pro reads a deed, extracts bearings and distances, and draws the boundary. Customers are land surveyors. The app in this repository is already running. Adapt new work to it.

Read this file, `docs/CONTRACTS.md`, `docs/RECONCILE.md`, and the task section you were assigned before writing code. Also follow the rules that were already here:

- `.cursorrules` — stack, domain language, upload limits, error handling
- `.cursor/rules/deedreadrule.mdc` — how to start the app, ports, health check
- `config/CLAUDE.md` — command cheat sheet and architecture map

If those files and this file disagree about the stack, the existing app wins. The disagreement is recorded in `docs/RECONCILE.md`.

## Stack (the one in the repo)

- Frontend: `deed-reader-web/frontend`. React 18, TypeScript strict, Create React App (`react-scripts`), Tailwind, React Router 6, TanStack Query, Axios. Package manager: **npm**.
- Backend: `deed-reader-web/backend`. Flask `app.py` is the server `scripts/RUN_APP.bat` starts, port **5000**. FastAPI `main.py` is a migration in progress (documents and analysis only). Python 3.11+ with type hints. Package manager: **pip** and `requirements.txt`.
- AI: Anthropic Claude through `deed-reader-web/backend/services/claude_service.py`. Key: `ANTHROPIC_API_KEY` in `deed-reader-web/backend/.env`.
- Database: none in the running app. Do not add Prisma. SQLAlchemy, Alembic, and asyncpg are already declared and unused. Persistence is an open question in `docs/REQUESTS.md`.
- Files: local `uploads/`.
- Tests: pytest (backend) and Jest via `npm test` (frontend). There are no assertion tests yet. Do not switch the repo to Vitest, Playwright, or pnpm.
- Lint: `python lint.py` in the backend; `npm run lint` in the frontend. Pre-commit config: `config/.pre-commit-config.yaml`.

Do not introduce Next.js, a pnpm workspace, `packages/`, `apps/web`, Clerk, Stripe, pg-boss, or MapLibre unless a row in `docs/REQUESTS.md` is answered that way.

## Layout and ownership

| Path | What it is | Who edits it |
| --- | --- | --- |
| `docs/CONTRACTS.md` | Shared shapes | 00-foundation, then 06-contracts-update |
| `deed-reader-web/frontend/src/types/`, `src/services/api.ts` | TypeScript shapes already in use | 00 may add optional fields. 03 owns UI |
| `deed-reader-web/backend/core/` | Deterministic parsing and future survey math | 01-engine |
| `deed-reader-web/backend/services/claude_service.py`, `services/ocr_service.py`, `routes/document_routes.py`, `routers/documents.py` | Reading and upload | 02-reading |
| `deed-reader-web/frontend/src/` | UI | 03-web |
| Export builders in `services/plotting_service.py` (`_generate_dxf_data`, `_generate_csv_data`, `_generate_esri_traverse`, `_generate_autocad_script`, `_generate_kml_data`) and `routes/plotting_routes.py` export routes, `frontend/src/components/Plot/ExportMenu.tsx` | Exports | 04-exports |
| `services/plotting_service.py` coordinate and closure methods | Existing plot path. It calls Claude. Leave it alone until the AI-geometry question is answered | Nobody, until `docs/REQUESTS.md` says otherwise |
| Accounts | Not built | 05-accounts, after the auth question is answered |
| `plugins/` | Not built | Phase 2 and 3 CAD tasks |

Work only inside the paths your task owns. If you need a change elsewhere, write `docs/REQUESTS.md` and stub locally. Do not delete, rename, or rewrite existing parsers, routes, or tests to match the old kit layout.

`plotting_service.py` is shared by history. Task 01 adds new math under `backend/core/` and does not edit the export methods. Task 04 edits the export methods and does not change `_calculate_coordinates`.

## Hard rules

1. **No new AI in the math.** Bearings, distances, unit conversion, curves, closure, area, and coordinates added from now on are computed only in `deed-reader-web/backend/core/` by deterministic code. An AI call must not return a number that new code uses as geometry. The current plot path does this (`bearing_decimal` in `plotting_service.py`). That is a known break, recorded in `docs/RECONCILE.md` and `docs/REQUESTS.md`. Do not copy it.
2. **Store the model's raw output unmodified** before parsing, with `analysis_metadata.model_used` and `promptVersion`, when you add persistence or a new analysis response field. Those fields are listed in `docs/CONTRACTS.md`.
3. **New calls carry `source`:** page, bounding box, and character range, as specified in `docs/CONTRACTS.md`.
4. **Do not overwrite user edits.** When editing exists, reprocessing creates a new `DeedVersion`. There is no editor yet.
5. **Contracts stay frozen** after task 00 except for task 06. Request changes in `docs/REQUESTS.md`. Do not rename existing fields.
6. **Provider SDKs stay behind `ClaudeService`.** New files do not import `anthropic` or `openai`. Keys come from the environment. Existing OpenAI imports in `ocr_fallback_service.py` and the deed filters are legacy; do not add another one.
7. **Firm scoping is not implemented.** Do not pretend existing routes are tenant-safe. New persisted queries, once accounts exist, take a firm id. Until `docs/REQUESTS.md` answers auth, do not invent a tenancy scheme on the current public API.
8. **New geometry uses decimal degrees of azimuth from north, clockwise.** Store the deed's distance and unit string on the call. Convert at the edge of the solver, not inside a regex extractor. The existing `_convert_to_feet` path stays until a task replaces it with tests.
9. **No secrets, customer deeds, or real personal data in the repo.** Fixtures are synthetic or public record. `tests/golden/` and `samples/sample_simple_deed.txt` are synthetic.

## How to run

Windows, preferred by the existing rules:

```bat
scripts\RUN_APP.bat
```

Linux or macOS:

```bash
cd deed-reader-web/backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python app.py
```

```bash
cd deed-reader-web/frontend
npm install
npm start
```

- Frontend: http://localhost:3000
- Flask API: http://localhost:5000
- Health: `curl http://localhost:5000/api/health` (`services.claude` is `healthy` when the key works)
- FastAPI, only when you are touching the migration: `uvicorn main:app --port 8000` from `deed-reader-web/backend`, or `python run_migration.py`

Do not change these ports.

## Definition of done

- Backend: `python lint.py` from `deed-reader-web/backend`
- Frontend: `npm run lint` and `npx tsc --noEmit` from `deed-reader-web/frontend`
- Every acceptance bullet you still own has a pytest or Jest test that asserts it
- Golden fixtures in `tests/golden/` that apply to the task pass against the deterministic solver in `backend/core/`. They are not wired yet. Do not mark them passing because Claude returned a similar number
- `docs/BOARD.md` row for the task is updated
- A pull request describes what was built and what was left out

`deed-reader-web/backend/test_*.py` are manual HTTP scripts. They are not the acceptance tests for new work. Do not rewrite them.

## When blocked

Do not guess a product decision. The open ones are already listed in `docs/REQUESTS.md`. Add a new row if you hit another, stub the smallest local type that lets you continue, and mark it `TODO(request)`.
