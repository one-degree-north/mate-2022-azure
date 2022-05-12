from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import Qt

from gui.tabs.camera import Camera 
from gui.tabs.console import ConsoleTab

import yaml

class ActiveTab(QTabWidget):
    def __init__(self, parent):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self.cam_tab = Camera(settings['camera-port'])
        self.console_tab = ConsoleTab()

        self.addTab(self.cam_tab, 'Camera')
        self.addTab(self.console_tab, 'Console')

        self.setTabPosition(QTabWidget.West)

        self.setDocumentMode(True)
        self.tabBar().hide()

    # def keyPressEvent(self, e):
    #     print(e.text())


# Defining global variable(s)
with open('settings.yml', 'r') as f:
    settings = yaml.safe_load(f)