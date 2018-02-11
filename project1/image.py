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

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 250, 250)

        hbox = QHBoxLayout(self)
        pixmap = QPixmap("./data/" + self.data_files[0])

        label = QLabel(self)
        label.setText("This is a QLabel")
        label.setStyleSheet("border: 10px solid grey")
        label.resize(200, 200)
        label.setPixmap(pixmap)

        hbox.addWidget(label)
        self.setLayout(hbox)

        self.show()

if __name__ == '__main__':
        app = QApplication(sys.argv)
        window = Window()
        sys.exit(app.exec_())
