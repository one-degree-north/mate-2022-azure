from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QTabWidget, QGridLayout, QHBoxLayout, \
    QLabel, QPushButton, QPlainTextEdit, QDialog, QVBoxLayout, QPushButton, QLabel, QLineEdit
from PyQt5.QtCore import Qt, QTimer, QPropertyAnimation, QPoint, QAbstractAnimation, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QTextCursor, QPixmap, QImage, QResizeEvent

from numpy import ndarray
from datetime import datetime

import sys
import yaml
import logging
import cv2

class AzureUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Azure UI')
        self.setStyleSheet('background: rgb(24, 40, 61)')

        self.frame = QWidget()
        self.frame.layout = QHBoxLayout()

        self.menu = MenuBar(self)
        self.active = ActiveTab()

        self.frame.layout.addWidget(self.menu)
        self.frame.layout.addWidget(self.active)

        self.frame.layout.setContentsMargins(0,0,0,0)


        self.frame.setLayout(self.frame.layout)
        self.setCentralWidget(self.frame)

        self.key_logging = False

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Tab:
            if self.menu.isVisible():
                self.menu.hide()
                
            else:
                self.menu.show()

        elif e.key() == Qt.Key_T:
            if self.active.tabBar().isVisible():
                self.active.tabBar().hide()
                self.frame.layout.insertWidget(0, window.menu)
            else:
                self.active.tabBar().show()
                self.frame.layout.removeWidget(window.menu)

            logging.info('Toggled styled tabs')

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

        elif self.key_logging and e.text() != chr(13):
            logging.debug(f'Key "{e.text() if e.text().isascii() else None}" pressed')
        
        
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
        self.pixmap = QPixmap('gui/odn-logo.png')
        self.pixmap.scaled(1, 1, Qt.KeepAspectRatio)

        self.image.setFixedSize(230, 260)

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

        self.tabs.setLayout(self.tabs.layout)


        # Bar layout
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.image)
        self.layout.addStretch()
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
        self.layout.setSpacing(0)

        self.display_width = 320
        self.display_height = 240


        self.cam1 = self.Camera(self, settings_yml['camera-ports']['cam-1'])
        self.cam2 = self.Camera(self, settings_yml['camera-ports']['cam-2'])


        self.layout.addWidget(self.cam1)
        self.layout.addWidget(self.cam2)

        self.setLayout(self.layout)

        self.resizeEvent = self.camera_resize

    def camera_resize(self, resizeEvent: QResizeEvent):
        self.display_width, self.display_height = (self.cam1.width() + self.cam2.width())/2, (self.cam1.height() + self.cam2.height())/2
        

    class Camera(QWidget):
        def __init__(self, parent, port):
            super().__init__()

            self.parent = parent

            self.camera = QLabel()
            self.camera.setGeometry(0, 0, self.parent.display_width, self.parent.display_height)
            self.camera.resize(self.parent.display_width, self.parent.display_height)
            
            self.camera.setMinimumWidth(self.parent.display_width)
            self.camera.setMinimumHeight(self.parent.display_height)

            self.layout = QVBoxLayout()

            self.layout.addWidget(self.camera)

            self.setLayout(self.layout)

            self.thread = VideoThread(port)
            self.thread.change_pixmap_signal.connect(self.update_image)
            self.thread.start()


        def close_event(self, event):
            self.thread.stop()
            event.accept()

        @pyqtSlot(ndarray)
        def update_image(self, cv_img):
            qt_img = self.convert_cv_qt(cv_img)
            self.camera.setPixmap(qt_img)

        def convert_cv_qt(self, cv_img):
            rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            p = convert_to_Qt_format.scaled(int(self.parent.display_width), int(self.parent.display_height), Qt.KeepAspectRatio)
            return QPixmap.fromImage(p)


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(ndarray)

    def __init__(self, port):
        super().__init__()
        self.running = True
        self.port = port

    def run(self):
        self.capture = cv2.VideoCapture(self.port)
        self.count = 0

        while self.running:
            self.ret, self.image = self.capture.read()

            if self.ret:
                self.change_pixmap_signal.emit(self.image)

                k = cv2.waitKey(1)
                if k%256 == 32:
                    cv2.imwrite(f'captures/img_{self.count}.png', self.image)
                    self.count += 1


        self.capture.release()

    def stop(self):
        self.running = False
        self.wait()

