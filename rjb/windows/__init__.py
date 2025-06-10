"""
窗口组件包
~~~~~~~~

包含所有功能窗口的实现。
"""

from .auth_windows import LoginWindow, RegisterWindow
from .teacher_windows import TeacherWindow
from .student_windows import StudentWindow
from .admin_windows import AdminWindow

__all__ = [
    'LoginWindow',
    'RegisterWindow',
    'TeacherWindow',
    'StudentWindow',
    'AdminWindow'
] 