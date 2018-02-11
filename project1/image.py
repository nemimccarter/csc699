from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLCDNumber, QSlider, QHBoxLayout, QApplication)
from PyQt5.QtGui import QPixmap

from os import listdir, walk
from os.path import isfile, join
import sys

class Window(QWidget):
    data_files = []

    def __init__(self):
        super().__init__()
        self.title = "CSC 690 - Project 0.5"
        for (dirpath, dirnames, filenames) in walk("./data"):
            self.data_files.extend(filenames)
            break
        print(self.data_files)

        self.initUI(int(sys.argv[1]), int(sys.argv[2]), sys.argv[3])

    def initUI(self, W, H, B):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, W, H)

        hbox = QHBoxLayout(self)
        pixmap = QPixmap("./data/" + self.data_files[0])

        label = QLabel(self)
        label.setText("This is a QLabel")
        label.setStyleSheet("border: " + B + " solid black")
        label.resize(W, H)
        label.setPixmap(pixmap)
        hbox.addWidget(label)
        self.setLayout(hbox)

        if (W > H):
            pixmap_scaled = pixmap.scaledToWidth(W - (2 * int(B)))
        else:
            pixmap_scaled = pixmap.scaledToHeight(H - (2 * int(B)))

        label.setPixmap(pixmap_scaled)
        label.setAlignment(Qt.AlignCenter)
        self.show()

if __name__ == '__main__':
        app = QApplication(sys.argv)
        window = Window()
        sys.exit(app.exec_())
