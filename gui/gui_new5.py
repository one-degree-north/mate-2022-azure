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
        self.setStyleSheet('background: rgb(24, 40, 61)')

        self.frame = QWidget()
        self.frame.layout = QHBoxLayout()

        self.menu = MenuBar(self)
        self.active = ActiveTab()


        # self.menu = Menu(self)
        # self.tabs = Tabs()

        # # self.menu.setStyleSheet('background: rgb(17, 28, 43); border-top-right-radius: 20px; border-bottom-right-radius: 20px')
        # # self.menu.setFixedWidth(300)


        self.frame.layout.addWidget(self.menu)
        self.frame.layout.addWidget(self.active)

        self.frame.layout.setContentsMargins(0,0,0,0)


        self.frame.setLayout(self.frame.layout)
        self.setCentralWidget(self.frame)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_H:
            if not self.menu.isVisible():
                self.menu.show()
            else:
                self.menu.hide()
            self.update() #######
        elif e.key() == Qt.Key_1:
            self.active.setCurrentIndex(0)
        elif e.key() == Qt.Key_2:
            self.active.setCurrentIndex(1)
        elif e.key() == Qt.Key_3:
            self.active.setCurrentIndex(2)
        elif e.key() == Qt.Key_4:
            self.active.setCurrentIndex(3)
        elif e.key() == Qt.Key_5:
            self.active.setCurrentIndex(4)
        
class MenuBar(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self.setStyleSheet("""
            QWidget {
                background: rgb(17, 28, 43);
                border-top-right-radius: 20px;
                border-bottom-right-radius: 20px;
            }
        """)

        # Image
        self.image = QLabel()
        self.pixmap = QPixmap('gui/my-image.png')
        self.pixmap.scaled(0.3, 0.3, Qt.KeepAspectRatio)

        self.image.setFixedSize(250, 280)

        self.image.setPixmap(self.pixmap)
        self.image.setAlignment(Qt.AlignHCenter)
        self.image.setStyleSheet("""
            QWidget {
                padding: 10px
            }
        """)

        # Tab buttons
        self.menu_button = TabButton('Menu')
        self.menu_button.clicked.connect(lambda: parent.active.setCurrentIndex(0))
        
        self.grid_button = TabButton('Camera Grid')
        self.grid_button.clicked.connect(lambda: parent.active.setCurrentIndex(1))

        self.cam1_button = TabButton('Camera 1')
        self.cam1_button.clicked.connect(lambda: parent.active.setCurrentIndex(2))

        self.cam2_button = TabButton('Camera 2')
        self.cam2_button.clicked.connect(lambda: parent.active.setCurrentIndex(3))

        self.logs_button = TabButton('Logs')
        self.logs_button.clicked.connect(lambda: parent.active.setCurrentIndex(4))

        # Tab layout
        self.tabs = QWidget()
        self.tabs.layout = QVBoxLayout()

        self.tabs.layout.addWidget(self.menu_button)
        self.tabs.layout.addWidget(self.grid_button)
        self.tabs.layout.addWidget(self.cam1_button)
        self.tabs.layout.addWidget(self.cam2_button)
        self.tabs.layout.addWidget(self.logs_button)

        # self.tabs.setFixedSize(100,200)

        self.tabs.setLayout(self.tabs.layout)


        # Bar layout
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.image)
        self.layout.addWidget(self.tabs)

        self.setLayout(self.layout)
    

class ActiveTab(QTabWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        
        self.menu_tab = MenuTab()
        self.grid_tab = CameraGrid()
        self.cam1_tab = Camera(settings_yml['camera-ports']['cam-1'])
        self.cam2_tab = Camera(settings_yml['camera-ports']['cam-2'])
        self.logs_tab = LogsTab()


        self.addTab(self.menu_tab, 'Menu')
        self.addTab(self.grid_tab, 'Camera Grid')
        self.addTab(self.cam1_tab, 'Camera 1')
        self.addTab(self.cam2_tab, 'Camera 2')
        self.addTab(self.logs_tab, 'Logs')

        self.setTabPosition(QTabWidget.West)

        self.setDocumentMode(True)
        self.tabBar().hide()


class CameraGrid(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()
        # self.layout.setSpacing(0)

        self.cam1 = Camera(settings_yml['camera-ports']['cam-1'])
        self.cam2 = Camera(settings_yml['camera-ports']['cam-2'])

        self.layout.addWidget(self.cam1)
        self.layout.addWidget(self.cam2)

        self.setLayout(self.layout)


class RawCamera(QCameraViewfinder):
    def __init__(self, port):
        super().__init__()

        self.camera = QCamera(cameras[port])
        self.camera.setViewfinder(self)
        self.camera.start()

class Camera(QWidget):
    def __init__(self, port):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        # self.setStyleSheet("""
        #     QWidget {
        #         background: rgb(17, 28, 43);
        #         border-radius: 8px;
        #         margin: 10px
        #     }
        # """)

        # Defining objects
        self.camera = RawCamera(port)
        self.label = QLabel(f'Port {port}')

        self.label.setStyleSheet("""
            QLabel {
                color: white;
                font: 30px bold
            }
        """)

        # Layout
        self.layout = QGridLayout()

        self.layout.addWidget(self.camera, 0,0)
        self.layout.addWidget(self.label, 1,0)

        self.setLayout(self.layout)


class LoggerBox(logging.Handler):
    def __init__(self, parent):
        super().__init__()
        self.logger = QPlainTextEdit()
        self.logger.setReadOnly(True)

    
    def emit(self, record):
        self.msg = self.format(record)
        self.logger.appendPlainText(self.msg)


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

class MenuTab(QWidget):
    def __init__(self):
        super().__init__()

class LogsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(245, 245, 245);
                border-radius: 10px;
                margin: 20px
            }
        """)

        self.logs = Logs()

        self.layout = QVBoxLayout()


        self.layout.addWidget(self.logs)

        self.setLayout(self.layout)
        self.setAttribute(Qt.WA_TranslucentBackground)





class TabButton(QPushButton):
    def __init__(self, name):
        super().__init__(name)

        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    spread: pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(25, 38, 62), stop:1 rgb(26, 45, 69)
                );
                color: white;

                padding: 20px;
                font: bold 18px;

                border-radius: 10px
            }

            QPushButton:hover {
                background: rgb(45, 58, 82)
            }
        """)

        # self.setStyleSheet('color: white; font: bold 18px; background: rgb(25, 38, 62); \
        #     border-radius: 10px; padding: 10px; margin: 2px; border: 5px solid rgb(26, 45, 69)')#'QLabel::hover''{''background: green''}')
        


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