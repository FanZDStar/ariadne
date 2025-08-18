#file:ariadne/backend/app/api/__init__.py
from fastapi import APIRouter
from app.api.routes import auth, diary, image, feedback
from app.api.routes import ai_dialog, chat_history,tree_hole, tree_hole_chat

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(diary.router)
api_router.include_router(image.router)
api_router.include_router(feedback.router)
api_router.include_router(ai_dialog.router)
api_router.include_router(chat_history.router, prefix="/chat", tags=["chat"])
api_router.include_router(tree_hole.router)
api_router.include_router(tree_hole_chat.router)