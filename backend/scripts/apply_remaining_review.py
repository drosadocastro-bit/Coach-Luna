"""Apply the final cached human decisions without provider calls.

Provider IDs absent from the existing cache remain named, approved decisions with
needs_provider_id so they cannot be exposed as runtime media prematurely.
"""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app.services.media_mapping import load_mappings, save_mappings

DECISIONS = {
    "biceps_curl": {"name": "Dumbbell Curl", "status": "exact_match", "provider_id": None, "note": "Human-reviewed and approved. Dumbbell Curl is the canonical Coach Luna match; provider ID was not present in the existing cache.", "alternates": []},
    "chest_supported_row": {"name": "Dumbbell Laying Incline Row", "status": "acceptable_variant", "provider_id": None, "note": "Human-reviewed and approved as an acceptable variant; provider ID was not present in the existing cache.", "alternates": []},
    "dead_bug": {"name": None, "status": "no_match", "provider_id": None, "note": "Removed from the Coach Luna catalog by human review. Historical mapping retained for provenance only; no runtime media.", "alternates": []},
    "farmer_carry": {"name": "Dumbbell Farmer Walk", "status": "exact_match", "provider_id": None, "note": "Human-reviewed and approved. Dumbbell Farmer Walk is canonical; provider ID was not present in the existing cache.", "alternates": []},
    "one_arm_row": {"name": "Dumbbell Single Arm Row", "status": "exact_match", "provider_id": None, "note": "Human-reviewed and approved. Dumbbell Single Arm Row is canonical; provider ID was not present in the existing cache.", "alternates": []},
    "single_leg_rdl": {"name": "Dumbbell Single Leg Single Arm Deadlift", "status": "acceptable_variant", "provider_id": "461", "note": "Human-reviewed and approved as an acceptable unilateral deadlift variant.", "alternates": []},
    "step_up": {"name": "Dumbbell Step Up", "status": "exact_match", "provider_id": None, "note": "Human-reviewed and approved. Provider ID was not present in the existing cache.", "alternates": []},
    "triceps_extension": {"name": "Dumbbell Overhead Tricep Extension", "status": "exact_match", "provider_id": None, "note": "Human-reviewed and approved. Provider ID was not present in the existing cache.", "alternates": []},
    "walking_lunge": {"name": "Walking Lunge", "status": "acceptable_variant", "provider_id": None, "note": "Human-reviewed and approved as an acceptable unloaded instructional variant; provider ID was not present in the existing cache.", "alternates": []},
    "db_deadlift": {"name": "Dumbbell Romanian Deadlift", "status": "no_match", "provider_id": "291", "note": "RDL remains rejected for conventional Dumbbell Deadlift. Kettlebell Conventional Deadlift (Double) is an acceptable equipment variant; provider ID was not present in the existing cache.", "alternates": [{"provider": "musclewiki", "provider_exercise_id": None, "provider_exercise_name": "Kettlebell Conventional Deadlift (Double)", "variant_type": "equipment", "review_status": "approved"}]},
}


def main():
    path = Path(__file__).resolve().parents[1] / "app" / "data" / "media_mappings.json"
    mappings = load_mappings(path)
    for exercise_id, decision in DECISIONS.items():
        current = mappings[exercise_id]
        status = decision["status"] if decision["provider_id"] is not None else ("no_match" if exercise_id == "dead_bug" or exercise_id == "db_deadlift" else "needs_provider_id")
        mappings[exercise_id] = current.model_copy(update={"provider_exercise_id": decision["provider_id"], "provider_exercise_name": decision["name"], "match_status": status, "review_status": "rejected" if exercise_id == "dead_bug" or exercise_id == "db_deadlift" else "approved", "review_notes": decision["note"], "alternates": decision["alternates"]})
    save_mappings(mappings, path)
    print("Applied final review decisions: 10 catalog/provenance records")
    print("Provider calls: 0")


if __name__ == "__main__":
    main()
