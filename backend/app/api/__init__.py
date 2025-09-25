# #file:ariadne/backend/app/api/__init__.py
# from fastapi import APIRouter
# from app.api.routes import auth, diary, image, feedback
# from app.api.routes import ai_dialog, chat_history,tree_hole, tree_hole_chat, crisis_warning, risk_assessment

# api_router = APIRouter()
# api_router.include_router(auth.router)
# api_router.include_router(diary.router)
# api_router.include_router(image.router)
# api_router.include_router(feedback.router)
# api_router.include_router(ai_dialog.router)
# api_router.include_router(chat_history.router, prefix="/chat", tags=["chat"])
# api_router.include_router(chat_history.router, prefix="/chat-history", tags=["chat-history"])  # 添加chat-history前缀的路由
# api_router.include_router(tree_hole.router)
# api_router.include_router(tree_hole_chat.router)
# api_router.include_router(crisis_warning.router, prefix="/crisis", tags=["crisis-warning"])
# api_router.include_router(risk_assessment.router, prefix="/risk-assessment", tags=["risk-assessment"])


from fastapi import APIRouter
from app.api.routes import auth, diary, image, feedback
from app.api.routes import (
    ai_dialog,
    chat_history,
    tree_hole,
    tree_hole_chat,
    crisis_warning,
    risk_assessment,
)
from app.api.routes import (
    social_skills,
    emotional_protection,
    mood_tracker,
    skill_favorites,
    diary_backgrounds,
    user_diary_backgrounds,
)

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(diary.router)
api_router.include_router(image.router)
api_router.include_router(feedback.router)
api_router.include_router(ai_dialog.router)
api_router.include_router(chat_history.router, prefix="/chat", tags=["chat"])
api_router.include_router(
    chat_history.router, prefix="/chat-history", tags=["chat-history"]
)  # 添加chat-history前缀的路由
api_router.include_router(tree_hole.router)
api_router.include_router(tree_hole_chat.router)
api_router.include_router(
    crisis_warning.router, prefix="/crisis", tags=["crisis-warning"]
)
api_router.include_router(
    risk_assessment.router, prefix="/risk-assessment", tags=["risk-assessment"]
)
api_router.include_router(
    social_skills.router, prefix="/social-skills", tags=["social-skills"]
)
api_router.include_router(
    emotional_protection.router,
    prefix="/emotional-protection",
    tags=["emotional-protection"],
)
api_router.include_router(
    mood_tracker.router, prefix="/mood-tracker", tags=["mood-tracker"]
)
api_router.include_router(
    skill_favorites.router, prefix="/skill-favorites", tags=["skill-favorites"]
)
api_router.include_router(diary_backgrounds.router)
api_router.include_router(user_diary_backgrounds.router)
