from fastapi import APIRouter, HTTPException, Request

from app.models.media import MediaResponse

router = APIRouter()


@router.get("/exercises/{exercise_id}/media", response_model=MediaResponse)
def media(exercise_id: str, request: Request, angle: str | None = None):
    exercise = request.app.state.library.get(exercise_id)
    if exercise is None or not exercise.enabled:
        raise HTTPException(404, "Exercise not found")
    return request.app.state.media_service.resolve(exercise_id, angle)
