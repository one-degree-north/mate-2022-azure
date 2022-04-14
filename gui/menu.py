from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap

from gui.tabs.console import MiniLogsWindow

import cv2

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

        self.setFixedWidth(250)

        # Image
        self.image = cv2.imread('gui/odn-logo.png', cv2.IMREAD_UNCHANGED)
        self.image = QImage(self.image.data, self.image.shape[1], self.image.shape[0], QImage.Format_ARGB32)

        
        self.image_frame = QLabel()
        self.image_frame.setPixmap(QPixmap.fromImage(self.image))

        self.image_frame.setStyleSheet("""
            QWidget {
                padding: 10px
            }
        """)

        self.image_frame.setAlignment(Qt.AlignCenter)

        # Mini logs
        self.logs = MiniLogsWindow()

        # Tab buttons
        self.menu_button = TabButton('Menu')
        self.menu_button.clicked.connect(lambda: parent.active.setCurrentIndex(0))

        # self.cam_button = TabButton('Camera')
        # self.cam_button.clicked.connect(lambda: parent.active.setCurrentIndex(1))

        self.console_button = TabButton('Console')
        self.console_button.clicked.connect(lambda: parent.active.setCurrentIndex(1))

        # Tab layout
        self.tabs = QWidget()
        self.tabs.layout = QVBoxLayout()

        self.tabs.layout.addWidget(self.menu_button)
        # self.tabs.layout.addWidget(self.cam_button)
        self.tabs.layout.addWidget(self.console_button)

        self.tabs.setLayout(self.tabs.layout)

        # Bar layout
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.image_frame)
        self.layout.addStretch()
        self.layout.addWidget(self.logs)
        self.layout.addWidget(self.tabs)

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