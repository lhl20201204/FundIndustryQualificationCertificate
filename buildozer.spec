[app]

# (str) 应用标题
title = 基金从业资格证答题

# (str) 包名
package.name = fundexam

# (str) 包域名
package.domain = org.example

# (str) 源代码目录
source.dir = .

# (list) 应用源代码
source.include_exts = py,png,jpg,kv,atlas,json

# (list) 需要排除的文件/目录
source.exclude_exts = spec,pyc,pyo,main.py,run.sh,install.sh,build_android.sh,test_android.py

# (list) 需要包含的额外文件
source.include_patterns = questions.json

# (str) 主程序入口文件
source.main = main_android.py

# (list) 应用依赖
requirements = python3,kivy>=2.1.0,plyer>=2.1.0

# (str) 自定义源码包含路径（例如为Android提供额外的源码）
#source.include_patterns = assets/*,images/*.png

# (str) 应用版本号
version = 0.1

# (list) 应用权限（Android）
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Android API 最小版本号
android.minapi = 21

# (int) Android API 目标版本号
android.api = 30

# (str) Android NDK 版本（留空使用默认）
#android.ndk = 

# (str) Android SDK 目录（留空自动检测）
#android.sdk_path = 

# (str) Android Build Tools 版本
android.build_tools_version = 33.0.0 

# (str) Android 架构
android.archs = arm64-v8a,armeabi-v7a

# (bool) 是否启用 AndroidX
android.enable_androidx = True

# (str) 应用图标（相对于项目根目录）
#icon.filename = %(source.dir)s/icon.png

# (str) 启动画面图片（相对于项目根目录）
#presplash.filename = %(source.dir)s/presplash.png

# (str) Android 应用图标（48x48像素）
#icon.48.filename = %(source.dir)s/icon-48.png

# (str) Android 应用图标（72x72像素）
#icon.72.filename = %(source.dir)s/icon-72.png

# (str) Android 应用图标（96x96像素）
#icon.96.filename = %(source.dir)s/icon-96.png

# (str) Android 应用图标（144x144像素）
#icon.144.filename = %(source.dir)s/icon-144.png

# (list) 应用包含的文件（例如 questions.json）
android.extra_manifest_application = 

# (list) Android 应用元数据
#android.meta_data = 

# (str) 应用名称
#android.label = 

# (str) 应用描述
#android.description = 

# (str) 应用作者
#android.author = 

# (str) 应用组织
#android.organization = 

# (str) 应用许可证
#android.license = 

# (str) 应用网站
#android.site = 

# (str) 应用仓库URL
#android.repository = 

# (str) 应用问题追踪URL
#android.issue = 

# (list) Android intent filters
#android.intent_filters = 

# (str) Android 应用主题
#android.theme = 

# (list) 日志过滤
#logcat.filters = 

[buildozer]

# (int) 日志级别 (0 = 最小, 1 = 正常, 2 = 详细)
log_level = 2

# (int) 显示警告次数
warn_on_root = 1

