from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QTabBar, QToolBar, QGridLayout, QLabel, QPushButton, QPlainTextEdit, QDialog
from PyQt5.QtMultimedia import QCameraInfo, QCamera
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor

import sys
import yaml
import logging
from time import sleep
from threading import Thread
import asyncio

class AzureUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Azure UI')

        self.resize(800,446)
        # self.setMinimumSize(800,446)

        self.tabs = Tabs()

        self.setCentralWidget(self.tabs)


class Tabs(QTabWidget):
    def __init__(self):
        super().__init__()

        self.camera_tab = CameraTab()
        self.logs_tab = LogsTab()
        self.settings_tab = SettingsTab()

        self.addTab(self.camera_tab, 'Camera Grid')
        self.addTab(Camera(settings_yml['camera-ports']['cam-1']), 'Camera 1')
        self.addTab(Camera(settings_yml['camera-ports']['cam-2']), 'Camera 2')
        self.addTab(Camera(settings_yml['camera-ports']['cam-3']), 'Camera 3')
        self.addTab(Camera(settings_yml['camera-ports']['cam-4']), 'Camera 4')
        self.addTab(self.logs_tab, 'Logs')
        self.addTab(self.settings_tab, 'Settings')

        self.setDocumentMode(True)

        self.setTabPosition(QTabWidget.West if settings_yml['vertical-tabs'] else QTabWidget.North)

    def add_tab(self):
        pass

class CameraTab(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        # self.layout.setSpacing(0)

        self.cam1 = Camera(settings_yml['camera-ports']['cam-1'])
        self.cam2 = Camera(settings_yml['camera-ports']['cam-2'])
        self.cam3 = Camera(settings_yml['camera-ports']['cam-3'])
        self.cam4 = Camera(settings_yml['camera-ports']['cam-4'])

        self.layout.addWidget(self.cam1, 0,0)
        self.layout.addWidget(self.cam2, 0,1)
        self.layout.addWidget(self.cam3, 1,0)
        self.layout.addWidget(self.cam4, 1,1)

        self.setLayout(self.layout)

class Camera(QCameraViewfinder):
    def __init__(self, port):
        super().__init__()

        self.camera = QCamera(cameras[port])
        self.camera.setViewfinder(self)
        self.camera.start()

class LoggerBox(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.logger = QPlainTextEdit()
        self.logger.setReadOnly(True)
    
    def emit(self, record):
        self.msg = self.format(record)
        self.logger.appendPlainText(self.msg)
        # QApplication.processEvents()
        # self.logger.moveCursor(QTextCursor.End)
        # self.messages_text_box.moveCursor(QtGui.QTextCursor.End)

# class Logger(QDialog, QPlainTextEdit):


class LogsTab(QDialog, QPlainTextEdit):
    def __init__(self):
        super().__init__()

        self.logger = LoggerBox(self)
        self.logger.setFormatter(logging.Formatter('[%(asctime)s] %(message)s', '%H:%M:%S'))

        logging.getLogger().addHandler(self.logger)
        logging.getLogger().setLevel(logging.DEBUG)
        

        self.layout = QGridLayout()
        self.layout.addWidget(self.logger.logger)

        self.setLayout(self.layout)

        # for _ in range(40):
        #     sleep(0.7)
        #     self.update_log('testinfijgwsojdasfpoisjsdafoisjdjsfsais')
    
    def update_log(self, msg):
        logging.debug(msg)

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()


# async def testing_func(x):
#     for _ in range(100):
#         x.tabs.logs_tab.update_log('a')
#         await asyncio.sleep(0.5)

class TestingLog(Thread):
    def __init__(self, window_name):
        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        for _ in range(1000000):
            sleep(0.01)
            window.tabs.logs_tab.update_log('ok')

if __name__ == '__main__':
    # Defining global variables
    cameras = QCameraInfo.availableCameras()

    with open('gui/settings.yml', 'r') as f:
        settings_yml = yaml.safe_load(f)
    print(settings_yml)

    # Create UI application
    app = QApplication([])

    window = AzureUI()
    window.show()

    TestingLog(window)

    # t1 = Thread(target=testing_func(window))
    # t1.start()

    sys.exit(app.exec())

# t = Thread(target=threaded_func(window))
# t.start()

    


# cameras = QCameraInfo.availableCameras()

# with open('gui/settings.yml', 'r') as f:
#     settings_yml = yaml.safe_load(f)
# print(settings_yml)