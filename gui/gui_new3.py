from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QGridLayout, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit, QDialog, QVBoxLayout, QPushButton, QLabel, QToolTip, QLayout, QStyle
from PyQt5.QtMultimedia import QCameraInfo, QCamera
from PyQt5.QtMultimediaWidgets import QCameraViewfinder
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor, QPixmap

import sys
import yaml
import logging
# maybe qstackedlayout/widget

class AzureUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Azure UI')
        self.setStyleSheet('background: rgb(24, 40, 61)')#; margin: 6px')

        self.frame = QWidget()
        self.frame.layout = QHBoxLayout()

        # Window setup
        self.menu_window = MenuWindow()
        self.grid_window = GridWindow()
        self.cam1_window = Camera(settings['camera-ports']['cam-1'])
        self.cam2_window = Camera(settings['camera-ports']['cam-2'])
        self.cam3_window = Camera(settings['camera-ports']['cam-3'])
        self.cam4_window = Camera(settings['camera-ports']['cam-4'])
        self.logs_window = Logs()

        self.active = self.grid_window

        # Tab events
        self.tabs = Tabs()

        self.tabs.grid_button.clicked.connect(lambda: self.change_tab(self.grid_window))
        self.tabs.cam1_button.clicked.connect(lambda: self.change_tab(self.cam1_window))
        self.tabs.cam2_button.clicked.connect(lambda: self.change_tab(self.cam2_window))
        self.tabs.cam3_button.clicked.connect(lambda: self.change_tab(self.cam3_window))
        self.tabs.cam4_button.clicked.connect(lambda: self.change_tab(self.cam4_window))
        self.tabs.logs_button.clicked.connect(lambda: self.change_tab(self.logs_window))

        
        

        # self.menu.setStyleSheet('background: rgb(17, 28, 43); border-top-right-radius: 20px; border-bottom-right-radius: 20px')
        # self.menu.setFixedWidth(300)


        self.frame.layout.addWidget(self.tabs)
        self.frame.layout.addWidget(self.active)

        self.frame.layout.setContentsMargins(0,0,0,0)


        self.frame.setLayout(self.frame.layout)
        self.setCentralWidget(self.frame)

    def change_tab(self, new):
        self.frame.layout.replaceWidget(self.frame.layout.itemAt(1).widget(), new)
        
        
        
class ActiveWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        # self.setStyleSheet('background: rgb(17, 28, 43); border-top-right-radius: 20px; border-bottom-right-radius: 20px')
        # self.setFixedWidth(300)


        # Active window setup
        self.menu_window = MenuWindow()
        self.grid_window = GridWindow()
        self.cam1_window = Camera(settings['camera-ports']['cam-1'])
        self.cam2_window = Camera(settings['camera-ports']['cam-2'])
        self.cam3_window = Camera(settings['camera-ports']['cam-3'])
        self.cam4_window = Camera(settings['camera-ports']['cam-4'])
        self.logs_window = Logs()

        # # Tab events
        # self.tabs = parent.menu

        


        # Layout
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.tabs)
        self.layout.addWidget(self.grid_window) # default is menu

        self.setLayout(self.layout)
    
    def change_tab(self, new):
        # self.layout.removeWidget(self.menu_window)
        # self.layout.removeWidget(self.grid_window)
        # self.layout.removeWidget(self.cam1_window)
        # self.layout.removeWidget(self.cam2_window)
        # self.layout.removeWidget(self.cam3_window)
        # self.layout.removeWidget(self.cam4_window)
        # self.layout.removeWidget(self.logs_window)
        self.layout.replaceWidget(new)

        # self.menu_window.close()
        # self.grid_window.close()
        # self.cam1_window.close()
        # self.cam2_window.close()
        # self.cam3_window.close()
        # self.cam4_window.close()
        # self.logs_window.close()

        # self.layout.addWidget(new)
        # self.layout.update()


class Tabs(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet('background: rgb(17, 28, 43); border-top-right-radius: 20px; border-bottom-right-radius: 20px')
        self.setFixedWidth(300)


        # Defining tabs
        self.grid_button = TabButton('Camera Grid')
        # self.cams_button.clicked.connect(lambda: parent.tabs.setCurrentIndex(0))

        self.cam1_button = TabButton('Camera 1')
        # self.cam1_button.clicked.connect(lambda: parent.tabs.setCurrentIndex(1))

        self.cam2_button = TabButton('Camera 2')
        # self.cam2_button.clicked.connect(lambda: parent.tabs.setCurrentIndex(2))

        self.cam3_button = TabButton('Camera 3')
        # self.cam3_button.clicked.connect(lambda: parent.tabs.setCurrentIndex(3))

        self.cam4_button = TabButton('Camera 4')
        # self.cam4_button.clicked.connect(lambda: parent.tabs.setCurrentIndex(4))

        self.logs_button = TabButton('Logs')
        # self.logs_button.clicked.connect(lambda: parent.tabs.setCurrentIndex(5))


        # Layout
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.grid_button)
        self.layout.addWidget(self.cam1_button)
        self.layout.addWidget(self.cam2_button)
        self.layout.addWidget(self.cam3_button)
        self.layout.addWidget(self.cam4_button)
        self.layout.addWidget(self.logs_button)

        self.setLayout(self.layout)



class MenuWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

# class Tab_s(QTabWidget):
#     def __init__(self):
#         super().__init__()
#         self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
#         # self.menu_tab = CameraTab()
#         self.cam_grid_tab = CameraTab()
#         self.cam_1_tab = Camera(settings_yml['camera-ports']['cam-1'])
#         self.cam_2_tab = Camera(settings_yml['camera-ports']['cam-2'])
#         self.cam_3_tab = Camera(settings_yml['camera-ports']['cam-3'])
#         self.cam_4_tab = Camera(settings_yml['camera-ports']['cam-4'])
#         self.log_tab = LogsTab()


#         # self.addTab(self.menu_tab, 'Menu')
#         self.addTab(self.cam_grid_tab, 'Camera Grid')
#         self.addTab(self.cam_1_tab, 'Camera 1')
#         self.addTab(self.cam_2_tab, 'Camera 2')
#         self.addTab(self.cam_3_tab, 'Camera 3')
#         self.addTab(self.cam_4_tab, 'Camera 4')
#         self.addTab(self.log_tab, 'Logs')

#         # self.setDocumentMode(True)
#         self.tabBar().hide()

class GridWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QGridLayout()
        # self.layout.setSpacing(0)

        self.cam1 = Camera(settings['camera-ports']['cam-1'])
        self.cam2 = Camera(settings['camera-ports']['cam-2'])
        self.cam3 = Camera(settings['camera-ports']['cam-3'])
        self.cam4 = Camera(settings['camera-ports']['cam-4'])

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


class Logs(QDialog, QPlainTextEdit):
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

# class SettingsTab(QWidget):
#     def __init__(self):
#         super().__init__()

class TabButton(QPushButton):
    def __init__(self, name):
        super().__init__(name)

        self.setStyleSheet('color: white; font: bold 18px; background: rgb(25, 38, 62); \
            border-radius: 10px; padding: 10px; margin: 2px; border: 5px solid rgb(26, 45, 69)')#'QLabel::hover''{''background: green''}')
        


if __name__ == '__main__':
    # Defining global variables
    cameras = QCameraInfo.availableCameras()

    with open('gui/settings.yml', 'r') as f:
        settings = yaml.safe_load(f)
    print(settings)


    # Create UI application
    app = QApplication([])

    window = AzureUI()
    # window.setStyle(QStyle('fusion'))

    window.show()

    sys.exit(app.exec())