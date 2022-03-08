from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt


class HomeTab(QWidget):
    def __init__(self):
        super().__init__()

        # Title
        # self.frame = QWidget()

        self.title = QLabel('MATE Azure User Interface')
        self.title.setStyleSheet("""
            QLabel {
                font: bold 30px;
                color: white
            }
        """)

        # Control Bar
        self.control_layout = QWidget()
        
        self.control_layout.layout = QHBoxLayout()

        self.control_bar = QWidget()

        self.control_bar.setStyleSheet("""
            QWidget {
                background: rgb(0, 0, 0)
            }
        """)
        
        self.control_bar.setFixedSize(200,20)

        self.control_layout.layout.addWidget(self.control_bar)
        # self.control_layout.layout.setLayout(self.control_layout)

        ####### shift as killswitch and button on menu

        # Exit
        self.exit = Button('ok')

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.title)
        self.layout.addStretch()
        self.layout.addWidget(self.control_layout)
        # self.layout.addWidget(Button('ok'))

        self.layout.setAlignment(Qt.AlignRight)

        self.setLayout(self.layout)

class ControlBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(15, 29, 44)
            }
        """)

        # self.setAlignment(Qt.AlignRight | Qt.AlignBottom)



class Button(QPushButton):
    def __init__(self, name):
        super().__init__(name)

        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    spread: pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(235, 64, 52), stop:1 rgb(227, 95, 86)
                );
                color: rgb(210, 211, 210);

                padding: 10px;
                font: bold 20px;

                border-radius: 10px
            }

            QPushButton:hover {
                background: rgb(227, 140, 134)
            }
        """)

        self.setFixedSize(80,40)