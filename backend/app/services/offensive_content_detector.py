"""
冒犯性内容检测服务
使用 thu-coai/roberta-base-cold 模型 + 关键词黑名单混合检测评论中的侮辱性词汇
"""
import logging
import os
import re
from pathlib import Path
from typing import Dict, Optional
from functools import lru_cache

logger = logging.getLogger(__name__)


class OffensiveContentDetector:
    """冒犯性内容检测器（AI模型 + 关键词黑名单混合策略）"""
    
    # 模糊匹配黑名单 - 包含即拦截（使用 set 以获得 O(1) 查找性能）
    SUBSTRING_BLACKLIST = {
        # --- 严重侮辱 ---
        "你妈的", "妈的", "你娘的", "你爹的", "妈逼", "马的", "马b", "ma de", "tmd", "TMD", 
        "他妈的", "他妈", "特么", "特么的",
        "草你", "艹你", "操你", "干你", "日你", "肏你", "cao ni", "gan ni", "上你",
        "去你妈", "去你妈的", "滚蛋", "滚你",
        "傻逼", "傻b", "沙比", "煞笔", "shabi", "sha bi", "shǎbī", "S B", "s b",
        "智障", "弱智", "脑残", "低能", "白痴", "傻子", "傻X", "傻x", "傻叉",
        "贱人", "婊子", "骚货", "荡妇", "biao zi", "sao huo",
        "狗日", "狗东西", "畜生", "禽兽", "狗屁", "狗娘养的",
        "废物", "垃圾", "废柴", "loser",
        "死全家", "死妈", "死爹", "户口本", "灵车", "骨灰", "绝后", "断子绝孙", "不得好死",
        
        # --- 网络用语缩写 ---
        "nmsl", "cnm", "cnmb", "mlgb", "wdnmd", "nmd", 
        "NMSL", "CNM", "CNMB", "MLGB", "WDNMD", "NMD",
        "fuck", "f*ck", "f**k", "ucking", "shit", "bitch", "b*tch", "bi*ch", "damn",
        
        # --- 性相关侮辱 ---
        "鸡巴", "鸡八", "jb", "JB", "屌", "diao", "老二",
        "pussy", "dick", "cock",
        
        # --- 其他攻击性词汇 ---
        "找死", "作死", "活腻", "欠打", "欠揍",
        "丑逼", "丑八怪", "死肥猪",
        
        # --- 常见变体 ---
        "卧槽", "我操", "我艹", "我草", "wocao", "woc",
        "尼玛", "你马", "你🐴",
        "傻吊", "傻屌", "煞吊", "煞屌",
        "给爷爬", "给老子", "给爷滚",
        "司马", "司马脸", "死妈脸",
        "你妈逼", "你妈b", "草泥马", "草拟吗",
        "操你妈", "操你娘", "日你妈",
        "去死", "找抽", "欠骂",
        "蠢货", "蠢猪", "蠢驴",
        "神经病", "有病吧", "脑子有坑",
    }
    
    # 精确匹配黑名单 - 仅当评论完全等于这些词时才拦截（避免误伤）
    EXACT_BLACKLIST = {
        # --- 单字或短词（极易误伤，必须精确匹配）---
        "操", "草", "艹", "日", "干", "肏", "gun", "cao", "ri", "gan",
        "滚", "爬", "pa",
        "逼", "bi", "B",
        "贱", "骚", "jian", "sao",
        "狗", "猪", "gou", "zhu",
        "傻", "sha",
        "爹", "爷", "娘", "妈",
        
        # --- 极短的侮辱性短语 ---
        "你妈", "你爹", "你娘",
        "去你的",
        "给爷", "爷",
        
        # --- 缩写（单独出现时）---
        "sb", "SB", "Sb", "sB",
        "cb", "dd",
        "wc", "WC", "wtf", "WTF",
        "cn",
    }
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self._initialized = False
        self._initialization_failed = False
        
    def _check_keywords(self, text: str) -> Optional[str]:
        """
        关键词黑名单检测（模糊匹配 + 精确匹配）
        
        策略：
        1. 先进行精确匹配（去除首尾空格后，整条评论完全等于某个敏感词）
        2. 再进行模糊匹配（评论中包含某个敏感词）
        
        Args:
            text: 待检测文本
            
        Returns:
            匹配到的敏感词，如果没有则返回 None
        """
        if not text:
            return None
        
        # 去除首尾空格并转小写（用于精确匹配）
        text_stripped = text.strip()
        text_lower = text_stripped.lower()
        
        # 第一步：精确匹配检测（仅当整条评论完全等于某个短词时才拦截）
        if text_stripped in self.EXACT_BLACKLIST or text_lower in self.EXACT_BLACKLIST:
            return text_stripped
        
        # 第二步：模糊匹配检测（只要评论中包含某个敏感词就拦截）
        text_lower_full = text.lower()  # 用于模糊搜索的完整小写文本
        for keyword in self.SUBSTRING_BLACKLIST:
            # 使用 in 操作符进行子串查找（O(n)，但对于 set 中的每个元素都很快）
            if keyword.lower() in text_lower_full:
                return keyword
        
        return None
        
    def _get_model_path(self):
        """获取模型路径（优先使用本地模型）"""
        # 本地模型路径
        current_file = Path(__file__)
        backend_dir = current_file.parent.parent.parent  # 到达 backend 目录
        local_model_path = backend_dir / "models" / "offensive_detector" / "local_model"
        
        # 检查本地模型是否存在
        if local_model_path.exists() and (local_model_path / "config.json").exists():
            logger.info(f"✅ 使用本地模型: {local_model_path}")
            return str(local_model_path)
        
        # 使用远程模型
        logger.info("⏬ 使用远程模型: thu-coai/roberta-base-cold")
        return "thu-coai/roberta-base-cold"
        
    def _lazy_load_model(self):
        """延迟加载模型 - 只在第一次使用时加载"""
        if self._initialized:
            return True
            
        if self._initialization_failed:
            logger.warning("模型初始化之前已失败，跳过检测")
            return False
            
        try:
            logger.info("开始加载冒犯性内容检测模型...")
            from transformers import pipeline
            
            # 获取模型路径（本地或远程）
            model_path = self._get_model_path()
            
            # 使用 pipeline 方式，最简单高效
            self.pipeline = pipeline(
                "text-classification",
                model=model_path,
                # 如果有 GPU 可以取消下面的注释
                # device=0
            )
            
            self._initialized = True
            logger.info("✅ 冒犯性内容检测模型加载成功")
            return True
            
        except Exception as e:
            logger.error(f"❌ 模型加载失败: {str(e)}")
            logger.warning("将跳过冒犯性内容检测功能")
            self._initialization_failed = True
            return False
    
    def check_content(self, text: str, threshold: float = 0.5) -> Dict:
        """
        检测文本是否包含冒犯性内容（AI模型 + 关键词黑名单）
        
        Args:
            text: 待检测的文本内容
            threshold: AI模型判定阈值 (0-1)，默认 0.5
            
        Returns:
            dict: {
                "is_offensive": bool,  # 是否为冒犯性内容
                "confidence": float,   # 置信度 (0-1)
                "label": str,          # 标签 (NORMAL/OFFENSIVE)
                "message": str,        # 提示消息
                "matched_keyword": str # 匹配到的敏感词（如果有）
            }
        """
        # 基本验证
        if not text or not text.strip():
            return {
                "is_offensive": False,
                "confidence": 0.0,
                "label": "NORMAL",
                "message": "内容为空",
                "matched_keyword": None
            }
        
        # 第一步：关键词黑名单检测（快速且准确）
        matched_keyword = self._check_keywords(text)
        if matched_keyword:
            logger.info(f"🚫 关键词检测: 发现敏感词 '{matched_keyword}'")
            return {
                "is_offensive": True,
                "confidence": 1.0,  # 关键词匹配置信度为100%
                "label": "OFFENSIVE",
                "message": f"包含敏感词 '{matched_keyword}'",
                "matched_keyword": matched_keyword
            }
        
        # 第二步：AI模型检测（捕获隐晦的攻击性内容）
        if not self._lazy_load_model():
            # 模型加载失败，仅依赖关键词检测
            logger.warning("模型未加载，仅使用关键词检测")
            return {
                "is_offensive": False,
                "confidence": 0.0,
                "label": "NORMAL",
                "message": "内容正常（仅关键词检测）",
                "matched_keyword": None
            }
        
        try:
            # 执行AI模型检测
            result = self.pipeline(text)[0]
            
            label = result['label']
            score = result['score']
            
            # LABEL_0 = NORMAL (非冒犯性)
            # LABEL_1 = OFFENSIVE (冒犯性)
            is_offensive = (label == "LABEL_1" and score >= threshold)
            
            # 构造返回结果
            return {
                "is_offensive": is_offensive,
                "confidence": score,
                "label": "OFFENSIVE" if label == "LABEL_1" else "NORMAL",
                "message": f"AI检测到冒犯性内容（置信度: {score:.1%}）" if is_offensive else "内容正常",
                "matched_keyword": None
            }
            
        except Exception as e:
            logger.error(f"AI模型检测失败: {str(e)}")
            # 检测失败时返回通过（不影响用户体验）
            return {
                "is_offensive": False,
                "confidence": 0.0,
                "label": "ERROR",
                "message": "AI检测失败，已通过",
                "matched_keyword": None
            }
    
    def batch_check(self, texts: list, threshold: float = 0.5) -> list:
        """
        批量检测多条文本（AI模型 + 关键词黑名单）
        
        Args:
            texts: 文本列表
            threshold: AI模型判定阈值
            
        Returns:
            list: 检测结果列表
        """
        results = []
        
        for text in texts:
            # 先检查关键词
            matched_keyword = self._check_keywords(text)
            if matched_keyword:
                results.append({
                    "is_offensive": True,
                    "confidence": 1.0,
                    "label": "OFFENSIVE",
                    "message": f"包含敏感词 '{matched_keyword}'",
                    "matched_keyword": matched_keyword
                })
                continue
            
            # 再用AI模型检测
            if not self._lazy_load_model():
                results.append({
                    "is_offensive": False,
                    "confidence": 0.0,
                    "label": "NORMAL",
                    "message": "内容正常（仅关键词检测）",
                    "matched_keyword": None
                })
                continue
            
            try:
                result = self.pipeline(text)[0]
                is_offensive = (result['label'] == "LABEL_1" and result['score'] >= threshold)
                
                results.append({
                    "is_offensive": is_offensive,
                    "confidence": result['score'],
                    "label": "OFFENSIVE" if result['label'] == "LABEL_1" else "NORMAL",
                    "message": f"AI检测到冒犯性内容（置信度: {result['score']:.1%}）" if is_offensive else "内容正常",
                    "matched_keyword": None
                })
            except Exception as e:
                logger.error(f"批量检测失败 (text: {text[:20]}...): {str(e)}")
                results.append({
                    "is_offensive": False,
                    "confidence": 0.0,
                    "label": "ERROR",
                    "message": "AI检测失败",
                    "matched_keyword": None
                })
        
        return results


# 全局单例实例（延迟加载）
@lru_cache(maxsize=1)
def get_offensive_detector() -> OffensiveContentDetector:
    """获取冒犯性内容检测器单例"""
    return OffensiveContentDetector()


# 便捷函数
def check_offensive_content(text: str, threshold: float = 0.5) -> Dict:
    """
    检测文本是否包含冒犯性内容的便捷函数（AI模型 + 关键词黑名单）
    
    Args:
        text: 待检测文本
        threshold: AI模型判定阈值，默认 0.5
        
    Returns:
        dict: 检测结果
    """
    detector = get_offensive_detector()
    return detector.check_content(text, threshold)