class Camera(QWidget):
    def __init__(self, port):
        super().__init__()

        self.display_width = 320
        self.display_height = 240


        self.camera = QLabel()
        self.camera.setGeometry(0, 0, 320, 240)
        self.camera.resize(self.display_width, self.display_height)

        self.camera.setMinimumWidth(320)
        self.camera.setMinimumHeight(240)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.camera)

        self.setLayout(self.layout)

        self.camera.resizeEvent = self.camera_resize

        self.thread = VideoThread(port)
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.start()


    def camera_resize(self, resizeEvent: QResizeEvent):
        self.display_width, self.display_height = self.camera.width(), self.camera.height()

    def close_event(self, event):
        self.thread.stop()
        event.accept()

    @pyqtSlot(ndarray)
    def update_image(self, cv_img):
        qt_img = self.convert_cv_qt(cv_img)
        self.camera.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(ndarray)

    def __init__(self, port):
        super().__init__()
        self.running = True
        self.port = port

    def run(self):
        cap = cv2.VideoCapture(self.port)

        while self.running:

            ret, self.image = cap.read()
            if ret:
                self.change_pixmap_signal.emit(self.image)

                
                # cv2.imwrite('img.png', self.image)

        cap.release()

    def stop(self):
        self.running = False
        self.wait()


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
        self.logger.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s', '%H:%M:%S')) #LOGGING TYPE

        logging.getLogger().addHandler(self.logger)
        logging.getLogger().setLevel(logging.DEBUG)
        

        self.layout = QGridLayout()
        self.layout.addWidget(self.logger.logger)

        self.setLayout(self.layout)


    def reject(self):
        pass

class MenuTab(QWidget):
    def __init__(self):
        super().__init__()

class CommandLine(QLineEdit):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QWidget {
                background: rgb(235, 235, 235);
                border-radius: 5px;
                padding: 10px
            }
        """)

        self.setPlaceholderText('"help" for commands')
        self.setAttribute(Qt.WA_MacShowFocusRect, False) # Mac only
        self.setFocusPolicy(Qt.ClickFocus | Qt.NoFocus)

        self.returnPressed.connect(self.command_event)

    def command_event(self):
        self.split_text = self.text().split(' ')

        self.clear()

        if self.split_text[0] == 'help':
            logging.info(f"""

                Hotkeys:
                TAB - shows/hides the tab bar (if styled)
                t - toggles between styled tabs and regular tabs (styled by default)
                1 through 5 - switches active tab


                Commands:
                help - shows this menu
                return (++) - returns text to logs
                exit - stops the program

                key - toggles logging for keyboard presses (off by default)
                controller - toggles logging for controller (off by default) -- remove maybe


                Key:
                "()" = required
                "[]" = optional
                "+" = any value
                "++" = one or more values
                """)

        elif self.split_text[0] == 'return':
            if not len(self.split_text) > 1:
                logging.error('Please provide additional argument(s)')
            else:
                logging.info(' '.join(self.split_text[1:]))

        elif self.split_text[0] == 'exit':
            print('\033[92m\033[1mAzure UI has been stopped sucessfully\033[0m')
            exit()


        elif self.split_text[0] == 'key':
            if window.key_logging:
                window.key_logging = False
            else:
                window.key_logging = True

            logging.info('Toggled key logging')


        elif self.split_text[0] == 'ping':
            pass # ping to robot (maybe)
        
        elif self.split_text[0] == 'clear':
            pass # clear logs
        
        else:
            logging.error(f'Command "{self.split_text[0]}" does not exist')

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
        self.textbox = CommandLine()


        self.layout = QVBoxLayout()


        self.layout.addWidget(self.logs)
        self.layout.addWidget(self.textbox)

        self.layout.setSpacing(0)

        self.setLayout(self.layout)


class TabButton(QPushButton):
    def __init__(self, name):
        super().__init__(name)

        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    spread: pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(25, 38, 62), stop:1 rgb(26, 45, 69)
                );
                color: rgb(210, 211, 210);

                padding: 10px;
                font: bold 20px;

                border-radius: 10px
            }

            QPushButton:hover {
                background: rgb(45, 58, 82)
            }
        """)


if __name__ == '__main__':
    # Defining global variables/functions

    with open('gui/settings.yml', 'r') as f:
        settings_yml = yaml.safe_load(f)
    print(settings_yml)

    # Create UI application
    app = QApplication([])

    window = AzureUI()
    window.show()

    logging.info('Azure UI has loaded sucessfully')

    sys.exit(app.exec())