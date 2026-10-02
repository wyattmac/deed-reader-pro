# Phase 3

Start only after the Phase 2 gate. Run 12 to 16 in parallel.

## 12-more-cad

Owns: `plugins/intellicad/`, `plugins/bricscad/` (both new).

- Plugins for IntelliCAD-based programs and BricsCAD, sharing the Phase 2 server API on the Flask app. There is no Phase 2 plugin in the repo yet; this task starts after 07.
- Aerial imagery loaded into CAD at the correct scale and position.

## 13-chain-of-title

Owns: `deed-reader-web/backend/services/title/` (new) and the chain UI in the frontend.

- Link deeds through `references` and `priorRecord` into a chain. Claude may already return book and page text on one analysis. Nothing links two stored documents.
- Show the chain as a timeline with each tract's plot.

## 14-gaps-overlaps

Owns: additions in `deed-reader-web/backend/core/` and the merged-plot UI.

- Find and measure gaps and overlaps between adjoining tracts in a merged plot. Merged plot is task 08. This task does not exist in the app.

## 15-spirals

Owns: additions in `deed-reader-web/backend/core/`.

- Spiral curve solving, plotting, and export. Curve parsing today stores radius and delta text only.

## 16-platform

Owns: provider additions behind `ClaudeService`, and map additions in the frontend.

`frontend/src/pages/SettingsPage.tsx` shows a disabled API key field and points at the server environment. The live key is `ANTHROPIC_API_KEY` for the whole process. There is no map overlay.

- A firm connects its own AI provider API key, using the provider answer in `docs/REQUESTS.md`. Do not collect keys in the React state until that row is answered. The disabled settings field can become the UI once it is.
- County parcel layers as a map overlay. Depends on the map row in `docs/REQUESTS.md`.

## Finish line

All pull requests merged, CI green, golden fixtures pass, and every remaining bullet in `docs/tasks/` is marked done on `docs/BOARD.md`.
