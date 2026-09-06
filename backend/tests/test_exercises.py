import sqlite3

from app.services.exercise_library import ExerciseLibrary


def test_seed(catalog):
    assert len(catalog) == 25
    ids = {e.id for e in catalog}
    assert len(ids) == 25
    for e in catalog:
        assert e.name and e.display_name_es and e.primary_muscles and e.equipment
        assert e.instructions_en and e.instructions_es and e.common_mistakes_en and e.common_mistakes_es
        assert e.video.uri is None and e.video.angles
        assert set(e.alternatives) <= ids


def test_sqlite_persists_edits(tmp_path):
    library = ExerciseLibrary(tmp_path / "catalog.db")
    library.initialize()
    exercise = library.all()[0].model_copy(update={"enabled": False})
    with sqlite3.connect(library.database_path) as connection:
        connection.execute("UPDATE exercises SET payload=? WHERE id=?", (exercise.model_dump_json(), exercise.id))
    library.initialize()
    assert len(library.all()) == 25
    assert library.get(exercise.id).enabled is False
