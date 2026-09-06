from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class ProviderVideo:
    url: str
    angle: str | None
    gender: str | None
    poster_url: str | None = None


@dataclass(frozen=True)
class ProviderExercise:
    provider_id: str
    name: str
    primary_muscles: tuple[str, ...]
    equipment: str | None
    videos: tuple[ProviderVideo, ...]
    raw: dict


class MediaProvider(Protocol):
    def search_exercises(self, query: str) -> list[ProviderExercise]: ...
    def get_exercise(self, provider_id: str) -> ProviderExercise: ...
    def get_media(self, provider_id: str) -> tuple[ProviderVideo, ...]: ...
