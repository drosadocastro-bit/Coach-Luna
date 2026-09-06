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
