import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QCheckBox, QMessageBox, QTextEdit, QFileDialog, QListWidget, QListWidgetItem, QSizePolicy
)
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import Qt, QSize
import json

from utils.def_read_file import *
# 大模型API
from Large_Model.QWEN2_5_7B_Instruct_False import QWEN2_5_8B_False_API
from PyQt5.QtWidgets import QSplitter
import os
from datetime import datetime

def get_model_response(prompt, file_path=None):
    return f"模型回复: {prompt}" + (f"（已上传材料：{file_path}）" if file_path else "")

class LoginWindow(QWidget):
    def __init__(self, user_type):
        super().__init__()
        self.user_type = user_type
        self.next_window = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('登录界面')
        self.setWindowIcon(QIcon('Image/UI_images/logo.png'))
        self.resize(400, 400)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        welcome_label = QLabel('欢迎登录')
        welcome_label.setStyleSheet('''
            background-color: #3498db;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 20px;
            font-weight: bold;
        ''')
        welcome_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(welcome_label)

        account_layout = QHBoxLayout()
        account_label = QLabel('账号')
        account_label.setStyleSheet('''
            background-color: #2980b9;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        ''')
        self.account_edit = QLineEdit()
        self.account_edit.setStyleSheet('''
            background-color: white;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        ''')
        account_layout.addWidget(account_label)
        account_layout.addWidget(self.account_edit)
        main_layout.addLayout(account_layout)

        password_layout = QHBoxLayout()
        password_label = QLabel('密码')
        password_label.setStyleSheet('''
            background-color: #2980b9;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        ''')
        self.password_edit = QLineEdit()
        self.password_edit.setStyleSheet('''
            background-color: white;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        ''')
        self.password_edit.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_edit)
        main_layout.addLayout(password_layout)

        option_layout = QHBoxLayout()
        self.remember_account = QCheckBox('记住账号')
        self.remember_account.setStyleSheet('color: white; font-size: 16px;')
        self.remember_password = QCheckBox('记住密码')
        self.remember_password.setStyleSheet('color: white; font-size: 16px;')
        register_button = QPushButton('没有? 点击注册')
        register_button.setStyleSheet('''
            background-color: transparent;
            color: white;
            border: none;
            padding: 5px;
            font-size: 16px;
            text-decoration: underline;
        ''')
        register_button.clicked.connect(self.show_register_window)
        option_layout.addWidget(self.remember_account)
        option_layout.addWidget(self.remember_password)
        option_layout.addWidget(register_button)
        main_layout.addLayout(option_layout)

        login_button = QPushButton('登录')
        login_button.setStyleSheet('''
            background-color: #3498db;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
            min-width: 100px;
        ''')
        login_button.clicked.connect(self.handle_login_click)
        main_layout.addWidget(login_button)

        other_login_label = QLabel('其他登录方式：')
        other_login_label.setStyleSheet('color: red; font-size: 18px;')
        main_layout.addWidget(other_login_label)

        third_party_layout = QHBoxLayout()
        third_party_layout.setSpacing(20)

        widget_qq = QWidget()
        widget_qq.setFixedSize(200, 200)
        layout_qq = QVBoxLayout(widget_qq)
        layout_qq.setContentsMargins(0, 0, 0, 0)
        qq_button = QPushButton()
        qq_button.setIcon(QIcon('Image/UI_images/QQ.png'))
        qq_button.setIconSize(QSize(80, 80))
        qq_button.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0px;
            }
            QPushButton:hover {
                border-radius: 40px;
                background-color: rgba(0, 176, 240, 0.2);
            }
            QPushButton:pressed {
                background-color: rgba(0, 176, 240, 0.4);
            }
        ''')
        qq_button.clicked.connect(self.handle_qq_click)
        layout_qq.addWidget(qq_button)
        third_party_layout.addWidget(widget_qq)

        widget_wechat = QWidget()
        widget_wechat.setFixedSize(200, 200)
        layout_wechat = QVBoxLayout(widget_wechat)
        layout_wechat.setContentsMargins(0, 0, 0, 0)
        wechat_button = QPushButton()
        wechat_button.setIcon(QIcon('Image/UI_images/微信.png'))
        wechat_button.setIconSize(QSize(80, 80))
        wechat_button.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0px;
            }
            QPushButton:hover {
                border-radius: 40px;
                background-color: rgba(37, 211, 102, 0.2);
            }
            QPushButton:pressed {
                background-color: rgba(37, 211, 102, 0.4);
            }
        ''')
        wechat_button.clicked.connect(self.handle_wechat_click)
        layout_wechat.addWidget(wechat_button)
        third_party_layout.addWidget(widget_wechat)

        widget_github = QWidget()
        widget_github.setFixedSize(200, 200)
        layout_github = QVBoxLayout(widget_github)
        layout_github.setContentsMargins(0, 0, 0, 0)
        github_button = QPushButton()
        github_button.setIcon(QIcon('Image/UI_images/github.png'))
        github_button.setIconSize(QSize(80, 80))
        github_button.setStyleSheet('''
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0px;
            }
            QPushButton:hover {
                border-radius: 40px;
                background-color: rgba(51, 51, 51, 0.2);
            }
            QPushButton:pressed {
                background-color: rgba(51, 51, 51, 0.4);
            }
        ''')
        github_button.clicked.connect(self.handle_github_click)
        layout_github.addWidget(github_button)
        third_party_layout.addWidget(widget_github)

        main_layout.addLayout(third_party_layout)

        self.setLayout(main_layout)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(128, 211, 195))
        self.setPalette(palette)

    def show_register_window(self):
        self.register_window = RegisterWindow()
        self.register_window.show()

    def handle_login_click(self):
        account = self.account_edit.text().strip()
        password = self.password_edit.text().strip()
        if not account or not password:
            QMessageBox.warning(self, '输入错误', '账号和密码均不可为空！', QMessageBox.Ok)
            return

        # 登录成功后进入对应端
        if self.user_type == '我是学生':
            self.next_window = StudentWindow()
        elif self.user_type == '我是教师':
            self.next_window = TeacherWindow()
        elif self.user_type == '我是管理员':
            self.next_window = AdminWindow()
        else:
            QMessageBox.warning(self, '登录失败', '未知用户类型！', QMessageBox.Ok)
            return

        self.next_window.show()
        self.close()

    def handle_qq_click(self):
        QMessageBox.information(self, 'QQ登录', '您点击了QQ图标进行登录')

    def handle_wechat_click(self):
        QMessageBox.information(self, '微信登录', '您点击了微信图标进行登录')

    def handle_github_click(self):
        QMessageBox.information(self, 'GitHub登录', '您点击了GitHub图标进行登录')

class RegisterWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('注册界面')
        self.setWindowIcon(QIcon('Image/UI_images/logo.png'))
        self.resize(400, 400)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        welcome_label = QLabel('欢迎注册')
        welcome_label.setStyleSheet('''
            background-color: #2ecc71;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 20px;
            font-weight: bold;
        ''')
        welcome_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(welcome_label)

        account_layout = QHBoxLayout()
        account_label = QLabel('账号')
        account_label.setStyleSheet('''
            background-color: #3498db;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        ''')
        self.account_edit = QLineEdit()
        self.account_edit.setStyleSheet('''
            background-color: white;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        ''')
        account_layout.addWidget(account_label)
        account_layout.addWidget(self.account_edit)
        main_layout.addLayout(account_layout)

        password_layout = QHBoxLayout()
        password_label = QLabel('密码')
        password_label.setStyleSheet('''
            background-color: #3498db;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        ''')
        self.password_edit = QLineEdit()
        self.password_edit.setStyleSheet('''
            background-color: white;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        ''')
        self.password_edit.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_edit)
        main_layout.addLayout(password_layout)

        confirm_password_layout = QHBoxLayout()
        confirm_password_label = QLabel('确认密码')
        confirm_password_label.setStyleSheet('''
            background-color: #3498db;
            color: white;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        ''')
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setStyleSheet('''
            background-color: white;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
        ''')
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)
        confirm_password_layout.addWidget(confirm_password_label)
        confirm_password_layout.addWidget(self.confirm_password_edit)
        main_layout.addLayout(confirm_password_layout)

        register_button = QPushButton('注册')
        register_button.setStyleSheet('''
            background-color: #2ecc71;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            font-size: 16px;
            min-width: 100px;
        ''')
        register_button.clicked.connect(self.register)
        main_layout.addWidget(register_button)

        self.setLayout(main_layout)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(128, 211, 195))
        self.setPalette(palette)

    def register(self):
        password = self.password_edit.text()
        confirm_password = self.confirm_password_edit.text()
        if password != confirm_password:
            QMessageBox.warning(self, '错误', '两次输入的密码不一致，请重新输入')
            return
        QMessageBox.information(self, '成功', '注册成功，请登录')
        self.close()

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('管理端界面')
        self.setWindowIcon(QIcon('Image/UI_images/logo.png'))
        self.resize(800, 600)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        title_label = QLabel('管理端功能面板')
        title_label.setStyleSheet('font-size: 30px; font-weight: bold; color: #2c3e50;')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        button_style = '''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 20px;
                font-size: 20px;
                border-radius: 10px;
                min-width: 400px;
                min-height: 100px;
                font-weight: bold;
                transition: background-color 0.3s;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2471a3;
            }
        '''

        user_btn = QPushButton('用户管理 - 管理员/教师/学生等用户的基本管理')
        user_btn.setStyleSheet(button_style)
        user_btn.clicked.connect(self.show_user_manage)
        main_layout.addWidget(user_btn)

        resource_btn = QPushButton('课件资源管理 - 按学科列表教师备课产生的课件、练习等资源，可以导出')
        resource_btn.setStyleSheet(button_style)
        resource_btn.clicked.connect(self.show_resource_manage)
        main_layout.addWidget(resource_btn)

        overview_btn = QPushButton('大屏概览 - 综合统计信息')
        overview_btn.setStyleSheet(button_style)
        overview_btn.clicked.connect(self.show_overview)
        main_layout.addWidget(overview_btn)

        self.setLayout(main_layout)

    def show_user_manage(self):
        QMessageBox.information(self, '用户管理', '进入用户管理模块，可进行管理员/教师/学生的基本管理操作')

    def show_resource_manage(self):
        QMessageBox.information(self, '课件资源管理', '进入课件资源管理模块，可按学科管理教师备课资源并导出')

    def show_overview(self):
        msg = "大屏概览信息：\n"
        msg += "- 教师使用次数统计/活跃板块(当日/本周)\n"
        msg += "- 学生使用次数统计/活跃板块(当日/本周)\n"
        msg += "- 教学效率指数(备课与修正耗时、课后练习设计与修正耗时、课程优化方向)\n"
        msg += "- 学生学习效果(平均正确率趋势、知识点掌握情况，高频错误知识点等)"
        QMessageBox.information(self, '大屏概览', msg)

class StudentWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.study_helper_window = None
        self.practice_helper_window = None 
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('学生端界面')
        self.setWindowIcon(QIcon('Image/UI_images/logo.png'))
        self.resize(800, 600)

        # 主背景色
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(236, 250, 255))
        self.setPalette(palette)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # 顶部标题区
        title_widget = QWidget()
        title_widget.setStyleSheet('''
            background-color: #3498db;
            border-radius: 12px;
            padding: 24px 0px;
        ''')
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_label = QLabel('欢迎使用学生端功能')
        title_label.setStyleSheet('font-size: 28px; font-weight: bold; color: white; letter-spacing: 2px;')
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)
        main_layout.addWidget(title_widget)

        # 按钮区
        button_widget = QWidget()
        button_widget.setStyleSheet('''
            background: qlineargradient(x1:0, y1:0, x2:1, y2:1,
                                       stop:0 #eaf6ff, stop:1 #d1eaff);
            border-radius: 18px;
        ''')
        button_layout = QVBoxLayout(button_widget)
        button_layout.setContentsMargins(60, 60, 60, 60)
        button_layout.setSpacing(40)

        button_style = '''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 28px 0px;
                font-size: 22px;
                border-radius: 16px;
                min-height: 80px;
                font-weight: bold;
                letter-spacing: 1px;
                box-shadow: 0px 4px 12px rgba(52,152,219,0.08);
                transition: background-color 0.3s;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2471a3;
            }
        '''

        study_btn = QPushButton('📚 在线学习助手')
        study_btn.setStyleSheet(button_style)
        study_btn.setCursor(Qt.PointingHandCursor)
        study_btn.clicked.connect(self.show_study_helper)
        button_layout.addWidget(study_btn)

        practice_btn = QPushButton('📝 实时练习评测助手')
        practice_btn.setStyleSheet(button_style)
        practice_btn.setCursor(Qt.PointingHandCursor)
        practice_btn.clicked.connect(self.show_practice_helper)
        button_layout.addWidget(practice_btn)

        main_layout.addWidget(button_widget, stretch=1)

        # 底部提示
        tip_label = QLabel('Tip: 点击上方功能按钮，体验智能学习与练习！')
        tip_label.setStyleSheet('color: #888; font-size: 15px; margin-top: 20px;')
        tip_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(tip_label, alignment=Qt.AlignBottom)

        self.setLayout(main_layout)

    def show_study_helper(self):
        if self.study_helper_window is None:
            self.study_helper_window = StudyHelperWindow()
            self.study_helper_window.show()
            self.study_helper_window.destroyed.connect(self._on_study_helper_closed)
        elif not self.study_helper_window.isVisible():
            self.study_helper_window.show()
        else:
            self.study_helper_window.activateWindow()
            self.study_helper_window.raise_()

    def _on_study_helper_closed(self):
        self.study_helper_window = None

    def show_practice_helper(self):
        if self.practice_helper_window is None:
            self.practice_helper_window = PracticeHelperWindow()
            self.practice_helper_window.show()
            self.practice_helper_window.destroyed.connect(self._on_practice_helper_closed)
        elif not self.practice_helper_window.isVisible():
            self.practice_helper_window.show()
        else:
            self.practice_helper_window.activateWindow()
            self.practice_helper_window.raise_()

    def _on_practice_helper_closed(self):
        self.practice_helper_window = None

