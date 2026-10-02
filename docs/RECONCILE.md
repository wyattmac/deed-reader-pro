# Reconcile the planning kit with Deed Reader Pro

The planning kit in the uploaded `deed-kit/` folder was written for an empty repository. This repo already has a working Deed Reader Pro app. The app wins. This file records the overlap. Adapted instructions live in `AGENTS.md`, `docs/CONTRACTS.md`, `docs/tasks/`, `docs/BOARD.md`, `docs/prompts.md`, and `.cursor/rules/core.mdc`.

No application code, migration, or existing test was changed to produce this document. No bullet below is **DONE**. A bullet is DONE only when a test asserts it or it was executed in this session. This repo has no pytest assertions and no Jest test files. The `deed-reader-web/backend/test_*.py` files are manual scripts. Nothing in the kit was executed against a running server here.

## Stack

| Topic | This repo | Kit | Difference |
| --- | --- | --- | --- |
| Layout | `deed-reader-web/frontend`, `deed-reader-web/backend`, `docs/`, `scripts/`, `config/`, `samples/`, `src/` (pointer only) | pnpm workspace: `apps/web`, `packages/contracts`, `packages/engine`, `packages/reading`, `packages/exports`, `packages/accounts`, `plugins/` | No packages, no apps/web, no plugins directory |
| Package manager | npm (`deed-reader-web/frontend/package-lock.json`); pip (`requirements.txt`, `requirements-minimal.txt`) | pnpm workspaces | Do not introduce pnpm |
| Language | TypeScript strict on the frontend (`tsconfig.json`); Python type hints, uneven | TypeScript strict everywhere, Node 22 | Backend stays Python |
| Web | Create React App (`react-scripts` 5.0.1), React 18.2, React Router 6, TanStack Query 5, Axios, Tailwind 3. `public/` is gitignored, so `index.html` is not in git | Next.js App Router | Keep CRA |
| API | Flask `deed-reader-web/backend/app.py` on port 5000 is what `scripts/RUN_APP.bat` starts. FastAPI `main.py` exists. `run_migration.py` runs Flask on 5000 and FastAPI on 8000 | Next.js route handlers | Keep Flask as the running API. FastAPI migration stays in progress |
| Registered routes | Flask registers documents, analysis, chat, plotting (`app.py`). FastAPI mounts documents and analysis only; chat and plotting includes are commented out (`main.py`) | Not specified as Flask blueprints | Do not drop the Flask blueprints |
| Database | None. No schema, no SQLite file, no Prisma. `sqlalchemy`, `asyncpg`, and `alembic` are declared in `requirements.txt` and unused. `main.py` `database_url` defaults to `None` | PostgreSQL + Prisma | No database in the running app. ORM choice is an open question |
| Auth | None. No users, sessions (except an in-memory chat dict), or middleware | Clerk organizations = firms | Open question |
| Billing | None | Stripe subscription per firm, 30-day trial | Open question |
| Jobs | `celery`, `redis`, and `aioredis` are in `requirements.txt` and unused. Requests are synchronous | pg-boss | Open question. Do not add pg-boss while Celery is the declared dependency |
| Files | Local `uploads/` (`UPLOAD_FOLDER`) | S3-compatible bucket | Roadmap mentions Cloudflare R2. Running code is local disk |
| Map | SVG plot in `InteractivePlot.tsx`. `POST /api/plotting/transform` returns the same coordinates and sets `method` to `placeholder` | MapLibre GL, aerial and street basemaps, state plane | No map library |
| AI | `anthropic` in `services/claude_service.py` (model `claude-3-5-sonnet-20241022`). `openai` in `services/ocr_fallback_service.py` and optional filters in `core/deed_text_filter.py` and `core/advanced_deed_filter.py` | One provider interface at `packages/reading/src/provider.ts` | Two SDKs, no single interface |
| CAD | String exporters in `plotting_service.py` (DXF polyline, CSV, Esri traverse text, AutoCAD script, KML). No plugin | C# AutoCAD .NET plugin in `plugins/autocad/` | No C# project |
| Tests | pytest and Jest are dependencies only. Backend `test_*.py` scripts use `requests` or local PDF helpers and contain no `assert`. Frontend has no `*.test.*` files. `scripts/TEST_APP.bat` checks the venv, imports, and `npm run build` | Vitest and Playwright | Keep pytest and Jest as the intended runners. Do not add Vitest or Playwright in place of them |
| Lint | `deed-reader-web/backend/lint.py` (flake8, black, isort; mypy commented out), frontend `npm run lint`, `config/.pre-commit-config.yaml` | `pnpm lint`, `pnpm typecheck`, `pnpm test` | Use the existing lint entry points |
| CI | No `.github/workflows` | Required before merge | Missing |
| Env | `deed-reader-web/backend/.env.example` (`ANTHROPIC_API_KEY` required for AI), `deed-reader-web/frontend/.env.example` (`REACT_APP_API_URL`) | A root `.env.example` | Keep the two existing templates |
| Agent docs already here | `.cursorrules`, `.cursor/rules/deedreadrule.mdc`, `config/CLAUDE.md`, empty `config/CLAUDE.local.md`, `CURSOR_RULES_TASKS.md` | `AGENTS.md`, `.cursor/rules/core.mdc` | No root `AGENTS.md` existed. Those files were kept and merged into the new `AGENTS.md` by reference. They were not replaced |

