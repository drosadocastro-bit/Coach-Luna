from fastapi import APIRouter, HTTPException, Request

from app.models.routine import DisplayItem, DisplayRoutine, RoutineRequest, RoutineResponse
from app.services.routine_engine import GenerationError, generate_routine
from app.services.routine_validator import validate_routine

router = APIRouter()


@router.post("/routines/generate", response_model=RoutineResponse)
def generate(body: RoutineRequest, request: Request):
    library = request.app.state.library.all()
    try:
        routine = generate_routine(body, library)
    except GenerationError as error:
        raise HTTPException(422, {"code": "insufficient_exercises", "message": str(error)}) from None
    validation = validate_routine(routine, body, library)
    if not validation.valid:
        raise HTTPException(422, {"code": "routine_validation_failed", "validation": validation.model_dump()})
    catalog = {e.id: e for e in library}
    return RoutineResponse(
        routine=DisplayRoutine(name=routine.name, estimated_duration_minutes=routine.estimated_duration_minutes,
                               exercises=[DisplayItem(**item.model_dump(), exercise=catalog[item.exercise_id]) for item in routine.exercises]),
        validation=validation,
    )
