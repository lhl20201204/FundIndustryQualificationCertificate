# Android APK 打包替代方案

由于无法使用 Docker，以下是其他可行的打包方法：

## 方案一：GitHub Actions（推荐）⭐

使用 GitHub Actions 在云端自动构建，无需本地环境配置。

### 优点
- ✅ 完全免费（公开仓库）
- ✅ 无需本地安装任何工具
- ✅ 自动化构建流程
- ✅ 支持多架构构建

### 使用步骤

1. **创建 GitHub 仓库**（如果还没有）
   ```bash
   # 安装 GitHub CLI（可选）
   brew install gh
   
   # 创建仓库并推送代码
   gh repo create --public --source=. --remote=origin --push
   ```

2. **配置 GitHub Actions**
   ```bash
   # 工作流文件已创建在 .github/workflows/build-android.yml
   git add .github/workflows/build-android.yml
   git commit -m "Add GitHub Actions workflow"
   git push
   ```

3. **触发构建**
   - 推送到 GitHub 后自动触发
   - 或访问仓库的 Actions 页面手动触发

4. **下载 APK**
   - 构建完成后，在 Actions 页面下载 Artifacts

### 使用辅助脚本

```bash
./build_with_github.sh
```

## 方案二：使用 Linux 虚拟机

在 macOS 上运行 Linux 虚拟机进行构建。

### 虚拟机选项

1. **Parallels Desktop**（付费，性能好）
2. **VMware Fusion**（付费）
3. **UTM**（免费，开源）：https://mac.getutm.app/
4. **VirtualBox**（免费）

### 步骤

1. 安装虚拟机软件
2. 安装 Ubuntu Linux（推荐 22.04 LTS）
3. 在虚拟机中安装依赖：
   ```bash
   sudo apt-get update
   sudo apt-get install -y git zip unzip openjdk-11-jdk python3-pip
   pip3 install buildozer
   ```
4. 复制项目到虚拟机
5. 运行 `buildozer android debug`

## 方案三：使用云服务器

租用 Linux 云服务器进行构建。

### 云服务商

1. **阿里云** / **腾讯云**（国内，速度快）
2. **AWS EC2**（按需付费）
3. **DigitalOcean**（简单易用）
4. **Vultr**（性价比高）

### 步骤

1. 租用 Ubuntu 服务器（最低配置即可）
2. SSH 连接到服务器
3. 安装依赖并构建（同方案二）

## 方案四：使用在线构建服务

### Kivy Build Service

某些在线服务提供 Kivy 应用的云端构建（需要搜索最新可用服务）。

## 方案五：本地 macOS 构建（复杂，不推荐）

虽然理论上可以在 macOS 上本地构建，但需要：
- Android SDK
- Android NDK
- Java JDK
- 大量配置

**不推荐此方案**，因为配置复杂且容易出错。

## 推荐方案对比

| 方案 | 难度 | 成本 | 时间 | 推荐度 |
|------|------|------|------|--------|
| GitHub Actions | ⭐ 简单 | 免费 | 5-10分钟 | ⭐⭐⭐⭐⭐ |
| Linux 虚拟机 | ⭐⭐ 中等 | 免费/付费 | 30分钟+ | ⭐⭐⭐ |
| 云服务器 | ⭐⭐ 中等 | 按需付费 | 20分钟+ | ⭐⭐⭐⭐ |
| 本地 macOS | ⭐⭐⭐⭐⭐ 困难 | 免费 | 2小时+ | ⭐ |

## 快速开始（GitHub Actions）

```bash
# 1. 初始化 Git（如果还没有）
git init
git add .
git commit -m "Initial commit"

# 2. 创建 GitHub 仓库并推送
gh repo create --public --source=. --remote=origin --push

# 或者手动：
# - 在 GitHub 上创建新仓库
# - git remote add origin <your-repo-url>
# - git push -u origin main

# 3. 等待构建完成，在 Actions 页面下载 APK
```

## 常见问题

### GitHub Actions 构建失败

- 检查 `.github/workflows/build-android.yml` 是否正确
- 查看 Actions 日志找出错误原因
- 确保 `buildozer.spec` 配置正确

### 虚拟机性能慢

- 增加虚拟机分配的内存（至少 4GB）
- 使用 SSD 存储
- 关闭不必要的虚拟机功能

### 需要帮助？

- GitHub Actions：查看 GitHub 官方文档
- 虚拟机：查看对应虚拟机软件的文档
- 其他问题：查看 `BUILD_TROUBLESHOOTING.md`

