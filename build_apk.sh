#!/bin/bash
# Android APK 一键打包脚本
# 支持 Docker 模式和本地模式

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 脚本目录
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}基金从业资格证答题 - Android APK 打包工具${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查必要文件
check_files() {
    local missing_files=()
    
    if [ ! -f "main_android.py" ]; then
        missing_files+=("main_android.py")
    fi
    
    if [ ! -f "questions.json" ]; then
        echo -e "${YELLOW}警告: 未找到 questions.json 文件${NC}"
        echo -e "${YELLOW}程序可能无法正常工作${NC}"
    fi
    
    if [ ! -f "buildozer.spec" ]; then
        echo -e "${RED}错误: 未找到 buildozer.spec 文件${NC}"
        exit 1
    fi
    
    if [ ${#missing_files[@]} -gt 0 ]; then
        echo -e "${RED}错误: 缺少必要文件: ${missing_files[*]}${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ 文件检查通过${NC}"
}

# 检查 Docker 是否可用
check_docker() {
    # 方法1: 检查 docker 命令
    if command -v docker &> /dev/null; then
        if docker info &> /dev/null; then
            return 0
        fi
    fi
    
    # 方法2: 检查 Docker Desktop 是否安装
    if [ -d "/Applications/Docker.app" ]; then
        # Docker Desktop 已安装，但可能未启动
        if pgrep -f "Docker Desktop" &> /dev/null; then
            # Docker Desktop 正在运行，但命令行工具可能还没就绪
            # 尝试直接使用完整路径
            if [ -f "/usr/local/bin/docker" ]; then
                if /usr/local/bin/docker info &> /dev/null; then
                    return 0
                fi
            fi
            # 如果正在运行但命令不可用，可能是刚启动，返回特殊状态
            return 2
        else
            # Docker Desktop 未运行
            return 3
        fi
    fi
    
    return 1
}

# 检查 buildozer 是否已安装
check_buildozer() {
    # 方法1: 直接命令
    if command -v buildozer &> /dev/null; then
        BUILDOZER_CMD="buildozer"
        return 0
    fi
    # 方法2: 使用 python3 -m buildozer
    if python3 -m buildozer --version &> /dev/null; then
        BUILDOZER_CMD="python3 -m buildozer"
        return 0
    fi
    # 方法3: 检查是否在用户目录
    if [ -f "$HOME/Library/Python/3.9/bin/buildozer" ]; then
        BUILDOZER_CMD="$HOME/Library/Python/3.9/bin/buildozer"
        return 0
    fi
    return 1
}

# 显示使用说明
show_usage() {
    echo "使用方法:"
    echo "  ./build_apk.sh [选项]"
    echo ""
    echo "选项:"
    echo "  --docker        使用 Docker 模式打包（推荐，适合 macOS）"
    echo "  --local         使用本地 buildozer 打包（需要 Linux 环境）"
    echo "  --debug         打包 Debug 版本（默认）"
    echo "  --release       打包 Release 版本"
    echo "  --help          显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  ./build_apk.sh --docker --debug    # 使用 Docker 打包 Debug 版本"
    echo "  ./build_apk.sh --docker --release  # 使用 Docker 打包 Release 版本"
    echo "  ./build_apk.sh --local --debug     # 本地打包 Debug 版本"
}

# 解析参数
BUILD_MODE="docker"
BUILD_TYPE="debug"

while [[ $# -gt 0 ]]; do
    case $1 in
        --docker)
            BUILD_MODE="docker"
            shift
            ;;
        --local)
            BUILD_MODE="local"
            shift
            ;;
        --debug)
            BUILD_TYPE="debug"
            shift
            ;;
        --release)
            BUILD_TYPE="release"
            shift
            ;;
        --help)
            show_usage
            exit 0
            ;;
        *)
            echo -e "${RED}未知参数: $1${NC}"
            show_usage
            exit 1
            ;;
    esac
done

# 检查文件
check_files

# 初始化 BUILDOZER_CMD 变量
BUILDOZER_CMD="buildozer"

