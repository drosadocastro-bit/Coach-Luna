from collections import Counter

from app.models.exercise import Exercise
from app.models.routine import Routine, RoutineItem, RoutineRequest


class GenerationError(ValueError):
    pass


def experience_allows(request: RoutineRequest, exercise: Exercise) -> bool:
    levels = {"beginner": 0, "beginner_intermediate": 0, "intermediate": 1, "advanced": 2}
    return levels[exercise.difficulty] <= levels[request.experience_level]


def generate_routine(request: RoutineRequest, library: list[Exercise]) -> Routine:
    eligible = [e for e in library if e.enabled and set(e.equipment) <= set(request.equipment) and experience_allows(request, e)]
    if len(eligible) < request.exercise_count:
        raise GenerationError(f"Requested {request.exercise_count} exercises, but only {len(eligible)} are eligible for the available equipment and experience level.")
    selected: list[Exercise] = []
    patterns: Counter = Counter()
    uncovered = set(request.target_muscles)
    targets = set(request.target_muscles)
    while len(selected) < request.exercise_count:
        # Uncovered primary targets first; primary matches outweigh secondary matches.
        # Movement diversity breaks muscle-match ties; ID is the final stable tie-breaker.
        def rank(e):
            return (-len(uncovered & set(e.primary_muscles)),
                    -(3 * len(targets & set(e.primary_muscles)) + len(targets & set(e.secondary_muscles))),
                    patterns[e.movement_pattern], e.id)
        exercise = sorted(eligible, key=rank)[0]
        selected.append(exercise)
        eligible.remove(exercise)
        patterns[exercise.movement_pattern] += 1
        uncovered -= set(exercise.primary_muscles)
    return Routine(
        name=" + ".join(m.replace("_", " ").title() for m in request.target_muscles),
        estimated_duration_minutes=sum(e.default_sets * 3 for e in selected),
        exercises=[RoutineItem(exercise_id=e.id, sets=e.default_sets, rep_min=e.rep_min, rep_max=e.rep_max) for e in selected],
    )
