import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFrame, QSizePolicy, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QPalette, QColor, QFont, QPainter, QLinearGradient, QGradient
from PyQt5.QtCore import Qt, QPropertyAnimation, QRect, QEasingCurve, QPoint

from rjb.windows.auth_windows import LoginWindow
from rjb.windows.teacher_windows import TeacherWindow
from rjb.windows.student_windows import StudentWindow
from rjb.windows.admin_windows import AdminWindow

class GlassFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("GlassFrame")

class IconButton(QPushButton):
    def __init__(self, title, description, button_name, parent=None):
        super().__init__(parent)
        self.setFixedSize(220, 260)
        self.setObjectName(button_name)
        
        # 创建主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # 图标容器
        icon_container = QFrame(self)
        icon_container.setFixedSize(90, 90)
        icon_container.setStyleSheet('''
            QFrame {
                background-color: rgba(255, 192, 203, 0.3);
                border-radius: 45px;
            }
        ''')
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(20, 20, 20, 20)
        
        # 图标标签 - 使用文字替代图片
        icon_label = QLabel(title[0])  # 使用标题的第一个字作为图标
        icon_label.setFixedSize(50, 50)
        icon_label.setAlignment(Qt.AlignCenter)
        icon_label.setStyleSheet('''
            QLabel {
                color: #FF69B4;
                font-size: 24px;
                font-weight: bold;
                background-color: rgba(255, 192, 203, 0.2);
                border-radius: 25px;
            }
        ''')
        
        icon_layout.addWidget(icon_label)
        layout.addWidget(icon_container, 0, Qt.AlignCenter)
        
        # 标题
        title_label = QLabel(title)
        title_label.setFont(QFont('Microsoft YaHei', 16, QFont.Bold))
        title_label.setStyleSheet('color: #2c3e50;')
        title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(title_label)
        
        # 描述
        desc_label = QLabel(description)
        desc_label.setFont(QFont('Microsoft YaHei', 11))
        desc_label.setStyleSheet('color: #7f8c8d;')
        desc_label.setAlignment(Qt.AlignCenter)
        desc_label.setWordWrap(True)
        layout.addWidget(desc_label)
        
        self.setStyleSheet('''
            IconButton {
                background-color: white;
                border: 1px solid #e0e0e0;
                border-radius: 15px;
            }
            IconButton:hover {
                background-color: #f5f5f5;
                border: 1px solid #d0d0d0;
            }
            IconButton:pressed {
                background-color: #e0e0e0;
            }
        ''')

class RoleButton(QPushButton):
    def __init__(self, title, color, parent=None):
        super().__init__(parent)
        self.setFixedSize(240, 320)
        self.color = color
        self.is_hovered = False
        
        # 创建主布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 30, 20, 30)
        layout.setSpacing(15)
        
        # 图标容器
        self.icon_container = QFrame(self)
        self.icon_container.setFixedSize(140, 140)
        self.update_icon_style()
        
        # 添加图标容器到布局
        layout.addWidget(self.icon_container, 0, Qt.AlignCenter)
        
        # 文字容器
        text_container = QWidget()
        text_layout = QVBoxLayout(text_container)
        text_layout.setContentsMargins(0, 0, 0, 0)
        text_layout.setSpacing(10)
        
        # 标题
        title_label = QLabel(title)
        title_label.setFont(QFont('Microsoft YaHei', 22, QFont.Bold))
        title_label.setStyleSheet('color: #333333;')
        title_label.setAlignment(Qt.AlignCenter)
        text_layout.addWidget(title_label)
        
        layout.addWidget(text_container)
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 4)
        self.setGraphicsEffect(shadow)
        
        # 设置样式
        self.update_style()
        
    def update_icon_style(self):
        self.icon_container.setStyleSheet(f'''
            QFrame {{
                background-color: {self.color};
                border-radius: 70px;
                border: 4px solid white;
            }}
        ''')
        
    def update_style(self):
        hover_state = "true" if self.is_hovered else "false"
        self.setStyleSheet(f'''
            RoleButton {{
                background-color: white;
                border: 2px solid {self.color};
                border-radius: 15px;
            }}
            RoleButton[hovered="{hover_state}"] {{
                background-color: {self.color}11;
                border: 2px solid {self.color};
                transform: scale(1.05);
            }}
        ''')
        
    def enterEvent(self, event):
        self.is_hovered = True
        self.update_style()
        # 创建动画效果
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        current_geo = self.geometry()
        target_geo = QRect(current_geo.x(), current_geo.y() - 10, current_geo.width(), current_geo.height())
        self.anim.setStartValue(current_geo)
        self.anim.setEndValue(target_geo)
        self.anim.start()
        
    def leaveEvent(self, event):
        self.is_hovered = False
        self.update_style()
        # 创建动画效果
        self.anim = QPropertyAnimation(self, b"geometry")
        self.anim.setDuration(200)
        self.anim.setEasingCurve(QEasingCurve.OutCubic)
        current_geo = self.geometry()
        target_geo = QRect(current_geo.x(), current_geo.y() + 10, current_geo.width(), current_geo.height())
        self.anim.setStartValue(current_geo)
        self.anim.setEndValue(target_geo)
        self.anim.start()

