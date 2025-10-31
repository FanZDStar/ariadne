# 看板娘好感度系统使用指南

## 概述

看板娘好感度系统是在现有积分系统基础上引入的新功能，通过用户的各种行为来提升与看板娘的好感度，解锁不同等级的动作和奖励。

## 好感度获取规则

根据您的需求调整，好感度获取规则如下：

### 每日固定好感度来源：
- **每日登录**: +10 好感度 (每日一次)
- **购买服装**: 
  - 便宜服装(0-50星星): +10 好感度
  - 普通服装(51-100星星): +20 好感度  
  - 高级服装(101-200星星): +30 好感度
  - 豪华服装(201+星星): +50 好感度
- **情感对话**: +3 好感度 (前5次，每次+3)
- **完成日记**: +5 好感度 (每日一次)
- **心情记录**: +3 好感度 (每日一次)

## 好感度等级划分

共7个等级，每个等级都有对应的称号和解锁内容：

1. **1级 - 陌生** (0-99 好感度)
   - 解锁：挥手动作，5积分奖励
   - 随机掉落：10%概率获得1积分

2. **2级 - 熟悉** (100-299 好感度)
   - 解锁：微笑、点头动作，10积分奖励
   - 随机掉落：15%概率获得2积分或1水滴

3. **3级 - 友好** (300-599 好感度)
   - 解锁：爱心、眨眼动作，15积分奖励
   - 随机掉落：20%概率获得3积分或2水滴

4. **4级 - 亲密** (600-999 好感度)
   - 解锁：拥抱、舞蹈动作，20积分奖励
   - 随机掉落：25%概率获得5积分、3水滴或10星星优惠券

5. **5级 - 挚友** (1000-1499 好感度)
   - 解锁：飞吻、闪闪发光动作，30积分奖励
   - 随机掉落：30%概率获得8积分、5水滴或20星星优惠券

6. **6级 - 密友** (1500-2099 好感度)
   - 解锁：秘密、信任动作，40积分奖励
   - 随机掉落：35%概率获得10积分、8水滴、30星星优惠券或特殊服装

7. **7级 - 知己** (2100-2799 好感度)
   - 解锁：灵魂伴侣、永恒动作，50积分奖励
   - 随机掉落：40%概率获得15积分、10水滴、50星星优惠券或2件特殊服装

## 系统使用示例

### 1. 获取用户好感度信息

```python
from app.services.mascot_affection_service import MascotAffectionService
from app.database.session import get_db

# 初始化服务
db = next(get_db())
affection_service = MascotAffectionService(db)

# 获取用户好感度概览
user_id = 1
summary = affection_service.get_user_affection_summary(user_id)
print(f"当前好感度: {summary['current_affection']}")
print(f"当前等级: {summary['current_level']} - {summary['level_name']}")
print(f"等级进度: {summary['level_progress']:.2f}%")
```

### 2. 奖励每日登录好感度

```python
from app.utils.affection_types import MascotAffectionAction, AffectionSourceType

# 用户登录时奖励好感度
result = affection_service.award_affection(
    user_id=user_id,
    action=MascotAffectionAction.DAILY_LOGIN,
    source_type=AffectionSourceType.LOGIN
)

if result.rewarded:
    print(f"登录成功！{result.message}")
    if result.level_up:
        print(f"恭喜升级！从{result.old_level}级升到{result.new_level}级！")
else:
    print(f"今日已登录: {result.message}")
```

### 3. 购买服装时奖励好感度

```python
# 用户购买服装时自动计算好感度
star_cost = 150  # 服装价格150星星
outfit_id = "outfit_123"

result = affection_service.award_outfit_purchase_affection(
    user_id=user_id,
    star_cost=star_cost,
    source_id=outfit_id
)

if result.rewarded:
    print(f"购买成功！{result.message}")
```

### 4. 情感对话奖励好感度

```python
# 用户进行情感对话
chat_session_id = "chat_456"

result = affection_service.award_affection(
    user_id=user_id,
    action=MascotAffectionAction.EMOTION_CHAT,
    source_id=chat_session_id,
    source_type=AffectionSourceType.CHAT
)

if result.rewarded:
    print(f"对话愉快！{result.message}")
```

### 5. 获取好感度变动记录

```python
# 获取最近20条好感度记录
logs = affection_service.get_affection_logs(user_id, limit=20)

for log in logs:
    print(f"{log.created_at}: {log.description} {log.affection_change:+d}")
```

### 6. 获取未领取的奖励

```python
# 获取用户未领取的升级奖励
rewards = affection_service.get_unclaimed_rewards(user_id)

for reward in rewards:
    print(f"升级奖励: {reward.reward_content}")
    
    # 领取奖励
    success = affection_service.claim_reward(user_id, reward.id)
    if success:
        print("奖励领取成功！")
```

## 数据库初始化

1. **执行SQL脚本**:
   ```bash
   mysql -u username -p database_name < database/mascot_affection_schema.sql
   ```

2. **运行数据库迁移** (如果使用Alembic):
   ```bash
   alembic revision --autogenerate -m "Add mascot affection system"
   alembic upgrade head
   ```

## 集成到现有系统

### 在用户登录时自动奖励好感度

```python
# 在登录成功的路由中添加
@router.post("/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    # 现有登录逻辑...
    
    # 奖励登录好感度
    affection_service = MascotAffectionService(db)
    affection_result = affection_service.award_affection(
        user_id=user.user_id,
        action=MascotAffectionAction.DAILY_LOGIN,
        source_type=AffectionSourceType.LOGIN
    )
    
    # 在返回结果中包含好感度信息
    return {
        "user": user,
        "token": token,
        "affection_reward": affection_result if affection_result.rewarded else None
    }
```

### 在服装购买时自动奖励好感度

```python
# 在购买服装的路由中添加
@router.post("/purchase-outfit")
async def purchase_outfit(purchase_data: OutfitPurchase, db: Session = Depends(get_db)):
    # 现有购买逻辑...
    
    # 奖励购买好感度
    affection_service = MascotAffectionService(db)
    affection_result = affection_service.award_outfit_purchase_affection(
        user_id=user_id,
        star_cost=outfit.star_cost,
        source_id=str(outfit.id)
    )
    
    return {
        "purchase": purchase_result,
        "affection_reward": affection_result
    }
```

## 注意事项

1. **每日限制**: 系统会自动检查每日获取限制，重复行为不会重复奖励
2. **等级计算**: 好感度值会自动计算等级和进度百分比
3. **升级奖励**: 升级时会自动创建奖励记录，需要用户主动领取
4. **随机掉落**: 不同等级有不同概率的随机奖励掉落
5. **数据一致性**: 所有好感度变动都会记录日志，确保可追溯

通过以上系统，用户与看板娘的互动将更加丰富有趣，增强用户粘性和参与度。
