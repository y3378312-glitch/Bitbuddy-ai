from functools import lru_cache

from google import genai

from ..config import settings


class GeminiServiceError(RuntimeError):
    pass


@lru_cache
def get_client():

    if not settings.gemini_api_key:

        raise GeminiServiceError(
            "GEMINI_API_KEY/GOOGLE_API_KEY is not configured."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def generate_text(
    model,
    prompt,
    system_instruction=None
):

    try:

        client = get_client()

        config = None

        if system_instruction:

            config = {
                "system_instruction": system_instruction
            }

        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config
        )

        text = (
            response.text or ""
        ).strip()

        if not text:

            raise GeminiServiceError(
                "Gemini returned an empty response."
            )

        return text

    except GeminiServiceError:
        raise

    except Exception as exc:

        raise GeminiServiceError(
            f"Gemini request failed: {exc}"
        ) from exc