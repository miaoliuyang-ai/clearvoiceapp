#!/bin/bash

# ClearVoice API 服务启动脚本
# 使用方法: ./start.sh [端口号] [主机地址] [模式]
# 默认端口: 8000
# 默认主机: 0.0.0.0
# 默认模式: 生产模式（禁用自动重载）
# 开发模式: ./start.sh [端口] [主机] dev

export ASCEND_RT_VISIBLE_DEVICES=7

source /usr/local/Ascend/ascend-toolkit/set_env.sh

set -e  # 遇到错误立即退出

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 默认配置
DEFAULT_PORT=8000
DEFAULT_HOST="0.0.0.0"

# 获取参数
PORT=${1:-$DEFAULT_PORT}
HOST=${2:-$DEFAULT_HOST}

echo -e "${BLUE}🚀 ClearVoice API 服务启动脚本${NC}"
echo -e "${BLUE}======================================${NC}"

# 检查Python是否安装
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ 错误: Python3 未安装${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Python3 已安装: $(python3 --version)${NC}"

echo -e "${GREEN}✅ 在项目根目录${NC}"

# 检查是否存在run.py文件
if [ -f "run.py" ]; then
    START_SCRIPT="run.py"
    echo -e "${GREEN}✅ 使用 run.py 启动脚本${NC}"
else
    START_SCRIPT="main.py"
    echo -e "${GREEN}✅ 使用 main.py 启动脚本${NC}"
fi

# 显示服务信息
echo -e "${BLUE}🌐 服务配置:${NC}"
echo -e "   主机地址: ${HOST}"
echo -e "   端口号: ${PORT}"
echo -e ""
echo -e "${BLUE}📋 服务端点:${NC}"
echo -e "   健康检查: http://${HOST}:${PORT}/health"
echo -e "   API文档: http://${HOST}:${PORT}/docs"
echo -e "   音频降噪: POST http://${HOST}:${PORT}/v1/audio/clearvoice"
echo -e ""
echo -e "${YELLOW}🔄 正在启动服务...${NC}"
echo -e "${BLUE}======================================${NC}"

# 检查是否需要开发模式
if [ "$3" = "dev" ] || [ "$DEV_MODE" = "1" ]; then
    echo -e "${YELLOW}🔄 开发模式启动（启用自动重载）${NC}"
    # 临时启用重载模式
    python3 -c "
import uvicorn
from app.main import app
uvicorn.run(
    'app.main:app',
    host='${HOST}',
    port=${PORT},
    reload=True,
    log_level='info',
    access_log=True
)
"
else
    echo -e "${YELLOW}🏭 生产模式启动（禁用自动重载）${NC}"
    # 启动服务
    python3 ${START_SCRIPT}
fi

