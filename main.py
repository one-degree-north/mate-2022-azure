from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QObject, QThread

from gui.menu import MenuBar
from gui.active import ActiveTab

from threading import Thread
from time import sleep

import serial
import yaml
import sys
import os

import cv2
import logging
from datetime import datetime

class AzureUI(QMainWindow):
    def __init__(self):#, port: str, baud_rate: int):
        super().__init__()

        # self.ser = serial.Serial(port, baud_rate)
        # self.ser.close()
        # self.ser.open()
        
        self.claw_closed = True
        # self.servo_closed = chr(1) + chr(9) + chr(11) + chr(255)
        # self.ser.write(self.servo_closed.encode("latin"))

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
        self.resize(600, 400)

        self.ui_controls = []
        self.bot_controls = []

        # self.control_ui_logging = False
        # self.control_bot_logging = False
        # self.keys_logging = True

    def keyPressEvent(self, e):
        # if self.control_ui_logging:
        #     logging.debug(k.text())
            
        # elif self.control_bot_logging: 
        #     logging.debug(k.text())

        
        # # elif self.keys_logging and not (e.key() in ui_controls or e.key() in bot_controls):


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

                logging.info(f'Captured: captures/{timestamp}.png')
            except cv2.error:
                logging.error('Camera has not yet loaded, please wait')


        elif e.key() == Qt.Key_A:
            # self.value_rightMot = 170
            # self.packet_rightThruster = chr(1) + chr(7) + chr(self.value_rightMot) + chr(255)
            # self.ser.write(self.packet_rightThruster.encode("latin"))

            if self.active.console_tab.command_line.controls_logging:
                logging.debug("'a' pressed")
        elif e.key() == Qt.Key_D:
            # self.value_rightMot = 130
            # self.packet_rightThruster = chr(1) + chr(7) + chr(self.value_rightMot) + chr(255)
            # self.ser.write(self.packet_rightThruster.encode("latin"))

            if self.active.console_tab.command_line.controls_logging:
                logging.debug("'d' pressed")
        elif e.key() == Qt.Key_W:
            # self.value_motor = 127
            # self.packet_up = chr(1) + chr(13) + chr(self.value_motor) + chr(255)
            # self.ser.write(self.packet_up.encode("latin"))

            if self.active.console_tab.command_line.controls_logging:
                logging.debug("'w' pressed")
        elif e.key() == Qt.Key_S:
            # self.value_motor = 254
            # self.packet_down = chr(1) + chr(13) + chr(self.value_motor) + chr(255)
            # self.ser.write(self.packet_down.encode("latin"))
            
            if self.active.console_tab.command_line.controls_logging:
                logging.debug("'s' pressed")
        elif e.key() == Qt.Key_Up:
            # self.value_forward = 130
            # self.packet_forward = chr(1) + chr(2) + chr(self.value_forward) + chr(255)
            # self.ser.write(self.packet_forward.encode("latin"))
            # self.value_backward = 170
            # self.packet_backward = chr(1) + chr(3) + chr(self.value_backward) + chr(255)
            # self.ser.write(self.packet_backward.encode("latin"))

            if self.active.console_tab.command_line.controls_logging:
                logging.debug("Up arrow pressed")
        elif e.key() == Qt.Key_Down:
            # self.value_forward = 170
            # self.packet_forward = chr(1) + chr(2) + chr(self.value_forward) + chr(255)
            # self.ser.write(self.packet_forward.encode("latin"))
            # self.value_backward = 130
            # self.packet_backward = chr(1) + chr(3) + chr(self.value_backward) + chr(255)
            # self.ser.write(self.packet_backward.encode("latin"))

            if self.active.console_tab.command_line.controls_logging:
                logging.debug("Down arrow pressed")
        elif e.key() == Qt.Key_Escape:
            # self.kill_packet = chr(1) + chr(14) + chr(127) + chr(255)
            # self.ser.write(self.kill_packet.encode("latin"))

            if self.active.console_tab.command_line.controls_logging:
                logging.debug("'esc' pressed: KILL")
        elif e.key() == Qt.Key_X:
            if self.claw_closed:
                # claw should open now
                if self.active.console_tab.command_line.controls_logging:
                    logging.debug("'X' pressed: CLAW OPEN")
                # self.value_servo = 12
                # self.packet_servo = chr(1) + chr(9) + chr(self.value_servo) + chr(255)
                # self.ser.write(self.packet_servo.encode("latin"))
                self.claw_closed = False
            else:
                if self.active.console_tab.command_line.controls_logging:
                    logging.debug("'X' pressed: CLAW CLOSED")

                # self.value_servo = 11
                # self.packet_servo = chr(1) + chr(9) + chr(self.value_servo) + chr(255)
                # self.ser.write(self.packet_servo.encode("latin"))
                self.claw_closed = True

        if self.active.console_tab.command_line.key_logging and e.key() != Qt.Key_Return:
            logging.debug(f'Key pressed: {ascii(e.text())}')

        # if self.active.console_tab.command_line.controls_logging and e.key() != Qt.Key_Return:
        #     logging.debug(f'Key pressed: {ascii(e.text())}')

    
    def keyReleaseEvent(self, e):
        if e.key() == Qt.Key_A or e.key() == Qt.Key_D:
            if self.active.console_tab.command_line.controls_logging:
                logging.debug("'a'/'d' released")
            # self.value_rightMot = 150
            # self.packet_rightThruster = chr(1) + chr(7) + chr(self.value_rightMot) + chr(255)
            # self.ser.write(self.packet_rightThruster.encode("latin"))
        elif e.key() == Qt.Key_W or e.key() == Qt.Key_S:
            if self.active.console_tab.command_line.controls_logging:
                logging.debug("'w'/'s' released")
            # self.value_motor = 150
            # self.packet_motor = chr(1) + chr(13) + chr(self.value_motor) + chr(255)
            # self.ser.write(self.packet_motor.encode("latin"))
        elif e.key() == Qt.Key_Up or e.key() == Qt.Key_Down:
            # self.value_motor = 150
            # self.packet_motor_forward = chr(1) + chr(2) + chr(self.value_motor) + chr(255)
            # self.ser.write(self.packet_motor_forward.encode("latin"))
            # self.packet_motor_backward = chr(1) + chr(3) + chr(self.value_motor) + chr(255)
            # self.ser.write(self.packet_motor_backward.encode("latin"))
            if self.active.console_tab.command_line.controls_logging:
                logging.debug("Up arrow/down arrow released")

