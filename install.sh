#!/bin/bash
# 安装依赖脚本，使用国内镜像源

cd "$(dirname "$0")"

# 激活虚拟环境
source .venv/bin/activate

# 使用清华镜像源安装 PyQt6
echo "正在使用清华镜像源安装 PyQt6..."
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple PyQt6

echo "安装完成！"
echo "运行程序：python main.py"

