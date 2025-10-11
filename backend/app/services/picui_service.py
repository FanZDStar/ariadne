# file: backend/app/services/picui_service.py
import os
import requests
from typing import Optional, Dict, Any
import logging
from app.core.config import settings

logger = logging.getLogger(__name__)

class PICUIService:
    """PICUI 图床服务"""
    
    def __init__(self):
        self.api_url = settings.picui_api_url
        self.token = settings.picui_token
        self.strategy_id = settings.picui_strategy_id
        self.album_id = settings.picui_album_id
        
        if not self.token:
            logger.warning("PICUI_TOKEN not configured, image upload may fail")
    
    def _get_headers(self) -> Dict[str, str]:
        """获取请求头"""
        headers = {"Accept": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    def _get_upload_headers(self) -> Dict[str, str]:
        """获取上传请求头 - 不设置Content-Type，让requests自动设置multipart/form-data"""
        headers = {}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers
    
    async def upload_image(
        self, 
        file_content: bytes, 
        filename: str,
        permission: int = 1,
        album_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        上传图片到 PICUI
        
        Args:
            file_content: 文件内容
            filename: 文件名
            permission: 权限 (1=公开, 0=私有)
            album_id: 相册ID
            
        Returns:
            上传结果
        """
        try:
            print(f"[PICUI诊断] 🔍 开始PICUI上传流程")
            print(f"[PICUI诊断] API URL: {self.api_url}")
            print(f"[PICUI诊断] 文件名: {filename}")
            print(f"[PICUI诊断] 文件大小: {len(file_content)} bytes")
            print(f"[PICUI诊断] 权限设置: {permission}")
            
            # 检查token是否配置
            if not self.token or self.token == "your_picui_token_here":
                print(f"[PICUI诊断] ❌ PICUI_TOKEN未配置或使用默认值")
                logger.error("PICUI_TOKEN not configured or using default value")
                return {
                    "success": False,
                    "message": "PICUI_TOKEN not configured"
                }
            
            print(f"[PICUI诊断] ✅ Token已配置: {self.token[:10]}...")
            
            url = f"{self.api_url}/upload"
            print(f"[PICUI诊断] 上传URL: {url}")
            
            # 准备文件数据
            content_type = self._get_content_type(filename)
            files = {
                'file': (filename, file_content, content_type)
            }
            print(f"[PICUI诊断] 文件MIME类型: {content_type}")
            
            # 准备表单数据
            data = {
                'permission': permission
            }
            
            # 添加相册ID（strategy_id不是必须的，先不传）
            if album_id:
                data['album_id'] = int(album_id)
                print(f"[PICUI诊断] 使用传入的相册ID: {album_id}")
            elif self.album_id:
                data['album_id'] = int(self.album_id)
                print(f"[PICUI诊断] 使用配置的相册ID: {self.album_id}")
            else:
                print(f"[PICUI诊断] 未设置相册ID")
            
            print(f"[PICUI诊断] 请求数据: {data}")
            print(f"[PICUI诊断] 开始发送HTTP请求...")
            
            # 获取请求头
            headers = self._get_upload_headers()
            print(f"[PICUI诊断] 请求头: {headers}")
            
            # 发送请求
            try:
                response = requests.post(
                    url,
                    headers=headers,
                    files=files,
                    data=data,
                    timeout=30
                )
                
                print(f"[PICUI诊断] ✅ HTTP请求发送成功")
                print(f"[PICUI诊断] 响应状态码: {response.status_code}")
                print(f"[PICUI诊断] 响应头: {dict(response.headers)}")
                print(f"[PICUI诊断] 响应内容: {response.text}")
                
            except requests.exceptions.Timeout:
                print(f"[PICUI诊断] ❌ 请求超时")
                return {
                    "success": False,
                    "message": "Request timeout"
                }
            except requests.exceptions.ConnectionError as e:
                print(f"[PICUI诊断] ❌ 连接错误: {e}")
                return {
                    "success": False,
                    "message": f"Connection error: {e}"
                }
            except requests.exceptions.RequestException as e:
                print(f"[PICUI诊断] ❌ 请求异常: {e}")
                return {
                    "success": False,
                    "message": f"Request error: {e}"
                }
            
            if response.status_code == 200:
                print(f"[PICUI诊断] ✅ HTTP状态码正常，解析响应...")
                try:
                    result = response.json()
                    print(f"[PICUI诊断] 解析后的JSON: {result}")
                except Exception as json_e:
                    print(f"[PICUI诊断] ❌ JSON解析失败: {json_e}")
                    return {
                        "success": False,
                        "message": f"JSON parse error: {json_e}"
                    }
                
                if result.get('status'):
                    print(f"[PICUI诊断] ✅ 图床返回成功状态")
                    data = result.get('data', {})
                    print(f"[PICUI诊断] 返回数据: {data}")
                    return {
                        "success": True,
                        "data": {
                            "key": data.get('key'),
                            "name": data.get('name'),
                            "url": data.get('links', {}).get('url'),
                            "thumbnail_url": data.get('links', {}).get('thumbnail_url'),
                            "delete_url": data.get('links', {}).get('delete_url'),
                            "size": data.get('size'),
                            "extension": data.get('extension'),
                            "md5": data.get('md5'),
                            "sha1": data.get('sha1')
                        }
                    }
                else:
                    print(f"[PICUI诊断] ❌ 图床返回失败状态: {result.get('message', 'Unknown error')}")
                    print(f"[PICUI诊断] 完整响应: {result}")
                    return {
                        "success": False,
                        "message": result.get('message', 'Upload failed')
                    }
            else:
                print(f"[PICUI诊断] ❌ HTTP状态码异常: {response.status_code}")
                print(f"[PICUI诊断] 响应文本: {response.text}")
                logger.error(f"PICUI upload failed: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "message": f"Upload failed with status {response.status_code}"
                }
                
        except Exception as e:
            print(f"[PICUI诊断] ❌ 图床上传异常: {str(e)}")
            print(f"[PICUI诊断] ❌ 异常类型: {type(e).__name__}")
            import traceback
            print(f"[PICUI诊断] ❌ 异常堆栈: {traceback.format_exc()}")
            logger.error(f"Error uploading to PICUI: {str(e)}")
            return {
                "success": False,
                "message": f"Upload error: {str(e)}"
            }
    
    async def delete_image(self, image_key: str) -> Dict[str, Any]:
        """
        删除图片
        
        Args:
            image_key: 图片密钥
            
        Returns:
            删除结果
        """
        try:
            url = f"{self.api_url}/images/{image_key}"
            
            response = requests.delete(
                url,
                headers=self._get_headers(),
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status'):
                    return {
                        "success": True,
                        "message": "Image deleted successfully"
                    }
                else:
                    return {
                        "success": False,
                        "message": result.get('message', 'Delete failed')
                    }
            else:
                logger.error(f"PICUI delete failed: {response.status_code} - {response.text}")
                return {
                    "success": False,
                    "message": f"Delete failed with status {response.status_code}"
                }
                
        except Exception as e:
            logger.error(f"Error deleting image from PICUI: {str(e)}")
            return {
                "success": False,
                "message": f"Delete error: {str(e)}"
            }
    
    def _get_content_type(self, filename: str) -> str:
        """根据文件名获取内容类型"""
        extension = filename.lower().split('.')[-1] if '.' in filename else ''
        content_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp',
            'bmp': 'image/bmp'
        }
        return content_types.get(extension, 'application/octet-stream')
    
    @staticmethod
    def is_valid_image_type(filename: str) -> bool:
        """检查是否为有效的图片类型"""
        if not filename or '.' not in filename:
            return False
        valid_extensions = {'jpg', 'jpeg', 'png', 'gif', 'webp', 'bmp'}
        extension = filename.lower().split('.')[-1]
        return extension in valid_extensions
    
    @staticmethod
    def is_valid_file_size(size: int, max_size_mb: int = 10) -> bool:
        """检查文件大小是否有效"""
        max_size_bytes = max_size_mb * 1024 * 1024
        return size <= max_size_bytes

# 创建全局实例
picui_service = PICUIService()