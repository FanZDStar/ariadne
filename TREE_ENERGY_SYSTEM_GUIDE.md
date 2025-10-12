# 树洞能量系统使用说明

## ✅ 已完成的功能

### 1. 数据库表

- ✅ 创建了 `user_tree_energy` 表
- ✅ 字段包含：能量值、等级、创建时间、更新时间

### 2. 后端 API

- ✅ `GET /tree-energy/status` - 获取用户能量和等级
- ✅ `POST /tree-energy/water` - 浇水增加能量（+20 能量/次）
- ✅ 自动升级逻辑（满 100 能量升 1 级）
- ✅ 最高等级限制（30 级封顶）

### 3. 前端页面

- ✅ 全屏背景图片显示
- ✅ 根据等级显示不同背景：
  - 1-19 级：sun1.png / moon1.png
  - 20-29 级：sun2.png / moon2.png
  - 30 级：sun3.png / moon3.png
- ✅ 能量条显示（顶部居中）
- ✅ 水壶图片居中显示，点击浇水
- ✅ 实时更新能量和等级
- ✅ 升级提示和震动反馈
- ✅ 白天/夜晚主题切换

## 🎮 使用方法

### 浇水获得能量

1. 点击页面中心的水壶图片
2. 每次浇水获得 20 能量
3. 满 100 能量自动升级
4. 升级后能量归零，从 0 开始累积

### 等级与背景

- **1 级（默认）**：显示 sun1/moon1
- **20 级**：解锁 sun2/moon2 🎉
- **30 级**：解锁 sun3/moon3 🎉（最高级）

### 主题切换

- 点击右上角 🌙/☀️ 按钮切换白天/夜晚主题
- 背景图片会根据主题和等级自动切换

## 🐛 调试信息

打开浏览器控制台（F12），可以看到详细的调试日志：

### 页面加载时

```
🔄 正在获取能量状态...
📡 API响应: {...}
✅ 能量状态更新成功: { energy: 0, level: 1, ... }
🎨 背景图片更新: { theme: 'day', level: 1, imagePath: '/static/sun1.png' }
```

### 浇水时

```
💧 开始浇水...
🔍 浇水前状态: { energy: 80, level: 1, backgroundImage: '/static/sun1.png' }
📡 浇水API响应: {...}
✅ 浇水成功，更新数据: { oldEnergy: 80, newEnergy: 0, oldLevel: 1, newLevel: 2, ... }
📊 等级变化: 1 → 2
⚡ 能量变化: 80 → 0
🎨 浇水后背景图片路径: /static/sun1.png
```

### 升级时

```
🎉 恭喜升级！当前等级: 20
🖼️ 当前背景图片路径: /static/sun2.png
```

### 主题切换时

```
🌓 主题切换: day → night
🖼️ 当前背景图片路径: /static/moon1.png
```

## 📝 注意事项

1. **图片文件**：确保以下图片存在于 `frontend/src/static/` 目录：

   - sun1.png
   - sun2.png
   - sun3.png
   - moon1.png
   - moon2.png
   - moon3.png
   - kettle.png

2. **登录状态**：必须登录后才能浇水和记录能量

3. **实时更新**：

   - 能量和等级会实时更新
   - 背景图片会根据等级自动切换
   - 使用 Vue 的 watch 监听数据变化

4. **升级规则**：
   - 每次浇水 +20 能量
   - 100 能量 = 1 级
   - 例如：80 能量时浇水 → 100 能量 → 升级到下一级，能量变为 0

## 🔧 技术实现

### 前端关键代码

```vue
computed: { backgroundImage() { // 根据等级和主题选择背景 if (this.theme ===
"day") { if (this.level >= 30) return "/static/sun3.png"; if (this.level >= 20)
return "/static/sun2.png"; return "/static/sun1.png"; } else { if (this.level >=
30) return "/static/moon3.png"; if (this.level >= 20) return
"/static/moon2.png"; return "/static/moon1.png"; } } }, watch: { level(newLevel)
{ console.log("等级变化:", newLevel); // 自动触发背景图片更新 } }
```

### 后端关键逻辑

```python
# 浇水 +20 能量
energy += 20

# 检查是否升级
while energy >= 100 and level < 30:
    level += 1
    energy -= 100
    leveled_up = True
```

## 🎯 测试步骤

1. ✅ 确保数据库表已创建
2. ✅ 启动后端服务器
3. ✅ 启动前端服务器
4. ✅ 登录账号
5. ✅ 进入心理树洞页面
6. ✅ 查看控制台日志
7. ✅ 点击水壶浇水
8. ✅ 观察能量条和等级变化
9. ✅ 浇水 5 次（100 能量）观察升级
10. ✅ 升级到 20 级和 30 级观察背景变化
11. ✅ 切换白天/夜晚主题观察背景变化

## 📊 数据库查询

查看用户能量和等级：

```sql
SELECT * FROM user_tree_energy;
```

手动修改等级测试背景切换：

```sql
-- 测试20级背景
UPDATE user_tree_energy SET level = 20, energy = 0 WHERE user_id = YOUR_USER_ID;

-- 测试30级背景
UPDATE user_tree_energy SET level = 30, energy = 0 WHERE user_id = YOUR_USER_ID;
```

## 🚀 部署清单

- [x] 数据库表创建脚本
- [x] 后端 API 接口
- [x] 前端页面修改
- [x] 样式调整
- [x] 调试日志
- [x] 实时更新逻辑
- [x] 背景图片切换
- [x] 能量条显示
- [x] 升级提示

## 💡 未来优化建议

1. 添加浇水动画效果
2. 添加升级特效
3. 添加每日浇水限制
4. 添加浇水历史记录
5. 添加成就系统
6. 添加背景图片预加载
7. 添加离线浇水补偿机制
