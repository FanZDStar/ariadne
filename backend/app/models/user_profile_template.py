# file: ariadne/backend/app/models/user_profile_template.py
"""
用户个性化档案模板模型
用于存储用户填写的个人信息，供AI生成个性化回答时参考
"""

from sqlalchemy import Column, Integer, String, DateTime, JSON, Text, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.database.session import Base


class UserProfileTemplate(Base):
    """
    用户个性化档案表
    
    存储用户填写的个人信息，包括：
    - 基本信息：生日、星座
    - 性格标签：用户自定义或从预设标签选择
    - 爱好标签：用户自定义或从预设标签选择
    - 专业/职业标签：用户自定义或从预设标签选择
    """
    __tablename__ = "user_profile_templates"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, unique=True, nullable=False, index=True)
    
    # ========== 基本信息 ==========
    gender = Column(String(20), nullable=True)  # 性别: 男, 女, 其他
    birth_date = Column(String(10), nullable=True)  # 格式: YYYY-MM-DD
    zodiac_sign = Column(String(20), nullable=True)  # 十二星座: 白羊座, 金牛座等
    
    # ========== 性格特征 ==========
    # 预设性格标签 (JSON格式): 外向/内向, 感性/理性, 积极/保守等
    personality_tags = Column(JSON, nullable=True, default=[])
    # 自定义性格描述 (文本形式)
    personality_custom_description = Column(Text, nullable=True)
    
    # ========== 爱好兴趣 ==========
    # 预设爱好标签 (JSON格式): 阅读, 运动, 艺术, 编程等
    hobby_tags = Column(JSON, nullable=True, default=[])
    # 自定义爱好描述 (文本形式)
    hobby_custom_description = Column(Text, nullable=True)
    
    # ========== 专业/职业 ==========
    # 预设职业标签 (JSON格式): 学生, 工程师, 设计师等
    profession_tags = Column(JSON, nullable=True, default=[])
    # 自定义职业描述 (文本形式)
    profession_custom_description = Column(Text, nullable=True)
    # 具体专业/岗位
    job_title = Column(String(100), nullable=True)
    
    # ========== 其他个人背景 ==========
    # 生活阶段: 高中/大学/工作/已婚等
    life_stage = Column(String(50), nullable=True)
    # 城市/地区
    location = Column(String(100), nullable=True)
    # 个人座右铭或生活信条
    personal_motto = Column(Text, nullable=True)
    # 当前最关注的领域
    main_focus_areas = Column(JSON, nullable=True, default=[])
    
    # ========== 系统字段 ==========
    is_complete = Column(Boolean, default=False)  # 档案是否完整
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())


class PersonalityTagOption(Base):
    """
    性格标签预设选项表
    """
    __tablename__ = "personality_tag_options"
    
    id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String(50), unique=True, nullable=False)  # 标签名
    description = Column(Text, nullable=True)  # 标签描述
    category = Column(String(50), nullable=True)  # 分类: 内外向, 感理性等
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


class HobbyTagOption(Base):
    """
    爱好标签预设选项表
    """
    __tablename__ = "hobby_tag_options"
    
    id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String(50), unique=True, nullable=False)  # 标签名
    description = Column(Text, nullable=True)  # 标签描述
    category = Column(String(50), nullable=True)  # 分类: 运动, 艺术, 学习等
    emoji = Column(String(10), nullable=True)  # 对应的emoji
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


class ProfessionTagOption(Base):
    """
    专业/职业标签预设选项表
    """
    __tablename__ = "profession_tag_options"
    
    id = Column(Integer, primary_key=True, index=True)
    tag_name = Column(String(50), unique=True, nullable=False)  # 标签名
    description = Column(Text, nullable=True)  # 标签描述
    category = Column(String(50), nullable=True)  # 分类: 技术, 商业, 创意等
    related_skills = Column(JSON, nullable=True)  # 相关技能
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())


class ZodiacSignOption(Base):
    """
    十二星座预设选项表
    """
    __tablename__ = "zodiac_sign_options"
    
    id = Column(Integer, primary_key=True, index=True)
    sign_name = Column(String(20), unique=True, nullable=False)  # 星座名
    date_range = Column(String(50), nullable=True)  # 日期范围
    description = Column(Text, nullable=True)  # 星座性格描述
    emoji = Column(String(10), nullable=True)  # 对应的emoji
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
