from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PyQt5.QtCore import Qt, pyqtSlot

from menu import MenuBar
from active import ActiveTab

import sys
import os

import cv2
import logging
from datetime import datetime

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

        self.menu.logs.hide()

        self.key_logging = False

        self.resize(800, 600)

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

        elif e.key() == Qt.Key_L:
            # print()
            if self.menu.logs.isVisible():# and self.active.currentIndex() != 2:
                self.menu.logs.hide()
            else:
                self.menu.logs.show()

        elif e.key() == Qt.Key_Space:# and len(self.active.cam_tab.image):
            try:
                file_name = f'captures/{datetime.now().strftime("%d-%m-%y_%H:%M:%S")}.png'
                cv2.imwrite(file_name, self.active.cam_tab.image)

                logging.info(f'Image captured as {file_name}')

            except cv2.error:
                logging.error('Camera has not yet loaded; please try again')

        elif self.active.logs_tab.textbox.key_logging and e.text() != chr(13):
            logging.debug(f'Key "{e.text() if e.text().isascii() else None}" pressed')
        


if __name__ == '__main__':
    app = QApplication([])

    window = AzureUI()
    window.show()

    # Setup 
    logging.info('Starting up Azure UI...')

    # Create "captures" directory
    try:
        os.makedirs('captures')
        logging.warn('No captures directory detected; creating one for you!')
    except FileExistsError:
        pass

    logging.info('Azure UI has loaded sucessfully')
    logging.info('Captures are saved as "d-m-y_H:M:S"')
    print('\033[92m\033[1mAzure UI has loaded sucessfully\033[0m')

    sys.exit(app.exec())