# Phase 2

Start only after the Phase 1 gate. First, one agent reads the merged code and updates `docs/CONTRACTS.md` for the additions below (task 06). Then run 07 to 11 in parallel.

Field names already in the app stay. Phase 2 fields are additions.

## 06-contracts-update (run alone, first)

Owns: `docs/CONTRACTS.md` only.

Add optional fields for merged plots, review and audit records, PLSS references, firm CAD standards, and plugin API endpoints. Do not rename upload, analysis, `DeedCall`, or plot coordinate fields. There is no `packages/contracts/` directory. Do not create one.

## 07-cad-plugin

Owns: `plugins/autocad/` (new) and plugin API routes added under `deed-reader-web/backend/routes/`. Confirm the C# choice against `docs/REQUESTS.md` before writing the plugin.

The web app already draws linework, bearing and distance labels, and a closure report, and the server already builds DXF and script strings. That is not this task. Do not redo `InteractivePlot.tsx`.

Remaining:

- AutoCAD and Civil 3D plugin: sign in, choose a deed, pick a point or use the stored coordinates, and draw.
- In the plugin, draw linework, bearing and distance labels, monuments, adjoiners, and tie lines. The server plot does not draw adjoiners or tie lines into CAD.
- Line and curve tables for labels that do not fit.
- Layers, colors, text heights, annotative text, and groups.
- Area, closure, and deed information placed in the drawing with the tract. The web closure report is not a substitute.
- Firm CAD standards saved once on the server and applied for every user.
- All geometry comes from the server solver in `backend/core/`. The plugin does no survey math. Do not call the Claude `bearing_decimal` path for plugin geometry.

## 08-merged-plot

Owns: merged-plot UI in `deed-reader-web/frontend/` and additions in `deed-reader-web/backend/core/`.

- Many tracts from many documents on one sheet.
- Drag with corner snapping. Rotate one tract's line onto another's. Undo.
- Offset parcels and centerline easements.
- Polylines by bearing and distance. Measure distance and area. Convert an area to a tract.
- Text, leaders, tract legend, draw order. Save and reopen.

## 09-plss-maps

Owns: a new `deed-reader-web/backend/core/plss` package (or `services/plss` if it is I/O) and map additions in the frontend. Esri traverse text and the ZIP of current exports already exist (`plotting_service.py`, `POST /api/plotting/export/all`). Do not rewrite those.

- PLSS sections with quarter and aliquot lines from federal land records. Texas abstract surveys.
- Resolve calls that reference section corners or lines.
- Locate the point of beginning from a PLSS reference.
- Section corner coordinates viewable and correctable.
- GeoJSON and shapefile export. LandXML export. Batch export of those formats. Esri traverse export already exists; extend it only if the current `COURSE` lines are not enough, and keep the current text as a valid output.

## 10-title-tools

Owns: reading additions in the backend services the reading task owns, and title UI in the frontend.

`POST /api/analysis/compare` compares Claude with the regex parser for a single text. Keep that route. It is not a two-deed compare.

- Exceptions, easements, and restrictions extracted with short descriptions.
- Compare two deeds side by side with differences highlighted.
- Search every deed the firm has processed by name, book and page, or parcel.
- Line and curve tables read from plats. Transcribe-only mode. Full-document transcription.
- CSV point file import. Phone capture of deed-book pages. CSV export of plot points already exists.

## 11-review-audit

Owns: account additions and review UI. Roles are mentioned in `CURSOR_RULES_TASKS.md` and `docs/PRD.md` only. There is no role check in the app. `POST /api/plotting/export/all` zips coordinate files and is not a project package.

- Enforce roles for admin, drafter, and reviewer, using the auth answer in `docs/REQUESTS.md`.
- Reviewer sign-off with name and date. A deed cannot be marked reviewed until flags are cleared or explained.
- Change history: who changed which call and when, with the original AI reading kept (`rawExtraction`).
- Comments on individual calls.
- One-click project package: source pages, call tables, closure reports, and plots. The coordinate ZIP stays.
- Interface modes for Survey and CAD, GIS, and Title. Single sign-on, if the auth answer includes it.
- Radial bearing direction detected from closure. Compound and reverse curves grouped.
- Multi-cell paste, keyboard-only entry, and firm-wide label rules.

## Phase gate

All pull requests merged, CI green, golden fixtures pass, and the plugin has drawn one reviewed deed into AutoCAD on a real machine. If `docs/REQUESTS.md` says not to build the plugin, the gate is the rest of this list and that answer.
