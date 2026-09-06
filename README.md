# Coach Luna

Coach Luna is a bilingual English/Spanish mobile AI fitness coach for iPhone and Android, designed to be warm, motivating, grounded, visual-first, and safe by construction.

The current architecture uses a deterministic workout engine and an independent validator, with backend adapter interfaces prepared for future OpenAI and ElevenLabs integrations. Coach Luna's identity is independent of any model, provider or other project.

![Coach Luna](docs/assets/coach-luna-hero.png)

## Current Status

**Phase 0 is functionally complete but native device acceptance is pending.**

Recorded Phase 0 verification:

- 27 backend tests passed.
- TypeScript validation passed.
- Expo Doctor: 21/21 checks passed.
- Web preview and workout generation verified.
- Bilingual exercise details and exercise alternatives verified.
- Session-only completion tracking verified.
- Native Android testing pending.
- Native iPhone testing pending.

No OpenAI or ElevenLabs integration is active yet. Native bundle exports do not establish native device acceptance. See [verification results and known limitations](docs/VERIFICATION.md).

## Phase 0

Expo React Native + TypeScript → FastAPI → deterministic routine engine → independent validator → validated JSON → mobile workout and exercise details. A SQLite exercise catalog is seeded with 25 bilingual exercises. No external providers are called.

## Run the backend (WSL2 Ubuntu)

Use Python 3.11 or 3.12. The bootstrap was tested on Python 3.12.3.

```bash
cd /mnt/d/CoachLuna/backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

On Ubuntu, install `python3-venv` using your package manager if venv support is missing. The existing `.venv` is a Linux environment; do not run it with Windows Python. Use VS Code's WSL extension: run `code .` from `/mnt/d/CoachLuna`.

Open [health](http://localhost:8000/health) or [API documentation](http://localhost:8000/docs). The first startup seeds `backend/coach_luna.db`; later starts preserve database edits. See [backend README](backend/README.md).

**This machine:** Windows already occupies port 8000. Use `--port 8001` here; the local ignored `mobile/.env` is configured for `http://localhost:8001`. The working health URL is [localhost:8001/health](http://localhost:8001/health). Keep that `.env` or edit the copied example accordingly.

## Run the mobile app (Windows PowerShell)

Node 22.13+ is required by the SDK 57 template; bootstrap used Node 24.13.0. See the [versioned Expo reference](https://docs.expo.dev/versions/v57.0.0/).

```powershell
cd D:\CoachLuna\mobile
npm.cmd ci
Copy-Item .env.example .env
# Edit .env: use the Windows LAN address for a physical device.
npm.cmd start
```

Scan the QR code in a compatible Expo Go client, or press `a` for a configured Android emulator. Windows cannot run an iOS simulator. `npm.cmd run web` opens the same React Native screens in a browser for local flow testing. `localhost` works for the Windows browser via WSL forwarding, but refers to the phone itself on a physical device. Follow [local networking](docs/LOCAL_NETWORKING.md) before device testing.

```powershell
npm.cmd run typecheck
npx.cmd expo install --check
npm.cmd run export
```

## Endpoints

| Method | Path | Behavior |
| --- | --- | --- |
| GET | `/health` | Service health |
| GET | `/exercises` | Enabled catalog; optional `muscle` and `equipment` filters |
| GET | `/exercises/{exercise_id}` | Enabled exercise or 404 |
| POST | `/routines/generate` | Generate, independently validate, then enrich with catalog data |

Invalid schema/JSON, unsupported combinations and unmet targets return 422. Failed generation includes a clear code and reason. No partial unvalidated routine is sent.

## Repository

```text
CoachLuna/
├── README.md, .gitignore, .env.example
├── docs/
│   ├── ARCHITECTURE.md
│   ├── PRODUCT.md
│   ├── ROADMAP.md
│   ├── LOCAL_NETWORKING.md
│   ├── VERIFICATION.md
│   └── assets/coach-luna-hero.png
├── backend/
│   ├── README.md, requirements.txt, pyproject.toml, seed_catalog.py
│   ├── app/
│   │   ├── main.py, config.py
│   │   ├── api/routes/{health,exercises,routines}.py
│   │   ├── models/{exercise,routine}.py
│   │   ├── services/{exercise_library,routine_engine,routine_validator}.py
│   │   ├── adapters/llm/base.py
│   │   ├── adapters/tts/base.py
│   │   └── data/exercises.json
│   └── tests/{conftest,test_exercises,test_routine_engine,test_routine_validator,test_api}.py
├── mobile/
│   ├── README.md, AGENTS.md, .env.example
│   ├── App.tsx, index.ts, app.json, package.json, package-lock.json, tsconfig.json
│   ├── assets/ (Expo template icons and approved coach-luna-hero.png)
│   └── src/
│       ├── api/coachLunaApi.ts
│       ├── config/environment.ts
│       ├── types/{exercise,routine}.ts
│       ├── components/{ExerciseCard,WorkoutHeader,VideoPlaceholder,ui}.tsx
│       ├── screens/{HomeScreen,WorkoutScreen,ExerciseScreen}.tsx
│       └── i18n.ts
└── media/
    ├── README.md
    └── exercise-demos/.gitkeep
```

Python package directories also contain `__init__.py`. Runtime databases, virtual environments, dependencies and exports are ignored.

## Boundaries and deliberate limitations

The catalog is authoritative. Generation never invents exercises or prescriptions and never certifies itself. Target coverage requires at least one primary-muscle exercise for every requested target. Greedy selection is predictable, not an exhaustive optimizer. Duration is estimated as three minutes per set; an overrun is reported. Goals share catalog prescriptions in Phase 0. Beginner requests exclude intermediate/advanced movements.

The mobile app uses three state-based screens without deep links. Completion is session-only. A bench means an appropriate stable bench; inclined movements require adjustability. A mat is optional. Carries use steps and unilateral movements use repetitions per side, explicitly displayed.

No OpenAI, ElevenLabs, authentication, payments, analytics, cloud hosting, real video playback, workout history or progression is implemented. Provider names in future planning do not guarantee model availability. Backend-only adapter protocols reserve those boundaries. `.env` files and databases are ignored; mobile configuration contains only a public API URL.

See [architecture](docs/ARCHITECTURE.md), [product contract](docs/PRODUCT.md), [roadmap](docs/ROADMAP.md), [media plan](media/README.md) and [verification](docs/VERIFICATION.md).
