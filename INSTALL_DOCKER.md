# Docker 安装指南（macOS）

## 方法一：使用 Homebrew 安装（推荐）

### 1. 安装 Homebrew（如果还没有）

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### 2. 使用 Homebrew 安装 Docker

```bash
brew install --cask docker
```

### 3. 启动 Docker Desktop

```bash
# 打开 Docker Desktop
open /Applications/Docker.app

# 或者使用命令启动
open -a Docker
```

### 4. 等待 Docker 启动完成

首次启动需要一些时间，等待 Docker Desktop 图标在菜单栏显示为运行状态。

### 5. 验证安装

```bash
docker --version
docker info
```

## 方法二：直接下载安装包

### 1. 下载 Docker Desktop

访问官网下载：https://www.docker.com/products/docker-desktop

选择 **Mac with Apple Silicon**（M1/M2/M3 芯片）或 **Mac with Intel Chip**

### 2. 安装 Docker Desktop

1. 下载后双击 `.dmg` 文件
2. 将 Docker 拖拽到 Applications 文件夹
3. 打开 Applications，双击 Docker 启动
4. 按照提示完成初始设置

### 3. 验证安装

```bash
docker --version
```

## 安装后首次使用

### 1. 拉取 Kivy 构建镜像

```bash
docker pull kivy/buildozer
```

这可能需要一些时间，因为镜像较大（约 2-3GB）。

### 2. 测试 Docker 环境

```bash
docker run --rm kivy/buildozer --version
```

### 3. 开始打包

```bash
./build_apk.sh --docker --debug
```

## 常见问题

### Docker Desktop 启动失败

**问题**：Docker Desktop 无法启动

**解决**：
1. 检查系统要求：macOS 10.15 或更高版本
2. 确保有足够的内存（至少 4GB 可用）
3. 重启计算机后重试
4. 查看 Docker Desktop 的日志文件

### 镜像拉取慢

**问题**：拉取 Docker 镜像速度很慢

**解决**：
1. 使用国内镜像源（配置 Docker Desktop）
2. 使用 VPN（如果需要）
3. 在 Docker Desktop 设置中配置镜像加速器

### 权限问题

**问题**：Docker 命令需要 sudo

**解决**：
- Docker Desktop 安装后通常不需要 sudo
- 确保您的用户在 docker 组中（通常自动配置）

### 磁盘空间不足

**问题**：Docker 需要大量磁盘空间

**解决**：
- Docker 镜像和容器会占用磁盘空间
- 定期清理未使用的镜像：
  ```bash
  docker system prune -a
  ```

## 验证安装脚本

运行以下命令验证 Docker 是否正常工作：

```bash
# 检查 Docker 版本
docker --version

# 检查 Docker 是否运行
docker info

# 测试运行一个容器
docker run hello-world
```

如果所有命令都成功执行，说明 Docker 已正确安装并运行。

