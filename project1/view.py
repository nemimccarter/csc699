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

        self.hbox = QHBoxLayout(self)
        self.pixmap = QPixmap('./data/' + self.data_files[self.data_index])

        self.label = QLabel(self)
        self.label.setText('This is a QLabel')
        self.label.setStyleSheet('border: ' + str(CONST_BORDER) + ' solid black')
        self.label.resize(CONST_WIDTH, CONST_HEIGHT)
        self.label.setPixmap(self.pixmap)
        self.hbox.addWidget(self.label)
        self.setLayout(self.hbox)

        if (self.pixmap.height() > CONST_HEIGHT or self.pixmap.width() > CONST_WIDTH):
            if (self.pixmap.width() > self.pixmap.height()):
                self.pixmap = self.pixmap.scaledToWidth(CONST_WIDTH - (2 * CONST_BORDER))
            else:
                self.pixmap = self.pixmap.scaledToHeight(CONST_HEIGHT - (2 * CONST_BORDER))

        self.label.setPixmap(self.pixmap)
        self.label.resize(CONST_WIDTH, CONST_HEIGHT)
        self.label.setAlignment(Qt.AlignCenter)
        self.show()
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_A:
            self.data_index = self.data_index + 1
            print("A key hit")
            pixmap = QPixmap('./data/' + str(self.data_index))
            self.change_image()

    def change_image(self):
        self.data_index = self.data_index + 1
        self.pixmap = QPixmap('./data/' + self.data_files[self.data_index])

        if (self.pixmap.height() > CONST_HEIGHT or self.pixmap.width() > CONST_WIDTH):
            if (self.pixmap.width() > self.pixmap.height()):
                self.pixmap = self.pixmap.scaledToWidth(CONST_WIDTH - (2 * CONST_BORDER))
            else:
                self.pixmap = self.pixmap.scaledToHeight(CONST_HEIGHT - (2 * CONST_BORDER))

        self.label.setPixmap(self.pixmap)
        self.label.resize(CONST_WIDTH, CONST_HEIGHT)
        self.label.setAlignment(Qt.AlignCenter)
        self.show()

if __name__ == '__main__':
        app = QApplication(sys.argv)
        window = Window()
        sys.exit(app.exec_())
