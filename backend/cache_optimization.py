# Redis缓存优化配置
# 在backend/requirements.txt中添加：
# redis==4.5.4
# aioredis==2.0.1

# app/core/cache.py
import redis
import json
from typing import Any, Optional
import asyncio

class CacheManager:
    def __init__(self):
        self.redis_client = redis.Redis(
            host='localhost',
            port=6379,
            db=0,
            decode_responses=True
        )
    
    async def get(self, key: str) -> Optional[Any]:
        """获取缓存数据"""
        try:
            data = self.redis_client.get(key)
            return json.loads(data) if data else None
        except Exception:
            return None
    
    async def set(self, key: str, value: Any, ttl: int = 300):
        """设置缓存数据"""
        try:
            self.redis_client.setex(
                key, 
                ttl, 
                json.dumps(value, ensure_ascii=False)
            )
        except Exception:
            pass
    
    async def delete(self, key: str):
        """删除缓存"""
        self.redis_client.delete(key)

# 缓存键定义
class CacheKeys:
    USER_PROFILE = "user:profile:{user_id}"
    DIARY_LIST = "diary:list:{user_id}:{page}"
    CHAT_HISTORY = "chat:history:{session_id}"
    TREE_HOLE_LIST = "tree_hole:list:{page}"

# 使用示例
cache = CacheManager()

# 在API路由中使用缓存
async def get_user_diaries_cached(user_id: int, page: int = 1):
    cache_key = CacheKeys.DIARY_LIST.format(user_id=user_id, page=page)
    
    # 尝试从缓存获取
    cached_data = await cache.get(cache_key)
    if cached_data:
        return cached_data
    
    # 缓存未命中，从数据库查询
    diaries = await get_user_diaries_from_db(user_id, page)
    
    # 缓存结果
    await cache.set(cache_key, diaries, ttl=300)
    
    return diaries
