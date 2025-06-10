from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QSplitter, QTextEdit, QLineEdit, QFileDialog, QMessageBox,
    QFrame, QSizePolicy
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt
from datetime import datetime
import os

from rjb.styles.theme import Theme
from rjb.utils.file_utils import read_file_content
from rjb.Large_Model.DeepSeek import Deepseek_API

class TeacherWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.prepare_design_window = None
        self.exam_generate_window = None
        self.student_analysis_window = None
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
        title_label = QLabel('教师教学中心')
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
        subtitle_label = QLabel('智能备课 & 教学管理')
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

        # 备课与设计按钮
        prepare_btn = self.create_feature_button(
            '备课与设计',
            '📝',
            '课程大纲 | 教学内容 | 实训设计',
            '#3498db'
        )
        prepare_btn.clicked.connect(self.show_prepare_design)
        button_layout.addWidget(prepare_btn)

        # 作业与评测按钮
        homework_btn = self.create_feature_button(
            '作业与评测',
            '📊',
            '作业管理 | 自动批改 | 成绩分析',
            '#e74c3c'
        )
        homework_btn.clicked.connect(self.show_homework_assessment)
        button_layout.addWidget(homework_btn)

        # 教学资源管理按钮
        resource_btn = self.create_feature_button(
            '教学资源管理',
            '📚',
            '资源库 | 智能推荐 | 资源共享',
            '#2ecc71'
        )
        resource_btn.clicked.connect(self.show_resource_management)
        button_layout.addWidget(resource_btn)

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

    def show_homework_assessment(self):
        # TODO: 实现作业与评测功能
        pass

    def show_resource_management(self):
        # TODO: 实现教学资源管理功能
        pass


class PrepareDesignWindow(QWidget):
    messages = []
    def __init__(self):
        super().__init__()
        self.file_path = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('备课助手')
        self.resize(1200, 800)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title_label = QLabel('基于大模型的备课设计')
        title_label.setStyleSheet('font-size: 24px; font-weight: bold; color: #2c3e50;')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        splitter = QSplitter(Qt.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

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
        self.input_text.setPlaceholderText('请输入您的备课需求...')
        left_layout.addWidget(self.input_text)

        send_btn = QPushButton('发送')
        send_btn.setStyleSheet(Theme.BUTTON_STYLE)
        send_btn.clicked.connect(self.send_message)
        left_layout.addWidget(send_btn)

        splitter.addWidget(left_widget)

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
        splitter.addWidget(self.output_text)

        main_layout.addWidget(splitter)
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
        self.messages.append({"role": "user", "content": content})
        try:
            response = Deepseek_API(self.messages)
            self.messages.append({"role": "assistant", "content": response})
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            formatted_response = f'[{current_time}] 备课助手回复：\n{response}\n\n'
            self.output_text.append(formatted_response)
        except Exception as e:
            QMessageBox.critical(self, '错误', f'发送消息失败：{str(e)}')


class ExamGenerateWindow(QWidget):
    messages = []
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('试题生成')
        self.resize(1200, 800)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title_label = QLabel('基于大模型的试题生成')
        title_label.setStyleSheet('font-size: 24px; font-weight: bold; color: #2c3e50;')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        splitter = QSplitter(Qt.Horizontal)

        left_widget = QWidget()
        left_layout = QVBoxLayout(left_widget)

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
        self.input_text.setPlaceholderText('请输入试题生成需求（如：科目、难度、题型等）...')
        left_layout.addWidget(self.input_text)

        button_layout = QHBoxLayout()
        send_btn = QPushButton('生成试题')
        send_btn.setStyleSheet(Theme.BUTTON_STYLE)
        send_btn.clicked.connect(self.send_message)
        button_layout.addWidget(send_btn)

        export_btn = QPushButton('导出试题')
        export_btn.setStyleSheet(Theme.BUTTON_STYLE)
        export_btn.clicked.connect(self.export_content)
        button_layout.addWidget(export_btn)

        left_layout.addLayout(button_layout)
        splitter.addWidget(left_widget)

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
        splitter.addWidget(self.output_text)

        main_layout.addWidget(splitter)
        self.setLayout(main_layout)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))  # #f0f0f0
        self.setPalette(palette)

    def send_message(self):
        content = self.input_text.toPlainText().strip()
        if not content:
            QMessageBox.warning(self, '错误', '请输入试题生成需求！')
            return
        self.messages.append({"role": "user", "content": content})
        try:
            response = Deepseek_API(self.messages)
            self.messages.append({"role": "assistant", "content": response})
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            formatted_response = f'[{current_time}] 试题生成结果：\n{response}\n\n'
            self.output_text.append(formatted_response)
        except Exception as e:
            QMessageBox.critical(self, '错误', f'生成试题失败：{str(e)}')

    def export_content(self):
        content = self.output_text.toPlainText()
        if not content:
            QMessageBox.warning(self, '错误', '没有可导出的内容！')
            return

        file_path, _ = QFileDialog.getSaveFileName(self, '导出试题', '', 'Text Files (*.txt);;All Files (*)')
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                QMessageBox.information(self, '成功', '试题导出成功！')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'导出失败：{str(e)}')


