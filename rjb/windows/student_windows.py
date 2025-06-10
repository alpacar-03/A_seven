from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QSplitter, QTextEdit, QLineEdit, QFileDialog, QMessageBox,
    QFrame, QSizePolicy, QProgressBar, QApplication, QComboBox,
    QScrollArea, QWidget, QGridLayout
)
from PyQt5.QtGui import QPalette, QColor, QFont, QIcon
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject, QSize
from datetime import datetime
import os

from rjb.styles.theme import Theme
from rjb.utils.file_utils import read_file_content
from rjb.Large_Model.DeepSeek import Deepseek_API

class StudentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.learning_assistant_window = None
        self.practice_assistant_window = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('学生端界面')
        self.resize(800, 600)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # 顶部标题区
        title_frame = QFrame()
        title_frame.setStyleSheet('''
            QFrame {
                background-color: #2c3e50;
                border-radius: 12px;
                padding: 24px 0px;
            }
        ''')
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # 标题文本
        title_label = QLabel('学生学习中心')
        title_label.setStyleSheet('''
            color: white;
            font-size: 28px;
            font-weight: bold;
            font-family: Microsoft YaHei;
            letter-spacing: 2px;
        ''')
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)

        # 副标题
        subtitle_label = QLabel('智能学习 & 在线答疑')
        subtitle_label.setStyleSheet('''
            color: rgba(255, 255, 255, 0.8);
            font-size: 16px;
            font-family: Microsoft YaHei;
        ''')
        subtitle_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(subtitle_label)

        main_layout.addWidget(title_frame)

        # 功能按钮区
        button_frame = QFrame()
        button_frame.setStyleSheet('''
            QFrame {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f5f5f5, stop:1 #e0e0e0);
                border-radius: 18px;
            }
        ''')
        button_layout = QVBoxLayout(button_frame)
        button_layout.setContentsMargins(60, 60, 60, 60)
        button_layout.setSpacing(40)

        # 在线学习助手按钮
        assistant_btn = self.create_feature_button(
            '在线学习助手',
            '🤖',
            '智能答疑 | 知识解析 | 学习指导',
            '#2ecc71'
        )
        assistant_btn.clicked.connect(self.show_learning_assistant)
        button_layout.addWidget(assistant_btn)

        # 练习评测助手按钮
        practice_btn = self.create_feature_button(
            '练习评测助手',
            '📝',
            '智能出题 | 实时评测 | 错题分析',
            '#e74c3c'
        )
        practice_btn.clicked.connect(self.show_practice_assistant)
        button_layout.addWidget(practice_btn)

        main_layout.addWidget(button_frame)

        # 设置主布局
        self.setLayout(main_layout)

        # 设置窗口背景色
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

    def create_feature_button(self, title, icon, description, color):
        button = QPushButton()
        button.setFixedHeight(120)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 创建按钮内容布局
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(30, 15, 30, 15)
        content_layout.setSpacing(20)

        # 图标
        icon_label = QLabel(icon)
        icon_label.setFixedSize(60, 60)
        icon_label.setStyleSheet(f'''
            background-color: {color};
            color: white;
            font-size: 30px;
            border-radius: 30px;
            padding: 10px;
        ''')
        icon_label.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(icon_label)

        # 文本区域
        text_layout = QVBoxLayout()
        text_layout.setSpacing(5)

        # 标题
        title_label = QLabel(title)
        title_label.setStyleSheet('''
            color: #2c3e50;
            font-size: 20px;
            font-weight: bold;
            font-family: Microsoft YaHei;
        ''')
        text_layout.addWidget(title_label)

        # 描述
        desc_label = QLabel(description)
        desc_label.setStyleSheet('''
            color: #7f8c8d;
            font-size: 14px;
            font-family: Microsoft YaHei;
        ''')
        text_layout.addWidget(desc_label)

        content_layout.addLayout(text_layout)
        content_layout.addStretch()

        # 设置按钮样式和布局
        button.setLayout(content_layout)
        button.setStyleSheet(f'''
            QPushButton {{
                background-color: white;
                border: 2px solid {color};
                border-radius: 15px;
            }}
            QPushButton:hover {{
                background-color: {color}11;
            }}
            QPushButton:pressed {{
                background-color: {color}22;
            }}
        ''')

        return button

    def show_learning_assistant(self):
        if self.learning_assistant_window is None or not self.learning_assistant_window.isVisible():
            self.learning_assistant_window = LearningAssistantWindow()
            self.learning_assistant_window.show()
        else:
            self.learning_assistant_window.activateWindow()
            self.learning_assistant_window.raise_()

    def show_practice_assistant(self):
        if self.practice_assistant_window is None or not self.practice_assistant_window.isVisible():
            self.practice_assistant_window = PracticeAssistantWindow()
            self.practice_assistant_window.show()
        else:
            self.practice_assistant_window.activateWindow()
            self.practice_assistant_window.raise_()

