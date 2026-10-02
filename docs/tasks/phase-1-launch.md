# Phase 1: Launch (pilot product)

Goal: one deed from upload to a checked plot and DXF, in the browser, shared across a firm.

The app already uploads a file, asks Claude for an analysis, and draws an SVG plot. This file lists only what is left. Paths and field names are the ones in `AGENTS.md` and `docs/CONTRACTS.md`. Do not scaffold a new repository.

Run task 00 alone first. After it merges, run tasks 01 to 05 in parallel, one agent each. Task 05 waits on the auth and billing rows in `docs/REQUESTS.md`.

---

## 00-foundation (run alone, first)

Owns: CI config, additive types next to the existing ones, `tests/golden/` runner. Does not own a new monorepo.

Already in the repo, do not redo it:

- `deed-reader-web/frontend` (npm) and `deed-reader-web/backend` (pip)
- `deed-reader-web/backend/.env.example` and `deed-reader-web/frontend/.env.example`
- `python lint.py`, `npm run lint`, and `config/.pre-commit-config.yaml`

Remaining:

- GitHub Actions that run `python lint.py` from `deed-reader-web/backend`, and `npm run lint` plus `npx tsc --noEmit` from `deed-reader-web/frontend`. There is no `.github/workflows` directory.
- `public` is a gitignore rule, so Create React App has no committed `index.html`. Put a `public/index.html` in the repo in a way that ignore rule does not drop it.
- Pydantic models and TypeScript types for the **Additions** in `docs/CONTRACTS.md`, placed beside `DeedCall`, `AnalysisResult`, and the plot coordinate dict. Do not rename existing fields. Do not add zod unless it is already a dependency (it is not).
- A pytest that loads `tests/golden/*.json` and calls a deterministic solver in `deed-reader-web/backend/core/`. Skip with a clear message until task 01 adds that function. The loader must not call Claude.
- Do not add pnpm, Next.js, Prisma, Clerk, Stripe, or `packages/`. Database and job-queue choices are unanswered in `docs/REQUESTS.md`.

Done when: CI is green on lint and typecheck, and the golden loader runs (skip or pass) without a network call.

---

## 01-engine

Owns: `deed-reader-web/backend/core/` only.

`services/plotting_service.py` already computes x/y, closure, area, and perimeter from Claude `bearing_decimal`. Do not extend that. Do not edit it. New math goes in `core/` and is covered by pytest. `core/deed_parser.py` already extracts quadrant bearings and several units. `core/bearing_parser.py` already converts a quadrant string to a float. Extend those only where a bullet below says they fall short, and add tests. Do not import `anthropic` or `openai`.

Remaining:

- Traverse every `call_type` the contract already names (`bearing_distance`, `curve`, `tie`, `adjoiner`, `commencement`, `monument`) to coordinates. Today only AI line calls with `bearing_decimal` are traversed, and that code is off limits.
- Directions still missing: azimuth and south-azimuth input, cardinal-only calls, angle right, angle left, deflection, and interior angles. Quadrant bearings and decimal-degree quadrant forms are already parsed as strings.
- Units still missing: inches, a distinct US survey foot, perch, mile, two-pole chain, California vara, and fractions. Feet, yards, Gunter chains, poles, rods, links, meters, and a single vara factor (2.777778) already convert inside `_convert_to_feet`. Mixed chains-and-links and poles-and-links already become feet. New conversion for the solver happens at the edge of the calculation. Whether to keep the Texas vara as the default is an open question.
- Commencement calls and tie lines from point of commencement to point of beginning. The dataclass names exist. Nothing builds the traverse.
- Curve solve from any sufficient mix of radius, delta, arc, chord bearing, and chord distance, plus radial and tangent bearings once those optional fields exist. Left or right from concave direction. Delta over 180 degrees. Tangent detection within 0.02 ft. `_parse_curve_call` only stores raw pieces.
- Curve check: compare every unused stated value with the solved geometry.
- Closure distance, bearing, and precision ratio; area that includes curves; perimeter. Straight-line shoelace and perimeter already exist on the AI plot path. The new solver needs its own tested implementation, including curves.
- Force closure by adjusting one chosen call.
- Blunder detection: test single-value changes (transposed digits, wrong quadrant, dropped digit, swapped bearing letters) and rank those that close the figure.
- Ground-to-grid scale factor. `POST /api/plotting/transform` is a placeholder and is not in this task's path. Do not treat it as done.

Done when: every fixture in `tests/golden/` passes against the new solver, and each bullet above has a unit test. No network and no AI imports in `backend/core/`.

---

## 02-reading

Owns: `deed-reader-web/backend/services/claude_service.py`, `services/ocr_service.py`, `routes/document_routes.py`, `routers/documents.py`.

Already accepted: `txt`, `pdf`, `png`, `jpg`, `jpeg`, `tiff`, `bmp`, plus pasted text on the home page. OCR uses Tesseract and Claude vision. Analysis returns the JSON in `docs/CONTRACTS.md` and sets `model_used`. Do not rebuild that pipeline.

Remaining:

