#!/bin/bash
# 查找 Docker Desktop 位置

echo "正在查找 Docker Desktop..."
echo ""

DOCKER_PATH="/Applications/Docker.app"

if [ -d "$DOCKER_PATH" ]; then
    echo "✓ 找到 Docker Desktop:"
    echo "  位置: $DOCKER_PATH"
    echo ""
    
    # 获取应用信息
    if [ -f "$DOCKER_PATH/Contents/Info.plist" ]; then
        APP_NAME=$(defaults read "$DOCKER_PATH/Contents/Info.plist" CFBundleName 2>/dev/null || echo "Docker Desktop")
        VERSION=$(defaults read "$DOCKER_PATH/Contents/Info.plist" CFBundleShortVersionString 2>/dev/null || echo "未知")
        echo "  名称: $APP_NAME"
        echo "  版本: $VERSION"
    fi
    
    echo ""
    echo "在 Finder 中打开:"
    echo "  方法1: 运行: open /Applications"
    echo "  方法2: 运行: open /Applications/Docker.app"
    echo ""
    echo "或者直接在终端启动:"
    echo "  open /Applications/Docker.app"
else
    echo "✗ 未找到 Docker Desktop 在标准位置"
    echo ""
    echo "正在搜索其他位置..."
    
    # 搜索其他可能的位置
    OTHER_LOCATIONS=(
        "$HOME/Applications/Docker.app"
        "/usr/local/Applications/Docker.app"
        "/opt/homebrew-cask/Caskroom/docker"
    )
    
    for loc in "${OTHER_LOCATIONS[@]}"; do
        if [ -d "$loc" ]; then
            echo "  找到: $loc"
        fi
    done
    
    echo ""
    echo "如果确实找不到，请重新安装 Docker Desktop"
fi

