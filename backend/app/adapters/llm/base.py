from typing import Protocol

from app.models.routine import RoutineRequest


class IntentAdapter(Protocol):
    """Future provider boundary. Providers parse intent, never select exercises."""

    async def parse_intent(self, text: str, language: str) -> RoutineRequest: ...
