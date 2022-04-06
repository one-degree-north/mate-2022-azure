from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

from menu import MenuBar
from active import ActiveTab

import serial

import sys
import os

import cv2
import logging
from datetime import datetime


class AzureUI(QMainWindow):
    def __init__(self):#, port: str, baud_rate: int):
        # self.ser = serial.Serial(port, baud_rate)
        # self.ser.close()
        # self.ser.open()

        super().__init__()

        self.setWindowTitle('Azure UI')
        self.setStyleSheet('background: rgb(24, 40, 61)')

        # self.setFixedSize(1000,800)

        self.frame = QWidget()
        self.frame.layout = QHBoxLayout()

        self.menu = MenuBar(self)
        self.active = ActiveTab(self)

        self.frame.layout.addWidget(self.menu)
        self.frame.layout.addWidget(self.active)

        self.frame.layout.setContentsMargins(0,0,0,0)


        self.frame.setLayout(self.frame.layout)
        self.setCentralWidget(self.frame)

        self.menu.logs.hide()

        self.resize(800, 600)

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_QuoteLeft:
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
        elif e.key() == Qt.Key_6:
            self.active.setCurrentIndex(5)
        elif e.key() == Qt.Key_L:
            if self.menu.logs.isVisible():
                self.menu.logs.hide()
            else:
                self.menu.logs.show()
        elif e.key() == Qt.Key_C:

            try:
                timestamp = datetime.now().strftime(f'%d-%m-%y_%H:%M:%S.%f')[:-4]
                os.mkdir(f'captures/{timestamp}')

                file1_name = f'captures/{timestamp}/cap1.png'
                cv2.imwrite(file1_name, self.active.cam1_tab.image)

                file2_name = f'captures/{timestamp}/cap2.png'
                cv2.imwrite(file2_name, self.active.cam2_tab.image)


                logging.info(f"""captures/{timestamp}\n↪ cap1.png\n↪ cap2.png
                """)
            except FileNotFoundError:
                os.mkdir('captures')
                logging.warning('The "captures" folder was not found; one has been created for you')

            except cv2.error:
                logging.error('Camera has not yet loaded, please wait')

        elif e.key() == Qt.Key_W and not e.isAutoRepeat():
            packet_rightThruster = chr(1) + chr(6) + chr(127) + chr(255)
            self.ser.write(packet_rightThruster.encode("latin"))
            packet_leftThruster = chr(1) + chr(7) + chr(127) + chr(255)
            self.ser.write(packet_leftThruster.encode("latin"))
        elif e.key() == Qt.Key_S and not e.isAutoRepeat():
            packet_rightThruster = chr(1) + chr(6) + chr(128) + chr(255)
            self.ser.write(packet_rightThruster.encode("latin"))
            packet_leftThruster = chr(1) + chr(7) + chr(128) + chr(255)
            self.ser.write(packet_leftThruster.encode("latin"))     
        elif e.key() == Qt.Key_A and not e.isAutoRepeat():
            packet_rightThruster = chr(1) + chr(6) + chr(128) + chr(255)
            self.ser.write(packet_rightThruster.encode("latin"))
            packet_leftThruster = chr(1) + chr(7) + chr(127) + chr(255)
            self.ser.write(packet_leftThruster.encode("latin"))
        elif e.key() == Qt.Key_D and not e.isAutoRepeat():
            packet_rightThruster = chr(1) + chr(6) + chr(127) + chr(255)
            self.ser.write(packet_rightThruster.encode("latin"))
            packet_leftThruster = chr(1) + chr(7) + chr(128) + chr(255)
            self.ser.write(packet_leftThruster.encode("latin"))
        elif e.key() == Qt.Key_Up and not e.isAutoRepeat():
            packet = chr(1) + chr(13) + chr(127) + chr(255)
            self.ser.write(packet.encode("latin"))
        elif e.key() == Qt.Key_Down and not e.isAutoRepeat():
            packet = chr(1) + chr(13) + chr(254) + chr(255)
            self.ser.write(packet.encode("latin"))   
        elif self.active.console_tab.textbox.key_logging and e.text() != chr(13):
            logging.debug(f'Key "{e.text() if e.text().isascii() else None}" pressed')

    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_W and not e.isAutoRepeat():
            packet_rightThruster = chr(1) + chr(6) + chr(0) + chr(255)
            self.ser.write(packet_rightThruster.encode("latin"))
            packet_leftThruster = chr(1) + chr(7) + chr(0) + chr(255)
            self.ser.write(packet_leftThruster.encode("latin"))
        elif e.key() == Qt.Key_S and not e.isAutoRepeat():
            packet_rightThruster = chr(1) + chr(6) + chr(0) + chr(255)
            self.ser.write(packet_rightThruster.encode("latin"))
            packet_leftThruster = chr(1) + chr(7) + chr(0) + chr(255)
            self.ser.write(packet_leftThruster.encode("latin"))     
        elif e.key() == Qt.Key_A and not e.isAutoRepeat():
            packet_rightThruster = chr(1) + chr(6) + chr(0) + chr(255)
            self.ser.write(packet_rightThruster.encode("latin"))
            packet_leftThruster = chr(1) + chr(7) + chr(0) + chr(255)
            self.ser.write(packet_leftThruster.encode("latin"))
        elif e.key() == Qt.Key_D and not e.isAutoRepeat():
            packet_rightThruster = chr(1) + chr(6) + chr(0) + chr(255)
            self.ser.write(packet_rightThruster.encode("latin"))
            packet_leftThruster = chr(1) + chr(7) + chr(0) + chr(255)
            self.ser.write(packet_leftThruster.encode("latin"))
        elif e.key() == Qt.Key_Up and not e.isAutoRepeat():
            packet = chr(1) + chr(13) + chr(0) + chr(255)
            self.ser.write(packet.encode("latin"))
        elif e.key() == Qt.Key_Down and not e.isAutoRepeat():
            packet = chr(1) + chr(13) + chr(0) + chr(255)
            self.ser.write(packet.encode("latin"))

if __name__ == '__main__':
    app = QApplication([])

    app.setWindowIcon(QIcon('gui/icon.png'))

    window = AzureUI()
    window.show()

    # Setup 
    logging.info('Starting up Azure UI...')

    # Create "captures" directory
    try:
        os.mkdir('captures')
        logging.warning('No captures directory detected; one has been generated for you!')
    except FileExistsError:
        pass

    logging.info('Images are saved under the "captures" directory in the format "d-m-y_H:M:S"')

    logging.info('Azure UI has loaded sucessfully\n\n')
    print('\033[92m\033[1mAzure UI has loaded sucessfully\033[0m')

    sys.exit(app.exec())
