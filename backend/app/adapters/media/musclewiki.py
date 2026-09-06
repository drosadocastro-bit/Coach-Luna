import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from app.adapters.media.base import ProviderExercise, ProviderVideo


class MuscleWikiError(RuntimeError):
    pass


class MuscleWikiClient:
    """Small, cache-agnostic MuscleWiki adapter. API keys never leave this module."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None, timeout: float = 20):
        self.api_key = api_key or os.getenv("MUSCLEWIKI_API_KEY")
        if not self.api_key:
            raise MuscleWikiError("MUSCLEWIKI_API_KEY is not configured")
        self.base_url = (base_url or os.getenv("MUSCLEWIKI_BASE_URL", "https://api.musclewiki.com")).rstrip("/")
        self.timeout = timeout
        self.calls = 0

    @staticmethod
    def normalize_query(query: str) -> str:
        return re.sub(r"[^a-z0-9]+", "_", query.lower()).strip("_")

    def _get_json(self, path: str, params: dict[str, str]) -> object:
        url = f"{self.base_url}{path}?{urllib.parse.urlencode(params)}"
        request = urllib.request.Request(url, headers={"X-API-Key": self.api_key, "Accept": "application/json", "User-Agent": "CoachLuna/0.1 (media-audit)"})
        self.calls += 1
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                return json.load(response)
        except urllib.error.HTTPError as error:
            body = error.read().decode("utf-8", "replace")[:500]
            raise MuscleWikiError(f"MuscleWiki HTTP {error.code}: {body}") from None
        except urllib.error.URLError as error:
            raise MuscleWikiError(f"MuscleWiki network error: {error.reason}") from None

    @staticmethod
    def parse_exercise(item: dict) -> ProviderExercise:
        videos = tuple(ProviderVideo(url=v["url"], angle=v.get("angle"), gender=v.get("gender"), poster_url=v.get("og_image")) for v in item.get("videos", []) if isinstance(v, dict) and v.get("url"))
        return ProviderExercise(provider_id=str(item.get("id")), name=str(item.get("name", "")), primary_muscles=tuple(str(m) for m in item.get("primary_muscles", [])), equipment=item.get("category"), videos=videos, raw=item)

    def search_exercises(self, query: str) -> list[ProviderExercise]:
        payload = self._get_json("/search", {"q": query, "limit": "10"})
        if not isinstance(payload, list):
            payload = payload.get("results", []) if isinstance(payload, dict) else []
        return [self.parse_exercise(item) for item in payload if isinstance(item, dict)]

    def get_exercise(self, provider_id: str) -> ProviderExercise:
        payload = self._get_json(f"/exercises/{urllib.parse.quote(provider_id)}", {})
        if not isinstance(payload, dict):
            raise MuscleWikiError(f"Unexpected exercise response for {provider_id}")
        return self.parse_exercise(payload)

    def get_media(self, provider_id: str) -> tuple[ProviderVideo, ...]:
        return self.get_exercise(provider_id).videos
