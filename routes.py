from fastapi import APIRouter
from fastapi import Depends
from fastapi import Form
from fastapi import HTTPException
from fastapi import Request
from fastapi import status

from fastapi.responses import HTMLResponse

from fastapi.templating import Jinja2Templates

from sqlalchemy import select
from sqlalchemy.orm import Session

from .config import settings
from .database import get_db
from .models import User
from .schemas import FeedbackRequest
from .schemas import PlanResponse
from .schemas import UserInput

from .services.gemini_client import GeminiServiceError
from .services.gemini_flash_generator import (
    generate_nutrition_tip_with_flash
)
from .services.gemini_generator import (
    generate_workout_gemini
)
from .services.updated_plan import (
    update_workout_plan
)


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


def _admin_allowed(token):

    return (
        not settings.admin_token
        or token == settings.admin_token
    )


def _user_to_dict(user):

    return {

        "user_id": user.user_id,

        "username": user.username,

        "age": user.age,

        "weight": user.weight,

        "goal": user.goal,

        "intensity": user.intensity,

        "original_plan":
            user.original_plan,

        "updated_plan":
            user.updated_plan,

        "nutrition_tip":
            user.nutrition_tip,

        "last_feedback":
            user.last_feedback,

        "created_at":
            user.created_at.isoformat()
            if user.created_at
            else None,

        "updated_at":
            user.updated_at.isoformat()
            if user.updated_at
            else None
    }


@router.get(
    "/",
    response_class=HTMLResponse
)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "error": None
        }
    )


