# 数据隐私保护改进建议

## 1. 敏感数据加密
```python
# 在app/utils/encryption.py中添加加密功能
from cryptography.fernet import Fernet
import os

class DataEncryption:
    def __init__(self):
        self.key = os.getenv('ENCRYPTION_KEY', Fernet.generate_key())
        self.cipher = Fernet(self.key)
    
    def encrypt_sensitive_data(self, data: str) -> str:
        """加密敏感数据"""
        return self.cipher.encrypt(data.encode()).decode()
    
    def decrypt_sensitive_data(self, encrypted_data: str) -> str:
        """解密敏感数据"""
        return self.cipher.decrypt(encrypted_data.encode()).decode()
```

## 2. 数据访问控制
```python
# 在app/core/privacy.py中添加隐私控制
class PrivacyManager:
    @staticmethod
    def can_access_diary(current_user_id: int, diary_user_id: int, is_private: bool) -> bool:
        """检查是否可以访问日记"""
        if current_user_id == diary_user_id:
            return True
        return not is_private
    
    @staticmethod
    def anonymize_user_data(user_data: dict) -> dict:
        """用户数据匿名化"""
        sensitive_fields = ['email', 'bio', 'real_name']
        for field in sensitive_fields:
            if field in user_data:
                user_data[field] = "***"
        return user_data
```

## 3. 审计日志
```python
# 在app/models/audit_log.py中添加审计功能
class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    action = Column(String(100), nullable=False)  # CREATE, READ, UPDATE, DELETE
    resource_type = Column(String(50), nullable=False)  # diary, chat, etc.
    resource_id = Column(Integer)
    ip_address = Column(String(45))
    user_agent = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
```

## 4. 数据保留策略
```python
# 在app/tasks/data_retention.py中添加数据清理任务
import asyncio
from datetime import datetime, timedelta

class DataRetentionManager:
    @staticmethod
    async def cleanup_expired_sessions():
        """清理过期会话"""
        # 删除7天前的过期会话
        pass
    
    @staticmethod
    async def anonymize_old_data():
        """匿名化历史数据"""
        # 对6个月前的数据进行匿名化处理
        pass
```

## 5. 配置文件更新
```python
# 在app/core/config.py中添加隐私相关配置
class Settings(BaseSettings):
    # ... 现有配置 ...
    
    # 隐私保护配置
    encryption_key: str
    data_retention_days: int = 365
    session_timeout_minutes: int = 30
    enable_audit_log: bool = True
    
    # 性能优化配置
    db_pool_size: int = 20
    db_max_overflow: int = 30
    cache_ttl_seconds: int = 300
```
