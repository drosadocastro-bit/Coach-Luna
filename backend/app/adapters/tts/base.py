from typing import Protocol


class SpeechAdapter(Protocol):
    """Future backend-only speech boundary; no provider implementation in Phase 0."""

    async def synthesize(self, text: str, language: str) -> bytes: ...
