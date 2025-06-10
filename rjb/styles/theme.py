class Theme:
    # 主色调
    PRIMARY_COLOR = "#e91e63"       # 粉红色主色调
    PRIMARY_LIGHT = "#f8bbd0"       # 浅粉色
    PRIMARY_DARK = "#c2185b"        # 深粉色
    
    # 辅助色调
    SECONDARY_COLOR = "#3498db"     # 蓝色
    SECONDARY_LIGHT = "#5dade2"     # 浅蓝色
    SECONDARY_DARK = "#2980b9"      # 深蓝色
    
    # 状态颜色
    SUCCESS_COLOR = "#2ecc71"       # 成功绿色
    WARNING_COLOR = "#f1c40f"       # 警告黄色
    DANGER_COLOR = "#e74c3c"        # 危险红色
    INFO_COLOR = "#3498db"          # 信息蓝色
    
    # 中性色
    BACKGROUND_COLOR = "#fce4ec"    # 主背景色
    SURFACE_COLOR = "#fff0f6"       # 表面背景色
    BORDER_COLOR = "#f48fb1"        # 边框颜色
    
    # 文本颜色
    TEXT_PRIMARY = "#2c3e50"        # 主要文本
    TEXT_SECONDARY = "#7f8c8d"      # 次要文本
    TEXT_DISABLED = "#bdc3c7"       # 禁用文本
    
    # 字体设置
    FONT_FAMILY = "Microsoft YaHei"
    FONT_SIZE_SMALL = "13px"
    FONT_SIZE_MEDIUM = "15px"
    FONT_SIZE_LARGE = "18px"
    FONT_SIZE_XLARGE = "24px"
    
    # 阴影效果
    SHADOW_SMALL = "0 2px 4px rgba(0,0,0,0.1)"
    SHADOW_MEDIUM = "0 4px 8px rgba(0,0,0,0.1)"
    SHADOW_LARGE = "0 8px 16px rgba(0,0,0,0.1)"
    
    # 动画时间
    ANIMATION_SPEED_FAST = "0.2s"
    ANIMATION_SPEED_NORMAL = "0.3s"
    ANIMATION_SPEED_SLOW = "0.4s"

    # 所有样式定义
    CARD_STYLE = '''
        QFrame {
            background-color: #fff0f6;
            border-radius: 16px;
            border: 2px solid #f48fb1;
            padding: 20px;
        }
        QFrame:hover {
            background-color: #fce4ec;
        }
    '''

    # 输入框样式
    INPUT_STYLE = '''
        QLineEdit {
            background-color: white;
            border: 1px solid #ccc;
            padding: 10px;
            border-radius: 5px;
            font-size: 14px;
            font-family: Microsoft YaHei;
        }
        QLineEdit:focus {
            border: 2px solid #3498db;
        }
    '''

    # 按钮样式
    BUTTON_STYLE = '''
        QPushButton {
            background-color: #3498db;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 6px;
            font-size: 14px;
            font-family: Microsoft YaHei;
            font-weight: bold;
            min-width: 120px;
        }
        QPushButton:hover {
            background-color: #2980b9;
        }
        QPushButton:pressed {
            background-color: #2471a3;
        }
    '''

    LABEL_STYLE = '''
        QLabel {
            color: #2c3e50;
            font-family: Microsoft YaHei;
            font-size: 15px;
            padding: 5px;
        }
    '''

    CHECKBOX_STYLE = '''
        QCheckBox {
            font-family: Microsoft YaHei;
            font-size: 14px;
            color: #2c3e50;
            spacing: 8px;
        }
        QCheckBox::indicator {
            width: 20px;
            height: 20px;
            border-radius: 4px;
            border: 2px solid #e0e0e0;
        }
        QCheckBox::indicator:unchecked {
            background-color: white;
        }
        QCheckBox::indicator:checked {
            background-color: #3498db;
            border-color: #3498db;
            image: url(check.png);
        }
        QCheckBox::indicator:hover {
            border-color: #3498db;
        }
    '''

    LIST_STYLE = '''
        QListWidget {
            background-color: white;
            border-radius: 8px;
            border: 2px solid #e0e0e0;
            padding: 5px;
        }
        QListWidget::item {
            padding: 10px;
            border-radius: 4px;
            margin: 2px 0;
        }
        QListWidget::item:hover {
            background-color: #f5f6fa;
        }
        QListWidget::item:selected {
            background-color: #3498db;
            color: white;
        }
    '''

    SCROLLBAR_STYLE = '''
        QScrollBar:vertical {
            border: none;
            background-color: #f0f0f0;
            width: 10px;
            border-radius: 5px;
        }
        QScrollBar::handle:vertical {
            background-color: #c0c0c0;
            border-radius: 5px;
            min-height: 20px;
        }
        QScrollBar::handle:vertical:hover {
            background-color: #a0a0a0;
        }
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
            background: none;
        }
    '''

    DIALOG_STYLE = '''
        QDialog {
            background-color: white;
            border-radius: 10px;
        }
        QDialog QLabel {
            color: #2c3e50;
            font-size: 15px;
            font-family: Microsoft YaHei;
        }
        QDialog QPushButton {
            min-width: 80px;
        }
    '''

    TOOLTIP_STYLE = '''
        QToolTip {
            background-color: #2c3e50;
            color: white;
            border: none;
            padding: 8px;
            border-radius: 4px;
            font-size: 13px;
            font-family: Microsoft YaHei;
        }
    '''

    MENU_STYLE = '''
        QMenu {
            background-color: white;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 5px;
        }
        QMenu::item {
            padding: 8px 25px;
            border-radius: 4px;
            margin: 2px 5px;
        }
        QMenu::item:selected {
            background-color: #3498db;
            color: white;
        }
        QMenu::separator {
            height: 1px;
            background-color: #e0e0e0;
            margin: 5px 0;
        }
    '''

    PROGRESSBAR_STYLE = '''
        QProgressBar {
            border: none;
            border-radius: 10px;
            text-align: center;
            background-color: #f0f0f0;
            height: 20px;
        }
        QProgressBar::chunk {
            background-color: #3498db;
            border-radius: 10px;
        }
    ''' 