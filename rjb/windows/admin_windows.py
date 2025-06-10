from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFrame, QSizePolicy, QTableWidget, QTableWidgetItem, QComboBox,
    QMessageBox, QHeaderView, QFileDialog, QTreeWidget, QTreeWidgetItem,
    QDialog, QTextEdit,QGroupBox, QLineEdit, QProgressBar, QCheckBox
)
from PyQt5.QtGui import QPalette, QColor, QFont
from PyQt5.QtCore import Qt
import time
import os
import shutil
from datetime import datetime

from rjb.utils.db_utils import DatabaseManager
from rjb.utils.file_utils import read_file_content

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

        # 课间资源按钮
        monitor_btn = self.create_feature_button(
            '课件资源管理',
            '📊',
            '性能监控 | 日志分析 | 故障诊断',
            '#e67e22'
        )
        monitor_btn.clicked.connect(self.show_system_monitor)
        button_layout.addWidget(monitor_btn)

        # 数据备份按钮
        backup_btn = self.create_feature_button(
            '大屏概览',
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
        if not hasattr(self, 'user_management_window') or not self.user_management_window.isVisible():
            self.user_management_window = UserManagementWindow()
            self.user_management_window.show()
        else:
            self.user_management_window.activateWindow()
            self.user_management_window.raise_()

    def show_system_monitor(self):
        if not hasattr(self, 'resource_management_window') or not self.resource_management_window.isVisible():
            self.resource_management_window = ResourceManagementWindow()
            self.resource_management_window.show()
        else:
            self.resource_management_window.activateWindow()
            self.resource_management_window.raise_()

    def show_data_backup(self):
        # TODO: 实现数据备份功能
        pass

class UserManagementWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('用户管理')
        self.resize(1000, 600)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 标题
        title_label = QLabel('用户管理系统')
        title_label.setStyleSheet('''
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        ''')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 操作区域
        operations_layout = QHBoxLayout()
        
        # 角色选择下拉框
        self.role_combo = QComboBox()
        self.role_combo.addItems(['全部用户', '管理员', '教师', '学生'])
        self.role_combo.setStyleSheet('''
            QComboBox {
                padding: 5px;
                border: 2px solid #3498db;
                border-radius: 5px;
                min-width: 150px;
                font-size: 14px;
            }
        ''')
        operations_layout.addWidget(self.role_combo)
        
        # 刷新按钮
        refresh_btn = QPushButton('刷新列表')
        refresh_btn.setStyleSheet('''
            QPushButton {
                padding: 8px 15px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        refresh_btn.clicked.connect(self.refresh_user_list)
        operations_layout.addWidget(refresh_btn)
        
        operations_layout.addStretch()
        main_layout.addLayout(operations_layout)

        # 用户列表表格
        self.user_table = QTableWidget()
        self.user_table.setColumnCount(7)
        self.user_table.setHorizontalHeaderLabels(['ID', '用户名', '角色', '姓名', '邮箱', '创建时间', '操作'])
        self.user_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.user_table.setStyleSheet('''
            QTableWidget {
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        ''')
        main_layout.addWidget(self.user_table)

        self.setLayout(main_layout)
        
        # 设置窗口背景色
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        # 初始加载用户列表
        self.refresh_user_list()

    def refresh_user_list(self):
        try:
            # 获取选中的角色
            selected_role = self.role_combo.currentText()
            role_filter = None if selected_role == '全部用户' else selected_role.lower()
            
            # 从数据库获取用户列表
            users = self.db_manager.get_all_users(role_filter)
            
            # 清空表格
            self.user_table.setRowCount(0)
            
            # 填充用户数据
            for user in users:
                row_position = self.user_table.rowCount()
                self.user_table.insertRow(row_position)
                
                # 设置用户信息
                self.user_table.setItem(row_position, 0, QTableWidgetItem(str(user['id'])))
                self.user_table.setItem(row_position, 1, QTableWidgetItem(user['username']))
                self.user_table.setItem(row_position, 2, QTableWidgetItem(user['role']))
                self.user_table.setItem(row_position, 3, QTableWidgetItem(user['name'] or ''))
                self.user_table.setItem(row_position, 4, QTableWidgetItem(user['email'] or ''))
                self.user_table.setItem(row_position, 5, QTableWidgetItem(user['created_at']))
                
                # 添加操作按钮
                operations_widget = QWidget()
                operations_layout = QHBoxLayout(operations_widget)
                operations_layout.setContentsMargins(5, 2, 5, 2)
                
                # 重置密码按钮
                reset_pwd_btn = QPushButton('重置密码')
                reset_pwd_btn.setStyleSheet('''
                    QPushButton {
                        padding: 5px 10px;
                        background-color: #e74c3c;
                        color: white;
                        border: none;
                        border-radius: 3px;
                    }
                    QPushButton:hover {
                        background-color: #c0392b;
                    }
                ''')
                reset_pwd_btn.clicked.connect(lambda checked, u=user['username']: self.reset_password(u))
                
                # 删除用户按钮
                delete_btn = QPushButton('删除')
                delete_btn.setStyleSheet('''
                    QPushButton {
                        padding: 5px 10px;
                        background-color: #95a5a6;
                        color: white;
                        border: none;
                        border-radius: 3px;
                    }
                    QPushButton:hover {
                        background-color: #7f8c8d;
                    }
                ''')
                delete_btn.clicked.connect(lambda checked, u=user['username']: self.delete_user(u))
                
                operations_layout.addWidget(reset_pwd_btn)
                operations_layout.addWidget(delete_btn)
                operations_layout.addStretch()
                
                self.user_table.setCellWidget(row_position, 6, operations_widget)
                
        except Exception as e:
            QMessageBox.critical(self, '错误', f'加载用户列表失败：{str(e)}')

    def reset_password(self, username):
        reply = QMessageBox.question(self, '确认', f'确定要重置用户 {username} 的密码吗？',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                success = self.db_manager.reset_user_password(username)
                if success:
                    QMessageBox.information(self, '成功', '密码已重置为默认密码：123456')
                else:
                    QMessageBox.warning(self, '失败', '重置密码失败')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'重置密码时发生错误：{str(e)}')

    def delete_user(self, username):
        reply = QMessageBox.question(self, '确认', f'确定要删除用户 {username} 吗？此操作不可恢复！',
                                   QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            try:
                success = self.db_manager.delete_user(username)
                if success:
                    QMessageBox.information(self, '成功', '用户已删除')
                    self.refresh_user_list()
                else:
                    QMessageBox.warning(self, '失败', '删除用户失败')
            except Exception as e:
                QMessageBox.critical(self, '错误', f'删除用户时发生错误：{str(e)}') 

class ResourceManagementWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db_manager = DatabaseManager()
        self.current_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'resources')
        if not os.path.exists(self.current_path):
            os.makedirs(self.current_path)
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('课件资源管理')
        self.resize(1200, 800)

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)

        # 标题
        title_label = QLabel('课件资源管理系统')
        title_label.setStyleSheet('''
            font-size: 24px;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
        ''')
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        # 操作区域
        operations_layout = QHBoxLayout()
        
        # 学科选择下拉框
        self.subject_combo = QComboBox()
        self.subject_combo.addItems(['全部学科', '计算机基础', '程序设计', '数据结构', '数据库', '操作系统'])
        self.subject_combo.setStyleSheet('''
            QComboBox {
                padding: 5px;
                border: 2px solid #3498db;
                border-radius: 5px;
                min-width: 150px;
                font-size: 14px;
            }
        ''')
        self.subject_combo.currentTextChanged.connect(self.refresh_resource_list)
        operations_layout.addWidget(self.subject_combo)
        
        # 刷新按钮
        refresh_btn = QPushButton('刷新列表')
        refresh_btn.setStyleSheet('''
            QPushButton {
                padding: 8px 15px;
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
        ''')
        refresh_btn.clicked.connect(self.refresh_resource_list)
        operations_layout.addWidget(refresh_btn)

        # 导出按钮
        export_btn = QPushButton('导出所选资源')
        export_btn.setStyleSheet('''
            QPushButton {
                padding: 8px 15px;
                background-color: #27ae60;
                color: white;
                border: none;
                border-radius: 5px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
        ''')
        export_btn.clicked.connect(self.export_resources)
        operations_layout.addWidget(export_btn)
        
        operations_layout.addStretch()
        main_layout.addLayout(operations_layout)

        # 资源树形视图
        self.resource_tree = QTreeWidget()
        self.resource_tree.setHeaderLabels(['资源名称', '类型', '大小', '修改时间', '操作'])
        self.resource_tree.setColumnWidth(0, 300)  # 名称列宽
        self.resource_tree.setColumnWidth(1, 100)  # 类型列宽
        self.resource_tree.setColumnWidth(2, 100)  # 大小列宽
        self.resource_tree.setColumnWidth(3, 200)  # 时间列宽
        self.resource_tree.setStyleSheet('''
            QTreeWidget {
                border: 2px solid #e0e0e0;
                border-radius: 5px;
                background-color: white;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
        ''')
        main_layout.addWidget(self.resource_tree)

        self.setLayout(main_layout)
        
        # 设置窗口背景色
        palette = QPalette()
        palette.setColor(QPalette.Window, QColor(240, 240, 240))
        self.setPalette(palette)

        # 初始加载资源列表
        self.refresh_resource_list()

    def refresh_resource_list(self):
        try:
            self.resource_tree.clear()
            selected_subject = self.subject_combo.currentText()
            
            # 如果选择了特定学科，只显示该学科的目录
            if selected_subject != '全部学科':
                subject_path = os.path.join(self.current_path, selected_subject)
                if not os.path.exists(subject_path):
                    os.makedirs(subject_path)
                self.add_directory_to_tree(subject_path, self.resource_tree.invisibleRootItem())
            else:
                # 显示所有学科的目录
                for subject in os.listdir(self.current_path):
                    subject_path = os.path.join(self.current_path, subject)
                    if os.path.isdir(subject_path):
                        subject_item = QTreeWidgetItem(self.resource_tree)
                        subject_item.setText(0, subject)
                        subject_item.setText(1, "目录")
                        self.add_directory_to_tree(subject_path, subject_item)
                        self.resource_tree.addTopLevelItem(subject_item)
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'加载资源列表失败：{str(e)}')

    def add_directory_to_tree(self, path, parent_item):
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                tree_item = QTreeWidgetItem(parent_item)
                tree_item.setText(0, item)  # 名称
                
                # 获取文件信息
                stat = os.stat(item_path)
                mod_time = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                
                if os.path.isdir(item_path):
                    tree_item.setText(1, "目录")
                    tree_item.setText(2, "-")
                    self.add_directory_to_tree(item_path, tree_item)
                else:
                    # 获取文件扩展名
                    ext = os.path.splitext(item)[1].lower()
                    tree_item.setText(1, ext[1:] if ext else "文件")
                    
                    # 格式化文件大小
                    size = stat.st_size
                    if size < 1024:
                        size_str = f"{size} B"
                    elif size < 1024 * 1024:
                        size_str = f"{size/1024:.1f} KB"
                    else:
                        size_str = f"{size/(1024*1024):.1f} MB"
                    tree_item.setText(2, size_str)
                
                tree_item.setText(3, mod_time)  # 修改时间
                
                # 添加操作按钮
                if not os.path.isdir(item_path):
                    operations_widget = QWidget()
                    operations_layout = QHBoxLayout(operations_widget)
                    operations_layout.setContentsMargins(5, 2, 5, 2)
                    
                    # 预览按钮
                    preview_btn = QPushButton('预览')
                    preview_btn.setStyleSheet('''
                        QPushButton {
                            padding: 5px 10px;
                            background-color: #3498db;
                            color: white;
                            border: none;
                            border-radius: 3px;
                        }
                        QPushButton:hover {
                            background-color: #2980b9;
                        }
                    ''')
                    preview_btn.clicked.connect(lambda checked, path=item_path: self.preview_file(path))
                    
                    # 删除按钮
                    delete_btn = QPushButton('删除')
                    delete_btn.setStyleSheet('''
                        QPushButton {
                            padding: 5px 10px;
                            background-color: #e74c3c;
                            color: white;
                            border: none;
                            border-radius: 3px;
                        }
                        QPushButton:hover {
                            background-color: #c0392b;
                        }
                    ''')
                    delete_btn.clicked.connect(lambda checked, path=item_path: self.delete_resource(path))
                    
                    operations_layout.addWidget(preview_btn)
                    operations_layout.addWidget(delete_btn)
                    operations_layout.addStretch()
                    
                    self.resource_tree.setItemWidget(tree_item, 4, operations_widget)
        
        except Exception as e:
            print(f"添加目录到树形视图时出错: {e}")

    def preview_file(self, file_path):
        try:
            content = read_file_content(file_path)
            if content:
                preview_dialog = QDialog(self)
                preview_dialog.setWindowTitle('文件预览')
                preview_dialog.resize(800, 600)
                
                layout = QVBoxLayout()
                
                text_edit = QTextEdit()
                text_edit.setPlainText(content)
                text_edit.setReadOnly(True)
                layout.addWidget(text_edit)
                
                preview_dialog.setLayout(layout)
                preview_dialog.exec_()
            else:
                QMessageBox.warning(self, '警告', '无法预览此类型的文件')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'预览文件失败：{str(e)}')

    def delete_resource(self, file_path):
        try:
            reply = QMessageBox.question(self, '确认', '确定要删除此资源吗？此操作不可恢复！',
                                       QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                os.remove(file_path)
                self.refresh_resource_list()
                QMessageBox.information(self, '成功', '资源已删除')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'删除资源失败：{str(e)}')

    def export_resources(self):
        try:
            # 获取选中的项目
            selected_items = self.resource_tree.selectedItems()
            if not selected_items:
                QMessageBox.warning(self, '警告', '请先选择要导出的资源')
                return
            
            # 选择导出目录
            export_dir = QFileDialog.getExistingDirectory(self, '选择导出目录')
            if not export_dir:
                return
            
            # 导出选中的资源
            for item in selected_items:
                source_path = self.get_item_path(item)
                if os.path.exists(source_path):
                    if os.path.isdir(source_path):
                        # 复制目录
                        dest_path = os.path.join(export_dir, item.text(0))
                        shutil.copytree(source_path, dest_path, dirs_exist_ok=True)
                    else:
                        # 复制文件
                        shutil.copy2(source_path, export_dir)
            
            QMessageBox.information(self, '成功', '资源导出完成')
        except Exception as e:
            QMessageBox.critical(self, '错误', f'导出资源失败：{str(e)}')

    def get_item_path(self, item):
        """获取树形项目对应的完整路径"""
        path_parts = []
        while item is not None:
            path_parts.insert(0, item.text(0))
            item = item.parent()
        return os.path.join(self.current_path, *path_parts)

