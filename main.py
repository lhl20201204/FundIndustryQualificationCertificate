#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
基金从业从业资格证答题悬浮软件（修复语音引擎调用错误）
"""

import sys
import json
import os
import random
from pathlib import Path
from typing import List, Dict

from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, 
    QHBoxLayout, QRadioButton, QButtonGroup, QTextEdit, QScrollArea
)
from PyQt6.QtCore import Qt, QTimer, QPoint
from PyQt6.QtGui import QFont, QColor, QPainter, QPen, QBrush
from PyQt6.QtTextToSpeech import QTextToSpeech


class ScrollableOptionWidget(QWidget):
    """支持水平滚动的选项组件"""
    
    def __init__(self, option_key: str, parent=None):
        super().__init__(parent)
        self.option_key = option_key
        self.radio_button = None
        self.text_label = None
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # 单选按钮
        self.radio_button = QRadioButton()
        self.radio_button.setStyleSheet("""
            QRadioButton::indicator {
                width: 15px;
                height: 15px;
            }
        """)
        layout.addWidget(self.radio_button, 0)  # 不拉伸
        
        # 滚动区域和文本标签
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:horizontal {
                height: 8px;
                background: rgba(200, 200, 200, 0.3);
                border-radius: 4px;
            }
            QScrollBar::handle:horizontal {
                background: rgba(100, 100, 100, 0.5);
                border-radius: 4px;
                min-width: 20px;
            }
            QScrollBar::handle:horizontal:hover {
                background: rgba(80, 80, 80, 0.7);
            }
        """)
        
        self.text_label = QLabel()
        self.text_label.setStyleSheet("""
            QLabel {
                font-size: 12px;
                padding: 5px;
                background: transparent;
            }
        """)
        self.text_label.setWordWrap(False)  # 不自动换行，允许水平滚动
        self.text_label.setTextFormat(Qt.TextFormat.PlainText)
        self.text_label.setMinimumHeight(25)  # 设置最小高度
        
        scroll_area.setWidget(self.text_label)
        layout.addWidget(scroll_area, 1)  # 可拉伸
    
    def setText(self, text: str):
        """设置文本"""
        if self.text_label:
            self.text_label.setText(text)
            # 更新标签尺寸，确保可以滚动
            self.text_label.adjustSize()
            # 设置最小宽度，让文本可以完整显示
            fm = self.text_label.fontMetrics()
            text_width = fm.boundingRect(text).width()
            self.text_label.setMinimumWidth(text_width + 10)  # 加10px的padding
    
    def isChecked(self) -> bool:
        """是否选中"""
        return self.radio_button.isChecked() if self.radio_button else False
    
    def setChecked(self, checked: bool):
        """设置选中状态"""
        if self.radio_button:
            self.radio_button.setChecked(checked)
    
    def clicked(self):
        """返回点击信号的连接方法"""
        return self.radio_button.clicked if self.radio_button else None


