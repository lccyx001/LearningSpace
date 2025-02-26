from PyQt5.QtWidgets import QMenuBar
from PyQt5.QtCore import QObject, pyqtSignal

class MenuBar(QObject):
    # 定义基础信号
    menu_triggered = pyqtSignal(str)  # 发送菜单项标识符

    def __init__(self, menu_structure, parent=None):
        """
        初始化菜单管理器
        
        Args:
            menu_structure (dict): 菜单结构配置
            格式示例:
            {
                "File": {
                    "New": {"shortcut": "Ctrl+N", "identifier": "file_new"},
                    "Open": {"shortcut": "Ctrl+O", "identifier": "file_open"},
                },
                "Help": {
                    "About": {"shortcut": "", "identifier": "help_about"}
                }
            }
        """
        super().__init__(parent)
        self.menu_structure = menu_structure

    def create_menu_bar(self, window):
        """创建菜单栏"""
        menu_bar = window.menuBar()
        
        for menu_name, menu_items in self.menu_structure.items():
            menu = menu_bar.addMenu(menu_name)
            for item_name, item_info in menu_items.items():
                action = menu.addAction(item_name)
                
                # 设置快捷键
                if item_info.get("shortcut"):
                    action.setShortcut(item_info["shortcut"])
                
                # 特殊处理退出操作
                if item_info.get("identifier") == "exit":
                    action.triggered.connect(window.close)
                else:
                    # 使用 lambda 创建闭包来保存 identifier
                    identifier = item_info.get("identifier", "")
                    action.triggered.connect(
                        lambda checked, id=identifier: self.menu_triggered.emit(id)
                    )
                
                # 添加分隔符（如果需要）
                if item_info.get("separator_after", False):
                    menu.addSeparator()