# Backend

Run from WSL2 at `/mnt/d/CoachLuna/backend` using Python 3.11/3.12:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m pytest -q
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

`requirements.txt` pins direct and transitive dependencies. SQLite uses Python's standard library. `COACH_LUNA_DATABASE_PATH` overrides its location. `COACH_LUNA_CORS_ORIGINS` accepts a JSON list of exact web origins; the defaults allow localhost and 127.0.0.1 on port 8081. Native apps are not governed by browser CORS.

The JSON seed is validated before import. SQLite stores an ID primary key plus the complete Pydantic-validated JSON payload. It is seeded only when empty, in a transaction; existing records are never overwritten on restart. `python seed_catalog.py` rebuilds the JSON fixture, not the live database. For a disposable development reset, stop the backend and rename `coach_luna.db` to a backup before restarting. Do not reset a database containing data you need.

Normalized relational columns and migrations are deferred; the stable IDs and typed fields support later PostgreSQL migration. Tests each use an isolated temporary SQLite file.

Example request:

```bash
curl http://localhost:8000/routines/generate \
  -H 'Content-Type: application/json' \
  -d '{"target_muscles":["glutes","hamstrings"],"duration_minutes":45,"equipment":["dumbbells","bench"],"experience_level":"beginner","goal":"strength","exercise_count":5}'
```

Generation filters enabled records by all required equipment and experience, ranks uncovered primary targets first, then muscle matches, pattern reuse and ID. Validation is a separate module that checks catalog membership, duplicates, equipment, experience, exact count, reasonable/canonical prescriptions and primary target representation. It reports duration/pattern compromises as warnings. The API adds exercise details only after validation succeeds.

Request bounds: 10–120 minutes, 1–10 exercises, nonempty unique target/equipment lists, known literals only. Unknown IDs return 404; invalid requests and infeasible routines return 422. Server debug mode is disabled, so unexpected failures do not return stack traces.

Provider keys are not read or needed in this phase. Future adapters are Python protocols only. Networking and device instructions: [local networking](../docs/LOCAL_NETWORKING.md).