## Task bullets

Legend: **PARTIAL** means some of the behavior is in the code and is not covered by a test. **MISSING** means the behavior is not in the application code.

### Phase 1

| Task | Bullet | Status | Proof |
| --- | --- | --- | --- |
| 00 | Scaffold the pnpm monorepo with the folders in AGENTS.md | MISSING | Repo is `deed-reader-web/` plus npm and pip. No `pnpm-workspace.yaml` |
| 00 | Turn `docs/CONTRACTS.md` into TypeScript types and zod schemas | MISSING | Types are hand-written in `frontend/src/types/index.ts` and `frontend/src/services/api.ts`. No zod dependency. No `packages/contracts/` |
| 00 | Prisma schema for the entities in the contracts | MISSING | No Prisma schema and no database models |
| 00 | Lint, typecheck, test and CI scripts; `.env.example` | PARTIAL | Lint: `backend/lint.py`, `frontend/package.json` `lint`, `config/.pre-commit-config.yaml`. Env: `backend/.env.example`, `frontend/.env.example`. No CI workflow. No dedicated typecheck script. pytest and Jest are not wired to assertions. `frontend/public` is gitignored (`.gitignore`) |
| 00 | A golden-test runner that loads `tests/golden/*.json` and calls `engine.solve` | MISSING | `tests/golden/engine-fixtures.json` is added by this reconciliation and is not executed. No `engine.solve` |
| 01 | Traverse from calls to coordinates for every call type | PARTIAL | `services/plotting_service.py` `_calculate_coordinates` walks AI `calls` that have `bearing_decimal` and `distance`. Curves, ties, and commencement are not traversed |
| 01 | Directions: quadrant, azimuth, south azimuth, decimal degrees, cardinal, angle right and left, deflection, interior | PARTIAL | Quadrant and decimal-degree quadrant strings: `core/deed_parser.py` `BEARING_PATTERNS`. Quadrant to azimuth: `core/bearing_parser.py` `parse_bearing` (minutes, no seconds; not used by the plot path). Azimuth input, south azimuth, cardinal-only, angle right/left, deflection, and interior angles are absent |
| 01 | Units listed in the kit, mixed units, fractions | PARTIAL | `core/deed_parser.py` `DISTANCE_PATTERNS` and `_convert_to_feet`: feet, yards, chains (66 ft), poles/rods (16.5), links (0.66), meters (3.28084), vara (2.777778). Mixed chains+links and poles+links become feet inside the parser. Missing: inches, US survey foot vs international foot, perch, mile, two-pole chain, California vara, fractions, other mixed units |
| 01 | Commencement calls and tie lines from POC to POB | MISSING | `DeedCall.call_type` mentions `commencement` and `tie` in the docstring. No parser branch builds them. The plot prompt asks Claude for `commencement` and then ignores it in `_calculate_coordinates` |
| 01 | Curve solve from any sufficient set, left/right, delta over 180, tangent within 0.02 ft | PARTIAL | `deed_parser.py` `_parse_curve_call` stores radius, delta text, chord bearing, and chord distance. It does not solve a curve |
| 01 | Curve check of unused stated values | MISSING | No comparison of stated curve parts to solved geometry |
| 01 | Closure distance, bearing, precision; area with curves; perimeter | PARTIAL | `plotting_service.py` `_analyze_closure`, `_calculate_area` (shoelace), perimeter summed from call distances. Straight segments only. Inputs are AI-derived coordinates. UI: `components/Plot/ClosureReport.tsx` |
| 01 | Force closure by adjusting one chosen call | MISSING | No force-closure function |
| 01 | Blunder detection and ranking | MISSING | No blunder search |
| 01 | Ground-to-grid scale factor | MISSING | No scale-factor code. `POST /api/plotting/transform` is a placeholder (`routes/plotting_routes.py`) |
| 02 | Accept PDF, PNG, JPG, TIF, BMP, Word, RTF, text; pasted image or text; a drawn region | PARTIAL | `routes/document_routes.py` `ALLOWED_EXTENSIONS`: txt, pdf, png, jpg, jpeg, tiff, bmp. Same set in `routers/documents.py`. `HomePage.tsx` dropzone and paste-text box. No Word, RTF, clipboard image, or region |
| 02 | Find every description and return them in order | MISSING | One extracted string per upload (`extracted_text`). No segmentation into multiple descriptions |
| 02 | Transcribe the legal description, including cursive, watermarks, and poor scans | PARTIAL | `services/ocr_service.py` (Tesseract, then Claude vision), `claude_service.py` `enhance_ocr_text` and `extract_text_from_image`, `ocr_fallback_service.py` (OpenAI vision, not imported elsewhere) |
| 02 | Parse calls, monuments, passing monuments, adjoiners, commencement, and deed information into the contract shape | PARTIAL | Regex: `core/deed_parser.py`. AI JSON: `claude_service.py` `analyze_deed_document`. Neither emits the kit `Call` object. Commencement is not parsed |
| 02 | Page and bounding box on each call | MISSING | `DeedCall` has `raw_text` only. OCR may prefix `--- Page N ---` in `ocr_service.py` and does not attach that to a call |
| 02 | Double read, compare call by call, set confidence, raise `READ_DISAGREEMENT` | MISSING | `DeedCall.confidence` is a parser heuristic float. `POST /api/analysis/compare` compares one AI pass with the legacy parser (`routes/analysis_routes.py`). It is not two independent reads |
| 02 | Store raw output, model, and prompt version | PARTIAL | `routes/analysis_routes.py` and `routers/analysis.py` add `analysis_metadata.model_used`. The raw message is returned only when JSON parsing fails (`claude_service.py`). No prompt version is stored |
| 02 | One provider interface, one implementation, and a recorded-response mock | MISSING | `anthropic` is constructed in `ClaudeService`. Plotting and chat call `ClaudeService._client` directly. OpenAI is a second SDK |
| 02 | Background job with progress and retry | MISSING | Celery and Redis are unused. Analysis and plotting run inside the HTTP request |
| 03 | Drag and drop, many files, clipboard paste, draw a box on a page | PARTIAL | `HomePage.tsx`: `useDropzone` with `multiple: false`, paste text into a textarea. No multi-file upload, clipboard image, or box |
| 03 | Three-pane workspace | MISSING | Separate routes in `frontend/src/App.tsx`: `/`, `/analysis`, `/plotting`, `/chat`, `/settings` |
| 03 | Click a call to highlight text, plot, and page | MISSING | No selection sync |
| 03 | Editable call table with undo, versions, and edits that survive reprocessing | MISSING | `AnalysisPage.tsx` renders metes and bounds as read-only text. Re-analyze replaces component state |
| 03 | Flags panel | MISSING | No flags UI. `plotting_routes.py` `validate_plot` returns ad hoc warnings |
| 03 | Plot labels, table colors, north arrow, bar scale, border, title block, saved labels, print and PDF from Letter to Arch D | PARTIAL | `InteractivePlot.tsx`: boundary, bearing and distance labels, monument marker, north arrow, scale readout, closure line. `ClosureReport.tsx` shows area and closure. No adjoiner labels, title block, saved label positions, or print/PDF |
| 03 | Blunder suggestions with apply and undo | MISSING | No blunder UI |
| 03 | Aerial and street basemap, tract overlay, set POB, state plane | MISSING | No MapLibre. Transform route is a placeholder |
| 03 | Editable deed information panel | PARTIAL | `AnalysisPage.tsx` shows grantor, grantee, acres, and legal description as text. Not editable |
| 03 | Project list and project page | MISSING | No project model. Upload state is React Router location state |
| 04 | DXF 2000 and 2010 with units and layers | PARTIAL | `plotting_service.py` `_generate_dxf_data` writes a minimal POLYLINE on layer BOUNDARY. No units header, no 2000/2010 distinction, no label or monument layers. Download: `routes/plotting_routes.py`, `components/Plot/ExportMenu.tsx` |
| 04 | Point file with point, northing, easting, elevation, description | PARTIAL | `_generate_csv_data` header is `Point,X,Y,Description,Monument`. No elevation. Columns are X/Y, not northing/easting |
| 04 | AutoCAD script that draws the tract | PARTIAL | `_generate_autocad_script` emits `PLINE` and close |
| 04 | KML | PARTIAL | `_generate_kml_data` writes local x,y into KML coordinates. The comment in that function says lat/lon conversion is not done |
| 04 | Closure report PDF | MISSING | Closure is on screen only (`ClosureReport.tsx`) |
| 04 | Call table to Excel; deed information to Word and Excel, appending | MISSING | No xlsx or docx writer |
| 05 | Firms, named seats, sign-in from any computer | MISSING | No user or firm types |
| 05 | Pooled AI usage and metering | MISSING | No meter |
| 05 | 30-day trial and Stripe subscription per firm | MISSING | No Stripe |
| 05 | Projects owned by a firm, visible to members; notes | MISSING | No project store |
| 05 | Firm scoping in one data-access layer | MISSING | Routes take a raw body and do not receive a firm id |
| 05 | Reopening a deed does not reprocess or spend allowance | MISSING | Each visit to analysis or plotting calls the API again (`AnalysisPage.tsx`, `PlottingPage.tsx`) |

