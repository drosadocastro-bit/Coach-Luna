from app.adapters.media.base import ProviderExercise, ProviderVideo
from app.services.media_service import MediaService


class FakeClient:
    def __init__(self):
        self.calls = 0

    def get_media(self, provider_id):
        self.calls += 1
        return (
            ProviderVideo("https://cdn.example/stream/291-side.mp4", "side", "female"),
            ProviderVideo("https://cdn.example/stream/291-front.mp4", "front", "male"),
        )

    def create_media_token(self):
        self.calls += 1
        return "runtime-token", 900


def test_media_endpoint_pilot_and_runtime_token(client):
    fake = FakeClient()
    client.app.state.media_service = MediaService(client.app.state.library, lambda: fake)
    response = client.get("/exercises/db_rdl_001/media?angle=side")
    assert response.status_code == 200
    payload = response.json()
    assert payload["available"] is True
    assert payload["canonical"]["angle"] == "side"
    assert "token=runtime-token" in payload["canonical"]["url"]
    assert "MUSCLEWIKI" not in response.text
    assert fake.calls == 2
    assert client.get("/exercises/db_rdl_001/media?angle=side").json() == payload
    assert fake.calls == 2


def test_media_endpoint_only_pilot_and_unknown(client):
    assert client.get("/exercises/goblet_squat/media").json()["available"] is False
    assert client.get("/exercises/does_not_exist/media").status_code == 404


def test_media_service_rejected_mapping_is_unavailable(client):
    fake = FakeClient()
    client.app.state.media_service = MediaService(client.app.state.library, lambda: fake)
    payload = client.get("/exercises/db_deadlift/media").json()
    assert payload["available"] is False
    assert fake.calls == 0
