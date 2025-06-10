from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QTextEdit, QLineEdit, QMessageBox, QFrame, QSizePolicy
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt
from datetime import datetime

from rjb.styles.theme import Theme

class StudentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.study_helper_window = None
        self.practice_helper_window = None
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
                background-color: #3498db;
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
        subtitle_label = QLabel('智能学习助手 & 实时练习评测')
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
                    stop:0 #eaf6ff, stop:1 #d1eaff);
                border-radius: 18px;
            }
        ''')
        button_layout = QVBoxLayout(button_frame)
        button_layout.setContentsMargins(60, 60, 60, 60)
        button_layout.setSpacing(40)

        # 在线学习助手按钮
        study_btn = self.create_feature_button(
            '在线学习助手',
            '📚',
            '智能问答 | 知识解析 | 学习规划',
            '#4CAF50'
        )
        study_btn.clicked.connect(self.show_study_helper)
        button_layout.addWidget(study_btn)

        # 实时练习评测助手按钮
        practice_btn = self.create_feature_button(
            '实时练习评测助手',
            '✍',
            '练习生成 | 实时评测 | 错题分析',
            '#FF5722'
        )
        practice_btn.clicked.connect(self.show_practice_helper)
        button_layout.addWidget(practice_btn)

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

    def show_study_helper(self):
        if not self.study_helper_window:
            self.study_helper_window = StudyHelperWindow()
        self.study_helper_window.show()

    def show_practice_helper(self):
        if not self.practice_helper_window:
            self.practice_helper_window = StudyHelperWindow()  # 暂时使用学习助手窗口
        self.practice_helper_window.show()

# 学习助手窗口
class StudyHelperWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('学习助手')
        self.resize(1200, 800)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title_label = QLabel('基于大模型的学习辅导')
        title_label.setFont(QFont('Microsoft YaHei', 24, QFont.Bold))
        title_label.setStyleSheet('color: #2c3e50;')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        self.input_text = QTextEdit()
        self.input_text.setFont(QFont('Microsoft YaHei', 14))
        self.input_text.setStyleSheet('''
            QTextEdit {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
            }
            QTextEdit:focus {
                border-color: #3498db;
            }
        ''')
        self.input_text.setPlaceholderText('请输入您的学习问题...')
        main_layout.addWidget(self.input_text)

        send_btn = QPushButton('发送')
        send_btn.setFont(QFont('Microsoft YaHei', 14, QFont.Bold))
        send_btn.setStyleSheet(Theme.BUTTON_STYLE)
        send_btn.clicked.connect(self.send_message)
        main_layout.addWidget(send_btn)

        self.output_text = QTextEdit()
        self.output_text.setFont(QFont('Microsoft YaHei', 14))
        self.output_text.setStyleSheet('''
            QTextEdit {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
            }
        ''')
        self.output_text.setReadOnly(True)
        main_layout.addWidget(self.output_text)

        self.setLayout(main_layout)

        # 设置窗口背景
        self.setStyleSheet('''
            QWidget {
                background-color: #f0f0f0;
            }
        ''')

    def send_message(self):
        user_input = self.input_text.toPlainText().strip()
        if not user_input:
            return

        # 添加用户输入到输出区域
        current_time = datetime.now().strftime('%H:%M:%S')
        self.output_text.append(f'[{current_time}] 我: {user_input}\n')

        # 这里应该添加实际的AI响应逻辑
        ai_response = "这是一个示例回复。在实际应用中，这里应该是AI模型的响应。"
        self.output_text.append(f'[{current_time}] AI助手: {ai_response}\n\n')

        # 清空输入框
        self.input_text.clear() 