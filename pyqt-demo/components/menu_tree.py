from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal

class MenuTree(QTreeWidget):
    # 定义自定义信号，传递被点击的菜单项的文本
    item_clicked = pyqtSignal(str)
    
    def __init__(self, parent=None, menu_structure=None):
        super().__init__(parent)
        self.setHeaderHidden(True)  # 隐藏表头
        self.setMinimumWidth(250)   # 设置最小宽度
        self.setMaximumWidth(350)   # 设置最大宽度
        
        # 存储菜单项的字典，方便后续访问
        self.menu_items = {}
        
        # 初始化菜单结构
        self.init_menu(menu_structure)
        
        # 连接点击信号
        self.itemClicked.connect(self.on_item_clicked)

    def init_menu(self, menu_structure):
        self.menu_structure = menu_structure
        self.create_menu_items()

    def create_menu_items(self, parent_item=None, menu_dict=None):
        # 如果没有提供menu_dict，使用根菜单结构
        if menu_dict is None:
            menu_dict = self.menu_structure

        # 遍历菜单项
        for menu_name, menu_info in menu_dict.items():
            # 创建菜单项
            menu_item = QTreeWidgetItem([menu_name])
            if menu_info["icon"]:
                menu_item.setIcon(0, QIcon(menu_info["icon"]))
            
            # 存储菜单项引用
            self.menu_items[menu_name] = menu_item
            
            # 如果有父项，添加到父项
            if parent_item:
                parent_item.addChild(menu_item)
            else:
                self.addTopLevelItem(menu_item)
            
            # 递归处理子菜单
            if menu_info["children"]:
                self.create_menu_items(menu_item, menu_info["children"])

    def on_item_clicked(self, item, column):
        # 发射自定义信号，传递被点击项的文本
        self.item_clicked.emit(item.text(0))

    def get_item(self, item_name):
        # 获取指定名称的菜单项
        return self.menu_items.get(item_name)

    def expand_all(self):
        # 展开所有菜单项
        self.expandAll()

    def collapse_all(self):
        # 折叠所有菜单项
        self.collapseAll()

    def set_item_icon(self, item_name, icon_path):
        # 设置指定菜单项的图标
        item = self.get_item(item_name)
        if item:
            item.setIcon(0, QIcon(icon_path))
