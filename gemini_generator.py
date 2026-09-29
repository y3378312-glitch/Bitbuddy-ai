from ..config import settings

from .gemini_client import generate_text


SYSTEM_INSTRUCTION = """
You are FitBuddy's general wellness planning assistant.

Create practical, moderate, age-appropriate fitness guidance.

Do not diagnose medical conditions.
Do not prescribe medication.
Do not recommend extreme dieting.
Do not encourage dangerous challenges.

Avoid unsafe claims and promises of health outcomes.

Return a clear seven-day schedule with:
- focus
- warm-up
- main workout
- cooldown/recovery

Include rest or light-recovery days.
""".strip()


def _demo_plan(
    goal,
    intensity
):

    return f"""
7-DAY FITBUDDY DEMO PLAN

Goal: {goal}
Intensity: {intensity}


Day 1 — Full Body

Warm-up:
5–10 minutes of easy movement.

Main:
Chair squat 2×8–10
Wall/incline push-up 2×8–10
Hip hinge 2×8–10
Easy walk 10 minutes.

Cooldown:
Gentle mobility for 5 minutes.


Day 2 — Cardio & Mobility

Warm-up:
5 minutes easy walking.

Main:
Comfortable cardio 15–25 minutes.
Follow with gentle mobility.

Cooldown:
Easy breathing and stretching.


Day 3 — Upper Body & Core

Warm-up:
5–10 minutes.

Main:
Row variation 2×8–10
Incline push-up 2×8–10
Dead bug 2×6–8 each side.

Cooldown:
Gentle upper-body mobility.


Day 4 — Recovery

Easy walk or relaxed mobility
for 15–20 minutes.

Keep the effort comfortable.


Day 5 — Lower Body

Warm-up:
5–10 minutes.

Main:
Sit-to-stand 2×8–10
Supported split squat 2×6–8 each side
Calf raise 2×10.

Cooldown:
Gentle lower-body mobility.


Day 6 — Cardio & Core

Warm-up:
5 minutes.

Main:
Comfortable cardio 15–25 minutes.
Bird-dog 2×6–8 each side.
Side-plank variation 2×10–20 seconds.

Cooldown:
5 minutes easy movement.


Day 7 — Rest / Light Activity

Choose rest or a comfortable walk
and gentle mobility.


Progress gradually.

Stop if an exercise causes pain
or unusual symptoms.

This is demo content,
not medical advice.
""".strip()


def generate_workout_gemini(user):

    if (
        settings.demo_mode
        and not settings.gemini_api_key
    ):

        return _demo_plan(
            user.goal,
            user.intensity
        )

    prompt = f"""
Create a personalized seven-day
general wellness workout plan.

User profile:

Name: {user.username}
Age: {user.age}
Weight: {user.weight} kg
Goal: {user.goal}
Preferred intensity: {user.intensity}

Use the profile only to tailor
general wellness guidance.

Do not diagnose or prescribe.

Return day-by-day sections with:

- focus
- warm-up
- main workout
- cooldown/recovery

Include at least one recovery/rest day
and sensible progression.
""".strip()

    return generate_text(
        settings.workout_model,
        prompt,
        SYSTEM_INSTRUCTION
    )