### Phase 2

| Task | Bullet | Status | Proof |
| --- | --- | --- | --- |
| 06 | Add merged plots, review and audit records, PLSS references, firm CAD standards, and plugin API endpoints to the contracts | MISSING | No phase-2 fields in the current responses |
| 07 | AutoCAD and Civil 3D plugin: sign in, choose a deed, pick a point or use stored coordinates, draw | MISSING | No `plugins/` tree and no plugin routes |
| 07 | Draw linework, bearing and distance labels, monuments, adjoiners, tie lines | PARTIAL | Web plot and exporters draw linework and bearing/distance labels (`InteractivePlot.tsx`, `plotting_service.py`). Adjoiners are parsed (`deed_parser.py` `_parse_adjoiner_call`) and not drawn. No tie-line geometry. This is not a CAD plugin |
| 07 | Line and curve tables for labels that do not fit | MISSING | No line or curve table generator |
| 07 | Layers, colors, text heights, annotative text, groups | MISSING | DXF output is one polyline layer |
| 07 | Area, closure, and deed information placed with the tract | PARTIAL | Shown in the web plot and `ClosureReport.tsx`. Not placed in a CAD drawing |
| 07 | Firm CAD standards saved once and applied for every user | MISSING | No standards record |
| 07 | All geometry comes from the server; the plugin does no survey math | PARTIAL | Coordinates are computed in `plotting_service.py` on the server. There is no plugin to consume them, and that computation currently uses an AI `bearing_decimal` |
| 08 | Many tracts from many documents on one sheet | MISSING | One text blob is plotted |
| 08 | Drag with corner snapping; rotate one tract onto another; undo | MISSING | Plot is not editable |
| 08 | Offset parcels and centerline easements | MISSING | No offset tool |
| 08 | Polylines by bearing and distance; measure; convert an area to a tract | MISSING | No drafting tools |
| 08 | Text, leaders, legend, draw order; save and reopen | MISSING | No sheet model |
| 09 | PLSS sections, quarter and aliquot lines; Texas abstracts | MISSING | No PLSS data |
| 09 | Resolve calls that reference section corners or lines | MISSING | No section-corner resolver |
| 09 | Locate the POB from a PLSS reference | MISSING | POB is local (0, 0) in `_calculate_coordinates` |
| 09 | Section corner coordinates viewable and correctable | MISSING | No section corners |
| 09 | GeoJSON, shapefile, LandXML, Esri traverse, batch export | PARTIAL | `_generate_esri_traverse` and `POST /api/plotting/export/all` (ZIP of dxf, csv, esri, script, kml). No GeoJSON, shapefile, or LandXML |
| 10 | Exceptions, easements, and restrictions with short descriptions | MISSING | Those words appear as filter or chat context (`deed_text_filter.py`, `chat_routes.py`), not as extracted records |
| 10 | Compare two deeds side by side | PARTIAL | `compare_analysis` in `routes/analysis_routes.py` and `routers/analysis.py` compares AI output with the regex parser for one text |
| 10 | Search the firm's deeds by name, book and page, or parcel | MISSING | No deed index |
| 10 | Plat line and curve tables; transcribe-only mode; full-document transcription | MISSING | No plat-table reader and no transcribe-only mode. OCR returns one string |
| 10 | CSV point file import; phone capture of deed-book pages | MISSING | CSV is export only (`_generate_csv_data`) |
| 11 | Roles for admin, drafter, and reviewer | PARTIAL | Named only in `CURSOR_RULES_TASKS.md` and `docs/PRD.md`. No role checks in Python or TypeScript |
| 11 | Reviewer sign-off; cannot mark reviewed until flags are cleared or explained | MISSING | No review state |
| 11 | Change history with the original AI reading kept | MISSING | No version rows |
| 11 | Comments on individual calls | MISSING | No comment model |
| 11 | One-click project package of pages, tables, closure reports, and plots | PARTIAL | `export_all_formats` zips coordinate exports only (`routes/plotting_routes.py`) |
| 11 | Survey, GIS, and Title modes; single sign-on | MISSING | One UI. No SSO |
| 11 | Radial bearing from closure; compound and reverse curves grouped | MISSING | Curve parse does not group compound or reverse curves |
| 11 | Multi-cell paste, keyboard-only entry, firm-wide label rules | MISSING | No call grid |

