from pydantic import BaseModel, ConfigDict, Field


class MediaVideo(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: str = "video"
    url: str
    angle: str
    available_angles: list[str]


class MediaResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")
    exercise_id: str
    available: bool
    provider: str | None = None
    canonical: MediaVideo | None = None
    alternates: list[dict] = Field(default_factory=list)