@router.post(
    "/generate-workout",
    response_class=HTMLResponse
)
def generate_workout_form(

    request: Request,

    user_id: str = Form(...),

    username: str = Form(...),

    age: int = Form(...),

    weight: float = Form(...),

    goal: str = Form(...),

    intensity: str = Form(...),

    db: Session = Depends(get_db)
):

    try:

        data = UserInput(

            user_id=user_id,

            username=username,

            age=age,

            weight=weight,

            goal=goal,

            intensity=intensity
        )

        workout = generate_workout_gemini(
            data
        )

        tip = generate_nutrition_tip_with_flash(
            data.goal
        )

        user = db.scalar(
            select(User).where(
                User.user_id == data.user_id
            )
        )

        if user is None:

            user = User(

                user_id=data.user_id,

                username=data.username,

                age=data.age,

                weight=data.weight,

                goal=data.goal,

                intensity=data.intensity,

                original_plan=workout,

                nutrition_tip=tip
            )

            db.add(user)

        else:

            user.username = data.username
            user.age = data.age
            user.weight = data.weight

            user.goal = data.goal
            user.intensity = data.intensity

            user.original_plan = workout
            user.updated_plan = None
            user.last_feedback = None

            user.nutrition_tip = tip

        db.commit()

        db.refresh(user)

        return templates.TemplateResponse(

            request=request,

            name="result.html",

            context={

                "user": user,

                "workout_plan":
                    user.original_plan,

                "nutrition_tip":
                    user.nutrition_tip,

                "updated": False,

                "error": None
            }
        )

    except Exception as exc:

        return templates.TemplateResponse(

            request=request,

            name="index.html",

            context={
                "error": str(exc)
            },

            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.post(
    "/submit-feedback",
    response_class=HTMLResponse
)
def submit_feedback_form(

    request: Request,

    user_id: str = Form(...),

    feedback: str = Form(...),

    db: Session = Depends(get_db)
):

    try:

        data = FeedbackRequest(

            user_id=user_id,

            feedback=feedback
        )

        user = db.scalar(

            select(User).where(
                User.user_id == data.user_id
            )
        )

        if user is None:

            raise ValueError(
                "User ID was not found. "
                "Generate a plan first."
            )

        revised = update_workout_plan(

            user.original_plan,

            data.feedback,

            user.goal,

            user.intensity
        )

        user.updated_plan = revised

        user.last_feedback = data.feedback

        db.commit()

        db.refresh(user)

        return templates.TemplateResponse(

            request=request,

            name="result.html",

            context={

                "user": user,

                "workout_plan":
                    user.updated_plan,

                "nutrition_tip":
                    user.nutrition_tip,

                "updated": True,

                "error": None
            }
        )

    except Exception as exc:

        return templates.TemplateResponse(

            request=request,

            name="result.html",

            context={

                "user": None,

                "workout_plan": None,

                "nutrition_tip": None,

                "updated": False,

                "error": str(exc)
            },

            status_code=status.HTTP_400_BAD_REQUEST
        )


@router.get(
    "/view-all-users",
    response_class=HTMLResponse
)
def view_all_users(

    request: Request,

    token: str | None = None,

    db: Session = Depends(get_db)
):

    if not _admin_allowed(token):

        raise HTTPException(
            status_code=403,
            detail="Invalid admin token."
        )

    users = db.scalars(

        select(User).order_by(
            User.created_at.desc()
        )

    ).all()

    return templates.TemplateResponse(

        request=request,

        name="all_users.html",

        context={
            "users": users,
            "error": None
        }
    )


@router.post(
    "/api/generate-workout",
    response_model=PlanResponse
)
def generate_workout_api(

    payload: UserInput,

    db: Session = Depends(get_db)
):

    try:

        workout = generate_workout_gemini(
            payload
        )

        tip = generate_nutrition_tip_with_flash(
            payload.goal
        )

    except GeminiServiceError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc

    user = db.scalar(

        select(User).where(
            User.user_id == payload.user_id
        )
    )

    if user is None:

        user = User(

            user_id=payload.user_id,

            username=payload.username,

            age=payload.age,

            weight=payload.weight,

            goal=payload.goal,

            intensity=payload.intensity,

            original_plan=workout,

            nutrition_tip=tip
        )

        db.add(user)

    else:

        user.username = payload.username
        user.age = payload.age
        user.weight = payload.weight

        user.goal = payload.goal
        user.intensity = payload.intensity

        user.original_plan = workout
        user.updated_plan = None
        user.last_feedback = None

        user.nutrition_tip = tip

    db.commit()

    db.refresh(user)

    return PlanResponse(

        user_id=user.user_id,

        username=user.username,

        goal=user.goal,

        intensity=user.intensity,

        workout_plan=user.original_plan,

        nutrition_tip=user.nutrition_tip,

        updated=False
    )


@router.post(
    "/api/submit-feedback",
    response_model=PlanResponse
)
def submit_feedback_api(

    payload: FeedbackRequest,

    db: Session = Depends(get_db)
):

    user = db.scalar(

        select(User).where(
            User.user_id == payload.user_id
        )
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User ID was not found."
        )

    try:

        revised = update_workout_plan(

            user.original_plan,

            payload.feedback,

            user.goal,

            user.intensity
        )

    except GeminiServiceError as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc)
        ) from exc

    user.updated_plan = revised

    user.last_feedback = payload.feedback

    db.commit()

    return PlanResponse(

        user_id=user.user_id,

        username=user.username,

        goal=user.goal,

        intensity=user.intensity,

        workout_plan=revised,

        nutrition_tip=user.nutrition_tip,

        updated=True
    )


@router.get("/api/users")
def list_users(

    token: str | None = None,

    db: Session = Depends(get_db)
):

    if not _admin_allowed(token):

        raise HTTPException(
            status_code=403,
            detail="Invalid admin token."
        )

    users = db.scalars(

        select(User).order_by(
            User.created_at.desc()
        )

    ).all()

    return {
        "users": [
            _user_to_dict(user)
            for user in users
        ]
    }


@router.get(
    "/api/users/{user_id}"
)
def get_user(

    user_id: str,

    db: Session = Depends(get_db)
):

    user = db.scalar(

        select(User).where(
            User.user_id == user_id
        )
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    return _user_to_dict(user)


@router.delete(
    "/api/users/{user_id}"
)
def delete_user(

    user_id: str,

    token: str | None = None,

    db: Session = Depends(get_db)
):

    if not _admin_allowed(token):

        raise HTTPException(
            status_code=403,
            detail="Invalid admin token."
        )

    user = db.scalar(

        select(User).where(
            User.user_id == user_id
        )
    )

    if user is None:

        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    db.delete(user)

    db.commit()

    return {
        "message": "User deleted.",
        "user_id": user_id
    }


@router.get("/health")
def health():

    return {

        "status": "ok",

        "service": "fitbuddy",

        "demo_mode":
            settings.demo_mode
            and not bool(
                settings.gemini_api_key
            )
    }