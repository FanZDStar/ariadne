#file:ariadne/backend/app/api/__init__.py
from fastapi import APIRouter
from app.api.routes import auth

api_router = APIRouter()
api_router.include_router(auth.router)