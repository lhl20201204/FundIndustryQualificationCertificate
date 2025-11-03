# Docker 快速安装指南

## 您的系统信息
- macOS 版本: 13.0 (Ventura)
- 需要手动下载安装 Docker Desktop

## 快速安装步骤

### 1. 检测您的芯片类型

在终端运行：
```bash
uname -m
```

- 如果显示 `arm64`：您是 Apple Silicon (M1/M2/M3) 芯片
- 如果显示 `x86_64`：您是 Intel 芯片

### 2. 下载 Docker Desktop

根据您的芯片类型下载：

**Apple Silicon (M1/M2/M3):**
```
https://desktop.docker.com/mac/main/arm64/Docker.dmg
```

**Intel 芯片:**
```
https://desktop.docker.com/mac/main/amd64/Docker.dmg
```

或者访问官网：https://www.docker.com/products/docker-desktop

### 3. 安装 Docker Desktop

1. 下载完成后，双击 `.dmg` 文件
2. 将 Docker 图标拖拽到 Applications 文件夹
3. 打开 Applications 文件夹，找到 Docker，双击启动
4. 首次启动需要授权，点击"打开"
5. 等待 Docker Desktop 启动完成（可能需要几分钟）

### 4. 验证安装

打开终端运行：
```bash
docker --version
```

应该显示 Docker 版本号。

### 5. 运行检查脚本

```bash
./check_docker.sh
```

这个脚本会：
- 检查 Docker 是否安装
- 检查 Docker 是否运行
- 自动拉取 Kivy 构建镜像（如果需要）
- 测试 Docker 环境

### 6. 开始打包

```bash
./build_apk.sh --docker --debug
```

## 常见问题

### Docker Desktop 启动失败

- 确保有足够的内存（至少 4GB 可用）
- 重启计算机后重试
- 检查系统偏好设置中的安全和隐私设置

### 镜像拉取慢

首次拉取 Kivy 镜像可能需要一些时间（约 2-3GB），请耐心等待。

### 需要帮助？

运行检查脚本查看详细状态：
```bash
./check_docker.sh
```

