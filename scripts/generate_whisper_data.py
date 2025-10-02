#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
悄悄话测试数据生成脚本
生成30条悄悄话数据，包含标题、内容、心情、标签、图片等完整信息
"""

import mysql.connector
import json
import random
from datetime import datetime, timedelta
import string

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'admin123',  # 请根据实际情况修改密码
    'database': 'ariadne',
    'charset': 'utf8mb4'
}

# 可用的用户ID (1-6)
USER_IDS = [1, 2, 3, 4, 5, 6]

# 心情类型
MOODS = ['very_happy', 'happy', 'neutral', 'sad', 'very_sad']

# 预设标签池
TAG_POOL = [
    '心情', '秘密', '困扰', '感悟', '日常', '吐槽', '想法', '回忆',
    '学习', '工作', '生活', '友情', '爱情', '家庭', '梦想', '焦虑',
    '开心', '难过', '迷茫', '感动', '孤独', '温暖', '希望', '压力'
]

# 匿名头像池 (从前端静态资源)
ANONYMOUS_AVATARS = [
    '/src/static/avatar/头像.png',
    '/src/static/avatar/头像 (2).png',
    '/src/static/avatar/头像 (3).png',
    '/src/static/avatar/头像 (4).png',
    '/src/static/avatar/头像 (5).png',
    '/src/static/avatar/头像 (6).png',
    '/src/static/avatar/头像 (7).png',
    '/src/static/avatar/头像 (8).png',
    '/src/static/avatar/头像 (9).png'
]

# 可用图片池 (从前端静态资源) - 使用相对路径，前端会正确处理
IMAGE_POOL = [
    'mascot/happy.png',
    'mascot/idle.png', 
    'mascot/sleep.png',
    'mascot/wave.png',
    'outfits/default-full.png',
    'outfits/dinosaur.png',
    'outfits/red-dress.png',
    'outfits/shark.png',
    'outfits/wangzaixiaoqiao.png',
    'tree-day.png',
    'tree-night.png',
    'love-experiment.png',
    'love-yourself.png'
]

# 悄悄话内容模板
WHISPER_TEMPLATES = [
    {
        'title': '今天的心情',
        'content': '今天的天气很好，心情也跟着变得明朗起来。阳光透过窗户洒在桌子上，让我想起了小时候无忧无虑的日子。',
        'mood': 'happy',
        'tags': ['心情', '阳光', '回忆']
    },
    {
        'title': '深夜的思考',
        'content': '又是一个失眠的夜晚，脑子里想着白天发生的事情。有时候觉得生活就像一团乱麻，不知道该从哪里开始整理。',
        'mood': 'sad',
        'tags': ['失眠', '思考', '迷茫']
    },
    {
        'title': '小确幸',
        'content': '今天路过咖啡店，闻到了熟悉的咖啡香味。买了一杯最爱的拿铁，坐在窗边看着来往的行人，这样的小确幸让人感到温暖。',
        'mood': 'neutral',
        'tags': ['咖啡', '温暖', '日常']
    },
    {
        'title': '压力山大',
        'content': '最近工作压力好大，每天都有做不完的事情。有时候真想逃到一个没有人认识我的地方，重新开始。',
        'mood': 'very_sad',
        'tags': ['压力', '工作', '逃避']
    },
    {
        'title': '意外的惊喜',
        'content': '今天收到了朋友寄来的明信片，上面写着"想你了"。虽然只是简单的三个字，但让我开心了一整天。',
        'mood': 'very_happy',
        'tags': ['友情', '惊喜', '感动']
    },
    {
        'title': '雨天随想',
        'content': '下雨了，坐在教室里听着雨声打在窗户上的声音。有种莫名的安静感，让人想要静静地思考一些事情。',
        'mood': 'neutral',
        'tags': ['雨天', '安静', '思考']
    },
    {
        'title': '孤独的夜晚',
        'content': '一个人在宿舍里，室友都回家了。看着空荡荡的房间，突然感到很孤独。好想有个人陪我说说话。',
        'mood': 'sad',
        'tags': ['孤独', '想家', '陪伴']
    },
    {
        'title': '新的开始',
        'content': '今天是新学期的第一天，心情既紧张又兴奋。希望这个学期能有新的收获，遇到更好的自己。',
        'mood': 'happy',
        'tags': ['新开始', '学习', '希望']
    },
    {
        'title': '美食治愈',
        'content': '心情不好的时候就想吃甜食。今天买了最爱的草莓蛋糕，甜甜的味道瞬间治愈了我的心情。',
        'mood': 'happy',
        'tags': ['美食', '治愈', '甜品']
    },
    {
        'title': '梦想与现实',
        'content': '有时候会想，我的梦想还能实现吗？现实总是那么残酷，但我还是想要继续努力，不想放弃。',
        'mood': 'neutral',
        'tags': ['梦想', '现实', '坚持']
    },
    {
        'title': '家人的温暖',
        'content': '妈妈今天打电话问我吃饭了没有，虽然只是简单的关心，但让我感受到了家的温暖。',
        'mood': 'very_happy',
        'tags': ['家庭', '温暖', '关心']
    },
    {
        'title': '考试焦虑',
        'content': '马上就要期末考试了，复习得不够充分，心里很焦虑。希望能够超常发挥，不要辜负自己的努力。',
        'mood': 'sad',
        'tags': ['考试', '焦虑', '努力']
    },
    {
        'title': '音乐的力量',
        'content': '听到一首很好听的歌，歌词写得特别好，好像在诉说着我的心声。音乐真的有治愈人心的力量。',
        'mood': 'happy',
        'tags': ['音乐', '治愈', '共鸣']
    },
    {
        'title': '深夜emo',
        'content': '为什么深夜总是特别容易emo？想起了很多往事，有开心的也有难过的，五味杂陈。',
        'mood': 'sad',
        'tags': ['深夜', 'emo', '往事']
    },
    {
        'title': '阳光明媚',
        'content': '今天的阳光特别好，决定出去走走。看到路边开着的小花，心情也跟着明媚起来了。',
        'mood': 'very_happy',
        'tags': ['阳光', '散步', '花朵']
    }
]

def generate_random_name():
    """生成随机的匿名名称 (ariadne_xxxxx格式)"""
    chars = string.ascii_lowercase + string.digits
    random_str = ''.join(random.choice(chars) for _ in range(5))
    return f'ariadne_{random_str}'

def select_random_tags():
    """随机选择1-5个标签"""
    num_tags = random.randint(1, 5)
    return random.sample(TAG_POOL, num_tags)

def select_random_images():
    """随机选择0-3张图片"""
    num_images = random.randint(0, 3)
    if num_images == 0:
        return []
    return random.sample(IMAGE_POOL, num_images)

def generate_whisper_data():
    """生成一条悄悄话数据"""
    template = random.choice(WHISPER_TEMPLATES)
    user_id = random.choice(USER_IDS)
    is_anonymous = random.choice([True, False])  # 随机决定是否匿名
    
    # 基础数据
    data = {
        'user_id': user_id,
        'title': template['title'],
        'content': template['content'],
        'mood': template['mood'],
        'tags': json.dumps(template['tags'], ensure_ascii=False),
        'is_anonymous': is_anonymous,
        'anonymous_name': generate_random_name() if is_anonymous else None,
        'anonymous_avatar': random.choice(ANONYMOUS_AVATARS) if is_anonymous else None,
        'like_count': random.randint(0, 20),
        'comment_count': random.randint(0, 5),
        'created_at': datetime.now() - timedelta(days=random.randint(0, 30)),
    }
    
    return data

def create_whisper_images(cursor, whisper_id, images):
    """创建悄悄话图片记录"""
    if not images:
        return
    
    image_sql = """
    INSERT INTO tree_hole_whisper_images (whisper_id, image_url, image_order, created_at)
    VALUES (%s, %s, %s, %s)
    """
    
    for i, image_url in enumerate(images):
        cursor.execute(image_sql, (whisper_id, image_url, i, datetime.now()))

def generate_whispers():
    """生成30条悄悄话数据"""
    try:
        # 连接数据库
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        print("🚀 开始生成悄悄话测试数据...")
        
        # 清空现有数据（可选）
        print("📝 清空现有悄悄话数据...")
        cursor.execute("DELETE FROM tree_hole_whisper_images")
        cursor.execute("DELETE FROM tree_hole_whispers")
        conn.commit()
        
        # 插入悄悄话数据
        whisper_sql = """
        INSERT INTO tree_hole_whispers 
        (user_id, title, content, mood, tags, is_anonymous, anonymous_name, anonymous_avatar, 
         like_count, comment_count, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for i in range(30):
            whisper_data = generate_whisper_data()
            images = select_random_images()
            
            # 插入悄悄话
            cursor.execute(whisper_sql, (
                whisper_data['user_id'],
                whisper_data['title'],
                whisper_data['content'], 
                whisper_data['mood'],
                whisper_data['tags'],
                whisper_data['is_anonymous'],
                whisper_data['anonymous_name'],
                whisper_data['anonymous_avatar'],
                whisper_data['like_count'],
                whisper_data['comment_count'],
                whisper_data['created_at'],
                whisper_data['created_at']
            ))
            
            whisper_id = cursor.lastrowid
            
            # 插入图片（如果有）
            create_whisper_images(cursor, whisper_id, images)
            
            print(f"✅ 生成第 {i+1} 条悄悄话: {whisper_data['title']} (用户ID: {whisper_data['user_id']}, 图片: {len(images)}张)")
        
        conn.commit()
        print(f"\n🎉 成功生成 30 条悄悄话测试数据！")
        
        # 统计信息
        cursor.execute("SELECT COUNT(*) FROM tree_hole_whispers")
        whisper_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM tree_hole_whisper_images") 
        image_count = cursor.fetchone()[0]
        
        print(f"📊 数据统计:")
        print(f"   - 悄悄话总数: {whisper_count}")
        print(f"   - 图片总数: {image_count}")
        
        cursor.close()
        conn.close()
        
    except mysql.connector.Error as err:
        print(f"❌ 数据库错误: {err}")
    except Exception as e:
        print(f"❌ 发生错误: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print("🌟 悄悄话测试数据生成器")
    print("=" * 50)
    
    # 提示用户确认数据库配置
    print("📋 数据库配置:")
    print(f"   主机: {DB_CONFIG['host']}")
    print(f"   数据库: {DB_CONFIG['database']}")
    print(f"   用户: {DB_CONFIG['user']}")
    print()
    
    confirm = input("🤔 请确认数据库配置是否正确，继续执行？(y/N): ")
    if confirm.lower() in ['y', 'yes']:
        generate_whispers()
    else:
        print("❌ 已取消执行")
