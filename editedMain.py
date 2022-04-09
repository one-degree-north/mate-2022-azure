from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QObject, QThread

from gui.menu import MenuBar
from gui.active import ActiveTab

from threading import Thread
from time import sleep

import serial
import sys
import os

import cv2
import logging
from datetime import datetime


class AzureUI(QMainWindow):
    def __init__(self, port: str, baud_rate: int):
        super().__init__()
        

        self.ser = serial.Serial(port, baud_rate)
        self.ser.close()
        self.ser.open()
        self.claw_closed = True
        self.servo_closed = chr(1) + chr(9) + chr(11) + chr(255)
        self.ser.write(self.packet_servo.encode("latin"))

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
        elif e.key() == Qt.Key_W:
            self.value_forward = 170
            self.packet_rightThruster = chr(1) + chr(6) + chr(self.value_forward) + chr(255)
            self.ser.write(self.packet_rightThruster.encode("latin"))
            self.packet_leftThruster = chr(1) + chr(7) + chr(self.value_forward) + chr(255)
            self.ser.write(self.packet_leftThruster.encode("latin"))
        elif e.key() == Qt.Key_S:
            self.value_backward = 130
            self.packet_rightThruster = chr(1) + chr(6) + chr(self.value_backward) + chr(255)
            self.ser.write(self.packet_rightThruster.encode("latin"))
            self.packet_leftThruster = chr(1) + chr(7) + chr(self.value_backward) + chr(255)
            self.ser.write(self.packet_leftThruster.encode("latin"))
        elif e.key() == Qt.Key_A:
            # turn left - rightThruster forward, leftThruster backwards
            self.value_rightMot = 160
            self.packet_rightForward = chr(1) + chr(6) + chr(self.value_rightMot) + chr(255)
            self.ser.write(self.self.packet_rightForward.encode("latin"))
            self.value_lefttMot = 140
            self.packet_leftBackward = chr(1) + chr(7) + chr(self.value_lefttMot) + chr(255)
            self.ser.write(self.packet_leftBackward)
        elif e.key() == Qt.Key_D:
            # turn right - leftThruster forward, rightThruster backwards
            self.value_leftMot = 160
            self.packet_leftForward = chr(1) + chr(7) + chr(self.value_leftMot) + chr(255)
            self.ser.write(self.self.packet_rightForward.encode("latin"))
            self.value_rightMot = 140
            self.packet_rightBackward = chr(1) + chr(6) + chr(self.value_rightMot) + chr(255)
            self.ser.write(self.packet_leftBackward.encode("latin"))
        elif e.key() == Qt.Key_Up:
            # botUp
            self.packet_up = chr(1) + chr(13) + chr(127) + chr(255)
            self.ser.write(self.packet_up.encode("latin"))
        elif e.key() == Qt.Key_Down:
            # botDown
            self.packet_down = chr(1) + chr(13) + chr(254) + chr(255)
            self.ser.write(self.packet_down.encode("latin"))
        elif e.key() == Qt.Key_Escape:
            self.kill_packet = chr(1) + chr(14) + chr(127) + chr(255)
            self.ser.write(self.kill_packet.encode("latin"))
        elif e.key() == Qt.Key_X:
            if self.claw_closed == True:
                # claw should open now
                self.value_servoGrab = 12
                self.packet_servoGrab = chr(1) + chr(9) + chr(self.value_servoGrab) + chr(255)
                self.ser.write(self.packet_servoGrab.encode("latin"))
                self.claw_closed = False
            else:
                # claw should close now
                self.value_servo = 11
                self.packet_servo = chr(1) + chr(9) + chr(self.value_servo) + chr(255)
                self.ser.write(self.packet_servo.encode("latin"))
                self.open = True
        elif e.key() == Qt.Key_C:
            #servoRotate goes left
            self.value_servoRotate = 15
            self.packet_servoRotate = chr(1) + chr(8) + chr(self.value_servoRotate) + chr(255)
            self.ser.write(self.packet_servoRotate.encode("latin"))
        elif e.key() == Qt.Key_V:
            #servoRotate goes right
            self.value_servoRotate = 16
            self.packet_servoRotate = chr(1) + chr(8) + chr(self.value_servoRotate) + chr(255)
            self.ser.write(self.packet_servoRotate)
    
    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_W or e.key() == Qt.Key_S:
            self.value_stop = 150
            self.packet_leftMot = chr(1) + chr(7) + chr(self.value_stop) + chr(255)
            self.ser.write(self.packet_leftMot.encode("latin"))
            self.packet_rightMot = chr(1) + chr(6) + chr(self.value_stop) + chr(255)
            self.ser.write(self.packet_rightMot.encode("latin"))
        elif e.key() == Qt.Key_A or e.key() == Qt.Key_D:
            self.value_stop = 150
            self.packet_leftMot = chr(1) + chr(7) + chr(self.value_stop) + chr(255)
            self.ser.write(self.packet_leftMot.encode("latin"))
            self.packet_rightMot = chr(1) + chr(6) + chr(self.value_stop) + chr(255)
            self.ser.write(self.packet_rightMot.encode("latin"))
        elif e.key() == Qt.Key_Up or e.key() == Qt.Key_Down:
            self.value_stop = 150
            self.packet_stop = chr(1) + chr(13) + chr(self.value_stop) + chr(255)
            self.ser.write(self.packet_stop.encode("latin"))
       elif e.key() == Qt.Key_C or Qt.Key_V:
            #stop servo
            self.value_servoRotate_stop = 17
            self.packet_servoRotate = chr(1) + chr(8) + chr(self.value_servoRotate_stop) + chr(255)
            self.ser.write(self.packet_servoRotate.encode("latin"))
        
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
