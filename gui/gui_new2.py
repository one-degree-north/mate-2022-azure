from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QGridLayout, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit, QDialog, QVBoxLayout, QPushButton, QLabel, QToolTip
from PyQt5.QtMultimedia import QCameraInfo, QCamera
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QPixmap

import sys
import yaml
import logging

class AzureUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Azure UI')
        self.setStyleSheet('background: rgb(24, 40, 61)')#; margin: 6px')

        self.frame = QWidget()


        self.frame.layout = QHBoxLayout()

        self.menu = Menu()
        self.tabs = Tabs()
        self.tab_widget = self.tabs

        # self.menu.setStyleSheet('background: rgb(17, 28, 43); border-top-right-radius: 20px; border-bottom-right-radius: 20px')
        # self.menu.setFixedWidth(300)


        self.frame.layout.addWidget(self.menu)
        self.frame.layout.addWidget(self.tabs)

        self.frame.layout.setContentsMargins(0,0,0,0)


        self.frame.setLayout(self.frame.layout)
        self.setCentralWidget(self.frame)
        
class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self.setStyleSheet('background: rgb(17, 28, 43); border-top-right-radius: 20px; border-bottom-right-radius: 20px')
        self.setFixedWidth(300)

        self.layout = QVBoxLayout()

        self.menu_button = TabButton('Menu')
        self.menu_button.clicked.connect(self.menu_callback)
        
        self.image = QLabel(self)
        self.image_pixmap = QPixmap('gui/rsz_1mate_logo.png')
        # self.image_pixmap.scaled(0.3, 0.3, Qt.KeepAspectRatio)

        self.image.setPixmap(self.image_pixmap)
        self.image.setAlignment(Qt.AlignHCenter)

        self.cam_grid_button = TabButton('Camera Grid')
        self.cam_grid_button.clicked.connect(self.cam_grid_callback)

        self.cam_1_button = TabButton('Camera 1')
        self.cam_1_button.clicked.connect(self.cam_1_callback)

        self.cam_2_button = TabButton('Camera 2')
        self.cam_2_button.clicked.connect(self.cam_2_callback)

        self.cam_3_button = TabButton('Camera 3')
        self.cam_3_button.clicked.connect(self.cam_3_callback)

        self.cam_4_button = TabButton('Camera 4')
        self.cam_4_button.clicked.connect(self.cam_4_callback)

        self.log_button = TabButton('Logs')
        self.log_button.clicked.connect(self.log_callback)

        self.tabs = QWidget()
        self.tabs.layout = QVBoxLayout()

        self.tabs.layout.addWidget(self.menu_button)
        self.tabs.layout.addWidget(self.cam_grid_button)
        self.tabs.layout.addWidget(self.cam_1_button)
        self.tabs.layout.addWidget(self.cam_2_button)
        self.tabs.layout.addWidget(self.cam_3_button)
        self.tabs.layout.addWidget(self.cam_4_button)
        self.tabs.layout.addWidget(self.log_button)

        self.tabs.setLayout(self.tabs.layout)

        self.layout.addWidget(self.image)
        self.layout.addWidget(self.tabs)#, Qt.AnchorVerticalCenter)

        self.setLayout(self.layout)

    def menu_callback(self):
        print('hello')
        pass

    def cam_grid_callback(self):
        pass

    def cam_1_callback(self):
        self.tabs.setCurrentIndex(1)

    def cam_2_callback(self):
        pass

    def cam_3_callback(self):
        pass

    def cam_4_callback(self):
        pass

    def log_callback(self):
        pass

    def reset_color(self): # maybe not
        pass

        # self.setCentralWidget(self.menu)

class Tabs(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        # self.menu_tab = CameraTab()
        self.cam_grid_tab = CameraTab()
        self.cam_1_tab = Camera(settings_yml['camera-ports']['cam-1'])
        self.cam_2_tab = Camera(settings_yml['camera-ports']['cam-2'])
        self.cam_3_tab = Camera(settings_yml['camera-ports']['cam-3'])
        self.cam_4_tab = Camera(settings_yml['camera-ports']['cam-4'])
        self.log_tab = LogsTab()


        # self.addTab(self.menu_tab, 'Menu')
        self.addTab(self.cam_grid_tab, 'Camera Grid')
        self.addTab(self.cam_1_tab, 'Camera 1')
        self.addTab(self.cam_2_tab, 'Camera 2')
        self.addTab(self.cam_3_tab, 'Camera 3')
        self.addTab(self.cam_4_tab, 'Camera 4')
        self.addTab(self.log_tab, 'Logs')

        # self.setDocumentMode(True)
        self.tabBar().hide()

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

        for _ in range(20):
            self.update_log('ok')

        # for _ in range(40):
        #     sleep(0.7)
        #     self.update_log('testinfijgwsojdasfpoisjsdafoisjdjsfsais')
    
    def update_log(self, msg):
        logging.debug(msg)

class SettingsTab(QWidget):
    def __init__(self):
        super().__init__()

class TabButton(QPushButton):
    def __init__(self, name):
        super().__init__(name)

        self.setStyleSheet('color: white; font: bold 18px; background: rgb(25, 38, 62); \
            border-radius: 10px; padding: 10px; margin: 2px; border: 5px solid rgb(26, 45, 69)')#'QLabel::hover''{''background: green''}')
        


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

    sys.exit(app.exec())