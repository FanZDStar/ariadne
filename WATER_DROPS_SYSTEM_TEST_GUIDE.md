水滴系统测试指南

## 1. 创建数据库表

在 MySQL 中执行以下 SQL 文件：

```sql
source C:\Users\86135\Desktop\ariadne\database\water_drops_system.sql
```

或者直接执行：

```sql
CREATE TABLE IF NOT EXISTS user_water_drops (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    water_drops INT NOT NULL DEFAULT 0 COMMENT '用户当前拥有的水滴数量',
    total_earned INT NOT NULL DEFAULT 0 COMMENT '累计获得的水滴总数',
    total_used INT NOT NULL DEFAULT 0 COMMENT '累计使用的水滴总数',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY unique_user (user_id),
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户水滴表';
```

## 2. 验证后端 API

### 2.1 获取水滴状态

```bash
curl -X GET "http://localhost:8000/water-drops/status" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 2.2 领取水滴

```bash
curl -X POST "http://localhost:8000/water-drops/claim" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

### 2.3 转换水滴为能量

```bash
curl -X POST "http://localhost:8000/water-drops/convert-to-energy" \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## 3. 前端测试步骤

1. 登录应用
2. 进入心灵树洞页面
3. 检查页面顶部右侧是否显示水滴数量 💧
4. 检查左下角是否有任务按钮 🎁
5. 点击任务按钮，查看任务弹窗
6. 如果可以领取，点击绿色按钮领取 10 个水滴
7. 点击水壶图标，将水滴转换为能量

## 4. 功能说明

- **水滴获取**：每小时可领取 10 个水滴，需要点击任务按钮领取
- **冷却时间**：领取后需等待 1 小时才能再次领取
- **水滴转换**：点击水壶可将所有水滴一比一转换为能量
- **能量升级**：每 100 能量升 1 级，最高 30 级

## 5. 常见问题

### 问题 1：前端报错 "request:fail timeout"

- 检查后端服务是否正常运行
- 检查数据库表是否已创建
- 查看后端控制台是否有错误信息

### 问题 2：后端报错 "ImportError: cannot import name 'Base'"

- 已修复：将导入从 `app.core.database` 改为 `app.database.session`

### 问题 3：外键约束错误

- 已修复：将 `users.id` 改为 `users.user_id`

## 6. 数据库查询验证

检查用户水滴数据：

```sql
SELECT * FROM user_water_drops WHERE user_id = YOUR_USER_ID;
```

检查冷却记录：

```sql
SELECT * FROM user_watering_cooldown WHERE user_id = YOUR_USER_ID;
```

检查能量数据：

```sql
SELECT * FROM user_tree_energy WHERE user_id = YOUR_USER_ID;
```
