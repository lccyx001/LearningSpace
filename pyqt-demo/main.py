import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, 
    QMenuBar, QStatusBar, QFrame, QGridLayout, QTextEdit, QMessageBox, QTabWidget
)
from components.menu_tree import MenuTree
from components.menu_bar import MenuBar
from components.tab import TabManager
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("概率损伤容限软件")
        self.setGeometry(100, 100,2560, 1920)  # 修改为新的宽度和高度
        self.setStyleSheet("background-color: white;")
        self.tab_count = 0

        # 定义菜单结构
        self.menu_structure = {
            "File": {
                "New": {"shortcut": "Ctrl+N", "identifier": "file_new"},
                "Open": {"shortcut": "Ctrl+O", "identifier": "file_open"},
                "Save": {"shortcut": "Ctrl+S", "identifier": "file_save"},
                "Exit": {"shortcut": "Ctrl+Q", "identifier": "exit", "separator_after": True}
            },
            "DataBase": {
                "Material": {"shortcut": "", "identifier": "db_material"},
                "POD": {"shortcut": "", "identifier": "db_pod"},
                "Anomaly Distribution": {"shortcut": "", "identifier": "db_anomaly"}
            },
            "Help": {
                "About": {"shortcut": "", "identifier": "help_about"}
            }
        }

        self.tree_menu_structure = {
            "Project Setting": {
                "icon": "icons/project.png",
                "children": {}  # 空字典表示没有子菜单
            },
            "Geometry": {
                "icon": "icons/geometry.png",
                "children": {
                    "Geometry Setting": {
                        "icon": None,
                        "children": {}
                    },
                    "Plot Stress": {
                        "icon": None,
                        "children": {}
                    }
                }
            },
            "Property": {
                "icon": "icons/property.png",
                "children": {
                    "Anomaly": {
                        "icon": None,
                        "children": {
                        }
                    },
                    "Material": {
                        "icon": None,
                        "children": {}
                    },
                    "Inspection Events": {
                        "icon": None,
                        "children": {}
                    }
                }
            },
            "Spectrum": {
                "icon": "icons/spectrum.png",
                "children": {
                    "Spectrum Setting": {
                        "icon": None,
                        "children": {}
                    },
                    "Spectrum Plot": {
                        "icon": None,
                        "children": {}
                    }
                }
            },
            "Solve & Postprogress": {
                "icon": "icons/solve.png",
                "children": {
                    "Solve": {
                        "icon": None,
                        "children": {}
                    },
                    "Zone Update Or Refine": {
                        "icon": None,
                        "children": {}
                    },
                    "Evaluate Results": {
                        "icon": None,
                        "children": {
                            "Evaluate Report": {
                                "icon": None,
                                "children": {}
                            },
                            "Disk Assessment": {
                                "icon": None,
                                "children": {}
                            },
                            "Disk Assessment/Fights": {
                                "icon": None,
                                "children": {}
                            },
                            "Zone Assessment": {
                                "icon": None,
                                "children": {}
                            },
                            "Contributor Factor": {
                                "icon": None,
                                "children": {}
                            },
                            "Risk Cloud Map": {
                                "icon": None,
                                "children": {}
                            }
                        }
                    }
                }
            }
        }

        self.current_main_window = None  # 添加当前主窗口的引用

        self.initUI()

    def initUI(self):
        # 创建主窗口布局
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QGridLayout(central_widget)
        
        # 创建菜单管理器
        self.menu_manager = MenuBar(self.menu_structure)
        self.menu_manager.create_menu_bar(self)
        self.menu_manager.menu_triggered.connect(self.handle_menu_action)
        
        # 创建标签页管理器
        self.tab_manager = TabManager()
        main_layout.addWidget(self.tab_manager.get_tab_widget())
        

    def create_tab_content(self):
        """创建标签页内容"""
        tab = QWidget()
        layout = QGridLayout(tab)
        
        # 创建树形菜单
        menu_tree = MenuTree(menu_structure=self.tree_menu_structure)
        menu_tree.item_clicked.connect(self.handle_tree_item_clicked)
        
        # 创建右侧内容区域
        content_area = QVBoxLayout()
        
        # 主要操作窗口
        main_window = QFrame()
        main_window.setStyleSheet("background-color: lightgray;")
        main_window.setMinimumSize(600, 300)
        # 为main_window设置布局
        main_window_layout = QVBoxLayout()
        main_window.setLayout(main_window_layout)
        content_area.addWidget(main_window)
        self.main_window_container = main_window

        # 日志输出窗口
        log_output = QTextEdit()
        log_output.setStyleSheet("background-color: #f0f0f0; color: #333;")
        log_output.setMinimumHeight(100)
        log_output.setMaximumHeight(300)
        log_output.setReadOnly(True)
        content_area.addWidget(log_output)
        tab.log_output = log_output

        # 添加到布局
        layout.addWidget(menu_tree, 0, 0)
        layout.addLayout(content_area, 0, 1)
        return tab

    def handle_tree_item_clicked(self, item_text):
        """处理树形菜单项点击事件"""
        current_tab = self.tab_manager.get_current_tab()
        if current_tab:
            # 根据点击的菜单项更新主窗口
            self.update_main_window(item_text)

    def update_main_window(self, menu_item):
        """更新主窗口内容"""
        if self.current_main_window:
            self.current_main_window.layout().removeWidget(self.current_main_window)
            self.current_main_window.deleteLater()
            self.current_main_window = None

        # 根据菜单项创建相应的窗口
        new_window = self.create_window_for_menu(menu_item)
        self.log_message(f"已创建{menu_item}界面")
        if new_window:
            self.current_main_window = new_window
            self.main_window_container.layout().addWidget(new_window)
            self.log_message(f"已切换到{menu_item}界面")

    def create_window_for_menu(self, menu_item):
        """根据菜单项创建对应的窗口"""
        windows = {
            "Geometry Setting": self.create_geometry_setting_window,
            "Plot Stress": self.create_plot_stress_window,
            "Anomaly": self.create_anomaly_window,
            # "Material": self.create_material_window,
            # "Inspection Events": self.create_inspection_window,
            # "Spectrum Setting": self.create_spectrum_setting_window,
            # "Spectrum Plot": self.create_spectrum_plot_window,
            # "Solve": self.create_solve_window,
            # "Zone Update Or Refine": self.create_zone_update_window,
            # "Evaluate Report": self.create_evaluate_report_window,
            # 添加更多菜单项对应的窗口创建函数
        }
        
        creator = windows.get(menu_item)
        if creator:
            return creator()
        return None

    # 以下是各个具体窗口的创建函数
    def create_geometry_setting_window(self):
        window = QWidget()
        layout = QVBoxLayout(window)
        layout.addWidget(QLabel("几何设置界面"))
        # 添加具体的几何设置控件
        return window

    def create_plot_stress_window(self):
        window = QWidget()
        layout = QVBoxLayout(window)
        layout.addWidget(QLabel("应力绘图界面"))
        # 添加具体的应力绘图控件
        return window

    def create_anomaly_window(self):
        window = QWidget()
        layout = QVBoxLayout(window)
        layout.addWidget(QLabel("异常设置界面"))
        # 添加具体的异常设置控件
        return window

    def handle_menu_action(self, identifier):
        """处理菜单动作"""
        handlers = {
            "file_new": self.handle_new,
            "file_open": self.handle_open,
            "file_save": self.handle_save,
            "db_material": self.handle_material,
            "db_pod": self.handle_pod,
            "db_anomaly": self.handle_anomaly_distribution,
            "help_about": self.handle_about
        }
        
        handler = handlers.get(identifier)
        if handler:
            handler()

    def log_message(self, message):
        self.tab_manager.get_current_tab().log_output.append(message)

    def handle_new(self):
        """处理新建文件操作"""
        self.tab_count += 1
        new_tab = self.create_tab_content()
        self.tab_manager.create_tab(new_tab, f"文件 {self.tab_count}")
        
    def close_tab(self, index):
        """关闭标签页"""
        self.tab_manager.close_tab(index)
    
    def handle_open(self):
        QMessageBox.information(self, "打开", "打开文件")
        
    def handle_save(self):
        QMessageBox.information(self, "保存", "保存文件")
        
    def handle_material(self):
        QMessageBox.information(self, "材料", "材料")
        
    def handle_pod(self):
        QMessageBox.information(self, "POD", "POD")

    def handle_anomaly_distribution(self):
        QMessageBox.information(self, "异常分布", "异常分布")
        
    def handle_about(self):
        QMessageBox.information(self, "关于", "关于本软件")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())