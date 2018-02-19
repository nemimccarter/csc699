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

class Model():
    def __init__(self, dir_name):
        self.data_files = []
        self.data_index = 0
        self.dir_name = dir_name
        for (dirpath, dirnames, filenames) in walk(dir_name):
            self.data_files.extend(filenames)
            break
        self.data_files.sort()

    def next_image(self):
        self.data_index = self.data_index + 1
        if (self.data_index >= len(self.data_files)):
            self.data_index = 0

    def prev_image(self):
        self.data_index = self.data_index - 1
        if (self.data_index < 0):
            self.data_index = len(self.data_files) - 1


    def get_current_filename(self):
        return self.dir_name + self.data_files[self.data_index]

class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.title = 'CSC 690 - Project 1'
        self.data_files = []
        self.data_index = 0
        self.model = Model('./data/')

        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, CONST_WIDTH, CONST_HEIGHT)
        stylesheet = '''
                     border: 20px solid black;
                     background: blue;
                     '''
        self.hbox = QHBoxLayout(self)
        self.pixmap = QPixmap(self.model.get_current_filename())

        self.label = QLabel(self)
        self.label.setStyleSheet(stylesheet)
        self.hbox.addWidget(self.label)
        self.setLayout(self.hbox)

        self.show_image()

    def keyPressEvent(self, event):
        key_pressed = event.key()
        if key_pressed == Qt.Key_Right:
            self.model.next_image()
            self.show_image()

        elif key_pressed == Qt.Key_Left:
            self.model.prev_image()
            self.show_image()

    def show_image(self):
        self.pixmap = QPixmap(self.model.get_current_filename())
       
        self.pixmap = self.pixmap.scaled(CONST_WIDTH, CONST_HEIGHT, Qt.KeepAspectRatio)
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        self.show()

if __name__ == '__main__':
        app = QApplication(sys.argv)
        window = Window()
        sys.exit(app.exec_())