# 根据模式执行打包
if [ "$BUILD_MODE" = "docker" ]; then
    echo ""
    echo -e "${BLUE}使用 Docker 模式打包...${NC}"
    
    DOCKER_STATUS=$(check_docker; echo $?)
    
    if [ $DOCKER_STATUS -eq 1 ]; then
        # Docker 未安装
        echo -e "${RED}错误: Docker 未安装${NC}"
        echo ""
        echo "请安装 Docker Desktop for Mac:"
        echo ""
        echo "方法1: 使用安装脚本（推荐）"
        echo "  ./install_docker.sh"
        echo ""
        echo "方法2: 使用 Homebrew"
        echo "  brew install --cask docker"
        echo ""
        echo "方法3: 手动下载安装"
        echo "  https://www.docker.com/products/docker-desktop"
        exit 1
    elif [ $DOCKER_STATUS -eq 3 ]; then
        # Docker Desktop 已安装但未运行
        echo -e "${YELLOW}检测到 Docker Desktop 已安装，但未运行${NC}"
        echo ""
        echo "正在启动 Docker Desktop..."
        open "/Applications/Docker.app" 2>/dev/null || open -a Docker 2>/dev/null
        
        echo ""
        echo -e "${BLUE}请等待 Docker Desktop 启动完成...${NC}"
        echo "Docker Desktop 启动通常需要 30-60 秒"
        echo ""
        echo "等待 Docker 启动..."
        
        # 等待 Docker 启动（最多等待 60 秒）
        for i in {1..60}; do
            sleep 1
            if docker info &> /dev/null; then
                echo -e "${GREEN}✓ Docker 已启动${NC}"
                break
            fi
            if [ $((i % 10)) -eq 0 ]; then
                echo "  已等待 ${i} 秒..."
            fi
        done
        
        # 再次检查
        if ! docker info &> /dev/null; then
            echo -e "${RED}Docker 启动超时${NC}"
            echo ""
            echo "请手动："
            echo "1. 打开 Docker Desktop 应用"
            echo "2. 等待菜单栏显示 Docker 图标（鲸鱼图标）"
            echo "3. 运行检查: ./check_docker.sh"
            echo "4. 然后重新运行打包命令"
            exit 1
        fi
    elif [ $DOCKER_STATUS -eq 2 ]; then
        # Docker Desktop 正在运行但命令还不可用
        echo -e "${YELLOW}Docker Desktop 正在启动中，请稍候...${NC}"
        sleep 5
        if ! docker info &> /dev/null; then
            echo -e "${RED}Docker 命令不可用${NC}"
            echo ""
            echo "请尝试："
            echo "1. 重启终端"
            echo "2. 或运行: source ~/.zshrc"
            echo "3. 然后重新运行打包命令"
            exit 1
        fi
    fi
    
    echo -e "${GREEN}✓ Docker 可用${NC}"
    
    # 检查 Kivy Docker 镜像
    echo ""
    echo "检查 Kivy Docker 镜像..."
    if ! docker images | grep -q "kivy/buildozer"; then
        echo -e "${YELLOW}正在拉取 Kivy Docker 镜像（首次运行需要较长时间）...${NC}"
        docker pull kivy/buildozer || {
            echo -e "${RED}错误: 无法拉取 Docker 镜像${NC}"
            exit 1
        }
    fi
    
    echo -e "${GREEN}✓ Docker 镜像就绪${NC}"
    
    # 执行打包
    echo ""
    echo -e "${BLUE}开始打包 ${BUILD_TYPE^^} 版本...${NC}"
    echo "这可能需要较长时间，请耐心等待..."
    echo ""
    
    docker run --interactive --tty --rm \
        --volume "$SCRIPT_DIR":/home/user/hostcwd \
        --volume "$SCRIPT_DIR/.buildozer":/home/user/.buildozer \
        kivy/buildozer android $BUILD_TYPE
    
    BUILD_SUCCESS=$?
    
