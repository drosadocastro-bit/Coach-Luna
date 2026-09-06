import time
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

from app.adapters.media.musclewiki import MuscleWikiClient, MuscleWikiError
from app.models.media import MediaResponse, MediaVideo
from app.services.media_mapping import load_mappings


class MediaService:
    PILOT_IDS = {"db_rdl_001"}

    def __init__(self, library, client_factory=MuscleWikiClient):
        self.library = library
        self.client_factory = client_factory
        self._client = None
        self._token: tuple[str, float] | None = None
        self._cache: dict[tuple[str, str], MediaVideo] = {}

    def _get_client(self):
        if self._client is None:
            try:
                self._client = self.client_factory()
            except MuscleWikiError:
                return None
        return self._client

    @staticmethod
    def _with_token(url: str, token: str) -> str:
        parts = urlsplit(url)
        query = dict(parse_qsl(parts.query))
        query["token"] = token
        return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))

    def resolve(self, exercise_id: str, angle: str | None = None) -> MediaResponse:
        if exercise_id not in self.PILOT_IDS:
            return MediaResponse(exercise_id=exercise_id, available=False)
        mapping = load_mappings().get(exercise_id)
        if not mapping or mapping.review_status != "approved" or mapping.provider != "musclewiki" or not mapping.provider_exercise_id or mapping.match_status in {"no_match", "needs_provider_id"}:
            return MediaResponse(exercise_id=exercise_id, available=False)
        preferred = angle or mapping.preferred_angle or (mapping.available_angles[0] if mapping.available_angles else None)
        if not preferred:
            return MediaResponse(exercise_id=exercise_id, available=False)
        cached = self._cache.get((exercise_id, preferred))
        if cached:
            return MediaResponse(exercise_id=exercise_id, available=True, provider="musclewiki", canonical=cached, alternates=mapping.alternates)
        client = self._get_client()
        if client is None:
            return MediaResponse(exercise_id=exercise_id, available=False)
        try:
            videos = client.get_media(mapping.provider_exercise_id)
            candidates = [v for v in videos if "/stream/" in v.url]
            angles = sorted({v.angle for v in candidates if v.angle})
            selected = next((v for v in candidates if v.angle == preferred and (v.gender or "").lower() == "female"), None)
            selected = selected or next((v for v in candidates if v.angle == preferred), None)
            if selected is None:
                selected = next((v for v in candidates if (v.gender or "").lower() == "female"), None) or (candidates[0] if candidates else None)
            if selected is None:
                return MediaResponse(exercise_id=exercise_id, available=False)
            now = time.time()
            if not self._token or self._token[1] <= now + 10:
                token, expires = client.create_media_token()
                self._token = (token, now + max(30, expires))
            chosen_angle = selected.angle or preferred
            video = MediaVideo(url=self._with_token(selected.url, self._token[0]), angle=chosen_angle, available_angles=angles or [chosen_angle])
            self._cache[(exercise_id, preferred)] = video
            return MediaResponse(exercise_id=exercise_id, available=True, provider="musclewiki", canonical=video, alternates=mapping.alternates)
        except (MuscleWikiError, ValueError, TypeError):
            return MediaResponse(exercise_id=exercise_id, available=False)
