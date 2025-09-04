"""
数据加密服务
处理敏感数据的加解密逻辑
"""
from typing import Dict, Any, List
from app.utils.encryption import encryption
import logging

logger = logging.getLogger(__name__)

class PrivacyService:
    """隐私数据处理服务"""
    
    @staticmethod
    def encrypt_diary_data(diary_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        加密日记数据
        
        Args:
            diary_data: 包含日记信息的字典
            
        Returns:
            处理后的数据字典
        """
        try:
            # 如果是私密日记，加密标题和内容
            if diary_data.get('is_private', True):
                if 'title' in diary_data:
                    diary_data['title'] = encryption.encrypt_text(diary_data['title'])
                if 'content' in diary_data:
                    diary_data['content'] = encryption.encrypt_text(diary_data['content'])
            
            return diary_data
        except Exception as e:
            logger.error(f"日记数据加密失败: {e}")
            return diary_data
    
    @staticmethod
    def decrypt_diary_data(diary_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解密日记数据
        
        Args:
            diary_data: 包含加密日记信息的字典
            
        Returns:
            解密后的数据字典
        """
        try:
            # 如果是私密日记，解密标题和内容
            if diary_data.get('is_private', True):
                if 'title' in diary_data:
                    diary_data['title'] = encryption.decrypt_text(diary_data['title'])
                if 'content' in diary_data:
                    diary_data['content'] = encryption.decrypt_text(diary_data['content'])
            
            return diary_data
        except Exception as e:
            logger.error(f"日记数据解密失败: {e}")
            return diary_data
    
    @staticmethod
    def encrypt_whisper_data(whisper_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        加密悄悄话数据
        
        Args:
            whisper_data: 包含悄悄话信息的字典
            
        Returns:
            处理后的数据字典
        """
        try:
            # 如果是匿名悄悄话，加密内容
            if whisper_data.get('is_anonymous', True):
                if 'content' in whisper_data:
                    whisper_data['content'] = encryption.encrypt_text(whisper_data['content'])
            
            return whisper_data
        except Exception as e:
            logger.error(f"悄悄话数据加密失败: {e}")
            return whisper_data
    
    @staticmethod
    def decrypt_whisper_data(whisper_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解密悄悄话数据
        
        Args:
            whisper_data: 包含加密悄悄话信息的字典
            
        Returns:
            解密后的数据字典
        """
        try:
            # 如果是匿名悄悄话，解密内容
            if whisper_data.get('is_anonymous', True):
                if 'content' in whisper_data:
                    whisper_data['content'] = encryption.decrypt_text(whisper_data['content'])
            
            return whisper_data
        except Exception as e:
            logger.error(f"悄悄话数据解密失败: {e}")
            return whisper_data
    
    @staticmethod
    def encrypt_chat_message(message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        加密聊天消息
        
        Args:
            message_data: 包含消息信息的字典
            
        Returns:
            处理后的数据字典
        """
        try:
            # 聊天消息始终加密
            if 'content' in message_data:
                message_data['content'] = encryption.encrypt_text(message_data['content'])
            
            return message_data
        except Exception as e:
            logger.error(f"聊天消息加密失败: {e}")
            return message_data
    
    @staticmethod
    def decrypt_chat_message(message_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        解密聊天消息
        
        Args:
            message_data: 包含加密消息信息的字典
            
        Returns:
            解密后的数据字典
        """
        try:
            # 聊天消息始终解密
            if 'content' in message_data:
                message_data['content'] = encryption.decrypt_text(message_data['content'])
            
            return message_data
        except Exception as e:
            logger.error(f"聊天消息解密失败: {e}")
            return message_data
    
    @staticmethod
    def decrypt_diary_list(diary_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        批量解密日记列表
        
        Args:
            diary_list: 日记列表
            
        Returns:
            解密后的日记列表
        """
        return [PrivacyService.decrypt_diary_data(diary) for diary in diary_list]
    
    @staticmethod
    def decrypt_whisper_list(whisper_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        批量解密悄悄话列表
        
        Args:
            whisper_list: 悄悄话列表
            
        Returns:
            解密后的悄悄话列表
        """
        return [PrivacyService.decrypt_whisper_data(whisper) for whisper in whisper_list]
    
    @staticmethod
    def decrypt_chat_history(chat_history: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        批量解密聊天历史
        
        Args:
            chat_history: 聊天历史列表
            
        Returns:
            解密后的聊天历史列表
        """
        return [PrivacyService.decrypt_chat_message(message) for message in chat_history]

# 全局隐私服务实例
privacy_service = PrivacyService()
