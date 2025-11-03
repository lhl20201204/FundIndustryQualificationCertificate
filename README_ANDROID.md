# Android 版本使用说明

## 快速开始

### 1. 安装依赖（用于本地测试）

```bash
# 在 macOS 上使用 pip3 或 python3 -m pip
pip3 install kivy plyer

# 或者
python3 -m pip install kivy plyer
```

### 2. 本地测试运行

```bash
python3 test_android.py
```

或者直接运行：

```bash
python3 main_android.py
```

### 3. 打包 Android APK

详细打包步骤请参考 [ANDROID_BUILD.md](./ANDROID_BUILD.md)

## 主要改动说明

### 框架变更

- **从 PyQt6 改为 Kivy**：PyQt6 不支持 Android，Kivy 是跨平台的移动应用框架
- **UI 组件**：使用 Kivy 的组件替代 PyQt6 组件
  - `QWidget` → `Widget` / `BoxLayout`
  - `QRadioButton` → `ToggleButton`（模拟单选）
  - `QScrollArea` → `ScrollView`
  - `QTextToSpeech` → `plyer.tts`

### 功能保持

✅ 题目显示和切换  
✅ 选项选择（使用 ToggleButton 模拟单选）  
✅ 答案查看  
✅ 自动轮播  
✅ 语音朗读（使用 Android 系统 TTS）  
✅ 题目随机排序

### 界面适配

- **触摸优化**：按钮和选项区域适合触摸操作
- **滚动支持**：题目、选项、答案都支持滚动
- **响应式布局**：适配不同屏幕尺寸

## 注意事项

1. **语音功能**：
   - Android 版本使用 `plyer` 库调用系统 TTS
   - 需要设备已安装 TTS 引擎（通常自带）
   - 朗读时间通过估算，可能不够精确

2. **文件访问**：
   - `questions.json` 需要打包进 APK
   - 确保文件在 `source.include_exts` 中包含 `json`

3. **性能**：
   - 大量题目时建议分批加载
   - Kivy 启动可能比原生应用稍慢

## 测试建议

1. **本地测试**：在开发机器上先测试基本功能
2. **模拟器测试**：使用 Android 模拟器测试
3. **真机测试**：在真实设备上测试性能和体验

## 打包后的文件位置

打包成功后，APK 文件位于：

```
bin/
├── fundexam-0.1-arm64-v8a-debug.apk  # Debug 版本
└── fundexam-0.1-arm64-v8a-release.apk  # Release 版本
```

