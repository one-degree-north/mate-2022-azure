from PyQt5.QtWidgets import QApplication, QMainWindow, QHBoxLayout, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, QObject, QThread

from gui.menu import MenuBar
from gui.active import ActiveTab

from controller import Controller
from comms import Comms

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
    def __init__(self):
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
    
    def run_controller(self):
        while True:
            events = get_events()
            for event in events:
                controller = self.controllers[event.user_index]

                if event.type == EVENT_STICK_MOVED:
                    if event.stick == LEFT:
                        self.l_thumb_stick_pos = (int(round(self.l_thumb_pos[0] + 25 * event.x,0)), int(round(self.l_thumb_pos[1] - 25 * event.y,0)))
                        if self.l_thumb_stick_pos[1] > 80:
                            self.percentage_x = int(((self.l_thumb_stick_pos[1] - 80)/25)*100)
                            self.comms.packetControls.packet[1] = self.percentage_x
                            print("Robot goes backward")
                            self.value = controller.send_value(self.percentage_x)
                            self.packet_rightThruster = chr(1) + chr(6) + chr(self.value) + chr(255)
                            self.comms.write(self.packet_rightThruster.encode("latin"))
                            self.packet_leftThruster = chr(1) + chr(7) + chr(self.value) + chr(255)
                            self.comms.write(self.packet_leftThruster.encode("latin"))

                        elif self.l_thumb_stick_pos[1] < 80:
                            self.percentage_x = int(((80 - self.l_thumb_stick_pos[1])/25)*100)
                            self.comms.packetControls.packet[1] = self.percentage_x
                            print("Robot goes forward")
                            self.value = controller.send_value(self.percentage_x)
                            self.packet_rightThruster = chr(1) + chr(6) + chr(self.value) + chr(255)
                            self.comms.write(self.packet_rightThruster.encode("latin"))
                            self.packet_leftThruster = chr(1) + chr(7) + chr(self.value) + chr(255)
                            self.comms.write(self.packet_leftThruster.encode("latin"))

                    elif event.stick == RIGHT:
                        self.r_thumb_stick_pos = (int(round(controller.r_thumb_pos[0] + 25 * event.x,0)), int(round(controller.r_thumb_pos[1] - 25 * event.y,0)))
                        if self.r_thumb_stick_pos[0] > 200:
                            self.percentage_y = int(((self.r_thumb_stick_pos[0] - 200)/25)*100)
                            self.comms.packetControls.packet[2] = self.percentage_y
                            print("Robot goes right")

                            self.value_leftMot = controller.send_value(controller.rightJoy_LR)
                            self.packet_leftThruster = chr(1) + chr(6) + chr(self.value_leftMot) + chr(255)
                            self.comms.write(self.packet_leftThruster.encode("latin"))

                            self.value_rightMot = controller.send_value(-controller.rightJoy_LR)
                            self.convert_value_rightMot = (self.value_rightMot).encode("latin")
                            self.packet_rightThruster = chr(1) + chr(7) + chr(self.value_rightMot) + chr(255)
                            self.comms.write(self.packet_rightThruster.encode("latin"))

                        elif self.r_thumb_stick_pos[0] < 200:
                            self.percentage_y = int(((200 - self.r_thumb_stick_pos[0])/25)*100)
                            self.comms.packetControls.packet[2] = self.percentage_y
                            print("Robot goes left")

                            self.value_rightMot = controller.send_value(controller.rightJoy_LR)
                            self.packet_rightThruster = chr(1) + chr(6) + chr(self.value_rightMot) + chr(255)
                            self.comms.write(self.packet_rightThruster.encode("latin"))

                            self.value_leftMot = controller.send_value(-controller.rightJoy_LR)
                            self.packet_leftThruster = chr(1) + chr(7) + chr(self.value_leftMot) + chr(255)
                            self.comms.write(self.packet_leftThruster.encode("latin"))

                elif event.type == EVENT_TRIGGER_MOVED:
                    if event.trigger == LEFT:
                        self.l_trigger_index_pos = (controller.l_trigger_pos[0], controller.l_trigger_pos[1] - 20 + int(round(40 * event.value, 0)))
                        print(self.l_trigger_index_pos)
                        if self.l_trigger_index_pos[1] > 30:
                            self.comms.packetControls.packet[7] = True
                            print("Robot goes down")
                            self.packet_LB_up = chr(1) + chr(13) + chr(254) + chr(255)
                            self.comms.write(self.packet_LB_up.encode("latin"))

                    elif event.trigger == RIGHT:
                        self.r_trigger_index_pos = (controller.r_trigger_pos[0], controller.r_trigger_pos[1] - 20 + int(round(40 * event.value, 0)))
                        print(self.r_trigger_index_pos)
                        if self.r_trigger_index_pos[1] > 30:
                            self.comms.packetControls.packet[6] = True
                            print("Robot goes up")
                            self.packet_RB_up = chr(1) + chr(13) + chr(127) + chr(255)
                            self.comms.write(self.packet_RB_up.encode("latin"))

                elif event.type == EVENT_BUTTON_PRESSED:                

                    if event.button == "DPAD_LEFT":
                        print("Switch to Camera 2")
                    elif event.button == "DPAD_RIGHT":
                        print("Switch to Camera 3")
                    elif event.button == "DPAD_UP":
                        print("Switch to Camera 1")
                    elif event.button == "DPAD_DOWN":
                        print("Switch to Camera 4")

                    elif event.button == "A":
                        self.comms.packetControls.packet[5] = True

                        self.open = True
                        if self.open == True:
                            self.packet_servoGrab = chr(1) + chr(9) + chr(12) + chr(255)
                            self.comms.write(self.packet_servoGrab.encode("latin"))
                            self.open = False
                        else:
                            self.packet_servoGrab = chr(1) + chr(9) + chr(11) + chr(255)
                            self.comms.write(self.packet_servoGrab.encode("latin"))
                            self.open = True

                    elif event.button == "X":
                        print("Take picture")

                    elif event.button == "Y":
                        self.comms.packetControls.packet[7] = True
                        print("Robot is killed")
                        self.packet_killSwitch = chr(1) + chr(14) + chr(100) + chr(255)
                        self.comms.write(self.packet_killSwitch.encode("latin"))

                elif event.type == EVENT_BUTTON_RELEASED:                
                    if event.button == "DPAD_LEFT":
                        print("Remain on Camera 2")
                    elif event.button == "DPAD_RIGHT":
                        print("Remain on Camera 3")
                    elif event.button == "DPAD_UP":
                        print("Remain on Camera 1")
                    elif event.button == "DPAD_DOWN":
                        print("Remain on Camera 4")

    

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
