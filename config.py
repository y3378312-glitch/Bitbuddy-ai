import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    app_name = "FitBuddy"

    database_url = os.getenv(
        "DATABASE_URL",
        "sqlite:///./fitbuddy.db"
    )

    gemini_api_key = (
        os.getenv("GEMINI_API_KEY")
        or os.getenv("GOOGLE_API_KEY")
    )

    workout_model = os.getenv(
        "GEMINI_WORKOUT_MODEL",
        "gemini-2.5-pro"
    )

    fast_model = os.getenv(
        "GEMINI_FAST_MODEL",
        "gemini-2.5-flash"
    )

    demo_mode = os.getenv(
        "DEMO_MODE",
        "true"
    ).lower() in {"1", "true", "yes", "on"}

    admin_token = os.getenv("ADMIN_TOKEN") or None


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
