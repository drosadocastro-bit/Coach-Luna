import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.models.routine import RoutineRequest
from app.services.exercise_library import ExerciseLibrary, load_seed


@pytest.fixture
def catalog():
    return load_seed()


@pytest.fixture
def request_body():
    return RoutineRequest(target_muscles=["glutes", "hamstrings"], duration_minutes=45, equipment=["dumbbells", "bench"], experience_level="beginner", goal="strength", exercise_count=5)


@pytest.fixture
def client(tmp_path):
    with TestClient(create_app(ExerciseLibrary(tmp_path / "test.db"))) as test_client:
        yield test_client
