# Architecture

```text
Mobile form
  ↓ typed request
FastAPI
  ↓
Deterministic engine ← SQLite exercise catalog ← validated JSON seed (first run)
  ↓ candidate routine
Independent validator ← same catalog + original request
  ↓ validated result
Response enrichment with authoritative exercise metadata
  ↓
Mobile workout and exercise details
```

The generator returns only IDs and prescriptions. It does not import or call the validator. The API orchestrates both and rejects invalid results with structured validation errors. IDs never come from free text. Disabled records cannot be selected or fetched as selectable exercises. List equipment filters mean “uses this equipment”; generation requires the entire equipment set to be available.

Primary target coverage is explicit: every requested target must appear in at least one selected exercise's primary muscles. Secondary-only coverage is insufficient. Pattern diversity breaks scoring ties; it does not override target coverage. The ID tie-breaker makes outputs repeatable even if database row order changes. Greedy selection can reject a request that an exhaustive search might solve; no search optimizer is claimed.

SQLite currently stores stable ID and validated JSON payload. A future migration will normalize exercise, muscle, equipment, instruction and alternative relationships into tables. There is no history table until Phase 4. JSON is the bootstrap fixture; the persisted catalog is authoritative after import.

## Future flow

```text
Mobile → FastAPI → Intent/LLM adapter → deterministic engine
       → independent validator → response formatter → TTS adapter
```

`IntentAdapter` maps text to `RoutineRequest`. `SpeechAdapter` maps approved text/language to audio bytes. They are protocols with no provider code, dependencies or network requests. OpenAI and ElevenLabs are possible future implementations; provider/model identifiers will be backend configuration after availability checks. Coach Luna's identity belongs to the product contract, independent of either provider.

Only the backend may access provider secrets. No provider key reaches the mobile bundle, response or public environment variables. No authentication or production exposure is part of Phase 0. LAN setup is explicitly scoped to development.

## Phase 1 media mapping

MuscleWiki is an initial media provider behind `app/adapters/media/musclewiki.py`; its schema is converted into Coach Luna's provider-neutral `ProviderExercise` and `ProviderVideo` types. `scripts/audit_musclewiki_catalog.py` searches once per normalized Coach Luna name, writes raw discovery responses to the ignored `.cache/musclewiki/` directory, and emits an ignored report under `backend/reports/`. It prints API calls, cache hits and misses and stops at `--max-api-calls` (30 by default).

The first live audit used 25 calls, then a corrected cached rerun used 0 calls. Adding the separate barbell bench press used 1 additional call. The original 25 results were 9 exact matches, 1 acceptable variant, 6 needs-review candidates and 9 no-match results; the new barbell bench press is an exact match. The report is discovery evidence; human review approved 13 canonical mappings. Persisted mappings omit runtime video/poster URLs. A future media service must resolve only approved identities and mint safe short-lived playback access in the backend. Ambiguous candidates, such as RDL versus conventional deadlift or bilateral versus single-arm press, remain `needs_review`.
