#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
生成50篇碎碎念数据脚本
- 生成50篇碎碎念（emotional_diaries）
- 其中20篇附带图片（diary_images）
- 用户ID固定为6
- 从前端static目录选取图片
"""

import os
import sys
import random
from datetime import datetime, timedelta
from typing import List

# 添加backend目录到路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'backend'))

from sqlalchemy.orm import sessionmaker
from app.database.session import engine
from app.models.emotional_diary import EmotionalDiary
from app.models.diary_image import DiaryImage

# 创建数据库会话
SessionLocal = sessionmaker(bind=engine)

# 用户ID
USER_ID = 6

# 心情类型
MOODS = ["very_happy", "happy", "neutral", "sad", "very_sad"]

# 可用的图片路径（相对于static目录，避免中文文件名）
STATIC_IMAGES = [
    "avatar.png",
    "chat-icon.png", 
    "logo.png",
    "love-experiment.png",
    "love-yourself.png",
    "self-dialog.png",
    "tree-day.png",
    "tree-hole.png",
    "tree-night.png",
    "mascot/happy.png",
    "mascot/idle.png",
    "mascot/sleep.png",
    "mascot/wave.png",
    # 避免使用中文文件名，容易出现URL编码问题
    # "mascot/头像 (10).png",
    # "mascot/头像 (11).png",
    # "mascot/头像 (4).png",
    # "mascot/头像 (6).png",
    # "mascot/头像 (7).png",
    # "mascot/头像 (8).png",
    # "mascot/头像 (9).png",
    "outfits/default-full.png",
    "outfits/dinosaur.png",
    "outfits/red-dress.png",
    "outfits/shark.png",
    "outfits/wangzaixiaoqiao.png"
]

# 碎碎念内容模板
DIARY_TEMPLATES = [
    {
        "title": "今天的小确幸",
        "content": "今天在咖啡厅看到一只小猫咪，它慵懒地趴在阳光下，那份安静美好让我想起了生活中的小确幸。有时候幸福就是这么简单，一束阳光，一杯咖啡，一个安静的午后。",
        "mood": "happy"
    },
    {
        "title": "深夜思绪",
        "content": "夜深了，窗外的城市逐渐安静下来。躺在床上看着天花板，脑海中闪过今天发生的种种。有些事情让我开心，有些让我思考。人生就像这深夜，有时明亮，有时黑暗，但总会有星星指引方向。",
        "mood": "neutral"
    },
    {
        "title": "雨天心情",
        "content": "今天下雨了，淅淅沥沥的雨声敲打着窗户。我坐在窗边，看着雨滴顺着玻璃缓缓滑落，心情也跟着沉静下来。雨天总是让人容易陷入回忆，想起过去的人和事。",
        "mood": "sad"
    },
    {
        "title": "意外的惊喜",
        "content": "今天收到了朋友寄来的礼物，完全没有预料到！打开包装的那一刻，心情瞬间被点亮了。原来被人惦记着是这么温暖的感觉，这个小小的惊喜让整天都变得明媚起来。",
        "mood": "very_happy"
    },
    {
        "title": "学习的烦恼",
        "content": "今天的学习进度不太理想，有些知识点怎么都理解不了。看着堆积如山的作业和复习资料，心情有点沉重。不过没关系，慢慢来吧，每天进步一点点就好。",
        "mood": "sad"
    },
    {
        "title": "运动后的愉悦",
        "content": "今天去跑了步，虽然过程很累，但跑完之后那种畅快淋漓的感觉真的太棒了！汗水和阳光，还有耳机里的音乐，这一切组成了完美的下午。运动真的是治愈心情的良药。",
        "mood": "happy"
    },
    {
        "title": "美食的治愈",
        "content": "今天做了一道新菜，虽然卖相不太好，但味道出乎意料的不错！在厨房忙碌的时光总是让人感到充实，看着食材在自己手中变成美味，有种莫名的成就感。",
        "mood": "happy"
    },
    {
        "title": "孤独的夜晚",
        "content": "一个人在家的夜晚总是格外安静，连时钟滴答声都显得特别清楚。有时候享受这种独处，有时候又觉得有些寂寞。人啊，总是这么矛盾，既渴望热闹，又需要安静。",
        "mood": "neutral"
    },
    {
        "title": "阅读的快乐",
        "content": "今天读完了一本好书，那种沉浸在文字世界里的感觉真的很奇妙。作者的文笔很好，故事情节也很吸引人，让我忘记了时间的流逝。好书就像好朋友，总能在合适的时候给你温暖。",
        "mood": "happy"
    },
    {
        "title": "工作的压力",
        "content": "最近工作压力有点大，总觉得时间不够用，事情一件接一件。有时候真想找个地方好好放松一下，让自己的心情也跟着轻松一些。不过想想，这也是成长的一部分吧。",
        "mood": "sad"
    },
    {
        "title": "春天的气息",
        "content": "今天路过公园，看到花儿都开了，春天真的来了！那种生机勃勃的感觉让人心情大好，忍不住多走了几圈。春天总是给人希望，让人觉得一切都是新的开始。",
        "mood": "very_happy"
    },
    {
        "title": "朋友的陪伴",
        "content": "今天和老朋友聊了很久，从学生时代聊到现在，从梦想聊到现实。虽然大家都在各自的路上忙碌，但这份友谊依然珍贵。有些人，就算很久不见，一见面还是那么亲切。",
        "mood": "happy"
    },
    {
        "title": "失落的一天",
        "content": "今天遇到了一些不顺心的事情，心情一下子跌到了谷底。有时候觉得自己很努力了，但结果却不如人意。不过没关系，明天又是新的一天，总会好起来的。",
        "mood": "very_sad"
    },
    {
        "title": "音乐的力量",
        "content": "今天听到一首很喜欢的歌，旋律一响起就觉得心情被治愈了。音乐真的很神奇，能够瞬间改变人的心境，让人从烦躁变得平静，从悲伤变得温暖。",
        "mood": "happy"
    },
    {
        "title": "平凡的美好",
        "content": "今天没有发生什么特别的事情，就是很平常的一天。但有时候觉得，这种平凡也是一种幸福。没有波澜，没有惊喜，也没有失落，就这样安静地过着，也挺好的。",
        "mood": "neutral"
    },
    {
        "title": "梦想与现实",
        "content": "今天想起了小时候的梦想，那时候总觉得长大后会做很多了不起的事情。现在长大了，虽然没有成为想象中的英雄，但也在自己的道路上努力前行。梦想或许会变，但那份追求美好的心永远不变。",
        "mood": "neutral"
    },
    {
        "title": "温暖的阳光",
        "content": "今天阳光特别好，暖暖地洒在身上，让人感到无比舒适。在阳光下散步，看着路边的小花小草，心情也跟着明朗起来。有阳光的日子，总是让人充满希望。",
        "mood": "happy"
    },
    {
        "title": "深夜的思考",
        "content": "夜已经很深了，但我还是睡不着，脑子里想着各种各样的事情。关于未来，关于过去，关于那些说不清道不明的情感。深夜总是容易让人多愁善感，但也容易看清一些平时被忽略的东西。",
        "mood": "neutral"
    },
    {
        "title": "小小的成就",
        "content": "今天完成了一个一直拖延的任务，虽然不是什么大事，但完成的那一刻还是很有成就感的。原来拖延症也是可以战胜的，关键是要迈出第一步。小小的进步也值得庆祝！",
        "mood": "happy"
    },
    {
        "title": "回忆的温度",
        "content": "今天整理东西的时候发现了一些老照片，看着照片里年轻的自己和朋友们，忍不住笑了。那时候我们都那么青涩，却那么快乐。时间真的过得很快，但美好的回忆永远温暖。",
        "mood": "happy"
    }
]

def generate_diary_content():
    """生成碎碎念内容"""
    # 复制模板并添加一些随机变化
    templates = DIARY_TEMPLATES.copy()
    
    # 生成额外的内容来达到50篇
    additional_templates = []
    for i in range(30):  # 需要额外30篇
        base_template = random.choice(DIARY_TEMPLATES)
        
        # 创建变化版本
        variations = {
            "今天的小确幸": [
                "午后的温暖时光", "意外的小惊喜", "街角的美好瞬间", "心情明媚的一天"
            ],
            "深夜思绪": [
                "夜晚的独白", "静夜里的思考", "月光下的回忆", "深夜的感悟"
            ],
            "雨天心情": [
                "细雨绵绵的下午", "雨声中的思绪", "被雨困住的心情", "雨天的诗意"
            ],
        }
        
        new_title = base_template["title"]
        if base_template["title"] in variations:
            new_title = random.choice(variations[base_template["title"]])
        else:
            new_title = f"{base_template['title']} {i+1}"
            
        additional_templates.append({
            "title": new_title,
            "content": base_template["content"],
            "mood": base_template["mood"]
        })
    
    return templates + additional_templates

def create_diary_entries():
    """创建日记条目"""
    db = SessionLocal()
    
    try:
        # 生成50篇碎碎念内容
        diary_contents = generate_diary_content()
        
        # 随机选择20篇作为带图片的日记
        entries_with_images = random.sample(range(50), 20)
        
        created_entries = []
        
        for i in range(50):
            content_data = diary_contents[i]
            
            # 随机生成创建时间（最近30天内）
            days_ago = random.randint(0, 30)
            hours_ago = random.randint(0, 23) 
            minutes_ago = random.randint(0, 59)
            created_time = datetime.now() - timedelta(days=days_ago, hours=hours_ago, minutes=minutes_ago)
            
            # 创建日记条目
            diary = EmotionalDiary(
                user_id=USER_ID,
                title=content_data["title"],
                content=content_data["content"],
                mood=content_data["mood"],
                created_at=created_time,
                updated_at=created_time,
                is_private=False,  # 设置为公开（已移除加密功能）
                image_count=1 if i in entries_with_images else 0,
                tags=generate_random_tags()  # 生成随机标签
            )
            
            db.add(diary)
            db.flush()  # 获取生成的ID
            
            # 如果这是一个带图片的日记，添加图片
            if i in entries_with_images:
                image_url = f"/static/{random.choice(STATIC_IMAGES)}"
                diary_image = DiaryImage(
                    diary_id=diary.diary_id,
                    image_url=image_url,
                    image_order=1
                )
                db.add(diary_image)
            
            created_entries.append({
                "diary_id": diary.diary_id,
                "title": content_data["title"],
                "has_image": i in entries_with_images
            })
            
            print(f"✅ 创建第 {i+1} 篇日记: {content_data['title']} {'(带图片)' if i in entries_with_images else ''}")
        
        # 提交所有更改
        db.commit()
        
        print(f"\n🎉 成功生成 {len(created_entries)} 篇碎碎念！")
        print(f"📸 其中 {len(entries_with_images)} 篇包含图片")
        print(f"👤 所有日记都属于用户ID: {USER_ID}")
        
        return created_entries
        
    except Exception as e:
        db.rollback()
        print(f"❌ 创建日记时发生错误: {e}")
        raise
    finally:
        db.close()

def generate_random_tags():
    """生成随机标签"""
    all_tags = [
        "心情", "日常", "思考", "回忆", "成长", 
        "友谊", "家庭", "工作", "学习", "运动",
        "美食", "音乐", "阅读", "旅行", "梦想",
        "感悟", "温暖", "治愈", "快乐", "安静"
    ]
    
    # 随机选择2-4个标签
    num_tags = random.randint(2, 4)
    selected_tags = random.sample(all_tags, num_tags)
    
    return selected_tags

def main():
    """主函数"""
    print("🚀 开始生成碎碎念数据...")
    print(f"📝 将生成50篇碎碎念，其中20篇包含图片")
    print(f"👤 用户ID: {USER_ID}")
    print(f"📂 图片来源: frontend/src/static/")
    print("-" * 50)
    
    try:
        entries = create_diary_entries()
        
        print("\n📊 生成统计:")
        print(f"总计: {len(entries)} 篇")
        
        with_images = [e for e in entries if e["has_image"]]
        without_images = [e for e in entries if not e["has_image"]]
        
        print(f"带图片: {len(with_images)} 篇")
        print(f"纯文字: {len(without_images)} 篇")
        
        print("\n🖼️ 带图片的日记:")
        for entry in with_images:
            print(f"  - ID: {entry['diary_id']}, 标题: {entry['title']}")
            
    except Exception as e:
        print(f"\n❌ 程序执行失败: {e}")
        return False
        
    print("\n✨ 数据生成完成！")
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)
