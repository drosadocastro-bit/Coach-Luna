from typing import Literal

from pydantic import Field, model_validator

from app.models.exercise import Equipment, Exercise, Muscle, StrictModel


class RoutineRequest(StrictModel):
    target_muscles: list[Muscle] = Field(min_length=1, max_length=13)
    duration_minutes: int = Field(ge=10, le=120, strict=True)
    equipment: list[Equipment] = Field(min_length=1, max_length=6)
    experience_level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    goal: Literal["general_fitness", "strength", "hypertrophy"] = "general_fitness"
    exercise_count: int = Field(default=5, ge=1, le=10, strict=True)

    @model_validator(mode="after")
    def unique_values(self):
        if len(set(self.target_muscles)) != len(self.target_muscles) or len(set(self.equipment)) != len(self.equipment):
            raise ValueError("Target muscles and equipment must not contain duplicates")
        return self


class RoutineItem(StrictModel):
    exercise_id: str
    sets: int
    rep_min: int
    rep_max: int


class Routine(StrictModel):
    name: str
    estimated_duration_minutes: int
    exercises: list[RoutineItem]


class ValidationResult(StrictModel):
    valid: bool
    errors: list[str]
    warnings: list[str]


class DisplayItem(RoutineItem):
    exercise: Exercise


class DisplayRoutine(Routine):
    exercises: list[DisplayItem]


class RoutineResponse(StrictModel):
    routine: DisplayRoutine
    validation: ValidationResult