class GradientFrame(QFrame):
    def __init__(self, start_color, end_color, parent=None):
        super().__init__(parent)
        self.start_color = start_color
        self.end_color = end_color

    def paintEvent(self, event):
        painter = QPainter(self)
        gradient = QLinearGradient(0, 0, self.width(), 0)
        gradient.setColorAt(0, QColor(self.start_color))
        gradient.setColorAt(1, QColor(self.end_color))
        gradient.setSpread(QGradient.PadSpread)
        painter.fillRect(self.rect(), gradient)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('基于AI大模型的智能体教学实训平台')
        self.resize(1280, 800)
        self.setMinimumSize(1200, 750)

        # 设置主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # 创建顶部标题区域
        header_frame = GradientFrame("#FF6B6B", "#4ECDC4")
        header_frame.setStyleSheet('''
            QFrame {
                border-radius: 30px;
                padding: 20px;
            }
        ''')
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(30, 30, 30, 30)
        header_layout.setSpacing(15)

        # Logo和标题容器
        logo_title_container = QWidget()
        logo_title_layout = QHBoxLayout(logo_title_container)
        logo_title_layout.setSpacing(20)

        # 标题和副标题容器
        title_container = QWidget()
        title_layout = QVBoxLayout(title_container)
        title_layout.setSpacing(15)

        # 主标题
        title_label = QLabel('基于AI大模型的智能体教学实训平台')
        title_label.setFont(QFont('Microsoft YaHei', 32, QFont.Bold))
        title_label.setStyleSheet('color: #333333;')
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)

        # 副标题
        subtitle_label = QLabel('请选择您的角色')
        subtitle_label.setFont(QFont('Microsoft YaHei', 20))
        subtitle_label.setStyleSheet('color: #666666;')
        subtitle_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(subtitle_label)

        logo_title_layout.addWidget(title_container)
        header_layout.addWidget(logo_title_container)

        # 添加标题区域到主布局
        main_layout.addWidget(header_frame)

        # 创建角色选择区域
        roles_frame = QFrame()
        roles_frame.setStyleSheet('''
            QFrame {
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 30px;
                padding: 40px;
            }
        ''')
        
        # 添加阴影效果
        shadow = QGraphicsDropShadowEffect(roles_frame)
        shadow.setBlurRadius(30)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 5)
        roles_frame.setGraphicsEffect(shadow)
        
        roles_layout = QHBoxLayout(roles_frame)
        roles_layout.setSpacing(40)

        # 创建三个角色按钮
        teacher_btn = RoleButton(
            "教师",
            "#3498db"
        )
        student_btn = RoleButton(
            "学生",
            "#2ecc71"
        )
        admin_btn = RoleButton(
            "管理员",
            "#e74c3c"
        )

        # 连接按钮信号
        teacher_btn.clicked.connect(lambda: self.show_login_window("teacher"))
        student_btn.clicked.connect(lambda: self.show_login_window("student"))
        admin_btn.clicked.connect(lambda: self.show_login_window("admin"))

        # 添加按钮到布局
        roles_layout.addStretch()
        roles_layout.addWidget(teacher_btn)
        roles_layout.addWidget(student_btn)
        roles_layout.addWidget(admin_btn)
        roles_layout.addStretch()

        # 添加角色选择区域到主布局
        main_layout.addWidget(roles_frame)

        # 设置主布局
        self.setLayout(main_layout)

        # 设置窗口背景
        self.setStyleSheet('''
            QWidget {
                background-color: #f0f0f0;
            }
        ''')

    def show_login_window(self, role):
        self.login_window = LoginWindow(role)
        self.login_window.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_()) 