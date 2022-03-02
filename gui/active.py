from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import Qt

from tabs.home import HomeTab
from tabs.camera import Camera 
from tabs.logs import LogsTab 

import yaml

class ActiveTab(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self.home_tab = HomeTab()
        self.cam_tab = Camera(settings_yml['camera-port'])
        self.logs_tab = LogsTab()


        self.addTab(self.home_tab, 'Menu')
        self.addTab(self.cam_tab, 'Camera')
        self.addTab(self.logs_tab, 'Logs')

        self.setTabPosition(QTabWidget.West)

        self.setDocumentMode(True)
        self.tabBar().hide()

# Defining global variable(s)
with open('gui/settings.yml', 'r') as f:
    settings_yml = yaml.safe_load(f)