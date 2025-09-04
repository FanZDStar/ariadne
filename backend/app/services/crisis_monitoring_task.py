#file:ariadne/backend/app/services/crisis_monitoring_task.py
import asyncio
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.models.user import User
from app.models.crisis_warning import CrisisWarning, RiskLevel, WarningType
from app.services.crisis_warning_service import CrisisWarningService

logger = logging.getLogger(__name__)

class CrisisMonitoringTask:
    """心理危机监控定时任务"""
    
    def __init__(self):
        self.is_running = False
    
    async def start_monitoring(self, check_interval_hours: int = 6):
        """
        启动定时监控任务
        
        Args:
            check_interval_hours: 检查间隔（小时）
        """
        if self.is_running:
            logger.warning("监控任务已在运行中")
            return
        
        self.is_running = True
        logger.info(f"启动心理危机监控任务，检查间隔：{check_interval_hours}小时")
        
        try:
            while self.is_running:
                await self._perform_monitoring_check()
                await asyncio.sleep(check_interval_hours * 3600)  # 转换为秒
        except Exception as e:
            logger.error(f"监控任务异常退出: {str(e)}")
        finally:
            self.is_running = False
    
    def stop_monitoring(self):
        """停止监控任务"""
        self.is_running = False
        logger.info("心理危机监控任务已停止")
    
    async def _perform_monitoring_check(self):
        """执行监控检查"""
        logger.info("开始执行心理危机监控检查")
        
        try:
            # 获取数据库连接
            db = next(get_db())
            
            try:
                # 获取所有活跃用户（最近7天有活动的用户）
                active_users = self._get_active_users(db, days=7)
                logger.info(f"发现 {len(active_users)} 个活跃用户需要检查")
                
                # 为每个用户进行风险评估
                for user in active_users:
                    await self._check_user_risk(db, user)
                
                logger.info("心理危机监控检查完成")
                
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"监控检查过程中发生错误: {str(e)}")
    
    def _get_active_users(self, db: Session, days: int = 7) -> List[User]:
        """获取活跃用户列表"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # 查询最近有日记或聊天记录的用户
        from app.models.emotional_diary import EmotionalDiary
        from app.models.chat_history import ChatSession
        
        # 使用子查询找到活跃用户ID
        diary_users = db.query(EmotionalDiary.user_id).filter(
            EmotionalDiary.created_at >= cutoff_date
        ).distinct().subquery()
        
        chat_users = db.query(ChatSession.user_id).filter(
            ChatSession.created_at >= cutoff_date
        ).distinct().subquery()
        
        # 获取有活动的用户
        active_user_ids = set()
        
        # 添加有日记的用户
        diary_user_ids = db.query(diary_users.c.user_id).all()
        active_user_ids.update([uid[0] for uid in diary_user_ids])
        
        # 添加有聊天的用户
        chat_user_ids = db.query(chat_users.c.user_id).all()
        active_user_ids.update([uid[0] for uid in chat_user_ids])
        
        # 获取用户对象
        if active_user_ids:
            return db.query(User).filter(User.user_id.in_(active_user_ids)).all()
        else:
            return []
    
    async def _check_user_risk(self, db: Session, user: User):
        """检查单个用户的风险"""
        try:
            service = CrisisWarningService(db)
            
            # 检查用户是否在最近24小时内已经有预警
            recent_warnings = service.get_user_warnings(
                user_id=user.user_id,
                days=1,
                unresolved_only=True
            )
            
            # 如果已有未解决的高风险预警，跳过本次检查
            high_risk_warnings = [
                w for w in recent_warnings 
                if w.risk_level in [RiskLevel.HIGH, RiskLevel.CRITICAL]
            ]
            
            if high_risk_warnings:
                logger.debug(f"用户 {user.user_id} 已有未解决的高风险预警，跳过检查")
                return
            
            # 进行风险评估
            assessment = service.analyze_user_risk(user.user_id, days=7)
            
            # 根据风险等级决定是否创建预警
            if assessment.risk_level == RiskLevel.CRITICAL:
                # 紧急风险：立即创建预警
                service.create_warning(
                    user_id=user.user_id,
                    assessment=assessment,
                    warning_type=WarningType.BEHAVIOR_PATTERN,
                    source_data="定时监控检测到紧急风险"
                )
                logger.warning(f"用户 {user.user_id} 检测到紧急心理风险")
                
                # 这里可以添加紧急通知逻辑
                await self._send_emergency_alert(user, assessment)
                
            elif assessment.risk_level == RiskLevel.HIGH:
                # 高风险：创建预警
                service.create_warning(
                    user_id=user.user_id,
                    assessment=assessment,
                    warning_type=WarningType.BEHAVIOR_PATTERN,
                    source_data="定时监控检测到高风险"
                )
                logger.info(f"用户 {user.user_id} 检测到高心理风险")
                
            elif assessment.risk_level == RiskLevel.MEDIUM:
                # 中等风险：记录但不创建预警，可以发送关怀提醒
                logger.info(f"用户 {user.user_id} 检测到中等心理风险")
                await self._send_care_reminder(user, assessment)
            
            # 记录检查日志
            logger.debug(f"用户 {user.user_id} 风险检查完成，风险等级: {assessment.risk_level.value}")
            
        except Exception as e:
            logger.error(f"检查用户 {user.user_id} 风险时发生错误: {str(e)}")
    
    async def _send_emergency_alert(self, user: User, assessment):
        """发送紧急预警通知"""
        # 这里可以实现紧急通知逻辑，比如：
        # 1. 发送邮件给用户
        # 2. 通知管理员
        # 3. 推送消息到用户设备
        # 4. 记录到专门的紧急事件表
        
        logger.critical(
            f"紧急心理危机预警 - 用户ID: {user.user_id}, "
            f"风险评分: {assessment.score}, "
            f"原因: {'; '.join(assessment.reasons)}"
        )
        
        # 示例：可以在这里集成邮件或短信服务
        # await send_emergency_email(user.email, assessment)
        # await notify_crisis_team(user, assessment)
    
    async def _send_care_reminder(self, user: User, assessment):
        """发送关怀提醒"""
        # 为中等风险用户发送温和的关怀提醒
        logger.info(
            f"发送关怀提醒 - 用户ID: {user.user_id}, "
            f"风险评分: {assessment.score}"
        )
        
        # 这里可以实现关怀提醒逻辑，比如：
        # 1. 发送鼓励性的推送消息
        # 2. 推荐放松活动
        # 3. 提供心理健康资源链接
        
    async def manual_check_user(self, user_id: int) -> dict:
        """手动检查指定用户的风险（用于API调用）"""
        try:
            db = next(get_db())
            try:
                user = db.query(User).filter(User.user_id == user_id).first()
                if not user:
                    return {"error": "用户不存在"}
                
                service = CrisisWarningService(db)
                assessment = service.analyze_user_risk(user_id, days=14)
                
                return {
                    "user_id": user_id,
                    "risk_level": assessment.risk_level.value,
                    "score": assessment.score,
                    "reasons": assessment.reasons,
                    "recommendations": assessment.recommendations,
                    "check_time": datetime.now().isoformat()
                }
            finally:
                db.close()
                
        except Exception as e:
            logger.error(f"手动检查用户 {user_id} 失败: {str(e)}")
            return {"error": str(e)}

# 全局监控任务实例
crisis_monitor = CrisisMonitoringTask()
