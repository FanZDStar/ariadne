# 数据库优化实施指南

## 🎯 建议的执行顺序

### 1. 立即可执行（安全操作）

#### 步骤1：备份数据库
```bash
# 在 backend 目录下执行
cd E:\Desktop\online-ariadne\ariadne\backend
mysqldump -u root -p ariadne > ../database/ariadne_backup_$(Get-Date -Format "yyyyMMdd_HHmmss").sql
```

#### 步骤2：执行安全的索引优化
```bash
# 连接到MySQL数据库
mysql -u root -p ariadne

# 执行第一阶段的索引优化
source ../database/performance_optimization.sql
```

**预期效果：**
- 查询性能提升 20-40%
- 不影响现有功能
- 无数据丢失风险

### 2. 可选执行（根据需求）

#### 全文搜索索引
- 如果需要支持日记内容搜索功能，可以执行第二阶段
- 会增加存储空间和写入时间

#### 数据分区
- 当数据量超过100万条记录时考虑
- 需要在测试环境先验证

### 3. 定期维护（长期规划）

#### 数据归档
- 建议先制定数据保留政策
- 与用户协商数据保留期限

## 🔍 执行后验证

### 查看优化效果
```sql
-- 查看新添加的索引
SHOW INDEX FROM emotional_diaries;
SHOW INDEX FROM chat_messages;
SHOW INDEX FROM tree_hole_whispers;

-- 查看表大小
SELECT 
    table_name as '表名',
    ROUND(((data_length + index_length) / 1024 / 1024), 2) as '大小(MB)',
    table_rows as '行数'
FROM information_schema.tables 
WHERE table_schema = 'ariadne';
```

### 性能测试
```sql
-- 测试查询性能（执行前后对比）
EXPLAIN SELECT * FROM emotional_diaries 
WHERE user_id = 6 AND mood = 'happy' 
ORDER BY created_at DESC LIMIT 10;
```

## ⚠️ 注意事项

1. **备份是必须的** - 任何数据库操作前都要备份
2. **分阶段执行** - 不要一次性执行所有脚本
3. **监控性能** - 执行后观察系统性能变化
4. **测试功能** - 确保所有功能正常工作

## 🚨 如果出现问题

### 回滚索引
```sql
-- 如果索引导致问题，可以删除
DROP INDEX idx_user_mood_date ON emotional_diaries;
DROP INDEX idx_session_created ON chat_messages;
DROP INDEX idx_created_likes ON tree_hole_whispers;
```

### 恢复数据库
```bash
# 从备份恢复
mysql -u root -p ariadne < ariadne_backup_YYYYMMDD_HHMMSS.sql
```

## 📊 预期优化效果

- **查询速度**：提升 20-40%
- **并发处理**：提升 15-25%
- **数据库负载**：降低 10-20%
- **内存使用**：索引会增加 5-10% 内存使用
