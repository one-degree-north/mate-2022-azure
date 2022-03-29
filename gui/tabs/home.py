from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from pyqtgraph.opengl import GLViewWidget, MeshData, GLMeshItem

import numpy as np
from stl import mesh

import logging


class HomeTab(QWidget):
    def __init__(self):
        super().__init__()

        # Title
        self.title = QLabel('MATE Azure User Interface')
        self.title.setStyleSheet("""
            QLabel {
                font: bold 50px;
                color: white
            }
        """)
        self.title.setAlignment(Qt.AlignLeft)
        self.title.setFixedHeight(80)

        # View box
        self.view_box = ViewBox()

        # Layout
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.view_box)

        self.setLayout(self.layout)

class ViewBox(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(17, 28, 43);
                border-radius: 10px
            }
        """)

        self.view = View()

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.view)

        self.setLayout(self.layout)




class View(GLViewWidget):
    def __init__(self):
        super().__init__()

        self.setCameraPosition(distance=400)
        self.pan(dx=-160, dy=0, dz=0)
        self.setBackgroundColor((17, 28, 43))

        self.stl = mesh.Mesh.from_file('gui/rov.stl')
        
        self.points = self.stl.points.reshape(-1, 3)
        self.faces = np.arange(self.points.shape[0]).reshape(-1, 3)

        self.mesh_data = MeshData(vertexes=self.points, faces=self.faces)
        self.rendered_mesh = GLMeshItem(meshdata=self.mesh_data, computeNormals=False, drawEdges=True, edgeColor=QColor(Qt.GlobalColor.lightGray))
        self.rendered_mesh.setShader('edgeHilight')

        self.addItem(self.rendered_mesh)

class ok(QWidget):
    def __init__(self):
        # Title
        self.title = QLabel('MATE Azure User Interface')
        self.title.setStyleSheet("""
            QLabel {
                font: bold 50px;
                color: white
            }
        """)

        self.title.setAlignment(Qt.AlignLeft)

        # # Latency label
        # self.ping = QLabel(f'{self.latency}ms')
        # self.ping.setStyleSheet("""
        #     QLabel {
        #         background: rgb(14, 28, 44)
        #         font: bold 20px;
        #         color: white
        #         border-radius: 20px
        #     }
        # """)

        # Exit
        self.exit = QPushButton()

        self.exit.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    spread: pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(235, 64, 52), stop:1 rgb(227, 95, 86)
                );
                color: rgb(210, 211, 210);

                padding: 10px;
                font: bold 20px;

                border-radius: 15px
            }

            QPushButton:hover {
                background: rgb(227, 140, 134)
            }
        """)

        self.exit.setFixedSize(30,30)


        # Control bar
        self.control_bar = QWidget()
        
        self.control_bar.layout = QHBoxLayout()

        # self.control_bar.layout.addStretch()
        self.control_bar.layout.addWidget(self.control_label)
        self.control_bar.layout.addWidget(self.exit)


        # self.control_bar.setFixedWidth(150)
        self.control_bar.setLayout(self.control_bar.layout)

        self.control_bar.setStyleSheet("""
            QWidget {
                background: rgb(14, 28, 44);
                border-radius: 20px;
                padding: 5px
            }
        """)

        self.control_bar.setFixedHeight(30)

        # Controls enclosure
        self.enclosure = QWidget()
        self.enclosure.layout = QHBoxLayout()

        self.enclosure.layout.addStretch()
        self.enclosure.layout.addWidget()

        self.enclosure.setContentsMargins(0,0,0,0)

        self.enclosure.setLayout(self.enclosure.layout)


        self.layout = QVBoxLayout()

        self.layout.addWidget(self.title)
        self.layout.addStretch()
        # self.layout.addWidget(self.desc)
        self.layout.addWidget(self.enclosure)

        # self.layout.setAlignment(Qt.AlignRight)

        self.setLayout(self.layout)

class ControlBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(15, 29, 44);
                border-radius: 10px
            }
        """)


class Button(QPushButton):
    def __init__(self):
        super().__init__()

        self.setStyleSheet("""
            QPushButton {
                background: qlineargradient(
                    spread: pad, x1:0, y1:0.5, x2:1, y2:0.5, stop:0 rgb(235, 64, 52), stop:1 rgb(227, 95, 86)
                );
                color: rgb(210, 211, 210);

                padding: 10px;
                font: bold 20px;

                border-radius: 20
            }

            QPushButton:hover {
                background: rgb(227, 140, 134)
            }
        """)

        self.setFixedSize(40,40)