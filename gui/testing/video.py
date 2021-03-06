from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget#, QVBoxLayout
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
import cv2
import sys

class Video(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Video Testing')
        self.setFixedSize(800,400)


        self.media_player = QMediaPlayer(self, QMediaPlayer.VideoSurface)
        self.video = QVideoWidget()


        self.media_player.setVideoOutput(self.video)

        self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile('/Users/krishnakundalia/mate-2022-azure-2/gui/testing/rick_roll.mp4')))
        self.media_player.play()

        self.setCentralWidget(self.video)

        self.video.show()


if __name__ == '__main__':
    app = QApplication([])

    window = Video()
    window.show()

    sys.exit(app.exec())