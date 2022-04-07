from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtCore import Qt

from gui.tabs.home import HomeTab
from gui.tabs.grid import Grid
from gui.tabs.camera import Camera 
from gui.tabs.viewer import ImageViewer
from gui.tabs.logs import ConsoleTab

import yaml

class ActiveTab(QTabWidget):
    def __init__(self, parent):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self.home_tab = HomeTab(parent)
        self.grid_tab = Grid(settings['camera-port-1'], settings['camera-port-2'])
        self.cam1_tab = Camera(settings['camera-port-1'])
        self.cam2_tab = Camera(settings['camera-port-2'])
        self.viewer_tab = ImageViewer()
        self.console_tab = ConsoleTab()


        self.addTab(self.home_tab, 'Menu')
        self.addTab(self.grid_tab, 'Camera Grid')
        self.addTab(self.cam1_tab, 'Camera 1')
        self.addTab(self.cam2_tab, 'Camera 2')
        self.addTab(self.viewer_tab, 'Image Viewer')
        self.addTab(self.console_tab, 'Console')

        self.setTabPosition(QTabWidget.West)

        self.setDocumentMode(True)
        self.tabBar().hide()


# Defining global variable(s)
with open('settings.yml', 'r') as f:
    settings = yaml.safe_load(f)