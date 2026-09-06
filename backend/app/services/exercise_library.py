import json
import sqlite3
from pathlib import Path

from app.models.exercise import Exercise

SEED_PATH = Path(__file__).resolve().parents[1] / "data" / "exercises.json"


def load_seed(path: Path = SEED_PATH) -> list[Exercise]:
    exercises = [Exercise.model_validate(row) for row in json.loads(path.read_text(encoding="utf-8"))]
    ids = {exercise.id for exercise in exercises}
    if len(ids) != len(exercises):
        raise ValueError("Duplicate exercise IDs in seed")
    for exercise in exercises:
        if any(alt not in ids or alt == exercise.id for alt in exercise.alternatives):
            raise ValueError(f"Invalid alternative for {exercise.id}")
    return exercises


class ExerciseLibrary:
    """SQLite catalog, seeded once. Existing database rows remain authoritative."""

    def __init__(self, database_path: Path):
        self.database_path = database_path

    def initialize(self):
        self.database_path.parent.mkdir(parents=True, exist_ok=True)
        seed = load_seed()
        with sqlite3.connect(self.database_path) as connection:
            connection.execute("CREATE TABLE IF NOT EXISTS exercises (id TEXT PRIMARY KEY, payload TEXT NOT NULL)")
            existing = {row[0] for row in connection.execute("SELECT id FROM exercises")}
            missing = [(e.id, e.model_dump_json()) for e in seed if e.id not in existing]
            if missing:
                connection.executemany("INSERT INTO exercises VALUES (?, ?)", missing)

    def all(self) -> list[Exercise]:
        with sqlite3.connect(self.database_path) as connection:
            rows = connection.execute("SELECT payload FROM exercises ORDER BY id").fetchall()
        return [Exercise.model_validate_json(row[0]) for row in rows]

    def get(self, exercise_id: str) -> Exercise | None:
        return next((e for e in self.all() if e.id == exercise_id), None)