elif [ "$BUILD_MODE" = "local" ]; then
    echo ""
    echo -e "${BLUE}使用本地模式打包...${NC}"
    
    if ! check_buildozer; then
        echo -e "${RED}错误: buildozer 未安装${NC}"
        echo ""
        echo "请先安装 buildozer:"
        echo "  pip3 install buildozer"
        echo "  或者: python3 -m pip install buildozer"
        echo ""
        echo "如果已安装但仍找不到，可以尝试:"
        echo "  export PATH=\"\$HOME/Library/Python/3.9/bin:\$PATH\""
        echo ""
        echo "注意: 本地打包需要 Linux 环境，macOS 用户建议使用 --docker 模式"
        exit 1
    fi
    
    echo -e "${GREEN}✓ buildozer 已安装 (使用: $BUILDOZER_CMD)${NC}"
    
    # 检查是否为 Linux
    if [[ "$OSTYPE" != "linux-gnu"* ]]; then
        echo -e "${YELLOW}警告: 本地打包通常在 Linux 环境下运行${NC}"
        echo -e "${YELLOW}macOS 用户强烈建议使用 --docker 模式${NC}"
        echo ""
        echo "本地打包在 macOS 上需要安装大量依赖，包括："
        echo "  - Cython"
        echo "  - Android SDK 和 NDK"
        echo "  - Java JDK"
        echo "  - 其他构建工具"
        echo ""
        read -p "是否继续？(y/N) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${BLUE}建议使用 Docker 模式: ./build_apk.sh --docker --debug${NC}"
            exit 1
        fi
        
        # 检查常见依赖
        echo ""
        echo "检查构建依赖..."
        MISSING_DEPS=()
        
        if ! python3 -c "import Cython" 2>/dev/null; then
            MISSING_DEPS+=("Cython")
        fi
        
        if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
            echo -e "${YELLOW}缺少依赖: ${MISSING_DEPS[*]}${NC}"
            echo ""
            read -p "是否自动安装这些依赖？(Y/n) " -n 1 -r
            echo
            if [[ ! $REPLY =~ ^[Nn]$ ]]; then
                echo "正在安装依赖..."
                python3 -m pip install --user "${MISSING_DEPS[@]}" || {
                    echo -e "${RED}安装失败，请手动安装:${NC}"
                    echo "  python3 -m pip install --user ${MISSING_DEPS[*]}"
                    exit 1
                }
                echo -e "${GREEN}✓ 依赖安装完成${NC}"
            else
                echo -e "${YELLOW}请手动安装依赖后重试${NC}"
                exit 1
            fi
        else
            echo -e "${GREEN}✓ 基本依赖检查通过${NC}"
        fi
    fi
    
    # 执行打包
    echo ""
    echo -e "${BLUE}开始打包 ${BUILD_TYPE^^} 版本...${NC}"
    echo "这可能需要较长时间，请耐心等待..."
    echo ""
    
    # 使用检测到的命令执行打包
    $BUILDOZER_CMD android $BUILD_TYPE
    BUILD_SUCCESS=$?
else
    echo -e "${RED}错误: 未知的打包模式: $BUILD_MODE${NC}"
    exit 1
fi

# 检查打包结果
echo ""
echo -e "${BLUE}========================================${NC}"
if [ $BUILD_SUCCESS -eq 0 ]; then
    echo -e "${GREEN}✓ 打包成功！${NC}"
    echo ""
    
    # 查找生成的 APK 文件
    if [ -d "bin" ]; then
        APK_FILES=$(find bin -name "*.apk" -type f 2>/dev/null)
        if [ -n "$APK_FILES" ]; then
            echo -e "${GREEN}生成的 APK 文件:${NC}"
            echo "$APK_FILES" | while read -r apk; do
                SIZE=$(du -h "$apk" | cut -f1)
                echo -e "  ${BLUE}$apk${NC} (${SIZE})"
            done
            echo ""
            echo -e "${YELLOW}安装到设备:${NC}"
            echo "  adb install $(echo "$APK_FILES" | head -n1)"
        else
            echo -e "${YELLOW}未找到 APK 文件，请检查 bin/ 目录${NC}"
        fi
    else
        echo -e "${YELLOW}未找到 bin/ 目录${NC}"
    fi
else
    echo -e "${RED}✗ 打包失败${NC}"
    echo ""
    echo "请检查错误信息，常见问题："
    echo "  1. 网络连接问题"
    echo "  2. 磁盘空间不足"
    echo "  3. 依赖下载失败"
    echo ""
    echo "详细文档请参考: ANDROID_BUILD.md"
    exit 1
fi
echo -e "${BLUE}========================================${NC}"