- Word and RTF upload. Pasted image and a user-drawn region of a page are frontend work (task 03); accept the resulting file or text on these routes.
- Find every metes-and-bounds description in a document and return them in order. This is blocked if `docs/REQUESTS.md` says one text blob stays the rule. Until then, add the `Description` list from the contract without removing `extracted_text`.
- Parse calls, monuments, passing monuments, adjoiners, commencement calls, and deed information into the existing shapes plus the additive `id` and `source` fields. Do not invent the kit `L`/`C`/`TL` enum.
- Record page and bounding box for each call (`source` in `docs/CONTRACTS.md`).
- Double read: run extraction twice, compare call by call, and raise `READ_DISAGREEMENT` flags. Keep the existing float `confidence`. The enum is an open question. `POST /api/analysis/compare` is one AI pass versus the regex parser; it is not this bullet.
- Persist `rawExtraction` and `promptVersion` next to `model_used`. Do not drop the parsed JSON the app already returns.
- Route new model calls through `ClaudeService`. Add a recorded-response fake for tests. Do not import the Anthropic or OpenAI SDK from a new module. `ocr_fallback_service.py` is unused legacy; do not spread it.
- Run reading as a background job with progress and retry only after the jobs row in `docs/REQUESTS.md` is answered. Until then, leave the synchronous routes and record the skip in the pull request.

Done when: tests pass against the recorded-response fake, and a scripted run on `samples/sample_simple_deed.txt` (and any files in `tests/deeds/`) produces JSON that validates against the existing analysis shape.

---

## 03-web

Owns: `deed-reader-web/frontend/`.

Already built: single-file drag and drop, paste text, read-only analysis (parties, legal description, metes list, confidence), SVG plot with bearing and distance labels, monument marker, north arrow, scale readout, closure line, closure report, and the export menu. Chat UI is a stub; the API is not this task.

Remaining:

- Upload many files at once. Paste an image from the clipboard. Draw a box on a page. Single-file dropzone and the text box stay.
- Three-pane workspace: original page, call table, and live plot. The separate `/analysis` and `/plotting` routes can remain until the workspace replaces them.
- Click a call to highlight it in the text, the plot, and the page, and the reverse.
- Editable call table: missing data in red, add, delete, reorder, undo and redo, version history. Edits survive reprocessing by creating a new version rather than replacing the edit.
- Flags panel for the `flags` added in the contract.
- Plot labels still missing: monument text, adjoiner, area and closure drawn on the sheet, colors matched to the table, border, title block, saved label positions, and print or PDF from Letter to Arch D. Bearing, distance, north arrow, and scale readout already render.
- Blunder suggestions beside the page, with one-click apply and undo. Depends on task 01.
- Map: aerial and street basemap, tract overlay, click or type to set the point of beginning, state plane. Blocked on the map row in `docs/REQUESTS.md`. The SVG plot stays until that row is answered.
- Make the deed information panel editable. It is read-only today.
- Project list and project page with status, closure, area, and call count per description. Depends on the persistence row in `docs/REQUESTS.md`.

Done when: Jest or Playwright-style tests are not required to be Playwright. Use Jest and React Testing Library (already dependencies) to cover upload, edit, undo, plot, and flag clearing against a mocked reader and the real `core` solver. Map placement is in that set only after the map question is answered.

---

## 04-exports

Owns: the export methods in `deed-reader-web/backend/services/plotting_service.py`, the export routes in `routes/plotting_routes.py`, and `frontend/src/components/Plot/ExportMenu.tsx`.

Do not change `_calculate_coordinates` or `_analyze_closure`.

Already generated: a one-layer DXF polyline, a CSV of `Point,X,Y,Description,Monument`, an Esri traverse text, a `PLINE` script, a KML of local x/y, and a ZIP of those. Keep those keys working.

Remaining:

- DXF that declares units and separate layers for lines, labels, monuments, and adjoiners. The kit names 2000 and 2010; add those headers without removing the current polyline output.
- Point file columns for point, northing, easting, elevation, and description. The current CSV uses X and Y. Keep a column mapping that still emits X and Y, and add northing, easting, and elevation (elevation may be empty).
- AutoCAD script that draws the tract when dragged into a drawing, including the labels the current `PLINE` script omits.
- KML that does not pretend local x/y are longitude and latitude. Geographic KML waits on the coordinate-system question. Until then, document the local frame in the file and do not label it WGS84.
- Closure report PDF.
- Call table to Excel. Deed information to Word and Excel, appending to an existing file.

Done when: each new export has a snapshot test, and a test parses the DXF back and checks the geometry against the deterministic solver. Existing string builders need tests too if you change them.

---

## 05-accounts

Owns: new account modules under `deed-reader-web/backend/` (for example `services/` and `routes/`). Do not add Clerk, Stripe, or Prisma until `docs/REQUESTS.md` names them.

There is no firm, user, or project in the app. The current API is public. Do not lock existing routes behind an unanswered provider.

Remaining, after the auth and billing rows are answered:

- Firms, named seats, and sign-in from any computer, using the provider named in `docs/REQUESTS.md`.
- Pooled AI usage per firm, with metering.
- Trial and subscription behavior named in that same answer. If the answer is "no billing", skip Stripe and say so in the pull request.
- Projects owned by a firm and visible to its members. Notes on documents and descriptions.
- Firm scoping in one data-access layer for the new records. Existing public routes stay public until the answer says to wrap them.
- Reopening a stored deed does not call Claude again and does not spend allowance.

Done when: tests prove a user in one firm cannot read another firm's stored data through any new exported function. If the request is still unanswered, the task is not startable. Do not stub Clerk.

---

## Phase gate

Do not start Phase 2 until: the Phase 1 pull requests for the remaining bullets are merged, CI is green on main, the golden fixtures pass against `backend/core/`, and one real deed has been taken from upload to DXF by hand in the running app (Flask on port 5000, frontend on port 3000).
