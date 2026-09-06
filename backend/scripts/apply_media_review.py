"""Apply the human review decisions recorded for the Phase 1 pilot set."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.media_mapping import load_mappings, save_mappings

DECISIONS = {
    "barbell_bench_press": ("4", "Barbell Bench Press", "New Coach Luna catalog exercise approved as the barbell counterpart to Dumbbell Bench Press."),
    "bench_press": ("377", "Dumbbell Bench Press", "Barbell Bench Press rejected for this Coach Luna exercise; keep as a future separate catalog exercise."),
    "bulgarian_split_squat": ("317", "Dumbbell Bulgarian Split Squat", "Canonical dumbbell approved; barbell Bulgarian Split Squat remains a separate variant."),
    "db_deadlift": ("291", "Dumbbell Romanian Deadlift", "Human-reviewed and rejected. Dumbbell Romanian Deadlift is not equivalent to Coach Luna's Dumbbell Deadlift. No approved canonical media mapping exists."),
    "db_rdl_001": ("291", "Dumbbell Romanian Deadlift", "Exact canonical match approved."),
    "glute_bridge": ("293", "Dumbbell Glute Bridge", "Canonical match approved."),
    "goblet_squat": ("11", "Dumbbell Goblet Squat", "Canonical dumbbell approved; Kettlebell Goblet Squat remains an alternate variant."),
    "hammer_curl": ("3", "Dumbbell Hammer Curl", "Human-reviewed and approved. Band Bayesian Hammer Curl is rejected; Dumbbell Hammer Curl is canonical."),
    "hip_thrust": ("286", "Dumbbell Hip Thrust", "Canonical match approved."),
    "incline_press": ("398", "Dumbbell Incline Bench Press", "Human-reviewed and approved as the standard incline dumbbell press. Guillotine Incline Bench Press is explicitly rejected."),
    "lateral_raise": ("20", "Dumbbell Lateral Raise", "Canonical match approved; Dumbbell Full Lateral Raise remains a separate alternate."),
    "pullover": ("413", "Dumbbell Pullover", "Canonical match approved."),
    "rear_delt_fly": ("21", "Dumbbell Rear Delt Fly", "Canonical match approved; Dumbbell Seated Rear Delt Fly remains a separate alternate."),
    "reverse_lunge": ("414", "Dumbbell Reverse Lunge", "Canonical match approved; goblet and alternating reverse lunge variants remain separate alternates."),
    "russian_twist": ("289", "Dumbbell Russian Twist", "Canonical match approved; Dumbbell Feet Down Russian Twist remains a separate alternate."),
    "sumo_squat": ("467", "Dumbbell Sumo Squat", "Canonical match approved."),
    "shoulder_press": (None, "Dumbbell Overhead Press", "Human-reviewed and approved conceptually, but the verified provider ID is not present in the existing cache. Do not expose until the provider identity is confirmed. Single Arm Neutral Overhead Press is rejected."),
}


def main():
    path = Path(__file__).resolve().parents[1] / "app" / "data" / "media_mappings.json"
    mappings = load_mappings(path)
    for exercise_id, (provider_id, provider_name, notes) in DECISIONS.items():
        rejected = exercise_id == "db_deadlift"
        missing_id = exercise_id == "shoulder_press"
        mapping = mappings[exercise_id].model_copy(update={"provider_exercise_id": provider_id, "provider_exercise_name": provider_name, "match_status": "no_match" if rejected else ("needs_provider_id" if missing_id else "exact_match"), "review_status": "rejected" if rejected else "approved", "review_notes": notes})
        mappings[exercise_id] = mapping
    save_mappings(mappings, path)
    print(f"Applied reviewed mapping decisions: {len(DECISIONS)}")
    print("All other mappings remain unreviewed and are not production media.")


if __name__ == "__main__":
    main()
