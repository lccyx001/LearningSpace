from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import QObject, pyqtSignal

class TabManager(QObject):
    # 定义信号
    tab_created = pyqtSignal(int)      # 标签页创建信号(index)
    tab_closed = pyqtSignal(int)       # 标签页关闭信号(index)
    tab_changed = pyqtSignal(int)      # 标签页切换信号(index)
    tab_ask_close = pyqtSignal(int)    # 标签页关闭请求信号(index)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabsClosable(True)
        self.tab_count = 0
        
        # 连接基础信号
        self.tab_widget.tabCloseRequested.connect(self.close_tab)
        self.tab_widget.currentChanged.connect(self.tab_changed.emit)
        

    def create_tab(self, widget, title=None):
        """
        创建新的标签页
        
        Args:
            widget: 标签页的内容组件
            title (str, optional): 标签页标题
        """
        self.tab_count += 1
        title = title or f"Tab {self.tab_count}"
        
        index = self.tab_widget.addTab(widget, title)
        self.tab_widget.setCurrentIndex(index)
        self.tab_created.emit(index)
        return index

    def close_tab(self, index):
        """关闭指定的标签页"""
        if self.tab_widget.count() > 0:
            self.tab_widget.removeTab(index)
            self.tab_closed.emit(index)

    def ask_close_tab(self, index):
        """请求关闭指定的标签页"""
        self.tab_ask_close.emit(index)

    def get_current_tab(self):
        """获取当前标签页"""
        return self.tab_widget.currentWidget()

    def get_tab(self, index):
        """获取指定索引的标签页"""
        return self.tab_widget.widget(index)

    def get_current_index(self):
        """获取当前标签页索引"""
        return self.tab_widget.currentIndex()

    def get_tab_count(self):
        """获取标签页数量"""
        return self.tab_widget.count()

    def set_tab_title(self, index, title):
        """设置标签页标题"""
        self.tab_widget.setTabText(index, title)

    def get_tab_widget(self):
        """获取标签页组件"""
        return self.tab_widget