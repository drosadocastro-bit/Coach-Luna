"""Apply the human review decisions recorded for the Phase 1 pilot set."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.media_mapping import load_mappings, save_mappings

DECISIONS = {
    "bench_press": ("377", "Dumbbell Bench Press", "Barbell Bench Press rejected for this Coach Luna exercise; keep as a future separate catalog exercise."),
    "bulgarian_split_squat": ("317", "Dumbbell Bulgarian Split Squat", "Canonical dumbbell approved; barbell Bulgarian Split Squat remains a separate variant."),
    "db_rdl_001": ("291", "Dumbbell Romanian Deadlift", "Exact canonical match approved."),
    "glute_bridge": ("293", "Dumbbell Glute Bridge", "Canonical match approved."),
    "goblet_squat": ("11", "Dumbbell Goblet Squat", "Canonical dumbbell approved; Kettlebell Goblet Squat remains an alternate variant."),
    "hip_thrust": ("286", "Dumbbell Hip Thrust", "Canonical match approved."),
    "lateral_raise": ("20", "Dumbbell Lateral Raise", "Canonical match approved; Dumbbell Full Lateral Raise remains a separate alternate."),
    "pullover": ("413", "Dumbbell Pullover", "Canonical match approved."),
    "rear_delt_fly": ("21", "Dumbbell Rear Delt Fly", "Canonical match approved; Dumbbell Seated Rear Delt Fly remains a separate alternate."),
    "reverse_lunge": ("414", "Dumbbell Reverse Lunge", "Canonical match approved; goblet and alternating reverse lunge variants remain separate alternates."),
    "russian_twist": ("289", "Dumbbell Russian Twist", "Canonical match approved; Dumbbell Feet Down Russian Twist remains a separate alternate."),
    "sumo_squat": ("467", "Dumbbell Sumo Squat", "Canonical match approved."),
}


def main():
    path = Path(__file__).resolve().parents[1] / "app" / "data" / "media_mappings.json"
    mappings = load_mappings(path)
    for exercise_id, (provider_id, provider_name, notes) in DECISIONS.items():
        mapping = mappings[exercise_id].model_copy(update={"provider_exercise_id": provider_id, "provider_exercise_name": provider_name, "match_status": "exact_match", "review_status": "approved", "review_notes": notes})
        mappings[exercise_id] = mapping
    save_mappings(mappings, path)
    print(f"Approved canonical mappings: {len(DECISIONS)}")
    print("All other mappings remain unreviewed and are not production media.")


if __name__ == "__main__":
    main()
