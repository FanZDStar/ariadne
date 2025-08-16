import random
from datetime import datetime, timedelta

# 定义情绪类型
moods = ['very_happy', 'happy', 'neutral', 'sad', 'very_sad']

# 获取今天的日期
today = datetime.now()

# 存储生成的 SQL 语句
sql_statements = []

# 生成 365 条数据
for i in range(365):
    # 计算日期
    date = today - timedelta(days=i)
    # 随机选择情绪
    mood = random.choice(moods)
    # 生成标题和内容
    title = f"测试日记{i + 1}"
    content = f"今天的心情是 {mood.replace('_', ' ')}"
    # 格式化日期
    created_at = date.strftime('%Y-%m-%d %H:%M:%S')
    # 生成 SQL 插入语句
    sql = f"INSERT INTO emotional_diaries (user_id, title, content, mood, created_at) VALUES (6, '{title}', '{content}', '{mood}', '{created_at}');"
    sql_statements.append(sql)

# 输出所有 SQL 语句
with open("insert_emotional_diaries.sql", "w", encoding="utf-8") as file:
    file.write("\n".join(sql_statements))

print("SQL 插入语句已生成并保存到 insert_emotional_diaries.sql 文件中。")