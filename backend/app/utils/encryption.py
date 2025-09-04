"""
数据加密工具类
用于敏感数据的加解密处理
"""
import os
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class DataEncryption:
    """数据加密类"""
    
    def __init__(self, password: Optional[str] = None):
        """
        初始化加密器
        
        Args:
            password: 加密密码，如果为None则从环境变量获取
        """
        if password is None:
            password = os.getenv('ENCRYPTION_PASSWORD', 'ariadne_default_key_2025')
        
        # 固定盐值，确保相同密码生成相同密钥
        salt = b'ariadne_salt_2025'
        
        # 生成密钥
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        self.cipher = Fernet(key)
    
    def encrypt_text(self, text: str) -> str:
        """
        加密文本
        
        Args:
            text: 要加密的文本
            
        Returns:
            加密后的base64编码字符串
        """
        try:
            if not text:
                return text
            
            encrypted_data = self.cipher.encrypt(text.encode('utf-8'))
            return base64.urlsafe_b64encode(encrypted_data).decode('utf-8')
        except Exception as e:
            logger.error(f"加密失败: {e}")
            # 如果加密失败，返回原文本（生产环境应该抛出异常）
            return text
    
    def decrypt_text(self, encrypted_text: str) -> str:
        """
        解密文本
        
        Args:
            encrypted_text: 加密的base64编码字符串
            
        Returns:
            解密后的文本
        """
        try:
            if not encrypted_text:
                return encrypted_text
            
            encrypted_data = base64.urlsafe_b64decode(encrypted_text.encode('utf-8'))
            decrypted_data = self.cipher.decrypt(encrypted_data)
            return decrypted_data.decode('utf-8')
        except Exception as e:
            logger.error(f"解密失败: {e}")
            # 如果解密失败，返回原文本（可能是未加密的历史数据）
            return encrypted_text
    
    def is_encrypted(self, text: str) -> bool:
        """
        判断文本是否已加密
        
        Args:
            text: 要检查的文本
            
        Returns:
            True if encrypted, False otherwise
        """
        try:
            # 尝试base64解码，如果成功且能解密，则认为是加密数据
            base64.urlsafe_b64decode(text.encode('utf-8'))
            self.decrypt_text(text)
            return True
        except:
            return False

# 全局加密实例
encryption = DataEncryption()