# 实时练习评测助手窗口
class PracticeHelperWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('实时练习评测助手')
        self.setWindowIcon(QIcon('Image/UI_images/logo.png'))
        self.resize(700, 500)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)

        title_label = QLabel('实时练习评测助手')
        title_label.setStyleSheet('font-size: 22px; font-weight: bold; color: #3498db;')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet('''
            font-size: 14px;
            background: #f8f8f8;
            border-radius: 5px;
            padding: 10px;
        ''')
        self.chat_history.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chat_history.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        main_layout.addWidget(self.chat_history, stretch=1)

        input_layout = QHBoxLayout()
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText('请输入您想练习的知识点或题型...')
        self.input_edit.setStyleSheet('''
            font-size: 14px;
            padding: 8px;
            border-radius: 5px;
        ''')
        input_layout.addWidget(self.input_edit, stretch=1)

        send_btn = QPushButton('获取练习题')
        send_btn.setStyleSheet('''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        send_btn.clicked.connect(self.get_practice_question)
        input_layout.addWidget(send_btn)
        main_layout.addLayout(input_layout)

        # 答案输入区
        answer_layout = QHBoxLayout()
        self.answer_edit = QLineEdit()
        self.answer_edit.setPlaceholderText('请输入您的答案...')
        self.answer_edit.setStyleSheet('''
            font-size: 14px;
            padding: 8px;
            border-radius: 5px;
        ''')
        answer_layout.addWidget(self.answer_edit, stretch=1)

        submit_btn = QPushButton('提交答案')
        submit_btn.setStyleSheet('''
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        ''')
        submit_btn.clicked.connect(self.submit_answer)
        answer_layout.addWidget(submit_btn)
        main_layout.addLayout(answer_layout)

        # 支持回车发送
        self.input_edit.returnPressed.connect(self.get_practice_question)
        self.answer_edit.returnPressed.connect(self.submit_answer)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 248, 255))
        self.setPalette(palette)

        self.current_question = None
        self.current_answer = None

    def get_practice_question(self):
        user_input = self.input_edit.text().strip()
        if not user_input:
            self.input_edit.clear()
            return

        self.chat_history.append(f"👤 学生：我想练习：{user_input}\n")
        self.input_edit.clear()
        self.chat_history.append("🤖 智能体：正在为您生成练习题...\n")
        self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())
        QApplication.processEvents()

        # 调用大模型API生成题目和答案
        try:
            response = QWEN2_5_8B_False_API(
                API_key="Bearer sk-zhzgghmjikzcanzkauobxuhcqqwuzrtinaewvuxussxnpcik",
                content=f"请根据以下要求生成一道练习题，并给出标准答案（答案请用【答案】标注）：\n{user_input}"
            )
        except Exception as e:
            response = f"模型调用出错: {e}"

        if hasattr(response, 'status_code') and response.status_code == 200:
            data = json.loads(response.text)
            content = data['choices'][0]['message']['content']
            # 尝试提取题目和答案
            if "【答案】" in content:
                question, answer = content.split("【答案】", 1)
                self.current_question = question.strip()
                self.current_answer = answer.strip()
                self.chat_history.append(f"🤖 智能体：{self.current_question}\n")
            else:
                self.current_question = content.strip()
                self.current_answer = None
                self.chat_history.append(f"🤖 智能体：{self.current_question}\n")
        else:
            self.current_question = None
            self.current_answer = None
            self.chat_history.append(f"🤖 智能体：模型调用失败: {getattr(response, 'status_code', '未知错误')}\n")

        self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())

    def submit_answer(self):
        user_answer = self.answer_edit.text().strip()
        if not user_answer:
            self.answer_edit.clear()
            return

        if not self.current_question:
            self.chat_history.append("⚠️ 请先获取练习题后再提交答案。\n")
            self.answer_edit.clear()
            return

        self.chat_history.append(f"👤 学生答案：{user_answer}\n")
        self.answer_edit.clear()
        self.chat_history.append("🤖 智能体：正在评测您的答案...\n")
        self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())
        QApplication.processEvents()

        # 如果有标准答案，直接比对，否则调用大模型评测
        if self.current_answer:
            # 简单比对（可扩展为更复杂的比对逻辑）
            if user_answer.strip() == self.current_answer.strip():
                self.chat_history.append("✅ 回答正确！\n")
            else:
                self.chat_history.append(f"❌ 回答不正确。\n标准答案：{self.current_answer}\n")
        else:
            # 调用大模型评测
            try:
                prompt = (
                    f"请判断学生对如下题目的答案是否正确，并给出简要点评。\n"
                    f"题目：{self.current_question}\n"
                    f"学生答案：{user_answer}\n"
                )
                response = QWEN2_5_8B_False_API(
                    API_key="Bearer sk-zhzgghmjikzcanzkauobxuhcqqwuzrtinaewvuxussxnpcik",
                    content=prompt
                )
                if hasattr(response, 'status_code') and response.status_code == 200:
                    data = json.loads(response.text)
                    content = data['choices'][0]['message']['content']
                    self.chat_history.append(f"🤖 智能体：{content}\n")
                else:
                    self.chat_history.append(f"🤖 智能体：模型调用失败: {getattr(response, 'status_code', '未知错误')}\n")
            except Exception as e:
                self.chat_history.append(f"🤖 智能体：模型调用出错: {e}\n")

        self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())
        # 清空当前题目和答案，便于下一轮练习
        self.current_question = None
        self.current_answer = None


class StudyHelperWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('在线学习助手')
        self.setWindowIcon(QIcon('Image/UI_images/logo.png'))
        self.resize(700, 500)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)

        title_label = QLabel('在线学习助手')
        title_label.setStyleSheet('font-size: 22px; font-weight: bold; color: #3498db;')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet('''
            font-size: 14px;
            background: #f8f8f8;
            border-radius: 5px;
            padding: 10px;
        ''')
        self.chat_history.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.chat_history.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        main_layout.addWidget(self.chat_history, stretch=1)

        input_layout = QHBoxLayout()
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText('请输入您的学习问题...')
        self.input_edit.setStyleSheet('''
            font-size: 14px;
            padding: 8px;
            border-radius: 5px;
        ''')
        input_layout.addWidget(self.input_edit, stretch=1)

        send_btn = QPushButton('发送')
        send_btn.setStyleSheet('''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(send_btn)
        main_layout.addLayout(input_layout)

        # 支持回车发送
        self.input_edit.returnPressed.connect(self.send_message)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 248, 255))
        self.setPalette(palette)

    def send_message(self):
        user_input = self.input_edit.text().strip()
        if not user_input:
            self.input_edit.clear()
            return

        self.chat_history.append(f"👤 学生：{user_input}\n")
        self.input_edit.clear()
        self.chat_history.append("🤖 智能体：正在思考...\n")
        self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())
        QApplication.processEvents()

        # 调用大模型API
        try:
            response = QWEN2_5_8B_False_API(
                API_key="Bearer sk-zhzgghmjikzcanzkauobxuhcqqwuzrtinaewvuxussxnpcik",
                content=f"你是一个学习助手，请用简明易懂的方式回答学生的问题：\n{user_input}"
            )
        except Exception as e:
            response = f"模型调用出错: {e}"

        if hasattr(response, 'status_code') and response.status_code == 200:
            data = json.loads(response.text)
            content = data['choices'][0]['message']['content']
            self.chat_history.append(f"🤖 智能体：{content}\n")
        else:
            self.chat_history.append(f"🤖 智能体：模型调用失败: {getattr(response, 'status_code', '未知错误')}\n")

        self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())

