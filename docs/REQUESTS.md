# Requests

Product questions where the planning kit and the running app disagree. The app's current behavior stays until an answer is written in the Answer column. Newest at the bottom.

| Date | Task | Request | Answer |
| --- | --- | --- | --- |
| 2026-10-02 | 00-foundation | Persistence. The running app has no database. `requirements.txt` already lists SQLAlchemy, Alembic, and asyncpg, and the roadmap says PostgreSQL. The kit requires Prisma. Which store should new entities use? Do not add Prisma unless this row says so. | |
| 2026-10-02 | 00-foundation | Background work. Celery and Redis are declared and unused. The kit specifies pg-boss. Should long reads use the Celery packages already listed, or stay synchronous? | |
| 2026-10-02 | 00-foundation | File storage. Uploads go to local `uploads/`. The roadmap names Cloudflare R2. The kit says an S3-compatible bucket. Should new code keep local disk? | |
| 2026-10-02 | 05-accounts | Auth provider. The app has no users. `.cursorrules` and `docs/PRD.md` mention Clerk or Auth0. The kit requires Clerk organizations as firms. Which provider, if any, should task 05 use? | |
| 2026-10-02 | 05-accounts | Billing. The kit requires a 30-day trial and a Stripe subscription per firm. The app has no billing. Should task 05 integrate Stripe? | |
| 2026-10-02 | 01-engine | AI geometry. `plotting_service.py` uses Claude `bearing_decimal` as the traverse angle. The kit forbids that. Current behavior is unchanged. Should a later task replace that path with `backend/core/` math, or keep the Claude number? | |
| 2026-10-02 | 01-engine | Confidence. Parser and analysis use a float from 0 to 1. The kit uses `agreed`, `disagreed`, or `edited`. Keep the float? | |
| 2026-10-02 | 01-engine | Parties. `api.ts` `AnalysisResult` uses grantor and grantee strings. `types/index.ts` `DeedAnalysis` uses string arrays. The Claude prompt asks for strings. Which shape is canonical? | |
| 2026-10-02 | 01-engine | Call types. The app uses `bearing_distance`, `curve`, `monument`, `adjoiner`, `commencement`, `tie`. The kit uses `L`, `C`, `TL`, and the tangent/radial variants. Keep the app vocabulary? | |
| 2026-10-02 | 01-engine | Distances. The app stores a number plus a unit string, and converts some mixed units to feet inside the parser. The kit stores `distance.parts[]` and converts only at the edge. Keep the number-plus-unit shape? | |
| 2026-10-02 | 01-engine | Coordinates. The app uses local `x` and `y`. The kit uses `northing` and `easting` plus an optional CRS. Keep `x` and `y`? | |
| 2026-10-02 | 01-engine | Bearings. The app stores the deed wording as a string. The kit stores a structured direction (quadrant, azimuth, angles, deflection). Keep the string as the stored value? | |
| 2026-10-02 | 01-engine | Vara and chain. Any unit spelled `vara` becomes 2.777778 feet (Texas). The kit also has a California vara and a two-pole chain, chosen on the deed. Is the Texas factor the default to keep? | |
| 2026-10-02 | 02-reading | One description per file. The app returns a single `extracted_text`. The kit returns every metes-and-bounds description in order. Should a document stay one text blob? | |
| 2026-10-02 | 03-web | Map. The plot is an SVG. The kit requires MapLibre, aerial and street tiles, and state plane. `POST /api/plotting/transform` is a placeholder. Should the SVG remain the plot until this is answered? | |
| 2026-10-02 | 07-cad-plugin | CAD plugin language. The kit specifies C# on the AutoCAD .NET API. This repo has no plugin project. Confirm that Phase 2 still wants that plugin against the Flask API. | |