if __name__ == '__main__':
    # Initial checks

    # with open('settings.yml') as f:
    #     settings = yaml.safe_load(f)

    #     serial_port = settings['serial-port']
    #     baud_rate = settings['baud-rate']

    # if not os.path.exists(serial_port):
    #     print('\033[91m\033[1mInvalid serial port\033[0m')
    #     exit()


    ## Setup    

    app = QApplication([])

    app.setWindowIcon(QIcon('gui/icon.png'))

    window = AzureUI()#(port, baud)
    window.show()
 
    logging.info('Starting up Azure UI...')

    # Create "captures" directory
    try:
        os.mkdir('captures')
        logging.warning('No captures directory detected; one has been generated for you!')
    except FileExistsError:
        pass

    logging.info('Images are saved under the "captures" directory in the format "d-m-y_H:M:S"')

    # Create "logs" directory
    try:
        os.mkdir('logs')
        logging.warning('No logs directory detected; one has been generated for you!')
    except FileExistsError:
        pass

    ## Setup complete
    logging.info('Azure UI has loaded sucessfully\n\n')
    print('\033[92m\033[1mAzure UI has loaded sucessfully\033[0m')

    app.exec()

    # Release camera
    window.active.cam_tab.thread.capture.release()

    print('\033[93m\033[1mAzure UI has stopped sucessfully\033[0m')
    exit()
