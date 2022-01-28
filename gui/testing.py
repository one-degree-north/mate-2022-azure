from gui import window

from PyQt5.QtWidgets import QApplication
from PyQt5.QtMultimedia import QCameraInfo
from time import sleep
from threading import Thread
import yaml
import sys

    

while True:
    sleep(0.5)
    window.tabs.logs_tab.update_log('ok')
