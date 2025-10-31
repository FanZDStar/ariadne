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
    multimodal_chat,
)
from app.api.routes import (
    social_skills,
    emotional_protection,
    mood_tracker,
    skill_favorites,
    diary_backgrounds,
    user_diary_backgrounds,
    interpersonal_practice,
    protection_drill_reports,
    star_points,
    mascot_outfits,
    tree_energy,
    user_profile_template,
    water_drops,
)
from app.api import protection_drill

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
api_router.include_router(
    interpersonal_practice.router, 
    prefix="/interpersonal-practice", 
    tags=["interpersonal-practice"]
)
api_router.include_router(
    protection_drill_reports.router,
    prefix="/protection-drill",
    tags=["protection-drill-reports"]
)
api_router.include_router(
    protection_drill.router,
    tags=["protection-drill"]
)
api_router.include_router(
    star_points.router,
    tags=["星星积分"]
)
api_router.include_router(
    mascot_outfits.router,
    tags=["看板娘服装"]
)
api_router.include_router(
    tree_energy.router,
    tags=["树洞能量系统"]
)
api_router.include_router(
    multimodal_chat.router,
    prefix="/multimodal",
    tags=["多模态对话"]
)
api_router.include_router(
    user_profile_template.router,
    tags=["user-profile-template"]
)
api_router.include_router(
    water_drops.router,
    prefix="/water-drops",
    tags=["水滴系统"]
)

# 导入并添加看板娘好感度路由
from app.api.routes import mascot_affection
api_router.include_router(
    mascot_affection.router,
    prefix="/mascot-affection",
    tags=["看板娘好感度"]
)

