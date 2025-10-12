# 浇水冷却系统使用指南

## 功能概述

实现了 20 分钟浇水冷却机制，防止用户频繁浇水刷能量。

## 数据库结构

### user_watering_cooldown 表

```sql
CREATE TABLE user_watering_cooldown (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    last_watering_time DATETIME NOT NULL COMMENT '最后一次浇水时间',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    UNIQUE KEY unique_user (user_id)
);
```

## 后端 API

### GET /tree-energy/status

获取用户能量状态和冷却信息

**响应示例：**

```json
{
  "energy": 80,
  "level": 13,
  "energy_to_next_level": 20,
  "can_water": false,
  "remaining_seconds": 900,
  "next_watering_time": "2025-10-12T15:30:00"
}
```

### POST /tree-energy/water

浇水（需通过冷却检查）

**响应示例（成功）：**

```json
{
  "energy": 0,
  "level": 14,
  "leveled_up": true,
  "level_up_count": 1,
  "message": "恭喜升级！当前等级：14",
  "energy_to_next_level": 100,
  "can_water": false,
  "remaining_seconds": 1200
}
```

**响应示例（冷却中）：**

```json
{
  "detail": "浇水冷却中，还需等待 15分30秒"
}
```

## 前端功能

### 倒计时显示

- **冷却中**：显示红色倒计时（格式：`分钟:秒`）
- **可浇水**：显示绿色"可以浇水"提示
- **水壶状态**：冷却中时水壶半透明且灰度化

### 倒计时更新机制

- 页面加载时从 API 获取剩余秒数
- 使用 `setInterval` 每秒更新倒计时
- 倒计时结束时自动切换为"可以浇水"状态
- 页面卸载时清除定时器，防止内存泄漏

## 冷却时间配置

### 修改冷却时间

在 `backend/app/api/routes/tree_energy.py` 中修改：

```python
# 浇水冷却时间（分钟）
WATERING_COOLDOWN_MINUTES = 20  # 改为你想要的分钟数
```

## 测试步骤

1. **首次浇水**

   - 点击水壶，应该成功浇水
   - 能量 +20
   - 水壶变灰，下方显示倒计时 `20:00`

2. **冷却期间浇水**

   - 再次点击水壶
   - 应提示"冷却中，还需 X 分 X 秒"
   - 倒计时持续递减

3. **刷新页面**

   - 倒计时应该保持正确（从服务器重新获取）
   - 不会重置为 20 分钟

4. **冷却结束**
   - 倒计时到 0 后，自动显示"可以浇水"
   - 水壶恢复正常颜色
   - 可以再次浇水

## 样式说明

### 倒计时容器

- **冷却中**：红色背景 `rgba(255, 99, 71, 0.9)`
- **可浇水**：绿色背景 `rgba(76, 175, 80, 0.9)`
- 位置：水壶正下方，右下角区域

### 水壶样式

- **正常**：不透明度 0.95，原色
- **冷却中**：不透明度 0.5，灰度 50%
- **点击时**：放大到 1.15 倍

## 注意事项

1. **时区问题**：后端使用服务器本地时间，确保服务器时区设置正确
2. **定时器清理**：页面卸载时会自动清除定时器
3. **满级处理**：30 级且能量 ≥100 时，即使不在冷却期也无法浇水
4. **错误处理**：网络错误时会显示友好提示，不会破坏倒计时

## 未来优化方向

1. 使用 WebSocket 实时同步冷却状态（多设备）
2. 添加浇水历史记录
3. 实现浇水成就系统
4. 允许 VIP 用户缩短冷却时间
