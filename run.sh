#!/bin/bash
# 启动程序的便捷脚本

cd "$(dirname "$0")"

# 检查虚拟环境是否存在
if [ ! -d ".venv" ]; then
    echo "错误：虚拟环境不存在，请先运行安装脚本："
    echo "./install.sh"
    exit 1
fi

# 激活虚拟环境
source .venv/bin/activate

# 运行程序
python3 main.py

