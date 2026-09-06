import json


def test_six_review_decisions_are_safe():
    mappings = json.loads(open("app/data/media_mappings.json", encoding="utf-8").read())
    assert mappings["bulgarian_split_squat"]["provider_exercise_name"] == "Dumbbell Bulgarian Split Squat"
    assert mappings["db_deadlift"]["match_status"] == "no_match"
    assert mappings["db_deadlift"]["review_status"] == "rejected"
    assert mappings["db_deadlift"]["provider_exercise_id"] == "291"
    assert mappings["hammer_curl"]["provider_exercise_id"] == "3"
    assert mappings["incline_press"]["provider_exercise_id"] == "398"
    assert mappings["russian_twist"]["review_status"] == "approved"
    assert mappings["shoulder_press"]["match_status"] == "needs_provider_id"
    assert mappings["shoulder_press"].get("provider_exercise_id") is None


def test_removed_dead_bug_is_not_in_authoritative_seed(catalog):
    assert len(catalog) == 25
    assert all(exercise.id != "dead_bug" for exercise in catalog)
