#!/bin/bash
# 启动 Docker Desktop 脚本

echo "检查 Docker Desktop 状态..."

# 检查是否已安装
if [ ! -d "/Applications/Docker.app" ]; then
    echo "错误: 未找到 Docker Desktop"
    echo "请先安装 Docker Desktop"
    echo "运行: ./install_docker.sh"
    exit 1
fi

# 检查是否已在运行
if pgrep -f "Docker Desktop" &> /dev/null; then
    echo "Docker Desktop 已在运行"
    
    # 检查 docker 命令是否可用
    if command -v docker &> /dev/null; then
        if docker info &> /dev/null; then
            echo "✓ Docker 已就绪"
            docker --version
            exit 0
        fi
    fi
    
    echo "Docker Desktop 正在运行，但命令行工具可能还未就绪"
    echo "请稍候几秒后重试"
    exit 0
fi

# 启动 Docker Desktop
echo "正在启动 Docker Desktop..."
open "/Applications/Docker.app" 2>/dev/null || open -a Docker 2>/dev/null || {
    echo "无法自动启动，请手动打开 Docker Desktop："
    echo "1. 打开 Finder"
    echo "2. 进入 Applications 文件夹"
    echo "3. 双击 Docker 图标"
    exit 1
}

echo ""
echo "Docker Desktop 正在启动，请等待..."
echo "首次启动可能需要 30-60 秒"
echo ""

# 等待启动
for i in {1..60}; do
    sleep 1
    
    # 检查进程
    if ! pgrep -f "Docker Desktop" &> /dev/null; then
        continue
    fi
    
    # 检查命令是否可用
    if command -v docker &> /dev/null; then
        if docker info &> /dev/null; then
            echo ""
            echo "✓ Docker Desktop 已启动并就绪"
            docker --version
            exit 0
        fi
    fi
    
    if [ $((i % 10)) -eq 0 ]; then
        echo "  已等待 ${i} 秒..."
    fi
done

echo ""
echo "等待超时，但 Docker Desktop 可能仍在启动中"
echo ""
echo "请检查："
echo "1. 菜单栏是否有 Docker 图标（鲸鱼图标）"
echo "2. 如果图标显示 'Docker Desktop is starting...'，请继续等待"
echo "3. 如果图标显示为正常运行状态，运行: ./check_docker.sh"

