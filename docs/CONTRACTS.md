# Contracts

These are the data shapes Deed Reader Pro already uses. Names match the code. Task 00 may add the fields under **Additions**. It must not rename or remove an existing field. After task 00, this file stays frozen except for task 06.

Product conflicts are questions in `docs/REQUESTS.md`. They are not silent changes to these shapes.

## Where they live

| Shape | Code |
| --- | --- |
| Upload and text response | `deed-reader-web/frontend/src/services/api.ts` `DocumentData`; `deed-reader-web/backend/routers/documents.py` |
| Analysis response | `api.ts` `AnalysisResult`; Claude prompt in `deed-reader-web/backend/services/claude_service.py` `analyze_deed_document` |
| Alternate analysis type | `deed-reader-web/frontend/src/types/index.ts` `DeedAnalysis` (not what the analysis page renders) |
| Parser call | `deed-reader-web/backend/core/deed_parser.py` `DeedCall` |
| Plot coordinate and closure | `deed-reader-web/backend/services/plotting_service.py`; `frontend/src/pages/PlottingPage.tsx` |
| Chat | `api.ts` `ChatResponse`; `deed-reader-web/backend/routes/chat_routes.py` |

## Document upload (existing)

```ts
{
  success: boolean,
  filename?: string,
  file_type?: string,
  text_length: number,
  extracted_text: string,
  upload_id: string,
  message: string
}
```

Files are stored under `uploads/` using the sanitized filename. There is no database row.

## DeedCall (existing)

```ts
{
  call_type: "bearing_distance" | "curve" | "monument" | "adjoiner" | "commencement" | "tie",
  bearing: string | null,
  distance: number | null,
  units: string,                  // default "feet"
  curve_data: {
    radius?: number,
    delta?: string,
    chord_bearing?: string,
    chord_distance?: number,
    units?: string
  } | null,
  monument: string | null,
  description: string | null,
  passing_monuments: string[] | null,
  raw_text: string,
  confidence: number              // 0-1 heuristic from the parser
}
```

`commencement` and `tie` are named on the dataclass and are not produced by `_parse_clause` today.

## Analysis result (existing)

Returned by `ClaudeService.analyze_deed_document`, then wrapped by `POST /api/analysis/analyze`.

```ts
{
  summary: string,
  property_description: {
    legal_description: string | null,
    acres: string | null,
    lot_block: string | null,
    subdivision: string | null
  },
  parties: { grantor: string | null, grantee: string | null },
  metes_and_bounds: {
    call_number: number,
    bearing: string | null,
    distance: string | null,
    description: string | null
  }[],
  monuments: { type: string, description: string, action: string | null }[],
  dates: { deed_date: string | null, recording_date: string | null },
  references: {
    book_page: string | null,
    deed_book: string | null,
    plat_references: string | null
  },
  key_findings: string[],
  confidence_score: number,
  analysis_metadata: {
    text_length: number,
    token_count: number,
    analysis_timestamp: string | null,
    model_used: string
  }
}
```

`DeedAnalysis` in `frontend/src/types/index.ts` instead types `parties.grantor` and `parties.grantee` as `string[]`, and uses `metesAndBounds: string[]`. The API shape above is the one the analysis page reads. Do not collapse the two until `docs/REQUESTS.md` is answered.

## Plot coordinate and closure (existing)

```ts
{
  point_number: number,
  x: number,
  y: number,
  label: string,
  description: string,
  monument?: string | null,
  bearing?: string,
  distance?: number,
  units?: string
}
```

```ts
{
  closure_distance: number,
  closure_bearing: string,
  precision_ratio: string,        // "1:N" or "Perfect"
  area_acres: number,
  area_sq_feet: number,
  perimeter_feet: number,
  is_closed: boolean,
  closure_error_ppm: number,
  coordinates_to_close?: { dx: number, dy: number }
}
```

The plot route also returns `plotting_data` (parsed Claude JSON), `plotting_instructions`, and `export_formats`.

Coordinate math today reads `bearing_decimal` from that Claude JSON. New solver code must not. See `AGENTS.md`.

## Chat (existing)

The kit did not define chat. The Flask API does.

```ts
{
  success: boolean,
  question: string,
  answer: string,
  session_id: string,
  exchange_count: number,
  message: string
}
```

Sessions are a process-local dict, capped at 20 exchanges. They are not persisted.

## Export bodies (existing)

`AdvancedPlottingService._generate_export_data` returns strings:

| Key | What it is |
| --- | --- |
| `dxf` | Minimal POLYLINE on layer `BOUNDARY` |
| `csv` | `Point,X,Y,Description,Monument` |
| `esri_traverse` | `COURSE bearing distance` lines |
| `autocad_script` | `PLINE` vertices and close |
| `kml` | Local x,y written as KML coordinates |

## Additions

Add these as optional fields. Do not rename the fields above to match the old kit.

### New records (nothing in the app stores these)

