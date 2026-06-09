"""启动脚本"""

import os

# 清除代理环境变量，避免 httpx/requests 走不可用的 SOCKS 代理
for key in ["all_proxy", "ALL_PROXY", "http_proxy", "HTTP_PROXY", "https_proxy", "HTTPS_PROXY"]:
    os.environ.pop(key, None)

import uvicorn
from app.config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    
    uvicorn.run(
        "app.api.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
        log_level=settings.log_level.lower()
    )

