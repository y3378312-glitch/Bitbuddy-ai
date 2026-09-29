from typing import Literal

from pydantic import BaseModel
from pydantic import Field
from pydantic import field_validator


Goal = Literal[
    "weight loss",
    "muscle gain",
    "general wellness",
    "flexibility"
]


Intensity = Literal[
    "low",
    "medium",
    "high"
]


class UserInput(BaseModel):

    user_id: str = Field(
        min_length=1,
        max_length=80
    )

    username: str = Field(
        min_length=1,
        max_length=120
    )

    age: int = Field(
        ge=13,
        le=100
    )

    weight: float = Field(
        gt=0,
        le=500
    )

    goal: Goal

    intensity: Intensity

    @field_validator(
        "user_id",
        "username"
    )
    @classmethod
    def strip_text(cls, value):

        value = value.strip()

        if not value:
            raise ValueError(
                "Value cannot be blank"
            )

        return value


class FeedbackRequest(BaseModel):

    user_id: str = Field(
        min_length=1,
        max_length=80
    )

    feedback: str = Field(
        min_length=3,
        max_length=1000
    )


class PlanResponse(BaseModel):

    user_id: str
    username: str
    goal: str
    intensity: str
    workout_plan: str
    nutrition_tip: str
    updated: bool = False