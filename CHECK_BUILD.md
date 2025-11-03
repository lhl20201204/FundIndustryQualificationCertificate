# 构建检查清单

## 已提交的文件

请确认以下文件已成功推送到 GitHub：

- ✅ `.github/workflows/build-android.yml` - GitHub Actions 工作流
- ✅ `main_android.py` - Android 应用主程序
- ✅ `questions.json` - 题目数据文件
- ✅ `buildozer.spec` - Buildozer 配置文件
- ✅ `requirements_android.txt` - Python 依赖列表

## 检查构建状态

1. **访问 Actions 页面**：
   ```
   https://github.com/lhl20201204/FundIndustryQualificationCertificate/actions
   ```

2. **查看最新的构建任务**：
   - 点击最新的构建任务（最上面的）
   - 查看构建日志

## 常见构建错误及解决方案

### 错误 1: 文件缺失

**症状**：构建在 5-10 秒内失败，提示文件不存在

**解决方案**：
- 检查所有必需文件是否已提交
- 运行 `git ls-files` 确认文件已跟踪

### 错误 2: Buildozer 安装失败

**症状**：`pip install buildozer` 失败

**解决方案**：
- 已改进 workflow，使用 `pip install --user buildozer`
- 添加了 PATH 设置

### 错误 3: 依赖下载失败

**症状**：构建过程中下载 Android SDK/NDK 失败

**解决方案**：
- 首次构建需要下载大量依赖（约 1-2GB）
- 可能需要 20-30 分钟
- 已设置 60 分钟超时

### 错误 4: 内存不足

**症状**：构建过程中被杀死（killed）

**解决方案**：
- GitHub Actions 提供 7GB 内存，通常足够
- 如果仍失败，可能需要优化 buildozer.spec

## 查看详细日志

如果构建失败：

1. 点击失败的构建任务
2. 展开每个步骤查看详细日志
3. 特别关注：
   - "Verify project files" 步骤：确认文件存在
   - "Build APK" 步骤：查看具体错误信息

## 手动重新触发构建

1. 访问 Actions 页面
2. 点击左侧的 "Build Android APK"
3. 点击右侧的 "Run workflow" 按钮
4. 选择分支（main），点击 "Run workflow"

