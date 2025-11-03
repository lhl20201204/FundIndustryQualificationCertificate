#!/bin/bash
# Docker 环境检查脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Docker 环境检查${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查 Docker 是否安装
echo "1. 检查 Docker 是否安装..."
if command -v docker &> /dev/null; then
    DOCKER_VERSION=$(docker --version 2>/dev/null)
    echo -e "${GREEN}✓ Docker 已安装: $DOCKER_VERSION${NC}"
else
    echo -e "${RED}✗ Docker 未安装${NC}"
    echo ""
    echo "请安装 Docker Desktop for Mac:"
    echo "  方法1: brew install --cask docker"
    echo "  方法2: 访问 https://www.docker.com/products/docker-desktop 下载"
    exit 1
fi

# 检查 Docker 是否运行
echo ""
echo "2. 检查 Docker 是否运行..."
if docker info &> /dev/null; then
    echo -e "${GREEN}✓ Docker 正在运行${NC}"
else
    echo -e "${YELLOW}✗ Docker 未运行${NC}"
    echo ""
    echo "请启动 Docker Desktop:"
    echo "  open -a Docker"
    echo ""
    echo "或者:"
    echo "  在应用程序中打开 Docker Desktop"
    exit 1
fi

# 检查 Kivy 镜像
echo ""
echo "3. 检查 Kivy 构建镜像..."
if docker images | grep -q "kivy/buildozer"; then
    echo -e "${GREEN}✓ Kivy 构建镜像已存在${NC}"
    docker images | grep "kivy/buildozer"
else
    echo -e "${YELLOW}⚠ Kivy 构建镜像未找到${NC}"
    echo ""
    read -p "是否现在拉取镜像？(Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        echo "正在拉取镜像（这可能需要几分钟）..."
        docker pull kivy/buildozer
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ 镜像拉取成功${NC}"
        else
            echo -e "${RED}✗ 镜像拉取失败${NC}"
            exit 1
        fi
    fi
fi

# 测试运行
echo ""
echo "4. 测试 Docker 环境..."
if docker run --rm kivy/buildozer --version &> /dev/null; then
    echo -e "${GREEN}✓ Docker 环境测试通过${NC}"
    docker run --rm kivy/buildozer --version
else
    echo -e "${YELLOW}⚠ 环境测试失败，但可能不影响使用${NC}"
fi

echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}✓ Docker 环境检查完成${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "现在可以使用以下命令打包 APK："
echo "  ./build_apk.sh --docker --debug"

