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
