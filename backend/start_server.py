#!/usr/bin/env python
"""
启动服务器脚本
"""
import sys
import os

# 将当前目录添加到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 设置环境变量
os.environ['PYTHONPATH'] = current_dir

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
