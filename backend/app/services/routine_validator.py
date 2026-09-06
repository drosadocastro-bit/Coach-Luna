from collections import Counter

from app.models.exercise import Exercise
from app.models.routine import Routine, RoutineRequest, ValidationResult


def validate_routine(routine: Routine, request: RoutineRequest, library: list[Exercise]) -> ValidationResult:
    catalog = {e.id: e for e in library}
    errors, warnings = [], []
    ids = [item.exercise_id for item in routine.exercises]
    if len(ids) != request.exercise_count or not 1 <= len(ids) <= 10:
        errors.append("Exercise count does not match the request")
    if len(ids) != len(set(ids)):
        errors.append("Duplicate exercise IDs")
    represented = set()
    patterns: Counter = Counter()
    level = {"beginner": 0, "beginner_intermediate": 0, "intermediate": 1, "advanced": 2}
    for item in routine.exercises:
        exercise = catalog.get(item.exercise_id)
        if exercise is None:
            errors.append(f"Unknown exercise: {item.exercise_id}")
            continue
        if not exercise.enabled:
            errors.append(f"Disabled exercise: {exercise.id}")
        if not set(exercise.equipment) <= set(request.equipment):
            errors.append(f"Equipment mismatch: {exercise.id}")
        if level[exercise.difficulty] > level[request.experience_level]:
            errors.append(f"Experience mismatch: {exercise.id}")
        if not (1 <= item.sets <= 6 and 1 <= item.rep_min <= item.rep_max <= 30):
            errors.append(f"Unreasonable sets/reps: {exercise.id}")
        if (item.sets, item.rep_min, item.rep_max) != (exercise.default_sets, exercise.rep_min, exercise.rep_max):
            errors.append(f"Prescription differs from catalog: {exercise.id}")
        represented.update(exercise.primary_muscles)
        patterns[exercise.movement_pattern] += 1
    missing = sorted(set(request.target_muscles) - represented)
    if missing:
        errors.append("Targets lack primary muscle representation: " + ", ".join(missing))
    if any(count > 2 for count in patterns.values()):
        warnings.append("More than two exercises share a movement pattern")
    if routine.estimated_duration_minutes > request.duration_minutes:
        warnings.append("Estimated workout exceeds requested duration; reduce exercise count or allow more time")
    warnings.append("Phase 0 uses catalog prescriptions for all goals; duration is an estimate including rest")
    return ValidationResult(valid=not errors, errors=errors, warnings=warnings)
