#!/usr/bin/env python3
"""
ClearVoice API 服务启动脚本
"""

import uvicorn
from app.main import app

def main():
    """启动FastAPI服务器"""
    print("🚀 启动 ClearVoice API 服务...")
    print("📍 服务地址: http://localhost:8000")
    print("📖 API文档: http://localhost:8000/docs")
    print("🔄 按 Ctrl+C 停止服务")
    print("-" * 50)

    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",  # 本地开发使用localhost
        port=8000,
        reload=True,
        log_level="info",
        access_log=True
    )

if __name__ == "__main__":
    main()
