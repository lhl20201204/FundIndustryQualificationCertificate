# Android 打包问题排查指南

## 问题：缺少依赖

### 问题描述
```
Cython (cython) not found, please install it.
```

### 解决方案

#### 方案一：安装依赖后继续（不推荐，在 macOS 上复杂）

```bash
# 安装 Cython
python3 -m pip install --user Cython

# 但 macOS 上本地打包还需要：
# - Android SDK
# - Android NDK
# - Java JDK
# - 其他构建工具
```

**注意**：在 macOS 上本地打包 Android APK 非常复杂，需要大量依赖和配置。

#### 方案二：使用 Docker 模式（强烈推荐）

```bash
# 使用 Docker 模式打包，自动处理所有依赖
./build_apk.sh --docker --debug
```

Docker 模式的优势：
- ✅ 无需安装 Android SDK/NDK
- ✅ 无需安装 Java JDK
- ✅ 无需配置环境变量
- ✅ 自动处理所有依赖
- ✅ 构建环境完全隔离

### 安装 Docker

1. 下载 Docker Desktop for Mac：
   https://www.docker.com/products/docker-desktop

2. 安装并启动 Docker Desktop

3. 验证安装：
   ```bash
   docker --version
   ```

4. 使用 Docker 模式打包：
   ```bash
   ./build_apk.sh --docker --debug
   ```

## 其他常见问题

### 1. buildozer 找不到

**问题**：`zsh: command not found: buildozer`

**解决**：脚本已自动处理，会使用 `python3 -m buildozer`

### 2. 磁盘空间不足

**问题**：构建过程中提示磁盘空间不足

**解决**：
- Android SDK 和 NDK 占用空间较大（约 5-10GB）
- 确保有足够的磁盘空间
- 使用 Docker 时，清理未使用的镜像：
  ```bash
  docker system prune -a
  ```

### 3. 网络问题

**问题**：下载依赖失败

**解决**：
- 检查网络连接
- 使用 VPN（如果需要）
- 使用国内镜像源（配置 buildozer.spec）

### 4. 权限问题

**问题**：无法创建目录或文件

**解决**：
```bash
# 确保有写入权限
chmod -R 755 .
```

## 推荐工作流程

1. **开发测试**：使用 `./test_macos.sh` 在 macOS 上测试
2. **打包 APK**：使用 `./build_apk.sh --docker --debug` 打包
3. **发布版本**：使用 `./build_apk.sh --docker --release` 打包

## 获取帮助

如果遇到其他问题，请：
1. 查看 `ANDROID_BUILD.md` 详细文档
2. 检查错误日志
3. 确认 Docker 正常运行

