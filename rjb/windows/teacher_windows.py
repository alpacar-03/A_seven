from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QSplitter, QTextEdit, QLineEdit, QFileDialog, QMessageBox,
    QFrame, QSizePolicy, QProgressBar, QApplication, QComboBox, QSpinBox
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt, QTimer, QThread, pyqtSignal, QObject
from datetime import datetime
import os

from rjb.styles.theme import Theme
from rjb.utils.file_utils import read_file_content
from rjb.Large_Model.DeepSeek import Deepseek_API

class TeacherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.prepare_design_window = None
        self.student_analysis_window = None
        self.exam_generation_window = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('教师端界面')
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
        title_label = QLabel('教师备课中心')
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
        subtitle_label = QLabel('智能备课 & 教学设计')
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

        # 只保留已实现的"备课与设计"按钮
        prepare_btn = self.create_feature_button(
            '备课与设计',
            '📝',
            '课程大纲 | 教学内容 | 实训设计',
            '#3498db'
        )
        prepare_btn.clicked.connect(self.show_prepare_design)
        button_layout.addWidget(prepare_btn)

        # 添加考核内容生成按钮
        exam_btn = self.create_feature_button(
            '考核内容生成',
            '📋',
            '自动生成考核题目 | 参考答案 | 多样化题型',
            '#e74c3c'
        )
        exam_btn.clicked.connect(self.show_exam_generation)
        button_layout.addWidget(exam_btn)

        main_layout.addWidget(button_frame)

        # 设置主布局
        self.setLayout(main_layout)

        # 设置窗口背景色
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))  # #f0f0f0
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

    def show_prepare_design(self):
        if self.prepare_design_window is None or not self.prepare_design_window.isVisible():
            self.prepare_design_window = PrepareDesignWindow()
            self.prepare_design_window.show()
        else:
            self.prepare_design_window.activateWindow()
            self.prepare_design_window.raise_()

    def show_exam_generation(self):
        if self.exam_generation_window is None or not self.exam_generation_window.isVisible():
            self.exam_generation_window = ExamGenerationWindow()
            self.exam_generation_window.show()
        else:
            self.exam_generation_window.activateWindow()
            self.exam_generation_window.raise_()


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
            formatted_response = f'[{current_time}] 课件生成结果：\n{response}\n\n'
            self.finished.emit(formatted_response)
        except Exception as e:
            self.error.emit(str(e))

class PrepareDesignWindow(QWidget):
    messages = []
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.init_ui()
        self.thread = None  # For QThread
        self.worker = None  # For worker instance

    def init_ui(self):
        self.setWindowTitle('备课与教学设计')
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

        title_label = QLabel('备课与教学设计')
        title_label.setStyleSheet('''
            color: white;
            font-size: 28px;
            font-weight: bold;
            font-family: Microsoft YaHei;
            letter-spacing: 2px;
        ''')
        title_label.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(title_label)

        subtitle_label = QLabel('基于大模型的智能备课助手')
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

        # 左侧文件选择和输入区域
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

        file_layout = QHBoxLayout()
        self.file_label = QLabel('未选择文件')
        self.file_label.setStyleSheet('color: #7f8c8d;')
        file_layout.addWidget(self.file_label)

        select_file_btn = QPushButton('选择文件')
        select_file_btn.setStyleSheet(Theme.BUTTON_STYLE)
        select_file_btn.clicked.connect(self.select_file)
        file_layout.addWidget(select_file_btn)

        cancel_file_btn = QPushButton('取消选择')
        cancel_file_btn.setStyleSheet(Theme.BUTTON_STYLE)
        cancel_file_btn.clicked.connect(self.cancel_file)
        file_layout.addWidget(cancel_file_btn)

        left_layout.addLayout(file_layout)

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
        self.input_text.setPlaceholderText('请输入备课需求（如：课程主题、教学目标、教学重难点、课时安排等）...')
        left_layout.addWidget(self.input_text, stretch=2)

        send_btn = QPushButton('生成教案')
        send_btn.setStyleSheet(Theme.BUTTON_STYLE)
        send_btn.clicked.connect(self.send_message)
        self.send_button = send_btn  # Store reference to the button
        left_layout.addWidget(send_btn)

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

        # 添加输出区域标题
        output_title = QLabel('教案生成结果')
        output_title.setStyleSheet('''
            color: #2c3e50;
            font-size: 18px;
            font-weight: bold;
            font-family: Microsoft YaHei;
            padding: 10px 0;
        ''')
        right_layout.addWidget(output_title)

        self.output_text = QTextEdit()
        self.output_text.setStyleSheet('''
            QTextEdit {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-family: Microsoft YaHei;
            }
        ''')
        self.output_text.setReadOnly(True)
        right_layout.addWidget(self.output_text, stretch=3)

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
                background-color: #3498db;
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
        palette.setColor(QPalette.Window, QColor(240, 240, 240))  # #f0f0f0
        self.setPalette(palette)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '选择文件', '', 'Text Files (*.txt);;All Files (*)')
        if file_path:
            self.file_path = file_path
            self.file_label.setText(os.path.basename(file_path))
            content = read_file_content(file_path)
            if content:
                self.input_text.setText(content)

    def cancel_file(self):
        self.file_path = None
        self.file_label.setText('未选择文件')
        self.input_text.clear()

    def send_message(self):
        content = self.input_text.toPlainText().strip()
        if not content:
            QMessageBox.warning(self, '错误', '请输入备课需求！')
            return

        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.send_button.setEnabled(False)
        self.status_label.setText('正在生成教案...')

        # QThread + Worker
        self.thread = QThread()
        self.worker = GenerateWorker(self.messages, content)
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
        current_text = self.output_text.toPlainText()
        if current_text:
            self.output_text.setText(current_text + "\n" + response)
        else:
            self.output_text.setText(response)
        self.progress_bar.setVisible(False)
        self.send_button.setEnabled(True)
        self.status_label.setText('就绪')

    def show_error(self, error_msg):
        QMessageBox.critical(self, '错误', f'生成教案失败：{error_msg}')
        self.progress_bar.setVisible(False)
        self.send_button.setEnabled(True)
        self.status_label.setText('就绪')

