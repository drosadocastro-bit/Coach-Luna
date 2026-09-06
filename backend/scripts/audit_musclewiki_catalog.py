"""Discover and rank MuscleWiki candidates without approving ambiguous mappings.

Run from backend: python scripts/audit_musclewiki_catalog.py [--refresh] [--max-api-calls 30]
"""
import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parents[1] / ".env")

from app.adapters.media.musclewiki import MuscleWikiClient, MuscleWikiError
from app.services.exercise_library import load_seed
from app.services.media_cache import JsonMediaCache
from app.services.media_mapping import MediaMapping, save_mappings

CACHE_DIR = Path(__file__).resolve().parents[1] / ".cache" / "musclewiki"
REPORT_PATH = Path(__file__).resolve().parents[1] / "reports" / "musclewiki_catalog_audit.json"


def token_set(value: str) -> set[str]:
    return {token for token in value.lower().replace("-", " ").split() if token not in {"the", "with", "a", "an"}}


def rank(cl_exercise, candidate):
    name_overlap = len(token_set(cl_exercise.name) & token_set(candidate.name))
    muscle_overlap = len({m.lower() for m in cl_exercise.primary_muscles} & {m.lower() for m in candidate.primary_muscles})
    equipment_match = int(any(cl_equipment.lower().rstrip("s") in (candidate.equipment or "").lower() for cl_equipment in cl_exercise.equipment))
    exact = int(cl_exercise.name.lower() == candidate.name.lower())
    return (exact, name_overlap, muscle_overlap, equipment_match, -int(candidate.provider_id) if candidate.provider_id.isdigit() else 0)


def classify(cl_exercise, candidates):
    if not candidates:
        return None, "no_match"
    ranked = sorted(candidates, key=lambda candidate: rank(cl_exercise, candidate), reverse=True)
    best = ranked[0]
    score = rank(cl_exercise, best)
    coach_tokens = token_set(cl_exercise.name)
    provider_tokens = token_set(best.name)
    # Similar names can still describe a materially different movement.
    contradictory_pairs = [("romanian", "deadlift"), ("incline", "guillotine"), ("single", "bilateral"), ("one", "two"), ("band", "dumbbell"), ("kettlebell", "dumbbell")]
    if any((a in coach_tokens and b in provider_tokens and b not in coach_tokens) or (b in coach_tokens and a in provider_tokens and a not in coach_tokens) for a, b in contradictory_pairs):
        return best, "needs_review"
    if "single" in provider_tokens and "single" not in coach_tokens and "one" not in coach_tokens:
        return best, "needs_review"
    exact = score[0] == 1
    muscle = score[2] >= 1
    equipment = score[3] == 1
    if exact and muscle and equipment:
        status = "exact_match"
    elif score[1] >= 2 and muscle and equipment:
        status = "acceptable_variant"
    else:
        status = "needs_review"
    return best, status


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--refresh", action="store_true")
    parser.add_argument("--max-api-calls", type=int, default=30)
    args = parser.parse_args()
    client = MuscleWikiClient()
    cache = JsonMediaCache(CACHE_DIR)
    exercises = load_seed()
    report = {"generated_at": datetime.now(timezone.utc).isoformat(), "provider": "musclewiki", "api_calls": 0, "cache_hits": 0, "cache_misses": 0, "exercises": []}
    mappings = {}
    for exercise in exercises:
        key = client.normalize_query(exercise.name)
        cached = None if args.refresh else cache.get(key)
        if cached is None:
            if client.calls >= args.max_api_calls:
                raise SystemExit(f"API call limit reached before {exercise.id}; use --max-api-calls deliberately to raise it")
            candidates = client.search_exercises(exercise.name)
            cache.put(key, [candidate.raw for candidate in candidates])
        else:
            candidates = [client.parse_exercise(raw) for raw in cached]
        best, status = classify(exercise, candidates)
        selected = None
        if best:
            female = [video for video in best.videos if (video.gender or "").lower() == "female"]
            selected = female[0] if female else (best.videos[0] if best.videos else None)
        mapping = MediaMapping(exercise_id=exercise.id, provider="musclewiki" if best else None, provider_exercise_id=best.provider_id if best else None, provider_exercise_name=best.name if best else None, match_status=status, preferred_variant="female" if best and any((video.gender or "").lower() == "female" for video in best.videos) else ("male" if best and best.videos else "unavailable"), preferred_angle=selected.angle if selected else None, available_angles=sorted({video.angle for video in best.videos if video.angle} if best else []), review_status="unreviewed", review_notes="Candidate discovery only; human approval required." if best else "No provider candidate found.", last_verified=datetime.now(timezone.utc).isoformat(), primary_url=selected.url if selected else None, poster_url=selected.poster_url if selected else None)
        mappings[exercise.id] = mapping
        report["exercises"].append({"coach_luna": exercise.model_dump(), "candidates": [candidate.raw for candidate in candidates], "suggested_mapping": mapping.model_dump(exclude_none=True)})
    report["api_calls"] = client.calls
    report["cache_hits"] = cache.hits
    report["cache_misses"] = cache.misses
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    save_mappings(mappings)
    print(f"MuscleWiki API calls this run: {client.calls}")
    print(f"Cache hits: {cache.hits}")
    print(f"Cache misses: {cache.misses}")
    print(f"Audit report: {REPORT_PATH}")
    print("Mappings remain unreviewed; do not expose them as approved production media.")


if __name__ == "__main__":
    try:
        main()
    except MuscleWikiError as error:
        raise SystemExit(str(error)) from None
