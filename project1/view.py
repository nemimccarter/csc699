from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QHBoxLayout, QApplication)
from PyQt5.QtGui import QPixmap

from os import listdir, walk
from os.path import isfile, join
import sys
import click

CONST_WIDTH = 800
CONST_HEIGHT = 600
CONST_BORDER = 20

class Window(QWidget):

    def __init__(self):
        super().__init__()
        
        self.title = 'CSC 690 - Project 1'
        self.data_files = []
        self.data_index = 0
        
        for (dirpath, dirnames, filenames) in walk('./data'):
            self.data_files.extend(filenames)
            break
        self.data_files.sort()

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, CONST_WIDTH, CONST_HEIGHT)
        stylesheet = '''
                     border: 20px solid black;
                     background: blue;
                     '''
        self.hbox = QHBoxLayout(self)
        self.pixmap = QPixmap('./data/' + self.data_files[self.data_index])

        self.label = QLabel(self)
        self.label.setStyleSheet(stylesheet)
        self.hbox.addWidget(self.label)
        self.setLayout(self.hbox)

        self.show_image()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.data_index = self.data_index + 1
            if self.data_index >= len(self.data_files):
                self.data_index = 0

            self.show_image()

    def show_image(self):
        self.pixmap = QPixmap('./data/' + self.data_files[self.data_index])
       
        self.pixmap = self.pixmap.scaled(CONST_WIDTH, CONST_HEIGHT, Qt.KeepAspectRatio)
        self.label.setPixmap(self.pixmap)
        self.label.resize(CONST_WIDTH, CONST_HEIGHT)
        self.label.setAlignment(Qt.AlignCenter)
        self.show()

if __name__ == '__main__':
        app = QApplication(sys.argv)
        window = Window()
        sys.exit(app.exec_())
