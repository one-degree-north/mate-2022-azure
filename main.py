from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QObject, QThread

from gui.menu import MenuBar
from gui.active import ActiveTab

from controller import Controller

from threading import Thread
from time import sleep

from XInput import *

import serial
import sys
import os

import cv2
import logging
from datetime import datetime


class AzureUI(QMainWindow):
    def __init__(self, port: str, baud_rate: int):
        super().__init__()

        self.controllers = (
            Controller((150., 100.), None),
            Controller((450., 100.), None),
            Controller((150., 300.), None),
            Controller((450., 300.), None)
        )

        self.setWindowTitle('Azure UI')
        self.setStyleSheet('background: rgb(24, 40, 61)')

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
        
        self.ser = serial.Serial(port, baud_rate)
        self.ser.close()
        self.ser.open()

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
        elif e.key() == Qt.Key_L:
            if self.menu.logs.isVisible():
                self.menu.logs.hide()
            else:
                self.menu.logs.show()
        elif e.key() == Qt.Key_C:
            try:
                timestamp = datetime.now().strftime(f'%d-%m-%y_%H:%M:%S.%f')[:-4]

                filename = f'captures/{timestamp}.png'
                cv2.imwrite(filename, self.active.cam_tab.image)

                logging.info(f"""Captured: captures/{timestamp}
                """)
            except cv2.error:
                logging.error('Camera has not yet loaded, please wait')
        elif e.key() == Qt.Key_A:
            self.value_rightMot = 200
            self.packet_rightThruster = chr(1) + chr(7) + chr(self.value_rightMot) + chr(255)
            self.ser.write(self.packet_rightThruster.encode("latin"))
        elif e.key() == Qt.Key_D:
            self.value_rightMot = 100
            self.packet_rightThruster = chr(1) + chr(7) + chr(self.value_rightMot) + chr(255)
            self.ser.write(self.packet_rightThruster.encode("latin"))
        elif e.key() == Qt.Key_W:
            self.value_motor = 127
            self.packet_up = chr(1) + chr(13) + chr(self.value_motor) + chr(255)
            self.ser.write(self.packet_up.encode("latin"))
        elif e.key() == Qt.Key_S:
            self.value_motor = 254
            self.packet_down = chr(1) + chr(13) + chr(self.value_motor) + chr(255)
            self.ser.write(self.packet_down.encode("latin"))
        elif e.key() == Qt.Key_Up:
            self.value_forward = 100
            self.packet_forward = chr(1) + chr(2) + chr(self.value_forward) + chr(255)
            self.ser.write(self.packet_forward.encode("latin"))
            self.value_backward = 200
            self.packet_backward = chr(1) + chr(3) + chr(self.value_backward) + chr(255)
            self.ser.write(self.packet_backward.encode("latin"))
        elif e.key() == Qt.Key_Down:
            self.value_forward = 200
            self.packet_forward = chr(1) + chr(2) + chr(self.value_forward) + chr(255)
            self.ser.write(self.packet_forward.encode("latin"))
            self.value_backward = 100
            self.packet_backward = chr(1) + chr(3) + chr(self.value_backward) + chr(255)
            self.ser.write(self.packet_backward.encode("latin"))
        elif e.key() == Qt.Key_Escape:
            self.kill_packet = chr(1) + chr(14) + chr(127) + chr(255)
            self.ser.write(self.kill_packet.encode("latin"))
    
    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_A or e.key() == Qt.Key_D:
            self.value_rightMot = 0
            self.packet_rightThruster = chr(1) + chr(7) + chr(self.value_rightMot) + chr(255)
            self.ser.write(self.packet_rightThruster.encode("latin"))
        elif e.key() == Qt.Key_W or e.key() == Qt.Key_S:
            self.value_motor = 0
            self.packet_motor = chr(1) + chr(13) + chr(self.value_motor) + chr(255)
            self.ser.write(self.packet_motor.encode("latin"))
        elif e.key() == Qt.Key_Up or e.key() == Qt.Key_Down:
            self.value_motor = 0
            self.packet_motor_forward = chr(1) + chr(2) + chr(self.value_motor) + chr(255)
            self.ser.write(self.packet_motor_forward.encode("latin"))
            self.packet_motor_backward = chr(1) + chr(3) + chr(self.value_motor) + chr(255)
            self.ser.write(self.packet_motor_backward.encode("latin"))

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

    # Backend
    backend_thread = Thread(target=window.run_controller)
    backend_thread.start()

    # Start UI
    sys.exit(app.exec())
