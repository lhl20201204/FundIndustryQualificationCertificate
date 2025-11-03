#!/bin/bash
# Docker 安装辅助脚本

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}Docker Desktop 安装助手${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查系统版本
echo "检查系统版本..."
MACOS_VERSION=$(sw_vers -productVersion)
MACOS_MAJOR=$(echo $MACOS_VERSION | cut -d. -f1)
MACOS_MINOR=$(echo $MACOS_VERSION | cut -d. -f2)

echo "macOS 版本: $MACOS_VERSION"

# Docker Desktop 要求 macOS 11 或更高
if [ "$MACOS_MAJOR" -lt 11 ]; then
    echo -e "${YELLOW}警告: 您的 macOS 版本较旧，可能不支持 Docker Desktop${NC}"
    echo ""
    echo "可选方案："
    echo "1. 升级 macOS 到 11 (Big Sur) 或更高版本"
    echo "2. 使用 Linux 虚拟机或云服务器打包"
    echo "3. 使用 GitHub Actions 自动构建"
    exit 1
fi

# macOS 13 用户提示
if [ "$MACOS_MAJOR" -eq 13 ]; then
    echo -e "${YELLOW}提示: 您使用的是 macOS 13 (Ventura)${NC}"
    echo -e "${YELLOW}Homebrew 的最新版本可能要求 macOS 14+，建议手动下载安装${NC}"
fi

# 检查是否已安装 Docker
if command -v docker &> /dev/null; then
    echo -e "${GREEN}✓ Docker 已安装: $(docker --version)${NC}"
    exit 0
fi

# 检查 Homebrew（macOS 14+ 可以使用）
if command -v brew &> /dev/null && [ "$MACOS_MAJOR" -ge 14 ]; then
    echo -e "${GREEN}✓ 检测到 Homebrew${NC}"
    echo ""
    read -p "是否使用 Homebrew 安装 Docker Desktop？(Y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        echo ""
        echo "正在安装 Docker Desktop..."
        brew install --cask docker
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}✓ Docker Desktop 安装成功${NC}"
            echo ""
            echo "下一步："
            echo "1. 启动 Docker Desktop:"
            echo "   open -a Docker"
            echo ""
            echo "2. 等待 Docker 启动完成（首次启动需要一些时间）"
            echo ""
            echo "3. 运行检查脚本："
            echo "   ./check_docker.sh"
            exit 0
        else
            echo -e "${YELLOW}Homebrew 安装失败，请使用手动安装方式${NC}"
        fi
    fi
fi

# 手动安装提示
echo ""
echo "=========================================="
echo "手动安装 Docker Desktop（推荐方式）"
echo "=========================================="
echo ""
echo "1. 访问 Docker 官网下载页面："
echo "   https://www.docker.com/products/docker-desktop"
echo ""
echo "2. 或者直接下载适合您系统的版本："
ARCH=$(uname -m)
if [ "$ARCH" = "arm64" ]; then
    echo "   - 检测到 Apple Silicon 芯片"
    echo "   - 下载地址: https://desktop.docker.com/mac/main/arm64/Docker.dmg"
else
    echo "   - 检测到 Intel 芯片"
    echo "   - 下载地址: https://desktop.docker.com/mac/main/amd64/Docker.dmg"
fi
echo ""
echo "3. 安装步骤："
echo "   a) 下载 .dmg 文件后双击打开"
echo "   b) 将 Docker 图标拖拽到 Applications 文件夹"
echo "   c) 打开 Applications 文件夹，双击 Docker 启动"
echo "   d) 首次启动需要授权，按照提示操作"
echo ""
echo "4. 验证安装："
echo "   打开终端运行: docker --version"
echo ""
echo "5. 安装完成后运行检查脚本："
echo "   ./check_docker.sh"
echo ""
echo "6. 然后就可以开始打包了："
echo "   ./build_apk.sh --docker --debug"