class StudentAnalysisWindow(QWidget):
    messages = []
    def __init__(self):
        super().__init__()
        self.assignment_file = None
        self.student_answers_dir = None
        self.analysis_results = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('学生分析')
        self.resize(1200, 800)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        title_label = QLabel('基于大模型的学生作业分析')
        title_label.setStyleSheet('font-size: 24px; font-weight: bold; color: #2c3e50;')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 作业文件选择区域
        assignment_group = QWidget()
        assignment_layout = QHBoxLayout(assignment_group)
        self.assignment_label = QLabel('未选择作业文件')
        self.assignment_label.setStyleSheet('color: #7f8c8d;')
        assignment_layout.addWidget(self.assignment_label)

        select_assignment_btn = QPushButton('选择作业文件')
        select_assignment_btn.setStyleSheet(Theme.BUTTON_STYLE)
        select_assignment_btn.clicked.connect(self.select_assignment_file)
        assignment_layout.addWidget(select_assignment_btn)

        cancel_assignment_btn = QPushButton('取消选择')
        cancel_assignment_btn.setStyleSheet(Theme.BUTTON_STYLE)
        cancel_assignment_btn.clicked.connect(self.cancel_assignment_file)
        assignment_layout.addWidget(cancel_assignment_btn)

        main_layout.addWidget(assignment_group)

        # 学生答案目录选择区域
        answers_group = QWidget()
        answers_layout = QHBoxLayout(answers_group)
        self.answers_label = QLabel('未选择学生答案目录')
        self.answers_label.setStyleSheet('color: #7f8c8d;')
        answers_layout.addWidget(self.answers_label)

        select_answers_btn = QPushButton('选择答案目录')
        select_answers_btn.setStyleSheet(Theme.BUTTON_STYLE)
        select_answers_btn.clicked.connect(self.select_student_answers_dir)
        answers_layout.addWidget(select_answers_btn)

        cancel_answers_btn = QPushButton('取消选择')
        cancel_answers_btn.setStyleSheet(Theme.BUTTON_STYLE)
        cancel_answers_btn.clicked.connect(self.cancel_student_answers_dir)
        answers_layout.addWidget(cancel_answers_btn)

        main_layout.addWidget(answers_group)

        # 分析结果显示区域
        self.results_text = QTextEdit()
        self.results_text.setStyleSheet('''
            QTextEdit {
                background-color: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                padding: 10px;
                font-size: 16px;
                font-family: Microsoft YaHei;
            }
        ''')
        self.results_text.setReadOnly(True)
        main_layout.addWidget(self.results_text)

        # 按钮区域
        button_layout = QHBoxLayout()
        analyse_btn = QPushButton('开始分析')
        analyse_btn.setStyleSheet(Theme.BUTTON_STYLE)
        analyse_btn.clicked.connect(self.analyse_students)
        button_layout.addWidget(analyse_btn)

        export_btn = QPushButton('导出分析结果')
        export_btn.setStyleSheet(Theme.BUTTON_STYLE)
        export_btn.clicked.connect(self.export_results)
        button_layout.addWidget(export_btn)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))  # #f0f0f0
        self.setPalette(palette)

    def select_assignment_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, '选择作业文件', '', 'Text Files (*.txt);;All Files (*)')
        if file_path:
            self.assignment_file = file_path
            self.assignment_label.setText(os.path.basename(file_path))

    def cancel_assignment_file(self):
        self.assignment_file = None
        self.assignment_label.setText('未选择作业文件')

    def select_student_answers_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, '选择学生答案目录')
        if dir_path:
            self.student_answers_dir = dir_path
            self.answers_label.setText(os.path.basename(dir_path))

    def cancel_student_answers_dir(self):
        self.student_answers_dir = None
        self.answers_label.setText('未选择学生答案目录')

    def analyse_students(self):
        if not self.assignment_file or not self.student_answers_dir:
            QMessageBox.warning(self, '错误', '请先选择作业文件和学生答案目录！')
            return

        try:
            # 读取作业文件
            assignment_content = read_file_content(self.assignment_file)
            if not assignment_content:
                QMessageBox.warning(self, '错误', '读取作业文件失败！')
                return

            # 读取所有学生答案
            student_answers = []
            for file_name in os.listdir(self.student_answers_dir):
                if file_name.endswith('.txt'):
                    file_path = os.path.join(self.student_answers_dir, file_name)
                    content1 = read_file_content(file_path)
                    if content1:
                        student_answers.append((file_name, content1))

            if not student_answers:
                QMessageBox.warning(self, '错误', '未找到任何学生答案文件！')
                return

            # 构建分析请求
            content = f"作业要求：\n{assignment_content}\n\n"
            for student_file, answer in student_answers:
                content += f"学生 {student_file}的答案：\n{answer}\n\n"
            content += "请分析每个学生的答案质量，并给出具体的评分和改进建议。"
            
            self.messages.append({"role": "user", "content": content})
            # 调用大模型进行分析
            response = Deepseek_API(self.messages)
            self.messages.append({"role": "assistant", "content": response})
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            self.analysis_results = f'[{current_time}] 分析结果：\n{response}\n\n'
            self.results_text.setText(self.analysis_results)

        except Exception as e:
            QMessageBox.critical(self, '错误', f'分析失败：{str(e)}')

    def export_results(self):
        if not self.analysis_results:
            QMessageBox.warning(self, '错误', '没有可导出的分析结果！')
            return

        file_path, _ = QFileDialog.getSaveFileName(self, '导出分析结果', '', 'Text Files (*.txt);;All Files (*)')
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(self.analysis_results)
                QMessageBox.information(self, '成功', '分析结果导出成功！')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'导出失败：{str(e)}') 