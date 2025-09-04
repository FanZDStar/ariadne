"""
数据加密迁移脚本
将现有的明文数据加密存储
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings
from app.utils.encryption import encryption
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def migrate_diary_data(session):
    """迁移日记数据"""
    logger.info("开始迁移日记数据...")
    
    # 查询所有私密日记
    diaries = session.query(EmotionalDiary).filter(EmotionalDiary.is_private == True).all()
    
    updated_count = 0
    for diary in diaries:
        try:
            # 检查是否已经加密
            if not encryption.is_encrypted(diary.title):
                diary.title = encryption.encrypt_text(diary.title)
                updated_count += 1
            
            if not encryption.is_encrypted(diary.content):
                diary.content = encryption.encrypt_text(diary.content)
                updated_count += 1
                
        except Exception as e:
            logger.error(f"加密日记 {diary.diary_id} 失败: {e}")
    
    logger.info(f"日记数据迁移完成，共更新 {updated_count} 条记录")

def migrate_whisper_data(session):
    """迁移悄悄话数据"""
    logger.info("开始迁移悄悄话数据...")
    
    # 查询所有匿名悄悄话
    whispers = session.query(TreeHoleWhisper).filter(TreeHoleWhisper.is_anonymous == True).all()
    
    updated_count = 0
    for whisper in whispers:
        try:
            # 检查是否已经加密
            if not encryption.is_encrypted(whisper.content):
                whisper.content = encryption.encrypt_text(whisper.content)
                updated_count += 1
                
        except Exception as e:
            logger.error(f"加密悄悄话 {whisper.whisper_id} 失败: {e}")
    
    # 查询所有匿名评论
    comments = session.query(TreeHoleComment).filter(TreeHoleComment.is_anonymous == True).all()
    
    for comment in comments:
        try:
            # 检查是否已经加密
            if not encryption.is_encrypted(comment.content):
                comment.content = encryption.encrypt_text(comment.content)
                updated_count += 1
                
        except Exception as e:
            logger.error(f"加密评论 {comment.comment_id} 失败: {e}")
    
    logger.info(f"悄悄话数据迁移完成，共更新 {updated_count} 条记录")

def migrate_chat_data(session):
    """迁移聊天数据"""
    logger.info("开始迁移聊天数据...")
    
    # 查询所有聊天消息
    messages = session.query(ChatMessage).all()
    
    updated_count = 0
    for message in messages:
        try:
            # 检查是否已经加密
            if not encryption.is_encrypted(message.content):
                message.content = encryption.encrypt_text(message.content)
                updated_count += 1
                
        except Exception as e:
            logger.error(f"加密消息 {message.id} 失败: {e}")
    
    logger.info(f"聊天数据迁移完成，共更新 {updated_count} 条记录")

def backup_database():
    """备份数据库"""
    import subprocess
    import datetime
    
    backup_file = f"ariadne_backup_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.sql"
    backup_path = os.path.join(os.path.dirname(__file__), backup_file)
    
    try:
        # 假设MySQL连接信息
        cmd = [
            'mysqldump',
            '-h', 'localhost',
            '-u', 'root',
            '-p',  # 会提示输入密码
            'ariadne'
        ]
        
        with open(backup_path, 'w') as f:
            subprocess.run(cmd, stdout=f, check=True)
        
        logger.info(f"数据库备份完成: {backup_path}")
        return True
    except Exception as e:
        logger.error(f"数据库备份失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("阿里阿德涅数据加密迁移工具")
    print("=" * 60)
    print("此工具将对现有的敏感数据进行加密处理")
    print("包括:")
    print("1. 私密日记的标题和内容")
    print("2. 匿名悄悄话和评论")
    print("3. 所有聊天消息")
    print()
    
    # 确认执行
    confirm = input("请确认是否继续？(输入 'yes' 继续): ")
    if confirm.lower() != 'yes':
        print("操作已取消")
        return
    
    # 备份提醒
    print("\n⚠️  强烈建议在执行前备份数据库！")
    backup_confirm = input("是否现在备份数据库？(输入 'yes' 备份): ")
    if backup_confirm.lower() == 'yes':
        if not backup_database():
            print("备份失败，建议手动备份后再继续")
            return
    
    # 创建数据库连接
    engine = create_engine(settings.database_url)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = SessionLocal()
    
    try:
        # 开始迁移
        logger.info("开始数据加密迁移...")
        
        # 迁移日记数据
        migrate_diary_data(session)
        
        # 迁移悄悄话数据
        migrate_whisper_data(session)
        
        # 迁移聊天数据
        migrate_chat_data(session)
        
        # 提交更改
        session.commit()
        logger.info("所有数据迁移完成！")
        
    except Exception as e:
        logger.error(f"迁移过程中发生错误: {e}")
        session.rollback()
        logger.info("已回滚所有更改")
    finally:
        session.close()

if __name__ == "__main__":
    main()
