from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont

import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # self.container = QWidget()

        # self.container.layout = QVBoxLayout()

        self.button = QPushButton('ok')
        self.button.setStyleSheet('font: bold 50px')
    #     self.button.clicked.connect()

    #     self.ok_text = QLabel('')

    #     self.container.layout.addWidget(self.button)
    #     self.container.layout.addWidget(self.counter)

    #     self.container.setLayout(self.container.layout)

        self.setCentralWidget(self.button)

    # def update_counter(self):
    #     pass


app = QApplication([])

window = MainWindow()
window.show()

sys.exit(app.exec())

