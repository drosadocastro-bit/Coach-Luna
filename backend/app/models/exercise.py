from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, model_validator

Muscle = Literal["quads", "glutes", "hamstrings", "calves", "erectors", "chest", "shoulders", "upper_back", "lats", "biceps", "triceps", "forearms", "core"]
Equipment = Literal["dumbbells", "bench", "step", "mat", "cable_machine", "barbell"]
Pattern = Literal["squat", "hinge", "lunge", "bridge", "horizontal_push", "vertical_push", "horizontal_pull", "pullover", "isolation", "carry", "rotation", "anti_extension"]


class StrictModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Video(StrictModel):
    type: Literal["mp4"] = "mp4"
    uri: str | None = None
    angles: list[Literal["front", "side", "rear", "three_quarter"]] = Field(min_length=1)


class Exercise(StrictModel):
    id: str = Field(pattern=r"^[a-z][a-z0-9_]+$")
    name: str = Field(min_length=1)
    display_name_es: str = Field(min_length=1)
    primary_muscles: list[Muscle] = Field(min_length=1)
    secondary_muscles: list[Muscle]
    equipment: list[Equipment] = Field(min_length=1)
    movement_pattern: Pattern
    difficulty: Literal["beginner", "beginner_intermediate", "intermediate", "advanced"]
    unilateral: bool
    default_sets: int = Field(ge=1, le=6)
    rep_min: int = Field(ge=1, le=30)
    rep_max: int = Field(ge=1, le=30)
    prescription_unit: Literal["reps", "steps"] = "reps"
    video: Video
    instructions_en: list[str] = Field(min_length=1)
    instructions_es: list[str] = Field(min_length=1)
    common_mistakes_en: list[str] = Field(min_length=1)
    common_mistakes_es: list[str] = Field(min_length=1)
    alternatives: list[str]
    enabled: bool = True

    @model_validator(mode="after")
    def ordered_reps(self):
        if self.rep_min > self.rep_max:
            raise ValueError("rep_min must not exceed rep_max")
        return self