```ts
Firm        { id, name, plan, seatLimit }
User        { id, firmId, role: "admin" | "drafter" | "reviewer" }
Project     { id, firmId, name, notes }
Description { id, documentId, index, title, status }
DeedVersion { id, descriptionId, number, createdBy, source: "ai" | "edit" | "reprocess" }
```

How they are stored (SQLAlchemy versus anything else) is an open question. Do not add Prisma.

### On the upload response

- `projectId: string | null`
- `pageCount: number | null`
- `sha256: string | null`

Keep `upload_id`, `filename`, `file_type`, and `extracted_text`.

### On the analysis response

- `rawExtraction: unknown` — the model message before JSON parsing
- `promptVersion: string`

Keep `analysis_metadata.model_used`. Do not rename it to `model`.

### On `DeedCall`, each `metes_and_bounds` entry, and each plot call

- `id: string`
- `source: { page: number, bbox: [number, number, number, number] | null, charStart: number, charEnd: number }`

### Deed information fields that are missing

Add these next to the existing analysis blocks. Do not copy data into a second structure with different names.

- `deedType: string | null`
- `priorRecord: string | null`
- `county: string | null`
- `tractTitle: string | null`
- `address: string | null`
- `surveyor: string | null`
- `surveyDate: string | null`

Existing fields that already cover a kit name:

| Keep this | Kit name it covers |
| --- | --- |
| `parties.grantor`, `parties.grantee` | grantor, grantee |
| `references.book_page`, `references.deed_book` | record |
| `dates.recording_date` | dateRecorded |
| `dates.deed_date` | not in the kit; keep it |
| `property_description.acres` | calledArea |
| `property_description.lot_block` | parcelNumber |
| `references.plat_references` | plssReference |
| `key_findings` | notes |
| `property_description.legal_description` | not in the kit; keep it |
| `property_description.subdivision` | not in the kit; keep it |
| `summary`, `monuments`, `confidence_score` | not in the kit; keep them |

### Flags (new)

```ts
{
  code: "READ_DISAGREEMENT" | "MISSING_DATA" | "NO_CLOSURE" | "AREA_MISMATCH" | "CURVE_CHECK" | "DIRECTION_UNKNOWN",
  callId: string | null,
  message: string,
  cleared: boolean,
  clearedBy: string | null
}
```

`validate_plot` warnings stay as they are until a task writes flags beside them.

### Engine output, beside the existing coordinate list and `closure_analysis`

- `callId` on each point (the point keeps `point_number`, `x`, and `y`)
- `segments`: drawable lines and arcs
- `curveChecks: { callId, field, stated, solved, withinTolerance }[]`
- `blunderCandidates: { callId, field, from, to, resultingClosure }[]`
- `errors: { callId, code, message }[]`

### Optional curve fields on `curve_data`

- `turn: "left" | "right" | null`
- `concave: "N" | "NE" | "E" | "SE" | "S" | "SW" | "W" | "NW" | null`
- `arcLength` — the AI plot JSON already uses `curve_length`; accept that name when reading old payloads
- `radialBearingIn`, `radialBearingOut`, `tangentBearingIn`, `tangentBearingOut`
- `tangent: boolean`

## Not added

These kit ideas conflict with current behavior. They stay out of the schema until `docs/REQUESTS.md` has an answer.

- Replacing `confidence` / `confidence_score` floats with `"agreed" | "disagreed" | "edited"`
- Replacing `call_type` strings with `L`, `C`, `TL`, `TL+`, `RTL`, `RTL+`, `TC`, `TC+`, `RTC`, `RTC+`
- Replacing `distance` plus `units` with `distance.parts[]`
- Replacing `x` / `y` with `northing` / `easting`
- A `units` object `{ plot, vara, chain }` on the version
- A structured `direction` object in place of the bearing string
- Requiring `firmId` on existing routes
- Treating Claude `bearing_decimal` as legal geometry

## Module boundaries

There is no `packages/` tree. Future code calls these modules:

| Kit name | This repo |
| --- | --- |
| `engine.solve` | A deterministic function in `deed-reader-web/backend/core/`. It does not exist yet. Closure helpers that exist today are in `services/plotting_service.py` and currently depend on AI numbers |
| `convertDistance` | `AdvancedDeedParser._convert_to_feet` converts during parse. New conversion for the solver belongs in `core/` and runs at the edge of the calculation |
| `forceClosure` | Not implemented |
| `reading.read` | `routes/document_routes.py` plus `services/claude_service.py` and `services/ocr_service.py` |
| Provider interface | `ClaudeService`. New provider calls go through it |
| `toDxf`, `toPointFile`, `toScript`, `toKml` | `AdvancedPlottingService._generate_dxf_data`, `_generate_csv_data`, `_generate_autocad_script`, `_generate_kml_data` |
| `toClosureReport`, `toCallTableXlsx` | Not implemented |
