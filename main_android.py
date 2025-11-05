#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金从业资格证答题Android应用
基于 Kivy 框架开发
"""

import json
import random
import os
from pathlib import Path
from typing import List, Dict

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.stacklayout import StackLayout
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform as kivy_platform
from kivy.config import Config

# Android TTS 需要使用 plyer 库
try:
    from plyer import tts
    TTS_AVAILABLE = True
except ImportError:
    TTS_AVAILABLE = False
    print("警告: plyer 未安装，语音功能不可用")


def get_chinese_font():
    """获取支持中文的字体路径"""
    import os
    
    # kivy.utils.platform 是一个字符串，不是函数
    try:
        current_platform = kivy_platform
    except:
        # 如果无法获取，使用系统平台
        import sys
        if sys.platform == 'darwin':
            current_platform = 'macosx'
        elif sys.platform.startswith('linux'):
            current_platform = 'linux'
        elif sys.platform.startswith('win'):
            current_platform = 'win'
        else:
            current_platform = 'unknown'
    
    # macOS 字体 - 需要提供字体文件路径
    if current_platform == 'macosx':
        # 尝试多个 macOS 中文字体路径
        font_paths = [
            '/System/Library/Fonts/PingFang.ttc',           # macOS 10.11+
            '/System/Library/Fonts/PingFang SC.ttc',
            '/System/Library/Fonts/STHeiti Light.ttc',      # 旧版 macOS
            '/System/Library/Fonts/STHeiti Medium.ttc',
            '/System/Library/Fonts/Supplemental/STSong.ttc',
            '/System/Library/Fonts/STSong.ttc',
            '/Library/Fonts/Microsoft/Microsoft YaHei.ttf', # 如果有安装
        ]
        
        # 返回第一个存在的字体文件
        for font_path in font_paths:
            if os.path.exists(font_path):
                return font_path
        
        # 如果都找不到，返回 None（使用系统默认字体）
        print("警告: 未找到中文字体文件，使用系统默认字体")
        return None
    
    # Android 字体
    elif current_platform == 'android':
        # Android 系统字体路径
        fonts_to_try = [
            '/system/fonts/NotoSansCJK-Regular.ttc',
            '/system/fonts/DroidSansFallback.ttf',
            '/system/fonts/NotoSansSC-Regular.otf',
            'DroidSansFallback',
            'Noto Sans CJK SC'
        ]
        return fonts_to_try[0]
    
    # Linux 字体
    elif current_platform == 'linux':
        fonts_to_try = [
            '/usr/share/fonts/truetype/wqy/wqy-microhei.ttc',
            '/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc',
            'WenQuanYi Micro Hei',
            'WenQuanYi Zen Hei'
        ]
        return fonts_to_try[0]
    
    # Windows 字体
    elif current_platform == 'win':
        fonts_to_try = [
            'Microsoft YaHei',
            'SimHei',
            'SimSun',
            'KaiTi'
        ]
        return fonts_to_try[0]
    
    # 默认：尝试使用系统默认字体
    return None


# 获取中文字体
CHINESE_FONT = get_chinese_font()
print(f"使用字体: {CHINESE_FONT}")


class OptionButton(BoxLayout):
    """选项按钮组件"""
    
    def __init__(self, option_key, option_text, **kwargs):
        super().__init__(**kwargs)
        self.option_key = option_key
        self.orientation = 'horizontal'
        self.spacing = 10
        self.size_hint_y = None
        self.height = '50dp'
        
        # 单选按钮（使用 ToggleButton 模拟）
        self.toggle = ToggleButton(
            text=option_key,
            size_hint_x=0.15,
            group='options',
            state='normal'
        )
        
        # 选项文本（自动换行，不滚动）
        self.text_label = Label(
            text=option_text,
            text_size=(Window.width - 100, None),  # 自动换行，宽度为窗口宽度减去按钮和边距
            halign='left',
            valign='top',
            size_hint_x=0.85,
            size_hint_y=None,
            font_name=CHINESE_FONT if CHINESE_FONT else None,
            color=(0, 0, 0, 1)  # 黑色文字，确保可见性
        )
        # 绑定文本大小变化，自动调整高度
        self.text_label.bind(texture_size=self._update_height)
        
        self.add_widget(self.toggle)
        self.add_widget(self.text_label)
    
    def _update_height(self, instance, texture_size):
        """更新文本标签和整个选项按钮的高度"""
        if texture_size and texture_size[1] > 0:
            # 文本高度 + 一些边距
            instance.height = max(texture_size[1] + 20, 50)
            # 同时更新整个选项按钮的高度
            self.height = instance.height
    
    def is_selected(self):
        return self.toggle.state == 'down'
    
    def set_selected(self, selected):
        self.toggle.state = 'down' if selected else 'normal'


class QuestionApp(App):
    """主应用类"""
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questions: List[Dict] = []
        self.current_index = 0
        self.user_answers: Dict[int, str] = {}
        self.auto_play_enabled = False
        self.is_speaking = False
    
    def build(self):
        """构建UI"""
        # 设置窗口背景色
        Window.clearcolor = (0.95, 0.95, 0.95, 1)
        
        # 外层滚动容器（整个窗口可滚动）
        main_scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            bar_width='10dp'
        )
        
        # 主容器（内容区域，不定高度）
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint_y=None)
        main_layout.bind(minimum_height=main_layout.setter('height'))
        
        # 标题栏
        title_bar = Label(
            text='基金从业资格证答题',
            size_hint_y=None,
            height='60dp',
            font_size='20sp',
            font_name=CHINESE_FONT if CHINESE_FONT else None,
            bold=True,
            color=(0.2, 0.5, 0.8, 1),
            text_size=(None, None),
            halign='center'
        )
        title_bar.bind(size=title_bar.setter('text_size'))
        main_layout.add_widget(title_bar)
        
        # 题目计数器
        self.counter_label = Label(
            text='题目 1 / 1',
            size_hint_y=None,
            height='30dp',
            font_size='12sp',
            font_name=CHINESE_FONT if CHINESE_FONT else None,
            color=(0.4, 0.4, 0.4, 1)
        )
        main_layout.add_widget(self.counter_label)
        
        # 题目内容区域（不滚动，自动换行）
        self.question_label = Label(
            text='加载中...',
            text_size=(Window.width - 40, None),
            halign='left',
            valign='top',
            font_size='16sp',
            font_name=CHINESE_FONT if CHINESE_FONT else None,
            color=(0, 0, 0, 1),
            size_hint_y=None
        )
        self.question_label.bind(texture_size=self.question_label.setter('size'))
        main_layout.add_widget(self.question_label)
        
        # 选项区域（不滚动，自动换行）
        self.options_container = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint_y=None
        )
        self.options_container.bind(minimum_height=self.options_container.setter('height'))
        main_layout.add_widget(self.options_container)
        
        # 答案显示区域（不滚动，自动换行）
        self.answer_label = Label(
            text='',
            text_size=(Window.width - 40, None),
            halign='left',
            valign='top',
            font_size='14sp',
            font_name=CHINESE_FONT if CHINESE_FONT else None,
            color=(0, 0, 0, 1),
            size_hint_y=None,
            markup=True
        )
        self.answer_label.bind(texture_size=self.answer_label.setter('size'))
        self.answer_label.height = 0  # 初始隐藏
        main_layout.add_widget(self.answer_label)
        
        # 控制按钮
        controls_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, height='50dp')
        
        self.prev_btn = Button(
            text='上一题',
            background_color=(0.3, 0.7, 0.3, 1),
            font_size='14sp',
            font_name=CHINESE_FONT if CHINESE_FONT else None
        )
        self.prev_btn.bind(on_press=self.prev_question)
        
        self.next_btn = Button(
            text='下一题',
            background_color=(0.2, 0.6, 0.9, 1),
            font_size='14sp',
            font_name=CHINESE_FONT if CHINESE_FONT else None
        )
        self.next_btn.bind(on_press=self.next_question)
        
        self.show_answer_btn = Button(
            text='查看答案',
            background_color=(1.0, 0.65, 0.0, 1),
            font_size='14sp',
            font_name=CHINESE_FONT if CHINESE_FONT else None
        )
        self.show_answer_btn.bind(on_press=self.toggle_answer)
        
        self.auto_play_btn = Button(
            text='自动轮播',
            background_color=(0.6, 0.2, 0.7, 1),
            font_size='14sp',
            font_name=CHINESE_FONT if CHINESE_FONT else None
        )
        self.auto_play_btn.bind(on_press=self.toggle_auto_play)
        
        controls_layout.add_widget(self.prev_btn)
        controls_layout.add_widget(self.next_btn)
        controls_layout.add_widget(self.show_answer_btn)
        controls_layout.add_widget(self.auto_play_btn)
        
        main_layout.add_widget(controls_layout)
        
        # 将主容器添加到滚动视图
        main_scroll.add_widget(main_layout)
        
        # 加载题目数据
        self.load_questions()
        
        # 显示第一题
        if self.questions:
            try:
                self.show_question(0)
            except Exception as e:
                print(f"显示题目时出错: {e}")
                import traceback
                traceback.print_exc()
        
        return main_scroll
    
    def load_questions(self):
        """加载题目数据"""
        json_path = Path(__file__).parent / "questions.json"
        if json_path.exists():
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        self.questions = data
                    elif isinstance(data, dict) and 'questions' in data:
                        self.questions = data['questions']
                    else:
                        self.questions = []
                    
                    # 过滤掉格式不正确的题目
                    valid_questions = []
                    for i, q in enumerate(self.questions):
                        if isinstance(q, dict) and isinstance(q.get('options'), dict):
                            valid_questions.append(q)
                        else:
                            print(f"警告: 跳过格式不正确的题目 {i} (ID: {q.get('id', 'N/A') if isinstance(q, dict) else 'N/A'})")
                    
                    self.questions = valid_questions
                    print(f"成功加载 {len(self.questions)} 道有效题目")
                    
                    # 随机打乱题目
                    if self.questions:
                        random.shuffle(self.questions)
            except Exception as e:
                print(f"加载题目失败: {e}")
                import traceback
                traceback.print_exc()
                self.questions = []
        else:
            print(f"题目文件不存在: {json_path}")
            self.questions = []
    
    def show_question(self, index: int):
        """显示指定题目"""
        if not self.questions or index < 0 or index >= len(self.questions):
            return
        
        self.current_index = index
        question = self.questions[index]
        
        # 确保 question 是字典类型
        if not isinstance(question, dict):
            print(f"错误: 题目 {index} 不是字典类型: {type(question)}")
            return
        
        # 更新计数器
        question_id = question.get('id', 'N/A') if isinstance(question, dict) else 'N/A'
        self.counter_label.text = f"题目 {index + 1} / {len(self.questions)} (ID: {question_id})"
        
        # 显示题目
        question_title = question.get('title', '') if isinstance(question, dict) else ''
        self.question_label.text = question_title
        self.question_label.text_size = (Window.width - 40, None)
        
        # 清空并重建选项
        self.options_container.clear_widgets()
        self.option_buttons = {}
        
        # 获取选项，确保是字典类型
        options = question.get('options', {}) if isinstance(question, dict) else {}
        # 如果 options 不是字典，尝试处理
        if not isinstance(options, dict):
            print(f"警告: 题目 {index} 的 options 格式不正确: {type(options)}, 值: {options}")
            options = {}
        
        for opt in ['A', 'B', 'C', 'D']:
            if opt in options and isinstance(options[opt], str):
                option_widget = OptionButton(opt, options[opt])  # 不在这里添加 "A. " 前缀，在 OptionButton 中处理
                option_widget.toggle.bind(state=self.on_option_selected)
                self.option_buttons[opt] = option_widget
                self.options_container.add_widget(option_widget)
        
        # 恢复用户之前的选择
        if index in self.user_answers:
            selected = self.user_answers[index]
            if selected in self.option_buttons:
                self.option_buttons[selected].set_selected(True)
        
        # 隐藏答案
        self.hide_answer()
        
        # 如果自动轮播开启，自动显示答案并开始朗读
        if self.auto_play_enabled:
            self.show_answer()
            Clock.schedule_once(lambda dt: self.speak_question(), 0.3)
    
    def on_option_selected(self, instance, state):
        """选项被选择时的回调"""
        if state == 'down':
            # 找到对应的选项键
            for opt, widget in self.option_buttons.items():
                if widget.toggle == instance:
                    self.user_answers[self.current_index] = opt
                    break
    
    def prev_question(self, instance):
        """上一题"""
        if self.current_index > 0:
            self.show_question(self.current_index - 1)
        else:
            if self.questions:
                self.show_question(len(self.questions) - 1)
    
    def next_question(self, instance):
        """下一题"""
        if self.current_index < len(self.questions) - 1:
            self.show_question(self.current_index + 1)
        else:
            self.show_question(0)
    
    def show_answer(self):
        """显示答案"""
        if not self.questions or self.current_index >= len(self.questions):
            return
        
        question = self.questions[self.current_index]
        answer = question.get('answer', '')
        analysis = question.get('analysis', '')
        
        # 获取用户选择
        user_selected = None
        for opt, widget in self.option_buttons.items():
            if widget.is_selected():
                user_selected = opt
                break
        
        # 构建答案文本
        answer_text = f"[b]正确答案：{answer}[/b]\n"
        if user_selected:
            if user_selected == answer:
                answer_text += f"[color=00AA00]✓ 您的选择：{user_selected} (正确)[/color]\n\n"
            else:
                answer_text += f"[color=FF0000]✗ 您的选择：{user_selected} (错误)[/color]\n\n"
        
        if analysis:
            answer_text += f"[b]解析：[/b]\n{analysis}"
        
        self.answer_label.text = answer_text
        self.answer_label.text_size = (Window.width - 40, None)
        # 设置答案区域高度，允许滚动（最大高度为窗口的40%）
        max_height = Window.height * 0.4
        label_height = self.answer_label.texture_size[1] + 40 if self.answer_label.texture_size[1] else 0
        self.answer_scroll_view.height = min(label_height, max_height)
        self.show_answer_btn.text = "隐藏答案"
    
    def hide_answer(self):
        """隐藏答案"""
        self.answer_scroll_view.height = 0
        self.show_answer_btn.text = "查看答案"
    
    def toggle_answer(self, instance):
        """切换答案显示"""
        if self.answer_scroll_view.height == 0:
            self.show_answer()
        else:
            self.hide_answer()
    
    def speak_question(self):
        """朗读题目"""
        if not TTS_AVAILABLE:
            print("TTS 不可用")
            if self.auto_play_enabled:
                Clock.schedule_once(lambda dt: self.next_question(None), 3)
            return
        
        if not self.questions or self.current_index >= len(self.questions):
            return
        
        question = self.questions[self.current_index]
        title = question.get('title', '')
        answer = question.get('answer', '')
        analysis = question.get('analysis', '')
        options = question.get('options', {})
        
        # 构建朗读文本
        text = f"题目：{title}。"
        
        if options:
            text += "选项："
            for opt in ['A', 'B', 'C', 'D']:
                if opt in options:
                    text += f"{opt}，{options[opt]}。"
        
        text += f"答案：{answer}。"
        
        if analysis:
            text += f"解析：{analysis}。"
        
        # 使用 plyer TTS
        try:
            self.is_speaking = True
            # plyer TTS 是同步的，需要估算时间
            tts.speak(text)
            # 估算朗读时间（粗略估计：每秒3-5个字，中文稍慢）
            estimated_time = len(text) / 3  # 假设每秒3个字（中文）
            Clock.schedule_once(self.on_speak_finished, estimated_time)
        except Exception as e:
            print(f"朗读失败: {e}")
            self.is_speaking = False
            if self.auto_play_enabled:
                Clock.schedule_once(lambda dt: self.next_question(None), 3)
    
    def on_speak_finished(self, dt):
        """朗读完成回调"""
        if self.is_speaking and self.auto_play_enabled:
            self.is_speaking = False
            Clock.schedule_once(lambda dt: self.next_question(None), 0.5)
    
    def toggle_auto_play(self, instance):
        """切换自动轮播"""
        if self.auto_play_enabled:
            self.auto_play_enabled = False
            self.auto_play_btn.text = "自动轮播"
            self.auto_play_btn.background_color = (0.6, 0.2, 0.7, 1)
            self.hide_answer()
        else:
            self.auto_play_enabled = True
            self.auto_play_btn.text = "停止轮播"
            self.auto_play_btn.background_color = (0.8, 0.2, 0.2, 1)
            self.show_answer()
            Clock.schedule_once(lambda dt: self.speak_question(), 0.3)


if __name__ == '__main__':
    QuestionApp().run()

