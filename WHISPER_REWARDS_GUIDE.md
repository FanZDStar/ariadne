# 每日互动奖励系统使用指南

## 功能概述

用户在心灵树洞进行互动（评论、发布悄悄话）时可以获得水滴奖励，用于浇灌心灵树。

## 奖励规则

### 1. 评论奖励

- **奖励数量**：每条评论获得 **3💧 水滴**
- **每日上限**：每天最多可获得 **4 次** 评论奖励（共 12💧）
- **触发时机**：在悄悄话详情页成功发送评论后自动发放

### 2. 发布悄悄话奖励

- **奖励数量**：每次发布获得 **3💧 水滴**
- **每日上限**：每天最多可获得 **4 次** 发布奖励（共 12💧）
- **触发时机**：成功发布悄悄话后自动发放

### 3. 总计

- 每天通过互动最多可获得 **24💧 水滴**（评论 12💧 + 发布 12💧）
- 每天凌晨 0 点重置计数

## 数据库表结构

### daily_comment_rewards

| 字段名                 | 类型      | 说明               |
| ---------------------- | --------- | ------------------ |
| id                     | INT       | 主键，自增         |
| user_id                | INT       | 用户 ID（外键）    |
| comment_date           | DATE      | 日期               |
| comment_count          | INT       | 当日评论次数       |
| comment_rewards_earned | INT       | 当日评论获得的水滴 |
| whisper_count          | INT       | 当日发布悄悄话次数 |
| whisper_rewards_earned | INT       | 当日发布获得的水滴 |
| created_at             | TIMESTAMP | 创建时间           |
| updated_at             | TIMESTAMP | 更新时间           |

**约束**：

- 唯一键：`unique_user_date (user_id, comment_date)` - 每个用户每天只有一条记录
- 外键：`user_id` 引用 `users(user_id)` 级联删除

## API 接口

### 1. 评论奖励接口

**请求**：

```http
POST /comment-rewards/reward-comment
Authorization: Bearer {token}
```

**响应**：

```json
{
  "success": true,
  "message": "评论成功！获得3个水滴",
  "water_drops_earned": 3,
  "total_comments_today": 1,
  "remaining_rewards_today": 3,
  "current_water_drops": 15
}
```

### 2. 发布奖励接口

**请求**：

```http
POST /comment-rewards/reward-whisper
Authorization: Bearer {token}
```

**响应**：

```json
{
  "success": true,
  "message": "发布成功！获得3个水滴",
  "water_drops_earned": 3,
  "total_whispers_today": 1,
  "remaining_rewards_today": 3,
  "current_water_drops": 18
}
```

### 3. 查询奖励状态

**请求**：

```http
GET /comment-rewards/comment-status
Authorization: Bearer {token}
```

**响应**：

```json
{
  "total_comments_today": 2,
  "rewards_earned_today": 6,
  "remaining_rewards_today": 2
}
```

### 4. 调试接口（查看所有记录）

**请求**：

```http
GET /comment-rewards/debug/all-records
Authorization: Bearer {token}
```

## 前端集成

### 评论页面（whisper-detail.vue）

```javascript
// 评论成功后自动调用
async submitComment() {
  // ... 发送评论 ...

  // 领取奖励
  this.claimCommentReward(token);
}

async claimCommentReward(token) {
  const response = await api.claimCommentReward(token);
  if (response.success) {
    uni.showToast({ title: response.message });
  }
}
```

### 发布页面（write-whisper.vue）

```javascript
// 发布成功后自动调用
async publishWhisper() {
  // ... 发布悄悄话 ...

  // 领取奖励
  this.claimWhisperReward(token);
}

async claimWhisperReward(token) {
  const response = await api.claimWhisperReward(token);
  if (response.success) {
    setTimeout(() => {
      uni.showToast({ title: `+${response.water_drops_earned}💧` });
    }, 800);
  }
}
```

## 数据库迁移

### 步骤 1：执行迁移脚本

```sql
-- 连接到数据库
mysql -u root -p ariadne

-- 执行迁移
source database/migration_add_whisper_rewards.sql
```

### 步骤 2：验证表结构

```sql
SHOW COLUMNS FROM daily_comment_rewards;
```

预期结果应包含：

- comment_count
- comment_rewards_earned
- whisper_count
- whisper_rewards_earned

## 使用流程

### 用户视角

1. **发布悄悄话**

   - 用户在"写悄悄话"页面发布内容
   - 发布成功后显示 "+3💧"
   - 每天前 4 次发布都会获得奖励

2. **评论悄悄话**

   - 用户在"倾听者"页面浏览悄悄话
   - 点击进入详情页发送评论
   - 评论成功后显示 "评论成功！获得 3 个水滴"
   - 每天前 4 条评论都会获得奖励

3. **使用水滴**
   - 在"心灵树洞"页面点击水壶图标
   - 将水滴转换为能量浇灌树木

### 后端日志

```
🔍 评论奖励请求 - 用户ID: 123, 今日日期: 2025-10-31
📊 找到今日记录 - 已评论次数: 2
💧 发放奖励 - 评论次数: 3, 本次奖励: 3
```

## 注意事项

1. **时区一致性**：确保前后端使用相同的时区（使用 `date.today()` 而不是 `datetime.utcnow()`）

2. **事务处理**：所有数据库操作都包含在事务中，失败会自动回滚

3. **错误处理**：奖励失败不会影响评论或发布功能，静默处理

4. **防刷机制**：通过数据库唯一键约束和计数器防止重复奖励

5. **每日重置**：每天凌晨 0 点自动重置（通过日期查询实现）

## 故障排查

### 问题 1：奖励只能领取 4 次总共，而不是每天 4 次

**原因**：日期查询条件失效

**解决**：

1. 检查后端日志，确认 `comment_date` 是否正确
2. 调用调试接口查看所有记录
3. 确保使用 `date.today()` 而不是 `datetime.now()`

### 问题 2：提示"今日奖励已达上限"但实际未达到

**原因**：数据库中存在旧数据

**解决**：

```sql
-- 查看用户的所有记录
SELECT * FROM daily_comment_rewards WHERE user_id = 123;

-- 删除旧记录（如果需要）
DELETE FROM daily_comment_rewards
WHERE user_id = 123 AND comment_date < CURDATE();
```

### 问题 3：奖励接口返回 500 错误

**原因**：表结构未更新或字段名不匹配

**解决**：

1. 执行迁移脚本 `migration_add_whisper_rewards.sql`
2. 重启后端服务
3. 检查模型定义是否与数据库一致

## 更新日志

- **2025-10-31**：添加发布悄悄话奖励功能，更新表结构
- **初版**：实现评论奖励功能
