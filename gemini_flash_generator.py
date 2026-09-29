from ..config import settings

from .gemini_client import generate_text


def generate_nutrition_tip_with_flash(
    goal
):

    if (
        settings.demo_mode
        and not settings.gemini_api_key
    ):

        tips = {

            "weight loss":
                "Build balanced meals around vegetables or fruit, a protein source, satisfying carbohydrates, and water. Avoid extreme restriction.",

            "muscle gain":
                "Include a protein-rich food in regular meals and snacks, along with varied foods and fluids to support normal recovery.",

            "general wellness":
                "Prioritize regular meals, varied whole foods, adequate fluids, and consistent sleep and recovery habits.",

            "flexibility":
                "Pair regular movement with varied, balanced meals and enough fluids to support everyday energy and recovery."
        }

        return tips.get(
            goal,
            tips["general wellness"]
        )

    prompt = f"""
Give one concise general wellness
nutrition or recovery tip
for the goal:

{goal}

Keep it practical and non-extreme.

Do not prescribe:
- calories
- supplements
- medication
- restrictive diets

Keep the answer to 2–4 sentences.
"""

    return generate_text(
        settings.fast_model,
        prompt
    )