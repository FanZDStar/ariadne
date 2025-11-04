"""
冒犯性内容检测服务
使用 thu-coai/roberta-base-cold 模型检测评论中的侮辱性词汇
"""
import logging
import os
from pathlib import Path
from typing import Dict, Optional
from functools import lru_cache

logger = logging.getLogger(__name__)


class OffensiveContentDetector:
    """冒犯性内容检测器"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self._initialized = False
        self._initialization_failed = False
        
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
    
    def check_content(self, text: str, threshold: float = 0.7) -> Dict:
        """
        检测文本是否包含冒犯性内容
        
        Args:
            text: 待检测的文本内容
            threshold: 判定为冒犯性内容的阈值 (0-1)，默认 0.7
            
        Returns:
            dict: {
                "is_offensive": bool,  # 是否为冒犯性内容
                "confidence": float,   # 置信度 (0-1)
                "label": str,          # 标签 (NORMAL/OFFENSIVE)
                "message": str         # 提示消息
            }
        """
        # 基本验证
        if not text or not text.strip():
            return {
                "is_offensive": False,
                "confidence": 0.0,
                "label": "NORMAL",
                "message": "内容为空"
            }
        
        # 延迟加载模型
        if not self._lazy_load_model():
            # 模型加载失败，返回通过（不阻止用户评论）
            logger.warning("模型未加载，跳过检测")
            return {
                "is_offensive": False,
                "confidence": 0.0,
                "label": "NORMAL",
                "message": "检测服务不可用，已通过"
            }
        
        try:
            # 执行检测
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
                "message": f"检测到冒犯性内容（置信度: {score:.1%}）" if is_offensive else "内容正常"
            }
            
        except Exception as e:
            logger.error(f"内容检测失败: {str(e)}")
            # 检测失败时返回通过（不影响用户体验）
            return {
                "is_offensive": False,
                "confidence": 0.0,
                "label": "ERROR",
                "message": "检测失败，已通过"
            }
    
    def batch_check(self, texts: list, threshold: float = 0.7) -> list:
        """
        批量检测多条文本
        
        Args:
            texts: 文本列表
            threshold: 判定阈值
            
        Returns:
            list: 检测结果列表
        """
        if not self._lazy_load_model():
            return [{"is_offensive": False, "confidence": 0.0, "label": "NORMAL", "message": "检测服务不可用"} 
                    for _ in texts]
        
        try:
            results = self.pipeline(texts)
            
            return [
                {
                    "is_offensive": (result['label'] == "LABEL_1" and result['score'] >= threshold),
                    "confidence": result['score'],
                    "label": "OFFENSIVE" if result['label'] == "LABEL_1" else "NORMAL",
                    "message": f"检测到冒犯性内容（置信度: {result['score']:.1%}）" 
                               if (result['label'] == "LABEL_1" and result['score'] >= threshold)
                               else "内容正常"
                }
                for result in results
            ]
            
        except Exception as e:
            logger.error(f"批量检测失败: {str(e)}")
            return [{"is_offensive": False, "confidence": 0.0, "label": "ERROR", "message": "检测失败"} 
                    for _ in texts]


# 全局单例实例（延迟加载）
@lru_cache(maxsize=1)
def get_offensive_detector() -> OffensiveContentDetector:
    """获取冒犯性内容检测器单例"""
    return OffensiveContentDetector()


# 便捷函数
def check_offensive_content(text: str, threshold: float = 0.7) -> Dict:
    """
    检测文本是否包含冒犯性内容的便捷函数
    
    Args:
        text: 待检测文本
        threshold: 判定阈值，默认 0.7
        
    Returns:
        dict: 检测结果
    """
    detector = get_offensive_detector()
    return detector.check_content(text, threshold)
