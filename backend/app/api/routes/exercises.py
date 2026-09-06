from fastapi import APIRouter, HTTPException, Request

from app.models.exercise import Equipment, Exercise, Muscle

router = APIRouter()


@router.get("/exercises", response_model=list[Exercise])
def exercises(request: Request, muscle: Muscle | None = None, equipment: Equipment | None = None):
    return [e for e in request.app.state.library.all() if e.enabled
            and (muscle is None or muscle in e.primary_muscles + e.secondary_muscles)
            and (equipment is None or equipment in e.equipment)]


@router.get("/exercises/{exercise_id}", response_model=Exercise)
def exercise(exercise_id: str, request: Request):
    result = request.app.state.library.get(exercise_id)
    if result is None or not result.enabled:
        raise HTTPException(404, "Exercise not found")
    return result