Phase 2 gate (plugin draws one reviewed deed in AutoCAD, CI green, golden fixtures pass): **MISSING**. No plugin, no CI, fixtures not executed.

### Phase 3

| Task | Bullet | Status | Proof |
| --- | --- | --- | --- |
| 12 | IntelliCAD and BricsCAD plugins sharing the Phase 2 server API | MISSING | No plugin projects |
| 12 | Aerial imagery in CAD at the correct scale and position | MISSING | No imagery loader |
| 13 | Link deeds through prior-record references into a chain | MISSING | `claude_service.py` can return `references` text. Nothing links documents |
| 13 | Chain of title as a timeline with each tract plotted | MISSING | No timeline |
| 14 | Find and measure gaps and overlaps in a merged plot | MISSING | No merged plot |
| 15 | Spiral curve solving, plotting, and export | MISSING | No spiral code |
| 16 | Firms connect their own AI provider key | PARTIAL | `frontend/src/pages/SettingsPage.tsx` shows a disabled OpenAI key input and tells the user to use backend env vars. One server key: `ANTHROPIC_API_KEY` |
| 16 | County parcel layers as a map overlay | MISSING | No map overlay |

Phase 3 finish line: **MISSING**. There was no `docs/BOARD.md` before this reconciliation.

## Data model vs `CONTRACTS.md`

