# 快速开始指南

## macOS 本地测试

在 macOS 上测试 Android 版本的应用：

```bash
# 一键测试（自动检查依赖并安装）
./test_macos.sh

# 或直接运行测试脚本
python3 test_android.py
```

### 首次运行

首次运行会自动检查并安装依赖（Kivy、Plyer）。

如果遇到权限问题，可以手动安装：

```bash
python3 -m pip install --user kivy plyer
```

## 安装 Docker（首次使用）

如果还没有安装 Docker：

```bash
# 方法1: 使用安装脚本
./install_docker.sh

# 方法2: 使用 Homebrew
brew install --cask docker

# 然后启动 Docker Desktop
open -a Docker

# 验证安装
./check_docker.sh
```

## Android APK 打包

### 方式一：使用 Docker（推荐，适合 macOS）

```bash
# 打包 Debug 版本
./build_apk.sh --docker --debug

# 打包 Release 版本
./build_apk.sh --docker --release
```

### 方式二：本地打包（需要 Linux 环境）

```bash
# 打包 Debug 版本
./build_apk.sh --local --debug

# 打包 Release 版本
./build_apk.sh --local --release
```

### 查看帮助

```bash
./build_apk.sh --help
./test_macos.sh --help
```

## 脚本说明

### test_macos.sh

- ✅ 自动检查 Python 环境
- ✅ 自动检查必要文件
- ✅ 自动检查和安装依赖
- ✅ 启动应用进行测试

**使用场景**: 在 macOS 上测试 Android 版本的应用功能

### build_apk.sh

- ✅ 支持 Docker 模式和本地模式
- ✅ 支持 Debug 和 Release 版本
- ✅ 自动检查 Docker 和依赖
- ✅ 自动拉取 Docker 镜像（首次运行）
- ✅ 显示打包结果和 APK 文件位置

**使用场景**: 打包 Android APK 文件

## 常见问题

### 1. test_macos.sh 提示缺少依赖

**解决方案**:
```bash
python3 -m pip install --user kivy plyer
```

### 2. build_apk.sh Docker 模式失败

**检查项**:
- Docker Desktop 是否已安装并运行
- 是否有足够的磁盘空间（至少 5GB）
- 网络连接是否正常

**解决方案**:
```bash
# 检查 Docker
docker info

# 手动拉取镜像
docker pull kivy/buildozer
```

### 3. 本地打包模式失败

**注意**: 本地打包需要 Linux 环境，macOS 用户请使用 Docker 模式。

如果必须在 macOS 上本地打包（不推荐）:
```bash
# 安装 buildozer
python3 -m pip install buildozer

# 需要安装 Android SDK 和 NDK
# 详情参考 ANDROID_BUILD.md
```

## 工作流程建议

1. **开发阶段**: 使用 `test_macos.sh` 在 macOS 上快速测试
2. **测试通过**: 使用 `build_apk.sh --docker --debug` 打包测试版本
3. **发布版本**: 使用 `build_apk.sh --docker --release` 打包发布版本

## 文件说明

- `main_android.py` - Android 版本主程序
- `test_android.py` - 测试启动脚本
- `test_macos.sh` - macOS 测试脚本（一键测试）
- `build_apk.sh` - Android APK 打包脚本（一键打包）
- `buildozer.spec` - Buildozer 配置文件

## 更多信息

- 详细打包文档: [ANDROID_BUILD.md](./ANDROID_BUILD.md)
- Android 版本说明: [README_ANDROID.md](./README_ANDROID.md)
- macOS 安装说明: [INSTALL_MACOS.md](./INSTALL_MACOS.md)

