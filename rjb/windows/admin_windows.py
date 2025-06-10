from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFrame, QSizePolicy, QGroupBox, QLineEdit, QProgressBar, QCheckBox
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt
import time

class AdminWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('管理员端界面')
        self.resize(800, 600)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(40, 40, 40, 40)
        main_layout.setSpacing(30)

        # 顶部标题区
        title_frame = QFrame()
        title_frame.setStyleSheet('''
            QFrame {
                background-color: #34495e;
                border-radius: 12px;
                padding: 24px 0px;
            }
        ''')
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)

        # 标题文本
        title_label = QLabel('系统管理中心')
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
        subtitle_label = QLabel('用户管理 & 系统维护')
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

        # 用户管理按钮
        user_btn = self.create_feature_button(
            '用户管理',
            '👥',
            '用户权限 | 账号管理 | 角色分配',
            '#9b59b6'
        )
        user_btn.clicked.connect(self.show_user_management)
        button_layout.addWidget(user_btn)

        # 系统监控按钮
        monitor_btn = self.create_feature_button(
            '系统监控',
            '📊',
            '性能监控 | 日志分析 | 故障诊断',
            '#e67e22'
        )
        monitor_btn.clicked.connect(self.show_system_monitor)
        button_layout.addWidget(monitor_btn)

        # 数据备份按钮
        backup_btn = self.create_feature_button(
            '数据备份',
            '💾',
            '数据备份 | 恢复管理 | 存储优化',
            '#16a085'
        )
        backup_btn.clicked.connect(self.show_data_backup)
        button_layout.addWidget(backup_btn)

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

    def show_user_management(self):
        # TODO: 实现用户管理功能
        pass

    def show_system_monitor(self):
        # TODO: 实现系统监控功能
        pass

    def show_data_backup(self):
        # TODO: 实现数据备份功能
        pass 
        """显示数据备份窗口"""
        self.backup_window = QWidget()
        self.backup_window.setWindowTitle('数据备份')
        self.backup_window.resize(600, 400)

        # 主布局
        main_layout = QVBoxLayout(self.backup_window)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)

        # 标题
        title_label = QLabel('数据备份系统')
        title_label.setStyleSheet('font-size: 20px; font-weight: bold; color: #2c3e50;')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 备份源选择区域
        source_group = QGroupBox('备份源')
        source_layout = QVBoxLayout(source_group)
        
        self.source_path_edit = QLineEdit()
        self.source_path_edit.setPlaceholderText('请选择要备份的目录或文件')
        
        source_btn_layout = QHBoxLayout()
        select_file_btn = QPushButton('选择文件')
        select_file_btn.setStyleSheet('background-color: #3498db; color: white; padding: 8px;')
        select_file_btn.clicked.connect(self.select_backup_source_file)
        
        select_dir_btn = QPushButton('选择目录')
        select_dir_btn.setStyleSheet('background-color: #3498db; color: white; padding: 8px;')
        select_dir_btn.clicked.connect(self.select_backup_source_dir)
        
        source_btn_layout.addWidget(select_file_btn)
        source_btn_layout.addWidget(select_dir_btn)
        
        source_layout.addWidget(self.source_path_edit)
        source_layout.addLayout(source_btn_layout)
        main_layout.addWidget(source_group)

        # 备份目标区域
        target_group = QGroupBox('备份目标')
        target_layout = QVBoxLayout(target_group)
        
        self.target_path_edit = QLineEdit()
        self.target_path_edit.setPlaceholderText('请选择备份保存位置')
        
        select_target_btn = QPushButton('选择位置')
        select_target_btn.setStyleSheet('background-color: #3498db; color: white; padding: 8px;')
        select_target_btn.clicked.connect(self.select_backup_target)
        
        target_layout.addWidget(self.target_path_edit)
        target_layout.addWidget(select_target_btn)
        main_layout.addWidget(target_group)

        # 备份选项
        options_group = QGroupBox('备份选项')
        options_layout = QVBoxLayout(options_group)
        
        self.compress_checkbox = QCheckBox('压缩备份文件')
        self.compress_checkbox.setChecked(True)
        
        self.timestamp_checkbox = QCheckBox('添加时间戳')
        self.timestamp_checkbox.setChecked(True)
        
        options_layout.addWidget(self.compress_checkbox)
        options_layout.addWidget(self.timestamp_checkbox)
        main_layout.addWidget(options_group)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setStyleSheet('QProgressBar { height: 20px; }')
        main_layout.addWidget(self.progress_bar)

        # 操作按钮
        btn_layout = QHBoxLayout()
        
        backup_btn = QPushButton('开始备份')
        backup_btn.setStyleSheet('background-color: #2ecc71; color: white; padding: 10px;')
        backup_btn.clicked.connect(self.start_backup)
        
        cancel_btn = QPushButton('取消')
        cancel_btn.setStyleSheet('background-color: #e74c3c; color: white; padding: 10px;')
        cancel_btn.clicked.connect(self.backup_window.close)
        
        btn_layout.addWidget(backup_btn)
        btn_layout.addWidget(cancel_btn)
        main_layout.addLayout(btn_layout)

        self.backup_window.show()

    def select_backup_source_file(self):
        """选择备份源文件"""
        file_path, _ = QFileDialog.getOpenFileName(self.backup_window, '选择备份文件', '', 'All Files (*)')
        if file_path:
            self.source_path_edit.setText(file_path)

    def select_backup_source_dir(self):
        """选择备份源目录"""
        dir_path = QFileDialog.getExistingDirectory(self.backup_window, '选择备份目录')
        if dir_path:
            self.source_path_edit.setText(dir_path)

    def select_backup_target(self):
        """选择备份目标位置"""
        dir_path = QFileDialog.getExistingDirectory(self.backup_window, '选择备份保存位置')
        if dir_path:
            self.target_path_edit.setText(dir_path)

    def start_backup(self):
        """开始备份操作"""
        source_path = self.source_path_edit.text()
        target_path = self.target_path_edit.text()
        
        if not source_path or not target_path:
            QMessageBox.warning(self.backup_window, '错误', '请先选择备份源和目标路径')
            return
        
        # 模拟备份过程
        self.progress_bar.setValue(0)
        for i in range(1, 101):
            time.sleep(0.05)  # 模拟耗时操作
            self.progress_bar.setValue(i)
            QApplication.processEvents()  # 更新UI
        
        # 生成备份文件名
        backup_name = 'backup'
        if self.timestamp_checkbox.isChecked():
            backup_name += '_' + time.strftime('%Y%m%d_%H%M%S')
        
        if self.compress_checkbox.isChecked():
            backup_name += '.zip'
            # 这里应该添加实际压缩代码
            QMessageBox.information(self.backup_window, '完成', f'备份已完成，保存为: {backup_name}')
        else:
            # 这里应该添加实际文件复制代码
            QMessageBox.information(self.backup_window, '完成', '备份已完成')
        
        self.progress_bar.setValue(0) 
