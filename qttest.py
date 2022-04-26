from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.button = QPushButton('ok')

        self.setCentralWidget(self.button)


app = QApplication([])

window = MainWindow()
window.show()

sys.exit(app.exec())

