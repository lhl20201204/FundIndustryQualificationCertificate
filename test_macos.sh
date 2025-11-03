#!/bin/bash
# macOS 本地测试脚本
# 用于在 macOS 上测试 Android 版本的 Kivy 应用

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
echo -e "${GREEN}基金从业资格证答题 - macOS 测试工具${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""

# 检查 Python3
check_python() {
    if ! command -v python3 &> /dev/null; then
        echo -e "${RED}错误: 未找到 python3${NC}"
        exit 1
    fi
    
    PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
    echo -e "${GREEN}✓ Python 版本: $PYTHON_VERSION${NC}"
}

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
    
    if [ ! -f "test_android.py" ]; then
        echo -e "${YELLOW}警告: 未找到 test_android.py，将直接运行 main_android.py${NC}"
    fi
    
    if [ ${#missing_files[@]} -gt 0 ]; then
        echo -e "${RED}错误: 缺少必要文件: ${missing_files[*]}${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ 文件检查通过${NC}"
}

# 检查并安装依赖
check_dependencies() {
    echo ""
    echo "检查依赖..."
    
    local missing_deps=()
    
    # 检查 kivy
    if ! python3 -c "import kivy" 2>/dev/null; then
        missing_deps+=("kivy")
    else
        KIVY_VERSION=$(python3 -c "import kivy; print(kivy.__version__)" 2>/dev/null)
        echo -e "${GREEN}✓ Kivy $KIVY_VERSION${NC}"
    fi
    
    # 检查 plyer
    if ! python3 -c "import plyer" 2>/dev/null; then
        missing_deps+=("plyer")
    else
        echo -e "${GREEN}✓ Plyer${NC}"
    fi
    
    if [ ${#missing_deps[@]} -gt 0 ]; then
        echo ""
        echo -e "${YELLOW}缺少依赖: ${missing_deps[*]}${NC}"
        echo ""
        read -p "是否自动安装缺失的依赖？(Y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            echo ""
            echo "正在安装依赖..."
            python3 -m pip install --user "${missing_deps[@]}" || {
                echo -e "${RED}安装失败，请手动运行:${NC}"
                echo "  python3 -m pip install --user ${missing_deps[*]}"
                exit 1
            }
            echo -e "${GREEN}✓ 依赖安装完成${NC}"
        else
            echo -e "${RED}请手动安装依赖:${NC}"
            echo "  python3 -m pip install --user ${missing_deps[*]}"
            exit 1
        fi
    fi
}

# 显示使用说明
show_usage() {
    echo "使用方法:"
    echo "  ./test_macos.sh [选项]"
    echo ""
    echo "选项:"
    echo "  --direct        直接运行 main_android.py（不通过 test_android.py）"
    echo "  --help          显示此帮助信息"
    echo ""
    echo "功能说明:"
    echo "  此脚本会在 macOS 上运行 Android 版本的 Kivy 应用进行测试"
    echo "  用于在打包 APK 之前验证应用功能是否正常"
    echo ""
}

# 解析参数
RUN_MODE="test"
while [[ $# -gt 0 ]]; do
    case $1 in
        --direct)
            RUN_MODE="direct"
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

# 执行检查
check_python
check_files
check_dependencies

# 运行应用
echo ""
echo -e "${BLUE}========================================${NC}"
echo -e "${GREEN}启动应用...${NC}"
echo -e "${BLUE}========================================${NC}"
echo ""
echo "提示:"
echo "  - 按 Ctrl+C 退出应用"
echo "  - 应用窗口应该会显示中文界面"
echo "  - 如果出现乱码，请检查字体设置"
echo ""

# 设置环境变量（可选）
export KIVY_WINDOW=sdl2

# 根据模式运行
if [ "$RUN_MODE" = "direct" ]; then
    python3 main_android.py
else
    python3 test_android.py
fi

