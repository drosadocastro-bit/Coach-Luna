import pytest

from app.services.routine_engine import generate_routine
from app.services.routine_validator import validate_routine


def test_accepts_generated(request_body, catalog):
    assert validate_routine(generate_routine(request_body, catalog), request_body, catalog).valid


@pytest.mark.parametrize("mutation,expected", [("duplicate", "Duplicate"), ("unknown", "Unknown"), ("equipment", "Equipment"), ("count", "count"), ("reps", "Unreasonable"), ("metadata", "catalog"), ("disabled", "Disabled"), ("targets", "representation")])
def test_rejects_mutations(request_body, catalog, mutation, expected):
    routine = generate_routine(request_body, catalog)
    if mutation == "duplicate":
        routine.exercises[1] = routine.exercises[0]
    elif mutation == "unknown":
        routine.exercises[0].exercise_id = "invented"
    elif mutation == "equipment":
        request_body.equipment = ["mat"]
    elif mutation == "count":
        routine.exercises.pop()
    elif mutation == "reps":
        routine.exercises[0].rep_min = -1
    elif mutation == "metadata":
        routine.exercises[0].sets = 2
    elif mutation == "disabled":
        catalog = [e.model_copy(update={"enabled": False}) for e in catalog]
    elif mutation == "targets":
        request_body.target_muscles = ["chest"]
    result = validate_routine(routine, request_body, catalog)
    assert not result.valid
    assert any(expected in error for error in result.errors)


def test_duration_warning_and_experience(request_body, catalog):
    routine = generate_routine(request_body, catalog)
    request_body.duration_minutes = 10
    result = validate_routine(routine, request_body, catalog)
    assert result.valid and any("duration" in warning for warning in result.warnings)
    selected_id = routine.exercises[0].exercise_id
    modified = [e.model_copy(update={"difficulty": "advanced"}) if e.id == selected_id else e for e in catalog]
    result = validate_routine(routine, request_body, modified)
    assert not result.valid and any("Experience" in error for error in result.errors)
