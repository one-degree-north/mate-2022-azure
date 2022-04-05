from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor

from pyqtgraph.opengl import GLViewWidget, MeshData, GLMeshItem

import numpy as np
from stl import mesh

import logging


class HomeTab(QWidget):
    def __init__(self, parent):
        super().__init__()

        self.title = Title()

        # View box
        self.view_box = ViewBox(parent)

        # Layout
        self.layout = QVBoxLayout()

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.view_box)
        # self.layout.addWidget(ViewBox(parent), 1,1)

        # self.layout.setSpacing(20)

        self.setLayout(self.layout)



class Title(QLabel):
    def __init__(self):
        super().__init__('Azure User Interface')

        self.setStyleSheet("""
            QLabel {
                background: rgb(20, 33, 51);
                border-radius: 10px;
                padding: 12px;
                margin: 5px;

                font: bold 40px;
                color: white
            }
        """)

        # self.setFixedSize(450, 80)
        self.setFixedHeight(70)
        self.setAlignment(Qt.AlignCenter)
        

class ViewBox(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

        self.setStyleSheet("""
            QWidget {
                background: rgb(17, 28, 43);
                border-radius: 10px;
                margin: 5px
            }
        """)

        self.view = View(parent)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)

        self.setLayout(self.layout)


class View(GLViewWidget):
    def __init__(self, parent):
        super().__init__()

        self.parent = parent

        self.setCameraPosition(distance=400)
        self.pan(dx=-160, dy=0, dz=0)
        self.setBackgroundColor((17, 28, 43))

        self.stl = mesh.Mesh.from_file('gui/rov.stl')
        
        self.points = self.stl.points.reshape(-1, 3)
        self.faces = np.arange(self.points.shape[0]).reshape(-1, 3)

        self.mesh_data = MeshData(vertexes=self.points, faces=self.faces)
        self.rendered_mesh = GLMeshItem(meshdata=self.mesh_data, computeNormals=False, drawEdges=True, edgeColor=QColor(230, 230, 230))
        self.rendered_mesh.setShader('edgeHilight')

        self.addItem(self.rendered_mesh)

    def keyPressEvent(self, e):
        self.parent.keyPressEvent(e)