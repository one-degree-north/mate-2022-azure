from PyQt5.QtWidgets import QHBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QImage, QResizeEvent
from PyQt5.QtCore import Qt

from numpy import ndarray

import os
import cv2

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()

        self.display_width = 640
        self.display_height = 480

        self.images = self.update_captures()
        self.read(self.images[0])

        self.label = QLabel()
        # self.label.setGeometry(0,0,640,480)

        self.label.resizeEvent = self.label_resize
    
        # self.cv_img = cv2.imread(self.images[0])
        # self.qt_img = self.convert_cv_qt(self.cv_img)

        self.label.setPixmap(self.qt_img)
        # self.pixmap = QPixmap(self.images[0])
        # print(self.pixmap.width(), self.pixmap.height())
        # self.pixmap.width = self.pixmap.width() 
        # self.pixmap.scaled(100, 100)
        # self.pixmap.scaledToHeight(64)
        # self.pixmap.height = self.pixmap.height() - 1000
        # # self.label.height = 50

        # self.label.setPixmap(self.pixmap)

        # self.image = cv2.imread(self.images[0], cv2.IMREAD_UNCHANGED)
        # self.image = QImage(self.image.data, self.image.shape[1]/3, self.image.shape[0]/3)#, QImage.Format_RGB888)
        
        # self.image_frame = QLabel()
        # self.image_frame.setPixmap(QPixmap.fromImage(self.image))

        self.layout = QHBoxLayout()
        self.layout.addWidget(self.label)#_frame)
        self.setLayout(self.layout)

        

    def label_resize(self, resizeEvent: QResizeEvent):
        self.display_width, self.display_height = self.label.width(), self.label.height()

    def update_captures(self):
        images = []

        for path, _, files in os.walk('captures'):
            for filename in files:
                images.append(os.path.join(path, filename))

        return images
    
    def read(self, path):
        self.cv_img = cv2.imread(path)
        self.qt_img = self.convert_cv_qt(self.cv_img)

        return self.qt_img

    def convert_cv_qt(self, cv_img):
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.display_width, self.display_height, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


    def keyPressEvent(self, e):
        print(e.text())

