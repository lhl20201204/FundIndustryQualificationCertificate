# Android 应用打包指南

本文档说明如何将基金从业资格证答题应用打包成 Android APK。

## 前置要求

### 1. 安装依赖

在 macOS/Linux 上安装 Buildozer 和相关工具：

```bash
# 安装 Buildozer（macOS 上使用 pip3）
pip3 install buildozer
# 或者
python3 -m pip install buildozer

# 安装 Android 构建工具（需要在 Linux 系统上，或使用 Docker）
# macOS 用户建议使用 Docker 方式
```

### 2. 安装 Docker（推荐方式 - macOS）

由于 Buildozer 主要在 Linux 环境下运行，macOS 用户推荐使用 Docker：

```bash
# 安装 Docker Desktop for Mac
# 下载地址: https://www.docker.com/products/docker-desktop

# 拉取 Kivy 官方 Docker 镜像
docker pull kivy/buildozer
```

## 打包步骤

### 方式一：使用 Docker（推荐，适合 macOS）

```bash
# 1. 进入项目目录
cd /Users/sec-test2/Desktop/my-code/FundIndustryQualificationCertificate

# 2. 使用 Docker 运行 Buildozer
docker run --volume "$(pwd)":/home/user/hostcwd kivy/buildozer android debug

# 或构建 release 版本
docker run --volume "$(pwd)":/home/user/hostcwd kivy/buildozer android release
```

### 方式二：直接在 Linux 系统上（或 Linux VM）

```bash
# 1. 确保已安装所有依赖
sudo apt-get update
sudo apt-get install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

# 2. 安装 Buildozer
pip3 install --user buildozer

# 3. 初始化 Buildozer（如果需要）
buildozer init

# 4. 构建 APK
buildozer android debug
# 或构建 release 版本
buildozer android release
```

### 方式三：使用 GitHub Actions（自动化构建）

创建 `.github/workflows/build.yml`:

```yaml
name: Build Android APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      
      - name: Install dependencies
        run: |
          pip install buildozer
          sudo apt-get update
          sudo apt-get install -y git zip unzip openjdk-8-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmache libffi-dev libssl-dev
      
      - name: Build APK
        run: buildozer android release
      
      - name: Upload APK
        uses: actions/upload-artifact@v2
        with:
          name: app-release.apk
          path: bin/*.apk
```

## 配置文件说明

### buildozer.spec 主要配置项

- **package.name**: 应用包名（不能有中文字符）
- **package.domain**: 包域名
- **source.main**: 主程序入口文件
- **requirements**: Python 依赖包
- **android.permissions**: Android 权限
- **android.minapi**: 最低 Android API 版本
- **android.api**: 目标 Android API 版本
- **android.archs**: 支持的 CPU 架构

## 常见问题

### 1. 构建失败：找不到 Android SDK

**解决方案**：
```bash
# 设置 Android SDK 路径（如果已安装 Android Studio）
export ANDROID_HOME=$HOME/Android/Sdk
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/platform-tools
```

### 2. 构建失败：内存不足

**解决方案**：
```bash
# 增加 Swap 空间
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### 3. 权限问题

确保 `questions.json` 文件有读取权限，并且被包含在 APK 中。

### 4. TTS 语音功能

在 Android 上，TTS 通过 `plyer` 库调用系统 TTS 引擎。确保：
- 设备已安装 TTS 引擎（大多数 Android 设备自带）
- 应用有必要的权限

## 测试 APK

### 安装到设备

```bash
# 通过 ADB 安装
adb install bin/fundexam-0.1-arm64-v8a-debug.apk

# 或直接传输 APK 到手机后安装
```

### 运行调试

```bash
# 查看日志
adb logcat | grep python
```

## 发布 APK

### 签名 APK（Release 版本）

Release 版本需要签名：

```bash
# 生成密钥（首次）
keytool -genkey -v -keystore fundexam-release-key.keystore -alias fundexam -keyalg RSA -keysize 2048 -validity 10000

# Buildozer 会自动使用此密钥签名（需要配置 buildozer.spec）
```

### 上传到应用商店

1. **Google Play Store**：
   - 创建开发者账号
   - 准备应用截图、描述等
   - 上传 APK 或 AAB 格式

2. **其他应用市场**：
   - 华为应用市场
   - 小米应用商店
   - 应用宝等

## 性能优化建议

1. **减小 APK 大小**：
   - 只包含必要的架构（如只支持 arm64-v8a）
   - 优化图片资源

2. **提高启动速度**：
   - 使用 Python 3.10+（更好的启动性能）
   - 减少导入的库

3. **内存优化**：
   - 分批加载题目数据
   - 及时释放不需要的资源

## 参考资料

- [Kivy 官方文档](https://kivy.org/doc/stable/)
- [Buildozer 文档](https://buildozer.readthedocs.io/)
- [Plyer 文档](https://plyer.readthedocs.io/)

