import json

from app.adapters.media.musclewiki import MuscleWikiClient
from app.services.media_cache import JsonMediaCache
from app.services.media_mapping import MediaMapping, load_mappings, save_mappings


def test_provider_parser_prefers_neutral_internal_shape():
    result = MuscleWikiClient.parse_exercise({"id": 11, "name": "Dumbbell Goblet Squat", "primary_muscles": ["Glutes"], "category": "Dumbbells", "videos": [{"url": "https://example/video.mp4", "angle": "side", "gender": "female", "og_image": "https://example/poster.jpg"}]})
    assert result.provider_id == "11"
    assert result.videos[0].gender == "female"
    assert result.raw["id"] == 11


def test_cache_hit_miss_and_malformed(tmp_path):
    cache = JsonMediaCache(tmp_path)
    assert cache.get("goblet_squat") is None
    cache.put("goblet_squat", [{"id": 11}])
    assert cache.get("goblet_squat") == [{"id": 11}]
    (tmp_path / "broken.json").write_text("{bad", encoding="utf-8")
    assert cache.get("broken") is None
    assert (cache.hits, cache.misses) == (1, 2)


def test_mapping_storage_omits_runtime_urls(tmp_path):
    path = tmp_path / "mappings.json"
    save_mappings({"goblet_squat": MediaMapping(exercise_id="goblet_squat", provider="musclewiki", provider_exercise_id="11", match_status="exact_match", primary_url="https://example/video.mp4")}, path)
    raw = path.read_text(encoding="utf-8")
    assert "primary_url" not in raw and "https://" not in raw
    assert load_mappings(path)["goblet_squat"].provider_exercise_id == "11"
