import pytest

from app.services.routine_engine import GenerationError, generate_routine


def test_determinism_and_catalog_bounds(request_body, catalog):
    routine = generate_routine(request_body, catalog)
    assert routine == generate_routine(request_body, list(reversed(catalog)))
    assert routine == generate_routine(request_body, catalog)
    assert len(routine.exercises) == 5
    assert len({item.exercise_id for item in routine.exercises}) == 5
    lookup = {e.id: e for e in catalog}
    assert all(item.exercise_id in lookup for item in routine.exercises)
    assert all(set(lookup[item.exercise_id].equipment) <= set(request_body.equipment) for item in routine.exercises)
    assert all(set(lookup[item.exercise_id].primary_muscles) & set(request_body.target_muscles) for item in routine.exercises)
    assert len({lookup[item.exercise_id].movement_pattern for item in routine.exercises}) >= 3


def test_disabled_excluded(request_body, catalog):
    initial = generate_routine(request_body, catalog).exercises[0].exercise_id
    modified = [e.model_copy(update={"enabled": False}) if e.id == initial else e for e in catalog]
    assert initial not in [item.exercise_id for item in generate_routine(request_body, modified).exercises]


def test_insufficient(request_body, catalog):
    with pytest.raises(GenerationError, match="only 0"):
        generate_routine(request_body.model_copy(update={"equipment": ["mat"]}), catalog)
