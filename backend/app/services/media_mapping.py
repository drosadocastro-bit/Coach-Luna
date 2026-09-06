from datetime import datetime, timezone
from pathlib import Path
from typing import Literal
import json

from pydantic import Field

from app.models.exercise import StrictModel

MatchStatus = Literal["exact_match", "acceptable_variant", "no_match", "needs_review", "needs_provider_id"]
ReviewStatus = Literal["unreviewed", "approved", "rejected"]


class MediaMapping(StrictModel):
    exercise_id: str
    provider: str | None = None
    provider_exercise_id: str | None = None
    provider_exercise_name: str | None = None
    match_status: MatchStatus
    preferred_variant: Literal["female", "male", "mixed", "unavailable"] = "unavailable"
    preferred_angle: str | None = None
    available_angles: list[str] = Field(default_factory=list)
    review_status: ReviewStatus = "unreviewed"
    review_notes: str = ""
    last_verified: str | None = None
    primary_url: str | None = None
    poster_url: str | None = None
    alternates: list[dict] = Field(default_factory=list)


MAPPING_PATH = Path(__file__).resolve().parents[1] / "data" / "media_mappings.json"


def load_mappings(path: Path = MAPPING_PATH) -> dict[str, MediaMapping]:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return {exercise_id: MediaMapping.model_validate({"exercise_id": exercise_id, **value}) for exercise_id, value in payload.items()}


def save_mappings(mappings: dict[str, MediaMapping], path: Path = MAPPING_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    # Playback URLs are runtime provider data; persist identity/provenance only.
    transient = {"primary_url", "poster_url"}
    path.write_text(json.dumps({key: value.model_dump(exclude={"exercise_id", *transient}, exclude_none=True) for key, value in sorted(mappings.items())}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def unavailable_mapping(exercise_id: str, note: str = "No suitable provider candidate found") -> MediaMapping:
    return MediaMapping(exercise_id=exercise_id, match_status="no_match", review_notes=note, last_verified=datetime.now(timezone.utc).isoformat())