The kit's entities are not stored. The app keeps an upload response, a Claude analysis dict, a `DeedCall`, and plot coordinate dicts. There is no `Firm`, `User`, `Project`, `Description`, `DeedVersion`, or `Flag`.

| Kit | Existing shape | Difference |
| --- | --- | --- |
| `Document.id` | `upload_id` | Different name. Not a database id |
| `Document.fileKey` | `filename` plus `uploads/{filename}` | Local path, not an object-storage key |
| `Document.fileType` | `file_type` | Extension string |
| `Document.projectId`, `pageCount`, `sha256` | Absent | PDF page counts are computed during OCR and not stored on the response |
| `Document` extras | `success`, `text_length`, `extracted_text`, `message` | Kit has no transcription on `Document`; the app returns `extracted_text` immediately |
| `Description` | Absent | One text blob per upload |
| `DeedVersion` | Absent | Re-analyze replaces React state |
| Payload `transcription` | `extracted_text` | Different name |
| `rawExtraction`, `promptVersion` | Absent | `model_used` is set on success. `raw_response` is set only when JSON parsing fails |
| `units { plot, vara, chain }` | Per-call `units` string | Parser converts some mixed units to feet before the value is returned |
| `start { kind, northing, easting, crs }` | AI `point_of_beginning`, then coordinates start at x=0, y=0 | No POB/POC kind and no CRS |
| `Call.id`, `order` | `call_number` or `sequence` or list order | No stable id |
| `Call.type` `L`, `C`, `TL`, … | `call_type`: `bearing_distance`, `curve`, `monument`, `adjoiner`, `commencement`, `tie` | Different vocabulary |
| `direction` object | `bearing` string | `bearing_parser.py` can emit a float azimuth and is not what plotting uses |
| `distance.parts[]` | `distance` number plus `units`, or a distance string on the analysis JSON | Analysis `metes_and_bounds[].distance` is a string. Parser `DeedCall.distance` is a float |
| `curve` | `curve_data` dict: `radius`, `delta` (often a string), `chord_bearing`, `chord_distance`, `units`. AI plot `curves[]` uses `curve_length` | No turn, concave, radial bearings, or tangent flag |
| `passing[]` | `passing_monuments: string[]` | No distance or unit on each passing call |
| `adjoiner` | `call_type == "adjoiner"` plus `description`, or a separate `adjoiners` array on the plot prompt | Not a string field on every call |
| `source` page, bbox, char range | `raw_text` only | No provenance |
| `confidence` enum | `DeedCall.confidence` float and analysis `confidence_score` float | `frontend/src/types/index.ts` `DeedAnalysis.confidence` is also a float, and that interface is not what `AnalysisPage` renders |
| `asCalled` | `raw_text` on `DeedCall`; `description` on AI calls | Different name |
| Engine `points` northing/easting plus `callId` | `{ point_number, x, y, label, description, monument, bearing?, distance?, units? }` | x/y, no call id |
| `segments`, `curveChecks`, `blunderCandidates` | Absent | Lines for the SVG are built in `plotting_instructions.plot_elements.lines` |
| `closure.bearing` as `Direction`, `precision` number | `closure_bearing` string, `precision_ratio` string `"1:N"` or `"Perfect"`, plus `closure_error_ppm`, `is_closed`, `coordinates_to_close` | Extra closure fields the kit does not have |
| `area`, `perimeter` | `area_sq_feet`, `area_acres`, `perimeter_feet` | Named per unit |
| `errors[]` with codes | `validate_plot` warnings and errors with a `type` string | Not the kit error shape |
| `DeedInfo` | Spread across `parties`, `property_description`, `dates`, `references`, `key_findings` | See the map in `docs/CONTRACTS.md` |
| `parties.grantor` / `grantee` | Strings in `api.ts` `AnalysisResult`. Arrays in `types/index.ts` `DeedAnalysis` | The two TypeScript types disagree. The Claude prompt asks for strings |
| Kit does not model | `summary`, `subdivision`, `legal_description`, `monuments[]`, `dates.deed_date`, `key_findings`, `confidence_score`, chat session payloads, export format strings | Kept |