class FloatingWindow(QWidget):
    """悬浮窗主窗口"""
    
    def __init__(self):
        super().__init__()
        self.questions: List[Dict] = []
        self.current_index = 0
        self.user_answers: Dict[int, str] = {}
        
        # 自动轮播属性
        self.auto_play_enabled = False
        self.auto_play_timer = QTimer()
        self.auto_play_timer.timeout.connect(self.next_question)
        
        # 语音引擎修复核心部分
        self.tts = None
        try:
            # 强制使用macOS原生引擎
            os.environ["QT_TTS_USE_NATIVE_SPEECHSYNTHESIZER"] = "1"
            
            # 获取可用引擎
            engines = QTextToSpeech.availableEngines()
            print(f"检测到的语音引擎列表: {engines}")
            
            # 优先选择darwin引擎（macOS原生）
            selected_engine = "darwin" if "darwin" in engines else engines[0]
            self.tts = QTextToSpeech(selected_engine, self)
            print(f"成功加载语音引擎: {selected_engine}")
            
            # 修复语音选择逻辑（避免调用不存在的方法）
            voices = self.tts.availableVoices()
            if voices:
                # 直接使用索引选择语音（避开可能的属性调用问题）
                # 优先选择中文语音（通常索引1或2为中文）
                chinese_voice_index = next(
                    (i for i, v in enumerate(voices) if "chinese" in v.name().lower()),
                    0  # 默认第一个语音
                )
                self.tts.setVoice(voices[chinese_voice_index])
                print(f"使用语音: {voices[chinese_voice_index].name()}")
            
            # 语音参数（中文适配）
            self.tts.setRate(-0.1)  # 稍慢语速
            self.tts.setPitch(0.0)
            self.tts.setVolume(1.0)
            
            # 状态监听
            self.tts.stateChanged.connect(self.on_tts_state_changed)

        except Exception as e:
            print(f"语音引擎初始化失败: {str(e)}")
            print("将无法使用语音朗读功能，但其他功能正常")
            self.tts = None
        
        self.is_speaking = False
        
        # 加载题目
        self.load_questions()
        self.init_ui()
        self.setup_window()
    
    def load_questions(self):
        """加载题目数据"""
        json_path = Path(__file__).parent / "questions.json"
        if json_path.exists():
            try:
                with open(json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # 如果有将question随机排序
                    if isinstance(data, list):
                        raw_questions = data
                    else:
                        raw_questions = data.get('questions', [])
                    
                    # 过滤掉格式错误的题目
                    self.questions = []
                    for i, q in enumerate(raw_questions):
                        if not isinstance(q, dict):
                            print(f"警告: 跳过题目 {i}，数据格式错误（不是字典）")
                            continue
                        if 'options' not in q:
                            print(f"警告: 跳过题目 {i} (ID: {q.get('id', 'N/A')})，缺少 options 字段")
                            continue
                        if not isinstance(q.get('options'), dict):
                            print(f"警告: 跳过题目 {i} (ID: {q.get('id', 'N/A')})，options 不是字典类型")
                            continue
                        self.questions.append(q)
                    
                    print(f"成功加载 {len(self.questions)} 道有效题目（共 {len(raw_questions)} 道）")
                    
                    # 随机打乱题目顺序
                    random.shuffle(self.questions)
            except Exception as e:
                print(f"加载题目失败: {e}")
                self.questions = []
        else:
            print(f"题目文件不存在: {json_path}")
            self.questions = []
    
    def init_ui(self):
        """初始化界面"""
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(15, 15, 15, 15)
        
        # 标题栏（可拖拽）
        self.title_bar = QLabel("基金从业资格证答题")
        self.title_bar.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        self.title_bar.setStyleSheet("""
            QLabel {
                background-color: rgba(70, 130, 180, 0.9);
                color: white;
                padding: 8px;
                border-radius: 5px;
            }
        """)
        main_layout.addWidget(self.title_bar)
        
        # 题目计数器
        self.counter_label = QLabel()
        self.counter_label.setStyleSheet("color: #666; font-size: 11px;")
        main_layout.addWidget(self.counter_label)
        
        # 题目内容
        self.question_label = QTextEdit()
        self.question_label.setReadOnly(True)
        self.question_label.setMaximumHeight(80)
        self.question_label.setStyleSheet("""
            QTextEdit {
                background-color: rgba(255, 255, 255, 0.95);
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                font-size: 13px;
            }
        """)
        main_layout.addWidget(self.question_label)
        
        # 选项组（使用支持水平滚动的自定义组件）
        self.option_group = QButtonGroup()
        self.option_buttons = {}
        options_layout = QVBoxLayout()
        options_layout.setSpacing(5)
        
        for opt in ['A', 'B', 'C', 'D']:
            option_widget = ScrollableOptionWidget(opt)
            self.option_buttons[opt] = option_widget
            self.option_group.addButton(option_widget.radio_button)
            option_widget.radio_button.toggled.connect(lambda checked, o=opt: self.on_option_selected(o) if checked else None)
            options_layout.addWidget(option_widget)
        
        main_layout.addLayout(options_layout)
        
        # 答案区域
        self.answer_label = QLabel()
        self.answer_label.setWordWrap(True)
        self.answer_label.setStyleSheet("""
            QLabel {
                background-color: rgba(255, 250, 205, 0.9);
                border: 1px solid #ddd;
                border-radius: 5px;
                padding: 10px;
                font-size: 12px;
            }
        """)
        self.answer_label.hide()
        main_layout.addWidget(self.answer_label)
        
        # 控制按钮
        control_layout = QHBoxLayout()
        
        self.prev_btn = QPushButton("上一题")
        self.prev_btn.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.prev_btn.clicked.connect(self.prev_question)
        
        self.next_btn = QPushButton("下一题")
        self.next_btn.setStyleSheet("""
            QPushButton {
                background-color: #2196F3;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #0b7dda;
            }
        """)
        self.next_btn.clicked.connect(self.next_question)
        
        self.show_answer_btn = QPushButton("查看答案")
        self.show_answer_btn.setStyleSheet("""
            QPushButton {
                background-color: #FF9800;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #e68900;
            }
        """)
        self.show_answer_btn.clicked.connect(self.toggle_answer)
        
        self.auto_play_btn = QPushButton("自动轮播")
        self.auto_play_btn.setStyleSheet("""
            QPushButton {
                background-color: #9C27B0;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #7b1fa2;
            }
        """)
        self.auto_play_btn.clicked.connect(self.toggle_auto_play)
        
        control_layout.addWidget(self.prev_btn)
        control_layout.addWidget(self.next_btn)
        control_layout.addWidget(self.show_answer_btn)
        control_layout.addWidget(self.auto_play_btn)
        
        main_layout.addLayout(control_layout)
        
        # 关闭按钮
        close_btn = QPushButton("关闭")
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
        """)
        close_btn.clicked.connect(self.close)
        main_layout.addWidget(close_btn)
        
        self.setLayout(main_layout)
        
        # 显示第一题
        if self.questions:
            self.show_question(0)
    
    def setup_window(self):
        """设置窗口属性"""
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool |
            Qt.WindowType.Window  # 添加窗口标志，确保置顶生效
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setFixedSize(450, 550)
        
        # 移动到右上角
        screen = QApplication.primaryScreen().geometry()
        self.move(screen.width() - 470, 50)
        
        # 确保窗口始终置顶
        self.raise_()
        self.activateWindow()
        
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(240, 240, 240, 0.95);
                border-radius: 10px;
            }
        """)
    
    def showEvent(self, event):
        """窗口显示事件，确保窗口置顶"""
        super().showEvent(event)
        self.raise_()
        self.activateWindow()
        # 定期检查并确保窗口置顶
        QTimer.singleShot(100, lambda: (self.raise_(), self.activateWindow()))
    
    def paintEvent(self, event):
        """绘制窗口边框"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor(240, 240, 240, 245)))
        painter.setPen(QPen(QColor(200, 200, 200, 255), 2))
        painter.drawRoundedRect(1, 1, self.width() - 2, self.height() - 2, 10, 10)
    
    def mousePressEvent(self, event):
        """拖拽窗口"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_position = event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """移动窗口"""
        if event.buttons() == Qt.MouseButton.LeftButton and hasattr(self, 'drag_position'):
            self.move(event.globalPosition().toPoint() - self.drag_position)
            event.accept()
    
    def show_question(self, index: int):
        """显示指定题目"""
        if not self.questions or index < 0 or index >= len(self.questions):
            return
        
        self.current_index = index
        question = self.questions[index]
        
        # 验证题目数据格式
        if not isinstance(question, dict):
            print(f"警告: 题目 {index} 数据格式错误，跳过")
            return
        
        # 更新计数器
        self.counter_label.setText(f"题目 {index + 1} / {len(self.questions)} (ID: {question.get('id', 'N/A')})")
        
        # 显示题目
        self.question_label.setText(question.get('title', ''))
        
        # 显示选项 - 添加类型检查
        options = question.get('options', {})
        if not isinstance(options, dict):
            print(f"警告: 题目 {index} (ID: {question.get('id', 'N/A')}) 的 options 格式错误，期望字典但得到 {type(options).__name__}")
            # 如果 options 不是字典，跳过该题目，跳转到下一题
            if index + 1 < len(self.questions):
                QTimer.singleShot(100, lambda: self.show_question(index + 1))
            return
        
        for opt in ['A', 'B', 'C', 'D']:
            option_widget = self.option_buttons[opt]
            if opt in options and isinstance(options[opt], str):
                option_widget.setText(f"{opt}. {options[opt]}")
                option_widget.setVisible(True)
            else:
                option_widget.setVisible(False)
        
        # 恢复选择
        if index in self.user_answers:
            selected = self.user_answers[index]
            if selected in self.option_buttons:
                self.option_buttons[selected].setChecked(True)
        else:
            self.option_group.setExclusive(False)
            for btn in self.option_buttons.values():
                btn.setChecked(False)
            self.option_group.setExclusive(True)
        
        # 自动轮播逻辑
        if self.auto_play_enabled:
            self.show_answer()
            QTimer.singleShot(300, self.speak_question)
        else:
            self.answer_label.hide()
            self.show_answer_btn.setText("查看答案")
            if self.tts:
                try:
                    self.tts.stop()
                except:
                    pass
    
    def on_option_selected(self, option: str):
        """记录用户选择"""
        self.user_answers[self.current_index] = option
    
    def prev_question(self):
        """上一题"""
        self.save_current_selection()
        if self.current_index > 0:
            self.show_question(self.current_index - 1)
        else:
            self.show_question(len(self.questions) - 1)
    
    def next_question(self):
        """下一题"""
        self.save_current_selection()
        if self.current_index < len(self.questions) - 1:
            self.show_question(self.current_index + 1)
        else:
            self.show_question(0)
    
    def save_current_selection(self):
        """保存当前选择"""
        for opt, btn in self.option_buttons.items():
            if btn.isChecked():
                self.user_answers[self.current_index] = opt
                break
    
    def show_answer(self):
        """显示答案"""
        if not self.questions or self.current_index >= len(self.questions):
            return
        
        question = self.questions[self.current_index]
        answer = question.get('answer', '')
        analysis = question.get('analysis', '')
        user_selected = next((opt for opt, btn in self.option_buttons.items() if btn.isChecked()), None)
        
        answer_text = f"<b>正确答案：{answer}</b><br>"
        if user_selected:
            if user_selected == answer:
                answer_text += f"<span style='color: green;'>✓ 您的选择：{user_selected} (正确)</span><br><br>"
            else:
                answer_text += f"<span style='color: red;'>✗ 您的选择：{user_selected} (错误)</span><br><br>"
        
        if analysis:
            answer_text += f"<b>解析：</b><br>{analysis}"
        
        self.answer_label.setText(answer_text)
        self.answer_label.show()
        self.show_answer_btn.setText("隐藏答案")
    
    def hide_answer(self):
        """隐藏答案"""
        self.answer_label.hide()
        self.show_answer_btn.setText("查看答案")
    
    def toggle_answer(self):
        """切换答案显示状态"""
        if self.answer_label.isVisible():
            self.hide_answer()
        else:
            self.show_answer()
    
    def speak_question(self):
        """朗读题目（修复版）"""
        if not self.tts:
            print("语音引擎不可用，无法朗读")
            if self.auto_play_enabled:
                QTimer.singleShot(3000, self.next_question)
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
                    if opt == answer:
                        text += f"<b>{options[opt]}</b>。"
        # if analysis:
        #     text += f"解析：{analysis}。"
        
        # 简化朗读调用（避免复杂属性）
        try:
            self.is_speaking = True
            self.tts.say(text)
        except Exception as e:
            print(f"朗读失败: {e}")
            if self.auto_play_enabled:
                QTimer.singleShot(3000, self.next_question)
    
    def on_tts_state_changed(self, state):
        """语音状态回调（简化版）"""
        try:
            if not self.tts:
                return
                
            if state == QTextToSpeech.State.Speaking:
                self.is_speaking = True
            elif state in [QTextToSpeech.State.Ready, QTextToSpeech.State.Paused]:
                if self.is_speaking and self.auto_play_enabled:
                    self.is_speaking = False
                    QTimer.singleShot(500, self.next_question)
        except Exception as e:
            print(f"TTS状态错误: {e}")
            self.is_speaking = False
    
    def toggle_auto_play(self):
        """切换自动轮播"""
        if self.auto_play_enabled:
            self.auto_play_enabled = False
            if self.tts:
                try:
                    self.tts.stop()
                except:
                    pass
            self.auto_play_btn.setText("自动轮播")
            self.auto_play_btn.setStyleSheet("""
                QPushButton {
                    background-color: #9C27B0;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 5px;
                    font-size: 12px;
                }
            """)
        else:
            self.auto_play_enabled = True
            self.auto_play_btn.setText("停止轮播")
            self.auto_play_btn.setStyleSheet("""
                QPushButton {
                    background-color: #F44336;
                    color: white;
                    border: none;
                    padding: 8px 15px;
                    border-radius: 5px;
                    font-size: 12px;
                }
            """)
            self.show_answer()
            QTimer.singleShot(300, self.speak_question)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("基金从业资格证答题")
    window = FloatingWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()