class GenerateWorker(QObject):
    finished = pyqtSignal(str)
    error = pyqtSignal(str)

    def __init__(self, messages, content):
        super().__init__()
        self.messages = messages
        self.content = content

    def run(self):
        try:
            self.messages.append({"role": "user", "content": self.content})
            short_messages = self.messages[-2:]
            response = Deepseek_API(short_messages)
            self.messages.append({"role": "assistant", "content": response})
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            formatted_response = f'[{current_time}] 解答：\n{response}\n\n'
            self.finished.emit(formatted_response)
        except Exception as e:
            self.error.emit(str(e))

class LearningAssistantWindow(QWidget):
    messages = []
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.thread = None
        self.worker = None

    def init_ui(self):
        self.setWindowTitle('在线学习助手')
        self.resize(1200, 800)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 顶部导航栏
        nav_frame = QFrame()
        nav_frame.setStyleSheet('''
            QFrame {
                background-color: #2c3e50;
                border-radius: 12px;
                padding: 24px 0px;
            }
        ''')
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel('在线学习助手')
        title_label.setStyleSheet('''
            color: white;
            font-size: 28px;
            font-weight: bold;
            font-family: Microsoft YaHei;
            letter-spacing: 2px;
        ''')
        title_label.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(title_label)

        subtitle_label = QLabel('基于大模型的智能学习助手')
        subtitle_label.setStyleSheet('''
            color: rgba(255, 255, 255, 0.8);
            font-size: 16px;
            font-family: Microsoft YaHei;
        ''')
        subtitle_label.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(subtitle_label)

        main_layout.addWidget(nav_frame)

        # 内容区域
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # 左侧输入区域
        left_frame = QFrame()
        left_frame.setStyleSheet('''
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 2px solid #e0e0e0;
            }
        ''')
        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(20)

        # 学科选择
        subject_layout = QHBoxLayout()
        subject_label = QLabel('学科：')
        subject_label.setStyleSheet('font-size: 14px; font-weight: bold;')
        self.subject_combo = QComboBox()
        self.subject_combo.addItems(['计算机类', '数学类', '物理类', '化学类', '生物类', '其他'])
        self.subject_combo.setStyleSheet('''
            QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
                min-width: 150px;
            }
        ''')
        subject_layout.addWidget(subject_label)
        subject_layout.addWidget(self.subject_combo)
        subject_layout.addStretch()
        left_layout.addLayout(subject_layout)

        # 问题类型选择
        type_layout = QHBoxLayout()
        type_label = QLabel('问题类型：')
        type_label.setStyleSheet('font-size: 14px; font-weight: bold;')
        self.type_combo = QComboBox()
        self.type_combo.addItems(['概念理解', '解题思路', '代码实现', '实验操作', '其他'])
        self.type_combo.setStyleSheet('''
            QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
                min-width: 150px;
            }
        ''')
        type_layout.addWidget(type_label)
        type_layout.addWidget(self.type_combo)
        type_layout.addStretch()
        left_layout.addLayout(type_layout)

        # 问题输入区域
        question_label = QLabel('请输入你的问题：')
        question_label.setStyleSheet('font-size: 14px; font-weight: bold;')
        left_layout.addWidget(question_label)

        self.input_text = QTextEdit()
        self.input_text.setStyleSheet('''
            QTextEdit {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-family: Microsoft YaHei;
            }
        ''')
        self.input_text.setPlaceholderText('请详细描述你的问题，可以包含具体的知识点、代码或公式等...')
        left_layout.addWidget(self.input_text, stretch=2)

        # 提交按钮
        submit_btn = QPushButton('提交问题')
        submit_btn.setStyleSheet(Theme.BUTTON_STYLE)
        submit_btn.clicked.connect(self.submit_question)
        self.submit_button = submit_btn
        left_layout.addWidget(submit_btn)

        content_layout.addWidget(left_frame, stretch=2)

        # 右侧输出区域
        right_frame = QFrame()
        right_frame.setStyleSheet('''
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 2px solid #e0e0e0;
            }
        ''')
        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(20)

        # 输出区域标题
        output_title = QLabel('智能解答')
        output_title.setStyleSheet('''
            color: #2c3e50;
            font-size: 18px;
            font-weight: bold;
            font-family: Microsoft YaHei;
            padding: 10px 0;
        ''')
        right_layout.addWidget(output_title)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet('''
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        ''')

        # 创建内容容器
        content_widget = QWidget()
        self.output_layout = QVBoxLayout(content_widget)
        self.output_layout.setSpacing(15)
        self.output_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area.setWidget(content_widget)
        right_layout.addWidget(scroll_area, stretch=3)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet('''
            QProgressBar {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                text-align: center;
                background-color: white;
            }
            QProgressBar::chunk {
                background-color: #2ecc71;
                border-radius: 8px;
            }
        ''')
        self.progress_bar.setVisible(False)
        right_layout.addWidget(self.progress_bar)

        content_layout.addWidget(right_frame, stretch=3)

        main_layout.addLayout(content_layout, stretch=8)

        # 状态栏
        status_bar = QFrame()
        status_bar.setStyleSheet('''
            QFrame {
                background-color: #f5f5f5;
                border-radius: 8px;
                padding: 10px;
            }
        ''')
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(10, 10, 10, 10)

        self.status_label = QLabel('就绪')
        self.status_label.setStyleSheet('color: #7f8c8d;')
        status_layout.addWidget(self.status_label)

        main_layout.addWidget(status_bar, stretch=0)

        self.setLayout(main_layout)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

    def submit_question(self):
        content = self.input_text.toPlainText().strip()
        if not content:
            QMessageBox.warning(self, '错误', '请输入问题内容！')
            return

        # 构建提示词
        subject = self.subject_combo.currentText()
        question_type = self.type_combo.currentText()
        
        prompt = f"""请针对以下{subject}的{question_type}问题，提供详细的解答：

问题内容：
{content}

要求：
1. 解答要详细、准确、易于理解
2. 如果是概念理解问题，请提供清晰的解释和例子
3. 如果是解题思路问题，请提供详细的解题步骤
4. 如果是代码实现问题，请提供完整的代码和注释
5. 如果是实验操作问题，请提供具体的操作步骤和注意事项
6. 适当引用相关的知识点和原理
7. 如果可能，提供一些相关的练习题或思考题

请按以下格式输出：
解答：
[详细解答内容]

补充说明：
[补充说明内容]

相关练习：
[练习题内容]"""

        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.submit_button.setEnabled(False)
        self.status_label.setText('正在生成解答...')

        # QThread + Worker
        self.thread = QThread()
        self.worker = GenerateWorker(self.messages, prompt)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.update_ui)
        self.worker.error.connect(self.show_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.error.connect(self.thread.quit)
        self.worker.error.connect(self.worker.deleteLater)
        self.thread.start()

    def update_ui(self, response):
        # 创建新的回答框
        answer_frame = QFrame()
        answer_frame.setStyleSheet('''
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        ''')
        answer_layout = QVBoxLayout(answer_frame)
        answer_layout.setContentsMargins(15, 15, 15, 15)
        answer_layout.setSpacing(10)

        # 添加时间戳
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time_label = QLabel(f'回答时间：{timestamp}')
        time_label.setStyleSheet('color: #7f8c8d; font-size: 12px;')
        answer_layout.addWidget(time_label)

        # 添加回答内容
        answer_text = QTextEdit()
        answer_text.setReadOnly(True)
        answer_text.setStyleSheet('''
            QTextEdit {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                font-family: Microsoft YaHei;
            }
        ''')
        answer_text.setText(response)
        answer_layout.addWidget(answer_text)

        # 将回答框添加到输出区域
        self.output_layout.addWidget(answer_frame)

        self.progress_bar.setVisible(False)
        self.submit_button.setEnabled(True)
        self.status_label.setText('就绪')

    def show_error(self, error_msg):
        QMessageBox.critical(self, '错误', f'生成解答失败：{error_msg}')
        self.progress_bar.setVisible(False)
        self.submit_button.setEnabled(True)
        self.status_label.setText('就绪')

class PracticeAssistantWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.thread = None
        self.worker = None
        self.current_question = None
        self.history = []

    def init_ui(self):
        self.setWindowTitle('练习评测助手')
        self.resize(1200, 800)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 顶部导航栏
        nav_frame = QFrame()
        nav_frame.setStyleSheet('''
            QFrame {
                background-color: #2c3e50;
                border-radius: 12px;
                padding: 24px 0px;
            }
        ''')
        nav_layout = QVBoxLayout(nav_frame)
        nav_layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel('练习评测助手')
        title_label.setStyleSheet('''
            color: white;
            font-size: 28px;
            font-weight: bold;
            font-family: Microsoft YaHei;
            letter-spacing: 2px;
        ''')
        title_label.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(title_label)

        subtitle_label = QLabel('智能出题 | 实时评测 | 错题分析')
        subtitle_label.setStyleSheet('''
            color: rgba(255, 255, 255, 0.8);
            font-size: 16px;
            font-family: Microsoft YaHei;
        ''')
        subtitle_label.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(subtitle_label)

        main_layout.addWidget(nav_frame)

        # 内容区域
        content_layout = QHBoxLayout()
        content_layout.setSpacing(20)

        # 左侧设置区域
        left_frame = QFrame()
        left_frame.setStyleSheet('''
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 2px solid #e0e0e0;
            }
        ''')
        left_layout = QVBoxLayout(left_frame)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(20)

        # 学科选择
        subject_layout = QHBoxLayout()
        subject_label = QLabel('学科：')
        subject_label.setStyleSheet('font-size: 14px; font-weight: bold;')
        self.subject_combo = QComboBox()
        self.subject_combo.addItems(['计算机类', '数学类', '物理类', '化学类', '生物类', '其他'])
        self.subject_combo.setStyleSheet('''
            QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
                min-width: 150px;
            }
        ''')
        subject_layout.addWidget(subject_label)
        subject_layout.addWidget(self.subject_combo)
        subject_layout.addStretch()
        left_layout.addLayout(subject_layout)

        # 难度选择
        difficulty_layout = QHBoxLayout()
        difficulty_label = QLabel('难度：')
        difficulty_label.setStyleSheet('font-size: 14px; font-weight: bold;')
        self.difficulty_combo = QComboBox()
        self.difficulty_combo.addItems(['简单', '中等', '困难'])
        self.difficulty_combo.setStyleSheet('''
            QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
                min-width: 150px;
            }
        ''')
        difficulty_layout.addWidget(difficulty_label)
        difficulty_layout.addWidget(self.difficulty_combo)
        difficulty_layout.addStretch()
        left_layout.addLayout(difficulty_layout)

        # 题目数量
        count_layout = QHBoxLayout()
        count_label = QLabel('题目数量：')
        count_label.setStyleSheet('font-size: 14px; font-weight: bold;')
        self.count_combo = QComboBox()
        self.count_combo.addItems(['1', '3', '5', '10'])
        self.count_combo.setStyleSheet('''
            QComboBox {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
                min-width: 150px;
            }
        ''')
        count_layout.addWidget(count_label)
        count_layout.addWidget(self.count_combo)
        count_layout.addStretch()
        left_layout.addLayout(count_layout)

        # 练习要求输入
        requirements_label = QLabel('练习要求：')
        requirements_label.setStyleSheet('font-size: 14px; font-weight: bold;')
        left_layout.addWidget(requirements_label)

        self.requirements_text = QTextEdit()
        self.requirements_text.setStyleSheet('''
            QTextEdit {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-family: Microsoft YaHei;
            }
        ''')
        self.requirements_text.setPlaceholderText('请输入具体的练习要求，如：重点知识点、题型偏好等...')
        left_layout.addWidget(self.requirements_text, stretch=1)

        # 生成题目按钮
        generate_btn = QPushButton('生成练习题')
        generate_btn.setStyleSheet(Theme.BUTTON_STYLE)
        generate_btn.clicked.connect(self.generate_questions)
        left_layout.addWidget(generate_btn)

        content_layout.addWidget(left_frame, stretch=1)

        # 右侧练习区域
        right_frame = QFrame()
        right_frame.setStyleSheet('''
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 2px solid #e0e0e0;
            }
        ''')
        right_layout = QVBoxLayout(right_frame)
        right_layout.setContentsMargins(20, 20, 20, 20)
        right_layout.setSpacing(20)

        # 练习区域标题
        practice_title = QLabel('练习题')
        practice_title.setStyleSheet('''
            color: #2c3e50;
            font-size: 18px;
            font-weight: bold;
            font-family: Microsoft YaHei;
            padding: 10px 0;
        ''')
        right_layout.addWidget(practice_title)

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet('''
            QScrollArea {
                border: none;
                background-color: transparent;
            }
        ''')

        # 创建内容容器
        content_widget = QWidget()
        self.practice_layout = QVBoxLayout(content_widget)
        self.practice_layout.setSpacing(15)
        self.practice_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area.setWidget(content_widget)
        right_layout.addWidget(scroll_area, stretch=3)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet('''
            QProgressBar {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                text-align: center;
                background-color: white;
            }
            QProgressBar::chunk {
                background-color: #e74c3c;
                border-radius: 8px;
            }
        ''')
        self.progress_bar.setVisible(False)
        right_layout.addWidget(self.progress_bar)

        content_layout.addWidget(right_frame, stretch=2)

        main_layout.addLayout(content_layout, stretch=8)

        # 状态栏
        status_bar = QFrame()
        status_bar.setStyleSheet('''
            QFrame {
                background-color: #f5f5f5;
                border-radius: 8px;
                padding: 10px;
            }
        ''')
        status_layout = QHBoxLayout(status_bar)
        status_layout.setContentsMargins(10, 10, 10, 10)

        self.status_label = QLabel('就绪')
        self.status_label.setStyleSheet('color: #7f8c8d;')
        status_layout.addWidget(self.status_label)

        main_layout.addWidget(status_bar, stretch=0)

        self.setLayout(main_layout)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

    def generate_questions(self):
        subject = self.subject_combo.currentText()
        difficulty = self.difficulty_combo.currentText()
        count = self.count_combo.currentText()
        requirements = self.requirements_text.toPlainText().strip()

        if not requirements:
            QMessageBox.warning(self, '错误', '请输入练习要求！')
            return

        # 构建提示词
        prompt = f"""请根据以下要求生成{count}道{subject}的练习题：

难度级别：{difficulty}
练习要求：{requirements}

要求：
1. 每道题目都要有详细的解答和解析
2. 题目要符合学生的知识水平
3. 题目要覆盖重点知识点
4. 解答要包含解题思路和步骤
5. 对于编程题，要提供完整的代码和注释

请按以下格式输出：
题目1：
[题目内容]

解答：
[详细解答]

解析：
[解题思路和步骤]

题目2：
...

以此类推"""

        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.status_label.setText('正在生成练习题...')

        # QThread + Worker
        self.thread = QThread()
        self.worker = GenerateWorker(self.history, prompt)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.update_practice_ui)
        self.worker.error.connect(self.show_error)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.error.connect(self.thread.quit)
        self.worker.error.connect(self.worker.deleteLater)
        self.thread.start()

    def update_practice_ui(self, response):
        # 创建新的练习框
        practice_frame = QFrame()
        practice_frame.setStyleSheet('''
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                border: 1px solid #e0e0e0;
            }
        ''')
        practice_layout = QVBoxLayout(practice_frame)
        practice_layout.setContentsMargins(15, 15, 15, 15)
        practice_layout.setSpacing(10)

        # 添加时间戳
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        time_label = QLabel(f'生成时间：{timestamp}')
        time_label.setStyleSheet('color: #7f8c8d; font-size: 12px;')
        practice_layout.addWidget(time_label)

        # 添加练习内容
        practice_text = QTextEdit()
        practice_text.setReadOnly(True)
        practice_text.setStyleSheet('''
            QTextEdit {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 4px;
                padding: 8px;
                font-size: 14px;
                font-family: Microsoft YaHei;
            }
        ''')
        practice_text.setText(response)
        practice_layout.addWidget(practice_text)

        # 将练习框添加到练习区域
        self.practice_layout.addWidget(practice_frame)

        self.progress_bar.setVisible(False)
        self.status_label.setText('就绪')

    def show_error(self, error_msg):
        QMessageBox.critical(self, '错误', f'生成练习题失败：{error_msg}')
        self.progress_bar.setVisible(False)
        self.status_label.setText('就绪') 