`PlotPoint`, `PlotCall`, and `ClosureAnalysis` in `plotting_service.py` are defined and the plot path uses plain dicts instead.

FastAPI `CoordinatesResponse` types `coordinates` as a list of dicts. `ClaudeService.extract_coordinates` returns a dict with `bearings`, `distances`, and `curves`.

`routes/analysis_routes.py` and `routers/analysis.py` call `ClaudeService.generate_summary` and `ClaudeService.validate_deed_data`. Those methods are not defined on `ClaudeService` (`services/claude_service.py`).

## Hard rules in the kit `AGENTS.md`

| Rule | Existing code |
| --- | --- |
| 1. No AI in the math. An AI call never returns a number used as geometry | **Broken.** `plotting_service.py` `_extract_plotting_data_with_ai` asks Claude for `bearing_decimal`. `_calculate_coordinates` uses that number with `sin` and `cos`. `routes/plotting_routes.py` `plot_deed`, `get_coordinates`, and `validate_plot` call that path. `claude_service.py` `extract_coordinates` asks for `normalized` degrees and `in_feet`. `bearing_parser.py` is deterministic and is not used by plotting |
| 2. Store the AI's raw output unmodified, with model name and prompt version | **Broken.** Successful Claude calls keep parsed JSON. `model_used` is attached in the analysis routes. Prompt text is inline and has no version. `raw_response` is kept only after `json.JSONDecodeError` |
| 3. Every call links to page, bbox, and character range | **Broken** for every call the app creates. `DeedCall`, analysis `metes_and_bounds`, and plot `calls` have no `source` |
| 4. User edits are never overwritten. Reprocessing creates a new version | **Not applicable yet.** There is no saved edit and no version row. Re-analyze replaces UI state, which will break this rule once editing exists |
| 5. Do not edit `packages/contracts` or `docs/CONTRACTS.md` outside task 00 | **Not applicable.** Those paths did not exist. Shapes are duplicated in Python dataclasses, the Claude prompt, and TypeScript interfaces |
| 6. One provider interface. No provider SDK elsewhere. Keys from the environment | **Broken.** `ClaudeService` holds the Anthropic client, and `plotting_service.py` plus `routes/chat_routes.py` call `ClaudeService._client` directly. `ocr_fallback_service.py`, `deed_text_filter.py`, and `advanced_deed_filter.py` import OpenAI or Mistral. Keys do come from the environment (`ANTHROPIC_API_KEY`, optional `OPENAI_API_KEY`) |
| 7. Every query is scoped to a firm | **Broken** for every document, analysis, chat, and plotting route. None take a firm id. There is no firm record, so the rule cannot be satisfied by the current design. See `docs/REQUESTS.md` |
| 8. Internal distances are US survey feet or meters; angles are azimuth from north, clockwise; conversion happens at the edges | **Broken.** `_extract_distance` converts chains, links, poles, and vara to feet inside the parser (`_convert_to_feet`, Texas-style 2.777778 for any `vara`). Plot geometry uses AI `bearing_decimal`, not an azimuth parsed from the bearing string. `bearing_parser.py` uses `az = 90 - angle` for N/E, which is not azimuth from north for the usual quadrant reading, and nothing in the plot path calls it. Coordinates are `x`/`y`, not labeled US survey feet |
| 9. No secrets, customer deeds, or real personal data in the repo | **Holds** for the files reviewed. Samples use synthetic names (`samples/sample_simple_deed.txt`, `backend/test_deed_sample.txt`, `frontend/test-deed.txt`). `.env.example` and `env.template` contain placeholder keys. `backend/uploads/tint_rd.pdf` is in the tree; this reconciliation did not inspect it as a customer document |

