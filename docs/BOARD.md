# Board

Status is the state of the **remaining** work in `docs/tasks/`, not a claim that the whole kit task shipped. `partial` means some of the behavior is already in the app and is not covered by tests. `todo` means it is not started. Agents update only their own row when they finish the remaining bullets. Allowed values: `todo`, `partial`, `in progress`, `in review`, `merged`.

Nothing is `merged`. No acceptance bullet has a test. Detail is in `docs/RECONCILE.md`.

| Task | Phase | Status | Branch | Notes |
| --- | --- | --- | --- | --- |
| 00-foundation | 1 | partial | | Lint and `.env.example` exist. No CI, no shared models for the additive contract fields, no golden runner. Do not scaffold pnpm, Next, or Prisma |
| 01-engine | 1 | partial | | Quadrant strings, some unit conversion, straight-line closure and area. Plot math still uses Claude `bearing_decimal`. Solver in `backend/core/` is not built |
| 02-reading | 1 | partial | | PDF, images, and text upload; Claude analysis; OCR. No contract-shaped calls, no bbox, no double read, no job queue |
| 03-web | 1 | partial | | Single-file dropzone, paste text, read-only analysis, SVG plot, closure report, export menu. No workspace, editor, map, or projects |
| 04-exports | 1 | partial | | Minimal DXF, CSV, Esri traverse, AutoCAD script, KML, and a ZIP of those. No PDF, Excel, or Word |
| 05-accounts | 1 | todo | | No users, firms, or billing. Blocked on `docs/REQUESTS.md` |
| 06-contracts-update | 2 | todo | | Phase 2 fields are not in `docs/CONTRACTS.md` |
| 07-cad-plugin | 2 | partial | | Server exports and the web plot exist. No AutoCAD plugin |
| 08-merged-plot | 2 | todo | | |
| 09-plss-maps | 2 | partial | | Esri traverse text and ZIP export only |
| 10-title-tools | 2 | partial | | One-text AI vs regex compare only |
| 11-review-audit | 2 | partial | | Roles appear in roadmap docs only. ZIP export is not a project package |
| 12-more-cad | 3 | todo | | |
| 13-chain-of-title | 3 | todo | | |
| 14-gaps-overlaps | 3 | todo | | |
| 15-spirals | 3 | todo | | |
| 16-platform | 3 | partial | | Settings page has a disabled API key field. No per-firm key and no parcel overlay |
