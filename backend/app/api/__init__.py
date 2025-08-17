#file:ariadne/backend/app/api/__init__.py
from fastapi import APIRouter
from app.api.routes import auth, diary, image, feedback

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(diary.router)
api_router.include_router(image.router)
api_router.include_router(feedback.router)