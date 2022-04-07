from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

import logging
import sys
import os

from time import sleep

from threading import Thread

from gui.ui import AzureUI

def ok_thread():
    return None

def gui_thread():
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

#t1 = Thread(target=ok_thread)
t2 = Thread(target=gui_thread)
# gui_thread()

# t1.start()
t2.start()
# gui_thread()
