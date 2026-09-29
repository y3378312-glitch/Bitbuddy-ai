import os
from pathlib import Path

os.environ["DEMO_MODE"] = "true"

os.environ["DATABASE_URL"] = (
    "sqlite:///./test_fitbuddy.db"
)


from fastapi.testclient import TestClient

from APP.main import app


client = TestClient(app)


def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json()["status"] == "ok"


def test_home():

    response = client.get("/")

    assert response.status_code == 200

    assert "FitBuddy" in response.text


def test_generate():

    payload = {

        "user_id": "test-001",

        "username": "Test User",

        "age": 20,

        "weight": 65,

        "goal": "general wellness",

        "intensity": "medium"
    }

    response = client.post(

        "/api/generate-workout",

        json=payload
    )

    assert response.status_code == 200

    assert "Day 1" in (
        response.json()["workout_plan"]
    )


def test_feedback():

    response = client.post(

        "/api/submit-feedback",

        json={

            "user_id": "test-001",

            "feedback":
                "Add more mobility work."
        }
    )

    assert response.status_code == 200

    assert response.json()["updated"] is True


def test_get_user():

    response = client.get(
        "/api/users/test-001"
    )

    assert response.status_code == 200

    assert (
        response.json()["username"]
        == "Test User"
    )


def test_invalid_age():

    payload = {

        "user_id": "bad",

        "username": "Bad",

        "age": 10,

        "weight": 50,

        "goal": "general wellness",

        "intensity": "low"
    }

    response = client.post(

        "/api/generate-workout",

        json=payload
    )

    assert response.status_code == 422


def teardown_module():

    Path(
        "test_fitbuddy.db"
    ).unlink(
        missing_ok=True
    )