#================================================================
class ExamGenerateWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('考核内容生成')
        self.setWindowIcon(QIcon('Image/UI_images/logo.png'))
        # 增大初始窗口尺寸
        self.resize(800, 600)  

        # 主布局为水平布局
        main_h_layout = QHBoxLayout(self)
        main_h_layout.setContentsMargins(0, 0, 0, 0)
        main_h_layout.setSpacing(0)

        # 左侧导出按钮区域
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(20, 30, 10, 30)
        left_layout.setSpacing(10)
        
        export_btn = QPushButton('导出')
        export_btn.setStyleSheet('''
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        ''')
        export_btn.clicked.connect(self.export_content)
        left_layout.addWidget(export_btn)
        left_layout.addStretch(1)
        main_h_layout.addWidget(left_widget, stretch=0)

        # 右侧内容区域
        right_widget = QWidget()
        main_layout = QVBoxLayout(right_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)
        main_layout.setSpacing(15)

        # 标题
        title_label = QLabel('考核内容生成助手')
        title_label.setStyleSheet('font-size: 22px; font-weight: bold; color: #3498db;')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 聊天历史记录 - 使用QTextEdit代替QListWidget获得更好的长文本支持
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet('''
            font-size: 14px;
            background: #f8f8f8;
            border-radius: 5px;
            padding: 10px;
        ''')
        # 设置尺寸策略为扩展
        self.chat_history.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 确保垂直滚动条始终显示
        self.chat_history.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        main_layout.addWidget(self.chat_history, stretch=1)

        # 输入区域
        input_layout = QHBoxLayout()
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText('请输入您的考核内容需求...')
        self.input_edit.setStyleSheet('''
            font-size: 14px;
            padding: 8px;
            border-radius: 5px;
        ''')
        input_layout.addWidget(self.input_edit, stretch=1)
        
        send_btn = QPushButton('发送')
        send_btn.setStyleSheet('''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(send_btn)
        main_layout.addLayout(input_layout)

        # 背景色设置
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 248, 255))
        self.setPalette(palette)

        main_h_layout.addWidget(right_widget, stretch=1)

    def send_message(self):
        user_input = self.input_edit.text().strip()
        if not user_input:
            self.input_edit.clear()
            return

        # 显示用户输入
        self.chat_history.append(f"👤 教师：{user_input}\n")
        self.input_edit.clear()
        '''
        # 显示智能体思考状态，此处暂时不需要
        self.chat_history.append("🤖 智能体：正在生成考核内容...")
        self.chat_history.scrollToBottom()
        '''

        # 调用大模型API
        try:
            response = QWEN2_5_8B_False_API(
                API_key="Bearer sk-zhzgghmjikzcanzkauobxuhcqqwuzrtinaewvuxussxnpcik",
                content=f"请根据以下需求生成多样化考核题目及答案,必须有答案：\n{user_input}"
            )
        except Exception as e:
            response = f"模型调用出错: {e}"

        # 处理回复
        if hasattr(response, 'status_code') and response.status_code == 200:
            data = json.loads(response.text)
            content = data['choices'][0]['message']['content']
            # 直接追加智能体回复
            self.chat_history.append(f"🤖 智能体：{content}")
        else:
            self.chat_history.append(f"🤖 智能体：模型调用失败: {getattr(response, 'status_code', '未知错误')}")

        self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())

    def export_content(self):
        export_dir = os.path.join(os.getcwd(), "Ques_and_ask")
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        filename = datetime.now().strftime("exam_%Y%m%d_%H%M%S.md")
        filepath = os.path.join(export_dir, filename)

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(self.chat_history.toPlainText())
            QMessageBox.information(self, "导出成功", f"内容已保存至：\n{filepath}")
        except Exception as e:
            QMessageBox.warning(self, "导出失败", f"保存文件时出错：{e}")

class StudentAnalysisWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.assignment_file = None
        self.student_answers_dir = None
        self.analysis_results = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('学情数据分析')
        self.setWindowIcon(QIcon('Image/UI_images/logo.png'))
        self.resize(1100, 700)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 左侧按钮区
        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)
        left_layout.setContentsMargins(20, 30, 10, 30)
        left_layout.setSpacing(15)

        btn_select_assignment = QPushButton('选择上传作业及答案')
        btn_select_assignment.clicked.connect(self.select_assignment_file)
        btn_cancel_assignment = QPushButton('取消上传作业')
        btn_cancel_assignment.clicked.connect(self.cancel_assignment_file)
        btn_select_student = QPushButton('选择上传学生的答案')
        btn_select_student.clicked.connect(self.select_student_answers_dir)
        btn_cancel_student = QPushButton('取消上传学生的答案')
        btn_cancel_student.clicked.connect(self.cancel_student_answers_dir)

        for btn in [btn_select_assignment, btn_cancel_assignment, btn_select_student, btn_cancel_student]:
            btn.setStyleSheet('''
                QPushButton {
                    background-color: #3498db;
                    color: white;
                    border: none;
                    padding: 12px 18px;
                    border-radius: 8px;
                    font-size: 15px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            ''')
            left_layout.addWidget(btn)
        left_layout.addStretch(1)
        self.assignment_label = QLabel('未选择作业及答案')
        self.assignment_label.setStyleSheet('color: #888; font-size: 13px;')
        left_layout.addWidget(self.assignment_label)
        self.student_dir_label = QLabel('未选择学生答案文件夹')
        self.student_dir_label.setStyleSheet('color: #888; font-size: 13px;')
        left_layout.addWidget(self.student_dir_label)
        left_layout.addStretch(2)
        main_layout.addWidget(left_widget, stretch=0)

        # 中间对话区
        center_widget = QWidget()
        center_layout = QVBoxLayout(center_widget)
        center_layout.setContentsMargins(20, 20, 20, 20)
        center_layout.setSpacing(10)

        chat_label = QLabel('学情分析助手')
        chat_label.setStyleSheet('font-size: 18px; font-weight: bold; color: #3498db;')
        center_layout.addWidget(chat_label)

        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet('font-size: 15px; background: #f8f8f8; border-radius: 5px;')
        self.chat_history.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        center_layout.addWidget(self.chat_history, stretch=1)

        main_layout.addWidget(center_widget, stretch=1)

        # 右侧按钮区
        right_widget = QWidget()
        right_layout = QVBoxLayout(right_widget)
        right_layout.setContentsMargins(10, 30, 20, 30)
        right_layout.setSpacing(20)

        btn_analyse = QPushButton('分析')
        btn_analyse.setStyleSheet('''
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 16px 30px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        ''')
        btn_analyse.clicked.connect(self.analyse_students)

        btn_export = QPushButton('导出')
        btn_export.setStyleSheet('''
            QPushButton {
                background-color: #f09378;
                color: white;
                border: none;
                padding: 16px 30px;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #e67e22;
            }
        ''')
        btn_export.clicked.connect(self.export_results)

        right_layout.addStretch(1)
        right_layout.addWidget(btn_analyse)
        right_layout.addWidget(btn_export)
        right_layout.addStretch(10)
        main_layout.addWidget(right_widget, stretch=0)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 248, 255))
        self.setPalette(palette)

    def select_assignment_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择作业及答案", "", "所有文件 (*.*)")
        if file_path:
            self.assignment_file = file_path
            self.assignment_label.setText(f'已选择作业及答案: {os.path.basename(file_path)}')
        else:
            self.assignment_file = None
            self.assignment_label.setText('未选择作业及答案')

    def cancel_assignment_file(self):
        self.assignment_file = None
        self.assignment_label.setText('未选择作业及答案')

    def select_student_answers_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "选择学生答案文件夹", "")
        if dir_path:
            self.student_answers_dir = dir_path
            self.student_dir_label.setText(f'已选择学生答案文件夹: {dir_path}')
        else:
            self.student_answers_dir = None
            self.student_dir_label.setText('未选择学生答案文件夹')

    def cancel_student_answers_dir(self):
        self.student_answers_dir = None
        self.student_dir_label.setText('未选择学生答案文件夹')

    def analyse_students(self):
        self.chat_history.append("👤 教师：请分析学生作业的知识掌握情况及对错。")
        self.chat_history.append("🤖 智能体：正在分析，请稍候...\n")
        self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())
        QApplication.processEvents()

        if not self.assignment_file or not self.student_answers_dir:
            self.chat_history.append("⚠️ 请先选择作业及答案和学生答案文件夹。")
            return

        assignment_content = read_file_content(self.assignment_file)
        if assignment_content is None:
            self.chat_history.append("⚠️ 作业及答案文件读取失败。")
            return

        results = []
        for fname in os.listdir(self.student_answers_dir):
            fpath = os.path.join(self.student_answers_dir, fname)
            if not os.path.isfile(fpath):
                continue
            student_content = read_file_content(fpath)
            if student_content is None:
                result = f"学生文件 {fname} 读取失败。"
                self.chat_history.append(result)
                results.append(result)
                continue
            prompt = (
                f"请对比以下作业及标准答案和学生的答案，分析学生的知识掌握情况，并判断每题对错，输出简明分析报告。\n"
                f"【作业及标准答案】:\n{assignment_content}\n"
                f"【学生答案】:\n{student_content}\n"
                f"请以“学生：{fname}”开头输出分析结果。"
            )
            try:
                response = QWEN2_5_8B_False_API(
                    API_key="Bearer sk-zhzgghmjikzcanzkauobxuhcqqwuzrtinaewvuxussxnpcik",
                    content=prompt
                )
                if hasattr(response, 'status_code') and response.status_code == 200:
                    data = json.loads(response.text)
                    content = data['choices'][0]['message']['content']
                    self.chat_history.append(f"🤖 智能体：{content}\n")
                    results.append(f"学生：{fname}\n{content}\n")
                else:
                    err = f"学生：{fname} 分析失败: {getattr(response, 'status_code', '未知错误')}"
                    self.chat_history.append(f"🤖 智能体：{err}\n")
                    results.append(err)
            except Exception as e:
                err = f"学生：{fname} 分析出错: {e}"
                self.chat_history.append(f"🤖 智能体：{err}\n")
                results.append(err)
            self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())
            QApplication.processEvents()
        self.analysis_results = "\n".join(results)

    def export_results(self):
        if not self.analysis_results.strip():
            QMessageBox.warning(self, "导出失败", "没有可导出的分析结果，请先进行分析。")
            return
        export_dir = os.path.join(os.getcwd(), "Results", "Student_analyse")
        if not os.path.exists(export_dir):
            os.makedirs(export_dir)
        filename = datetime.now().strftime("student_analysis_%Y%m%d_%H%M%S.md")
        filepath = os.path.join(export_dir, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(self.analysis_results)
            QMessageBox.information(self, "导出成功", f"分析结果已保存至：\n{filepath}")
        except Exception as e:
            QMessageBox.warning(self, "导出失败", f"保存文件时出错：{e}")

class TeacherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.prepare_design_window = None
        self.exam_generate_window = None
        self.student_analysis_window = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('教师端界面')
        self.setWindowIcon(QIcon('Image/UI_images/logo.png'))
        self.resize(800, 600)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        title_label = QLabel('教师端功能面板')
        title_label.setStyleSheet('font-size: 28px; font-weight: bold; color: #2c3e50;')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        button_style = '''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 20px;
                font-size: 18px;
                border-radius: 10px;
                min-width: 350px;
                min-height: 100px;
                font-weight: bold;
                transition: background-color 0.3s;
                text-align: left;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2471a3;
            }
        '''

        prepare_btn = QPushButton('备课与设计 - 根据课程大纲自动设计教学内容（知识讲解、实训练习等）')
        prepare_btn.setStyleSheet(button_style)
        prepare_btn.clicked.connect(self.show_prepare_design)
        main_layout.addWidget(prepare_btn)

        exam_btn = QPushButton('考核内容生成 - 按教学内容生成多样化考核题目及答案')
        exam_btn.setStyleSheet(button_style)
        exam_btn.clicked.connect(self.show_exam_generate)
        main_layout.addWidget(exam_btn)

        analysis_btn = QPushButton('学情数据分析 - 自动化检测答案，分析学生知识掌握情况')
        analysis_btn.setStyleSheet(button_style)
        analysis_btn.clicked.connect(self.show_analysis)
        main_layout.addWidget(analysis_btn)

        self.setLayout(main_layout)

    def show_prepare_design(self):
        if self.prepare_design_window is None or not self.prepare_design_window.isVisible():
            self.prepare_design_window = PrepareDesignWindow()
            self.prepare_design_window.show()
        else:
            self.prepare_design_window.activateWindow()
            self.prepare_design_window.raise_()

    def show_exam_generate(self):
        if self.exam_generate_window is None or not self.exam_generate_window.isVisible():
            self.exam_generate_window = ExamGenerateWindow()
            self.exam_generate_window.setAttribute(Qt.WA_DeleteOnClose, False)
            self.exam_generate_window.closeEvent = self._exam_generate_close_event
            self.exam_generate_window.show()
        else:
            self.exam_generate_window.activateWindow()
            self.exam_generate_window.raise_()

    def _exam_generate_close_event(self, event):
        self.exam_generate_window.hide()
        event.ignore()

    def show_analysis(self):
        if self.student_analysis_window is None or not self.student_analysis_window.isVisible():
            self.student_analysis_window = StudentAnalysisWindow()
            self.student_analysis_window.show()
        else:
            self.student_analysis_window.activateWindow()
            self.student_analysis_window.raise_()

class PrepareDesignWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('备课与设计功能面板')
        self.setWindowIcon(QIcon('Image/UI_images/logo.png'))
        self.resize(1000, 700)

        # 使用 QSplitter 实现可拖动分隔
        splitter = QSplitter(Qt.Horizontal, self)
        splitter.setStyleSheet("QSplitter::handle { background-color: gray;}")  # 设置分割线为灰色

        # 左侧：文件上传面板
        left_widget = QWidget()
        left_panel = QVBoxLayout(left_widget)
        left_panel.setSpacing(20)
        left_panel.setContentsMargins(20, 20, 20, 20)

        file_label = QLabel('上传备课材料')
        file_label.setStyleSheet('font-size: 18px; font-weight: bold; color: #2c3e50;')
        left_panel.addWidget(file_label)

        self.file_info_label = QLabel('未选择文件')
        self.file_info_label.setStyleSheet('color: #888; font-size: 14px;')
        left_panel.addWidget(self.file_info_label)

        upload_btn = QPushButton('选择文件')
        upload_btn.setStyleSheet('''
            QPushButton {
                background-color: #27ae60;
                color: white;
                border: none;
                padding: 10px 10px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #229954;
            }
        ''')
        upload_btn.clicked.connect(self.select_file)
        left_panel.addWidget(upload_btn)

        # 新增取消文件按钮
        cancel_btn = QPushButton('取消文件')
        cancel_btn.setStyleSheet('''
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                padding: 10px 10px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        ''')
        cancel_btn.clicked.connect(self.cancel_file)
        left_panel.addWidget(cancel_btn)

        left_panel.addStretch(1)

        # 中间：对话面板
        center_widget = QWidget()
        center_panel = QVBoxLayout(center_widget)
        center_panel.setSpacing(10)
        center_panel.setContentsMargins(20, 20, 20, 20)

        chat_label = QLabel('备课小助手')
        chat_label.setStyleSheet('font-size: 18px; font-weight: bold; color: #3498db;')
        center_panel.addWidget(chat_label)

        # 使用 QTextEdit 替换 QListWidget 以支持长文本和自动换行
        self.chat_history = QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setStyleSheet('font-size: 15px; background: #f8f8f8; border-radius: 5px;')
        self.chat_history.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        center_panel.addWidget(self.chat_history, stretch=1)

        input_layout = QHBoxLayout()
        self.input_edit = QLineEdit()
        self.input_edit.setPlaceholderText('请输入您的问题...')
        self.input_edit.setStyleSheet('font-size: 16px; padding: 8px; border-radius: 5px;')
        input_layout.addWidget(self.input_edit, stretch=1)
        send_btn = QPushButton('发送')
        send_btn.setStyleSheet('''
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(send_btn)
        center_panel.addLayout(input_layout)

        # 支持回车发送
        self.input_edit.returnPressed.connect(self.send_message)

        # 将左右面板加入splitter
        splitter.addWidget(left_widget)
        splitter.addWidget(center_widget)
        splitter.setSizes([250, 750])  # 初始宽度比例，可根据需要调整

        # 主布局
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(splitter)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 248, 255))
        self.setPalette(palette)

    def select_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择备课材料", "", "所有文件 (*.*)")
        if file_path:
            self.file_path = file_path
            self.file_info_label.setText(f'已选择文件: {file_path}')
        else:
            self.file_path = None
            self.file_info_label.setText('未选择文件')

    def cancel_file(self):
        self.file_path = None
        self.file_info_label.setText('未选择文件')

    def send_message(self):
        user_input = self.input_edit.text().strip()
        if not user_input:
            self.input_edit.clear()
            return

        user_file = None
        if self.file_path is not None:
            file_content = read_file_content(self.file_path)
            if file_content is None:
                print("文件读取失败，程序退出")
                return
            # 获取文件基本信息
            file_size = os.path.getsize(self.file_path)
            file_info = f"文件名: {os.path.basename(self.file_path)}\n文件大小: {file_size} 字节"
            # 构建问题，包含文件信息
            user_input_full = f"请分析以下文件内容:\n\n{file_info}\n\n{file_content}"
            user_say = f"请分析以下文件内容:\n\n{file_info}"
            user_file = f"已上传材料：{self.file_path}"
        else:
            user_input_full = user_input
            user_say = user_input

        # 显示用户输入
        self.chat_history.append(f"👤 教师：{user_say}")
        self.input_edit.clear()
        self.chat_history.append("🤖 智能体：正在思考...")
        self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())

        # 调用大模型API
        try:
            response = QWEN2_5_8B_False_API(API_key="Bearer sk-zhzgghmjikzcanzkauobxuhcqqwuzrtinaewvuxussxnpcik",
                                            content=user_input_full)
        except Exception as e:
            response = f"模型调用出错: {e}"

        # 回复切片
        if hasattr(response, 'status_code') and response.status_code == 200:
            data = json.loads(response.text)
            content = data['choices'][0]['message']['content']
            # 显示模型回复
            if user_file:
                print(user_file)
            self.chat_history.append(f"🤖 智能体：{content}")
            self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())
        else:
            print("模型调用失败:", getattr(response, 'status_code', '未知错误'))
            self.chat_history.append(f"🤖 智能体：模型调用失败: {getattr(response, 'status_code', '未知错误')}")
            self.chat_history.verticalScrollBar().setValue(self.chat_history.verticalScrollBar().maximum())
