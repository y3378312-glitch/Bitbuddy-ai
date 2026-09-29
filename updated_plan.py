from ..config import settings

from .gemini_client import generate_text


def update_workout_plan(
    original_plan,
    feedback,
    goal,
    intensity
):

    if (
        settings.demo_mode
        and not settings.gemini_api_key
    ):

        return f"""
{original_plan}


FEEDBACK UPDATE

Requested changes:
{feedback}


Demo mode:

The production version sends
the original plan and feedback
to Gemini.
""".strip()

    system = """
You revise general wellness
workout plans.

Preserve useful parts while
applying the user's feedback.

Do not provide:

- medical diagnosis
- medication advice
- extreme dieting
- dangerous challenges
- unsafe exercise instructions

Include rest/recovery.

Return the complete revised
seven-day plan.
""".strip()

    prompt = f"""
Goal:
{goal}

Preferred intensity:
{intensity}


Original plan:

---BEGIN ORIGINAL---

{original_plan}

---END ORIGINAL---


User feedback:

---BEGIN FEEDBACK---

{feedback}

---END FEEDBACK---


Create the complete revised
seven-day plan.
""".strip()

    return generate_text(
        settings.workout_model,
        prompt,
        system
    )