## Features the kit does not mention

- Interactive Q&A API: `POST /api/chat/ask`, history, clear, list sessions, suggestions, and term explain (`routes/chat_routes.py`). The React page is a stub (`frontend/src/pages/ChatPage.tsx`, "Coming Soon"). Sessions live in a process-local dict.
- Deed text filtering before parse: `core/deed_text_filter.py`, `core/advanced_deed_filter.py`, used from `AdvancedDeedParser`.
- OCR pipeline: Tesseract, Claude vision, and an OpenAI vision fallback module.
- Document keyword validation: `POST /api/documents/validate`.
- Legacy parser route: `POST /api/analysis/parse`, which tries to import `deed_reader.core.deed_parser` from a path that is not this repo's `core/deed_parser.py`.
- Health and API info: `GET /api/health`, `GET /api/info` on Flask and FastAPI.
- Security headers and request logging middleware in `app.py` and `main.py`.
- Dual-server migration: `run_migration.py`, `MIGRATION_README.md`. FastAPI analysis routes exist even though `MIGRATION_README.md` still says they are pending.
- ZIP of every export format: `POST /api/plotting/export/all`.
- Esri traverse text export (the kit only asks for this in Phase 2).
- Settings screen with non-functional toggles (`SettingsPage.tsx`).
- Sample deed `samples/sample_simple_deed.txt`.
- Windows launch, lint, and git scripts in `scripts/`.
- Frontend hooks `useDebounce` and `useLocalStorage`.
- Roadmap docs that describe a different future stack than the kit: `docs/PRD.md`, `CURSOR_RULES_TASKS.md`, `docs/ENHANCEMENT_PLAN.md`.

## What was adapted

`deed-kit/` was not part of the git tree. It arrived as an upload. Adapted files were written to `AGENTS.md`, `docs/`, `.cursor/rules/core.mdc`, `.cursor/worktrees.json`, and `tests/golden/`. The kit folder was not added. Existing `.cursorrules`, `.cursor/rules/deedreadrule.mdc`, and `config/CLAUDE.md` were left in place. `AGENTS.md` tells agents to follow them.
