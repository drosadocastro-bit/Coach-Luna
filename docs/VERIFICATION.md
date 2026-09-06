# Phase 0 verification — 2026-09-06

## Verified

- WSL2 Ubuntu, Python 3.12.3; isolated Linux venv and fully pinned requirements.
- `python -m pytest -q`: **27 passed**, 2 dependency deprecation warnings, 0 failures (0.90 seconds test execution).
- Coverage includes 25 valid seeds, unique IDs, bilingual fields, alternative integrity, SQLite persistence, deterministic/reordered-library output, enabled/equipment/count/target rules, insufficient candidates, independent validator mutations, duration/experience checks, endpoints, malformed/invalid input and browser CORS.
- FastAPI launches under WSL. `/health` returns `{"status":"ok","service":"coach-luna-api"}`.
- On this machine, Windows owns port 8000 and returns Microsoft-HTTPAPI 400. Live Windows-to-WSL testing uses **8001**, without changing the existing Windows service.
- `npm.cmd run typecheck`: passed.
- `npx.cmd expo install --check`: dependencies up to date.
- `npx.cmd expo-doctor`: **21/21 checks passed**.
- `npm.cmd run export`: successful web, Android and iOS bundles. These are bundle exports, not installed native binaries.
- Live Expo Web → WSL FastAPI → SQLite catalog → deterministic engine → independent validator → workout display: passed at `http://localhost:8081` using backend port 8001.
- Default request displayed five exercises: Dumbbell Deadlift, Dumbbell Romanian Deadlift, Dumbbell Glute Bridge, Dumbbell Reverse Lunge and Dumbbell Hip Thrust.
- Browser interaction verified completion changing from 0/5 to 1/5, Spanish workout labels, Spanish exercise detail cues/mistakes, alternative detail navigation and return preserving the completion state.
- Infeasible equipment input returned a localized error. A backend connection failure also displayed a recoverable error during networking diagnosis.
- Phone-width browser check at 390 × 844 reported body width 390, without horizontal document overflow. Browser viewport restored afterward.
- No OpenAI or ElevenLabs dependency, provider integration or actual provider key was added. Every exercise video URI is null; no exercise media was downloaded.
- Runtime SQLite DB, venv, `.env`, node_modules and export output are ignored by Git.
- MuscleWiki pilot search succeeded using the configured backend-only key. The controlled 25-exercise audit used 25 API calls, then a classifier correction reran from cache with 0 calls (25 cache hits, 0 misses). Adding `barbell_bench_press` used 1 additional API call (25 cache hits, 1 miss). The original 25 discovery set classified as 9 exact, 1 acceptable variant, 6 needs review and 9 no match; the new barbell bench press is an exact match. Thirteen canonical pilot mappings are now approved; no unapproved media is exposed. Persisted mappings contain no provider playback URLs.
- The pilot response confirmed MuscleWiki returns exercise IDs, names, equipment categories, muscles, video URLs, angles and gender variants. Female videos were preferred for discovery where available. This is provider discovery only; licensing and human review are still required.

## Native acceptance

Native acceptance is now **verified on Android and iPhone**. Both devices reached the FastAPI backend over the local network and completed the mobile flow: workout generation, bilingual language switching, exercise details, alternatives, completion/undo and return navigation. This confirms the backend connection and app flow on both target mobile platforms. Device model, OS and Expo Go versions were not recorded in this session.

## GitHub baseline

Phase 0 is functionally complete and native device acceptance is verified on Android and iPhone. The initial baseline commit retains `native QA pending` in its historical message; this follow-up records the completed acceptance without changing the implementation. No automatic push is authorized.

The approved Coach Luna hero image is included unchanged in `docs/assets/coach-luna-hero.png` and `mobile/assets/coach-luna-hero.png`. It is branding artwork, not exercise demonstration media. No exercise videos have been added.

## Known compromises and dependency findings

- Greedy deterministic scoring, no exhaustive optimization; metadata sets/reps shared across goals; approximate duration and explicit overrun warning.
- SQLite JSON payload table; normalized schema, migrations and PostgreSQL conversion deferred.
- Three state-based screens, no deep links; completion and workouts are session-only. Alternative browsing does not perform replacements.
- `bench` does not encode adjustability as a separate equipment type; incline exercise cues and form help explain the requirement.
- Template icons remain; exercise demos are placeholders; catalog cues await professional review before broader testing.
- Starlette's current TestClient warns about the requested `httpx` dependency and an upstream AnyIO alias. Tests pass; no extra HTTP client dependency was added.
- `npm audit` reports **10 moderate transitive findings** through Expo's xcode/uuid tooling, with no high/critical findings. The proposed automatic remediation downgrades Expo to SDK 46, so it was not applied. Recheck an SDK-compatible upstream fix before native distribution. Do not use `npm audit fix --force` without reviewing its changes.
- MuscleWiki discovery uses `backend/.cache/musclewiki/` and is ignored. The raw audit report is ignored under `backend/reports/`; regenerate locally with `python scripts/audit_musclewiki_catalog.py`. No provider payload or key is committed.
- Six additional human review decisions were applied from the cached audit without provider calls: Bulgarian Split Squat approved to the canonical dumbbell variant; Dumbbell Deadlift rejected against the Romanian Deadlift candidate; Hammer Curl approved to Dumbbell Hammer Curl; Incline Dumbbell Press approved to the standard cached candidate (ID 398) and guillotine variant rejected; Russian Twist canonical approved with feet-down alternate; Shoulder Press approved conceptually but held at `needs_provider_id` because Dumbbell Overhead Press has no verified ID in the existing cache. This batch is 5 approved decisions and 1 rejected/no-approved mapping. Rejected provenance remains recorded; Phase 1B playback is not complete.
- Final cached review batch applied the remaining decisions without API calls: Dumbbell Curl, Dumbbell Laying Incline Row, Dumbbell Farmer Walk, Dumbbell Single Arm Row, Dumbbell Step Up, Dumbbell Overhead Tricep Extension and Walking Lunge were approved as canonical/acceptable reviewed names; Single Leg Single Arm Deadlift was approved as an acceptable variant (cached ID 461); conventional Dumbbell Deadlift remains rejected while Kettlebell Conventional Deadlift (Double) is retained as a named acceptable equipment alternate; Dumbbell Dead Bug was removed from the authoritative catalog, with its historical mapping retained as rejected provenance. Missing provider IDs remain non-runtime eligible.
