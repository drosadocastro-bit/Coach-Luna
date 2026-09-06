import pytest


def test_health(client):
    assert client.get("/health").json() == {"status": "ok", "service": "coach-luna-api"}


def test_exercises(client):
    response = client.get("/exercises")
    assert response.status_code == 200
    assert len(response.json()) == 25
    assert client.get("/exercises/db_rdl_001").json()["display_name_es"]
    assert client.get("/exercises/missing").status_code == 404
    for row in client.get("/exercises?muscle=glutes&equipment=dumbbells").json():
        assert "glutes" in row["primary_muscles"] + row["secondary_muscles"]
        assert "dumbbells" in row["equipment"]
    assert client.get("/exercises?equipment=spaceship").status_code == 422


def test_generate(client, request_body):
    response = client.post("/routines/generate", json=request_body.model_dump())
    assert response.status_code == 200
    assert response.json()["validation"]["valid"]
    assert len(response.json()["routine"]["exercises"]) == 5
    assert response.json() == client.post("/routines/generate", json=request_body.model_dump()).json()


@pytest.mark.parametrize("field,value", [("duration_minutes", -1), ("duration_minutes", 12.5), ("exercise_count", 26), ("equipment", ["unknown"]), ("target_muscles", []), ("target_muscles", ["glutes", "glutes"]), ("goal", "magic")])
def test_invalid(client, request_body, field, value):
    payload = request_body.model_dump()
    payload[field] = value
    assert client.post("/routines/generate", json=payload).status_code == 422


def test_malformed_and_infeasible(client, request_body):
    assert client.post("/routines/generate", content="{bad", headers={"Content-Type": "application/json"}).status_code == 422
    request_body.equipment = ["mat"]
    result = client.post("/routines/generate", json=request_body.model_dump())
    assert result.status_code == 422
    assert result.json()["detail"]["code"] == "insufficient_exercises"
    request_body.equipment = ["dumbbells"]
    request_body.target_muscles = ["calves"]
    result = client.post("/routines/generate", json=request_body.model_dump())
    assert result.status_code == 422
    assert result.json()["detail"]["validation"]["valid"] is False


def test_browser_cors(client):
    headers = {"Origin": "http://localhost:8081", "Access-Control-Request-Method": "POST", "Access-Control-Request-Headers": "content-type"}
    result = client.options("/routines/generate", headers=headers)
    assert result.status_code == 200
    assert result.headers["access-control-allow-origin"] == "http://localhost:8081"
    headers["Origin"] = "https://untrusted.example"
    assert client.options("/routines/generate", headers=headers).status_code == 400
