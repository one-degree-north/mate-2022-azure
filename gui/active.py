from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import Qt

from tabs.home import HomeTab
from tabs.camera import Camera 
from tabs.logs import ConsoleTab 

import yaml

class ActiveTab(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self.home_tab = HomeTab()
        self.cam_tab = Camera(port)
        self.console_tab = ConsoleTab()


        self.addTab(self.home_tab, 'Menu')
        self.addTab(self.cam_tab, 'Camera')
        self.addTab(self.console_tab, 'Console')

        self.setTabPosition(QTabWidget.West)

        self.setDocumentMode(True)
        self.tabBar().hide()


# Defining global variable(s)
with open('gui/settings.yml', 'r') as f:
    port = yaml.safe_load(f)['camera-port']