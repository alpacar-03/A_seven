from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QCheckBox, QMessageBox, QFrame, QSizePolicy,
    QFormLayout
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt

from rjb.styles.theme import Theme
from rjb.utils.db_utils import DatabaseManager
from rjb.windows.teacher_windows import TeacherWindow
from rjb.windows.student_windows import StudentWindow
from rjb.windows.admin_windows import AdminWindow

class LoginWindow(QWidget):
    def __init__(self, user_type):
        super().__init__()
        self.user_type = user_type
        self.next_window = None
        self.db_manager = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        # 设置窗口标题
        role_titles = {
            "teacher": "教师登录",
            "student": "学生登录",
            "admin": "管理员登录"
        }
        self.setWindowTitle(role_titles.get(self.user_type, "用户登录"))
        self.resize(400, 500)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # 欢迎标题
        welcome_label = QLabel(f'欢迎{role_titles.get(self.user_type, "登录")}')
        welcome_label.setStyleSheet('''
            background-color: #e91e63;
            color: white;
            padding: 20px;
            border-radius: 12px;
            font-size: 24px;
            font-family: Microsoft YaHei;
            font-weight: bold;
            text-align: center;
        ''')
        welcome_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(welcome_label)

        # 创建表单布局
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # 用户名输入
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("请输入用户名")
        self.username_edit.setStyleSheet(Theme.INPUT_STYLE)
        form_layout.addRow("用户名:", self.username_edit)

        # 密码输入
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("请输入密码")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setStyleSheet(Theme.INPUT_STYLE)
        form_layout.addRow("密码:", self.password_edit)

        # 添加表单到主布局
        main_layout.addLayout(form_layout)

        # 按钮容器
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setSpacing(20)

        # 登录按钮
        login_button = QPushButton('登录')
        login_button.setStyleSheet(Theme.BUTTON_STYLE)
        login_button.clicked.connect(self.handle_login)
        button_layout.addWidget(login_button)

        # 注册按钮
        register_button = QPushButton('注册')
        register_button.setStyleSheet(Theme.BUTTON_STYLE)
        register_button.clicked.connect(self.show_register_window)
        button_layout.addWidget(register_button)

        main_layout.addWidget(button_container)
        self.setLayout(main_layout)

        # 设置窗口背景色
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

    def handle_login(self):
        """处理登录逻辑"""
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()

        if not username or not password:
            QMessageBox.warning(self, '错误', '请输入用户名和密码！')
            return

        # 验证用户
        success, message = self.db_manager.verify_user(username, password, self.user_type)
        if success:
            QMessageBox.information(self, '成功', '登录成功！')
            self.open_main_window()
        else:
            QMessageBox.warning(self, '错误', message)

    def show_register_window(self):
        """显示注册窗口"""
        self.register_window = RegisterWindow(self.user_type)
        self.register_window.show()

    def open_main_window(self):
        """打开对应的主窗口"""
        if self.user_type == "teacher":
            self.next_window = TeacherWindow()
        elif self.user_type == "student":
            self.next_window = StudentWindow()
        elif self.user_type == "admin":
            self.next_window = AdminWindow()
        
        if self.next_window:
            self.next_window.show()
            self.close()

class RegisterWindow(QWidget):
    def __init__(self, user_type):
        super().__init__()
        self.user_type = user_type
        self.db_manager = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('用户注册')
        self.resize(400, 600)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(20)

        # 标题
        title_label = QLabel('新用户注册')
        title_label.setStyleSheet('''
            background-color: #2ecc71;
            color: white;
            padding: 20px;
            border-radius: 12px;
            font-size: 24px;
            font-family: Microsoft YaHei;
            font-weight: bold;
        ''')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 创建表单布局
        form_layout = QFormLayout()
        form_layout.setSpacing(15)

        # 用户名输入
        self.username_edit = QLineEdit()
        self.username_edit.setPlaceholderText("请输入用户名")
        self.username_edit.setStyleSheet(Theme.INPUT_STYLE)
        form_layout.addRow("用户名:", self.username_edit)

        # 密码输入
        self.password_edit = QLineEdit()
        self.password_edit.setPlaceholderText("请输入密码")
        self.password_edit.setEchoMode(QLineEdit.Password)
        self.password_edit.setStyleSheet(Theme.INPUT_STYLE)
        form_layout.addRow("密码:", self.password_edit)

        # 确认密码
        self.confirm_password_edit = QLineEdit()
        self.confirm_password_edit.setPlaceholderText("请再次输入密码")
        self.confirm_password_edit.setEchoMode(QLineEdit.Password)
        self.confirm_password_edit.setStyleSheet(Theme.INPUT_STYLE)
        form_layout.addRow("确认密码:", self.confirm_password_edit)

        # 姓名
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("请输入姓名")
        self.name_edit.setStyleSheet(Theme.INPUT_STYLE)
        form_layout.addRow("姓名:", self.name_edit)

        # 邮箱
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("请输入邮箱")
        self.email_edit.setStyleSheet(Theme.INPUT_STYLE)
        form_layout.addRow("邮箱:", self.email_edit)

        main_layout.addLayout(form_layout)

        # 注册按钮
        register_button = QPushButton('注册')
        register_button.setStyleSheet(Theme.BUTTON_STYLE)
        register_button.clicked.connect(self.handle_register)
        main_layout.addWidget(register_button)

        self.setLayout(main_layout)

        # 设置窗口背景
        self.setStyleSheet('''
            QWidget {
                background-color: #f0f0f0;
            }
        ''')

    def handle_register(self):
        """处理注册逻辑"""
        # 获取输入
        username = self.username_edit.text().strip()
        password = self.password_edit.text().strip()
        confirm_password = self.confirm_password_edit.text().strip()
        name = self.name_edit.text().strip()
        email = self.email_edit.text().strip()

        # 验证输入
        if not username or not password or not confirm_password:
            QMessageBox.warning(self, '错误', '请填写必要信息！')
            return

        if password != confirm_password:
            QMessageBox.warning(self, '错误', '两次输入的密码不一致！')
            return

        # 注册用户
        success, message = self.db_manager.register_user(
            username, password, self.user_type, name, email
        )

        if success:
            QMessageBox.information(self, '成功', '注册成功！')
            self.close()
        else:
            QMessageBox.warning(self, '错误', message) 