class ExamGenerationWindow(QWidget):
    messages = []
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.thread = None
        self.worker = None

    def init_ui(self):
        self.setWindowTitle('考核内容生成')
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

        title_label = QLabel('考核内容生成')
        title_label.setStyleSheet('''
            color: white;
            font-size: 28px;
            font-weight: bold;
            font-family: Microsoft YaHei;
            letter-spacing: 2px;
        ''')
        title_label.setAlignment(Qt.AlignCenter)
        nav_layout.addWidget(title_label)

        subtitle_label = QLabel('基于大模型的智能考核生成')
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
        subject_label = QLabel('学科类型：')
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

        # 题型选择
        type_layout = QHBoxLayout()
        type_label = QLabel('题型选择：')
        type_label.setStyleSheet('font-size: 14px; font-weight: bold;')
        self.type_combo = QComboBox()
        self.type_combo.addItems(['选择题', '填空题', '简答题', '编程题', '综合题'])
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

        # 题目数量
        count_layout = QHBoxLayout()
        count_label = QLabel('题目数量：')
        count_label.setStyleSheet('font-size: 14px; font-weight: bold;')
        self.count_spin = QSpinBox()
        self.count_spin.setRange(1, 20)
        self.count_spin.setValue(5)
        self.count_spin.setStyleSheet('''
            QSpinBox {
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 5px;
                min-width: 100px;
            }
        ''')
        count_layout.addWidget(count_label)
        count_layout.addWidget(self.count_spin)
        count_layout.addStretch()
        left_layout.addLayout(count_layout)

        # 教学内容输入
        content_label = QLabel('教学内容：')
        content_label.setStyleSheet('font-size: 14px; font-weight: bold;')
        left_layout.addWidget(content_label)

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
        self.input_text.setPlaceholderText('请输入教学内容（如：课程主题、知识点、重点难点等）...')
        left_layout.addWidget(self.input_text, stretch=2)

        generate_btn = QPushButton('生成考核内容')
        generate_btn.setStyleSheet(Theme.BUTTON_STYLE)
        generate_btn.clicked.connect(self.generate_exam)
        self.generate_button = generate_btn
        left_layout.addWidget(generate_btn)

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

        output_title = QLabel('考核内容生成结果')
        output_title.setStyleSheet('''
            color: #2c3e50;
            font-size: 18px;
            font-weight: bold;
            font-family: Microsoft YaHei;
            padding: 10px 0;
        ''')
        right_layout.addWidget(output_title)

        self.output_text = QTextEdit()
        self.output_text.setStyleSheet('''
            QTextEdit {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-family: Microsoft YaHei;
            }
        ''')
        self.output_text.setReadOnly(True)
        right_layout.addWidget(self.output_text, stretch=3)

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

    def generate_exam(self):
        content = self.input_text.toPlainText().strip()
        if not content:
            QMessageBox.warning(self, '错误', '请输入教学内容！')
            return

        # 构建提示词
        subject = self.subject_combo.currentText()
        question_type = self.type_combo.currentText()
        question_count = self.count_spin.value()
        
        prompt = f"""请根据以下教学内容，生成{question_count}道{subject}的{question_type}，并附带参考答案。

教学内容：
{content}

要求：
1. 题目难度适中，符合教学进度
2. 每道题都要有详细的参考答案
3. 如果是编程题，请提供完整的代码和注释
4. 题目要覆盖教学重点和难点
5. 答案要准确、详细、易于理解

请按以下格式输出：
题目1：
[题目内容]

参考答案：
[详细答案]

题目2：
[题目内容]

参考答案：
[详细答案]

...以此类推"""

        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.generate_button.setEnabled(False)
        self.status_label.setText('正在生成考核内容...')

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
        current_text = self.output_text.toPlainText()
        if current_text:
            self.output_text.setText(current_text + "\n" + response)
        else:
            self.output_text.setText(response)
        self.progress_bar.setVisible(False)
        self.generate_button.setEnabled(True)
        self.status_label.setText('就绪')

    def show_error(self, error_msg):
        QMessageBox.critical(self, '错误', f'生成考核内容失败：{error_msg}')
        self.progress_bar.setVisible(False)
        self.generate_button.setEnabled(True)
        self.status_label.setText('就绪') 