#==================================================

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.child_windows = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('基于开源AI大模型的教学实训智能体平台')
        self.setWindowIcon(QIcon('Image/UI_images/logo.png'))
        self.resize(800, 600)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title_widget = QWidget()
        title_widget.setStyleSheet('''
            background-color: #3498db;
            color: white;
            border-radius: 10px;
            padding: 20px;
            font-weight: bold;
        ''')
        title_layout = QVBoxLayout(title_widget)
        title_layout.setContentsMargins(0, 0, 0, 0)
        welcome_label = QLabel('欢迎使用基于开源AI大模型的教学实训智能体平台')
        welcome_label.setAlignment(Qt.AlignCenter)
        welcome_label.setStyleSheet('font-size: 24px; background: transparent;')
        title_layout.addWidget(welcome_label)
        main_layout.addWidget(title_widget, alignment=Qt.AlignTop)

        button_layout = QHBoxLayout()
        button_layout.setSpacing(30)
        button_stylesheet = '''
            QPushButton {
                background-color: #f09378;
                color: white;
                border: none;
                padding: 20px;
                font-size: 18px;
                border-radius: 10px;
                min-width: 180px;
                min-height: 120px;
                font-weight: bold;
                border-bottom: 4px solid #b36b50;
                border-right: 2px solid #b36b50;
            }
            QPushButton:hover {
                background-color: #e74c3c;
            }
            QPushButton:pressed {
                border-bottom: 2px solid #b36b50;
                border-right: 1px solid #b36b50;
            }
        '''
        teacher_button = QPushButton('我是教师')
        teacher_button.setStyleSheet(button_stylesheet)
        teacher_button.clicked.connect(lambda: self.show_login_window('我是教师'))

        student_button = QPushButton('我是学生')
        student_button.setStyleSheet(button_stylesheet)
        student_button.clicked.connect(lambda: self.show_login_window('我是学生'))

        admin_button = QPushButton('我是管理员')
        admin_button.setStyleSheet(button_stylesheet)
        admin_button.clicked.connect(lambda: self.show_login_window('我是管理员'))

        button_layout.addWidget(teacher_button)
        button_layout.addWidget(student_button)
        button_layout.addWidget(admin_button)
        button_layout.setAlignment(Qt.AlignHCenter)

        spacer_widget = QWidget()
        main_layout.addWidget(spacer_widget, stretch=1)
        main_layout.addLayout(button_layout)
        main_layout.addWidget(spacer_widget, stretch=1)

        question_button = QPushButton('我有问题?')
        question_button.setStyleSheet('''
            QPushButton {
                background-color: white;
                color: #333;
                border: 1px solid #ccc;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 5px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #f4f4f4;
                border-color: #aaa;
            }
            QPushButton:pressed {
                background-color: #eaeaea;
            }
        ''')
        main_layout.addWidget(question_button, alignment=Qt.AlignRight | Qt.AlignBottom)

        self.setLayout(main_layout)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(48, 108, 177))
        self.setPalette(palette)

    def show_login_window(self, user_type):
        login_window = LoginWindow(user_type)
        self.child_windows.append(login_window)
        login_window.show()

    def closeEvent(self, event):
        for window in self.child_windows:
            window.close()
        event.accept()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
