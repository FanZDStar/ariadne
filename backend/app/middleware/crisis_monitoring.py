#file:ariadne/backend/app/middleware/crisis_monitoring.py
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
import logging
import json
import asyncio
from typing import Callable

from app.database.session import get_db
from app.services.crisis_warning_service import CrisisWarningService, RiskLevel, WarningType
from app.models.user import User

logger = logging.getLogger(__name__)

class CrisisMonitoringMiddleware(BaseHTTPMiddleware):
    """
    心理危机实时监控中间件
    监控用户的日记提交和聊天内容，实时检测危机信号
    """
    
    # 需要监控的API端点
    MONITORED_ENDPOINTS = {
        "/api/diaries": "diary",      # 日记API
        "/api/ai-dialog": "chat",     # AI对话API
        "/api/tree-hole": "whisper"   # 树洞API
    }
    
    def __init__(self, app):
        super().__init__(app)
        self.warning_service = None
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """处理请求"""
        # 检查是否需要监控此端点
        endpoint_type = self._should_monitor_endpoint(request.url.path)
        
        if endpoint_type and request.method == "POST":
            # 获取用户信息
            user_id = await self._extract_user_id(request)
            
            if user_id:
                # 获取请求内容
                content = await self._extract_content(request, endpoint_type)
                
                if content:
                    # 异步进行危机检测，不阻塞正常响应
                    asyncio.create_task(
                        self._perform_crisis_detection(user_id, content, endpoint_type)
                    )
        
        # 继续处理请求
        response = await call_next(request)
        return response
    
    def _should_monitor_endpoint(self, path: str) -> str:
        """检查是否应该监控此端点"""
        for endpoint, endpoint_type in self.MONITORED_ENDPOINTS.items():
            if path.startswith(endpoint):
                return endpoint_type
        return None
    
    async def _extract_user_id(self, request: Request) -> int:
        """从请求中提取用户ID"""
        try:
            # 从Authorization header中提取用户信息
            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                return None
            
            # 这里需要根据你的JWT解析逻辑来获取用户ID
            # 简化示例，实际需要解析JWT token
            # token = auth_header.split(" ")[1]
            # user_id = decode_jwt_token(token)
            
            # 暂时返回None，需要根据实际JWT实现来完善
            return None
            
        except Exception as e:
            logger.error(f"提取用户ID失败: {str(e)}")
            return None
    
    async def _extract_content(self, request: Request, endpoint_type: str) -> str:
        """从请求中提取需要监控的内容"""
        try:
            # 读取请求体
            body = await request.body()
            if not body:
                return None
            
            # 解析JSON内容
            data = json.loads(body.decode('utf-8'))
            
            # 根据端点类型提取相应内容
            if endpoint_type == "diary":
                # 日记内容
                title = data.get("title", "")
                content = data.get("content", "")
                return f"{title} {content}"
            
            elif endpoint_type == "chat":
                # AI对话内容
                messages = data.get("messages", [])
                if messages:
                    # 提取最新的用户消息
                    user_messages = [msg.get("content", "") for msg in messages if msg.get("role") == "user"]
                    return " ".join(user_messages)
            
            elif endpoint_type == "whisper":
                # 树洞内容
                return data.get("content", "")
            
            return None
            
        except Exception as e:
            logger.error(f"提取内容失败: {str(e)}")
            return None
    
    async def _perform_crisis_detection(self, user_id: int, content: str, source: str):
        """执行危机检测"""
        try:
            # 获取数据库连接
            db = next(get_db())
            
            try:
                if not self.warning_service:
                    self.warning_service = CrisisWarningService(db)
                
                # 分析内容中的危机信号
                analysis_result = self.warning_service._analyze_text_for_crisis(content, source)
                
                # 如果检测到中等及以上风险，创建预警
                if analysis_result.risk_level in [RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.CRITICAL]:
                    warning = self.warning_service.create_warning(
                        user_id=user_id,
                        assessment=analysis_result,
                        warning_type=WarningType.KEYWORD_ALERT,
                        source_data=content[:500]  # 只保存前500字符
                    )
                    
                    logger.warning(
                        f"实时检测到用户 {user_id} 的危机信号 - "
                        f"风险等级: {analysis_result.risk_level.value}, "
                        f"来源: {source}, "
                        f"预警ID: {warning.warning_id}"
                    )
                    
                    # 如果是紧急风险，立即触发紧急响应
                    if analysis_result.risk_level == RiskLevel.CRITICAL:
                        await self._trigger_emergency_response(user_id, warning)
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"危机检测失败 - 用户ID: {user_id}, 错误: {str(e)}")
    
    async def _trigger_emergency_response(self, user_id: int, warning):
        """触发紧急响应"""
        logger.critical(f"触发紧急响应 - 用户ID: {user_id}, 预警ID: {warning.warning_id}")
        
        # 这里可以实现紧急响应逻辑：
        # 1. 立即通知在线的管理员或心理咨询师
        # 2. 发送紧急通知到用户设备
        # 3. 记录到紧急事件日志
        # 4. 触发自动回复机制，提供紧急联系方式
        
        # 示例：记录紧急事件
        try:
            # 这里可以调用紧急通知服务
            # await emergency_notification_service.notify(user_id, warning)
            pass
        except Exception as e:
            logger.error(f"紧急响应处理失败: {str(e)}")

class CrisisKeywordDetector:
    """
    危机关键词检测器（独立组件，可用于其他地方）
    """
    
    @staticmethod
    def quick_detect(text: str) -> dict:
        """
        快速检测文本中的危机关键词
        
        Returns:
            dict: {
                "has_crisis": bool,
                "risk_level": str,
                "detected_keywords": list,
                "categories": list
            }
        """
        if not text:
            return {
                "has_crisis": False,
                "risk_level": "low",
                "detected_keywords": [],
                "categories": []
            }
        
        # 使用CrisisWarningService中的关键词配置
        from app.services.crisis_warning_service import CrisisWarningService
        
        detected_keywords = []
        categories = []
        
        for category, keywords in CrisisWarningService.CRISIS_KEYWORDS.items():
            found_in_category = []
            for keyword in keywords:
                if keyword in text:
                    found_in_category.append(keyword)
            
            if found_in_category:
                detected_keywords.extend(found_in_category)
                categories.append(category)
        
        # 简单风险等级判定
        has_crisis = len(detected_keywords) > 0
        if "自伤" in categories:
            risk_level = "critical"
        elif len(categories) >= 3:
            risk_level = "high"
        elif len(categories) >= 2:
            risk_level = "medium"
        elif len(categories) >= 1:
            risk_level = "low"
        else:
            risk_level = "low"
        
        return {
            "has_crisis": has_crisis,
            "risk_level": risk_level,
            "detected_keywords": detected_keywords,
            "categories": categories
        }
