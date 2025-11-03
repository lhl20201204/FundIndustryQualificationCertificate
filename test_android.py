#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 Android 版本（在本地运行）
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(__file__))

# 设置 Kivy 配置（避免需要窗口管理器）
os.environ['KIVY_WINDOW'] = 'sdl2'

from main_android import QuestionApp

if __name__ == '__main__':
    QuestionApp().run()

