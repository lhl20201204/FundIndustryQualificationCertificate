#!/bin/bash
# Android APK 打包脚本

set -e

echo "=========================================="
echo "基金从业资格证答题 - Android 打包脚本"
echo "=========================================="

# 检查是否安装了 buildozer
BUILDOZER_CMD=""
if command -v buildozer &> /dev/null; then
    BUILDOZER_CMD="buildozer"
elif python3 -m buildozer --version &> /dev/null; then
    BUILDOZER_CMD="python3 -m buildozer"
elif [ -f "$HOME/Library/Python/3.9/bin/buildozer" ]; then
    BUILDOZER_CMD="$HOME/Library/Python/3.9/bin/buildozer"
fi

if [ -z "$BUILDOZER_CMD" ]; then
    echo "错误: 未找到 buildozer"
    echo "请先安装: pip3 install buildozer"
    echo "或者: python3 -m pip install buildozer"
    exit 1
fi

# 检查是否使用 Docker
USE_DOCKER=false
if [ "$1" == "--docker" ]; then
    USE_DOCKER=true
    echo "使用 Docker 模式"
fi

# 检查是否存在 questions.json
if [ ! -f "questions.json" ]; then
    echo "警告: 未找到 questions.json 文件"
    echo "请确保题目数据文件存在"
fi

# 检查是否存在 main_android.py
if [ ! -f "main_android.py" ]; then
    echo "错误: 未找到 main_android.py"
    exit 1
fi

echo ""
echo "开始构建 Android APK..."
echo ""

if [ "$USE_DOCKER" = true ]; then
    # 使用 Docker
    echo "使用 Docker 构建..."
    docker run --interactive --tty --rm \
        --volume "$(pwd)":/home/user/hostcwd \
        --volume "$(pwd)/.buildozer":/home/user/.buildozer \
        kivy/buildozer android debug
else
    # 直接使用 buildozer
    echo "直接使用 buildozer 构建..."
    $BUILDOZER_CMD android debug
fi

echo ""
echo "=========================================="
if [ -f "bin/*.apk" ]; then
    echo "构建成功！APK 文件位于 bin/ 目录"
    ls -lh bin/*.apk
else
    echo "构建完成，请检查 bin/ 目录中的 APK 文件"
fi
echo "=========================================="

