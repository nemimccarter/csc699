from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QFrame, QHBoxLayout, QApplication)
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

    def next_filename(self):
        self.data_index = self.data_index + 1
        if (self.data_index >= len(self.data_files)):
            self.data_index = 0

    def prev_filename(self):
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
        self.thumbnail_labels = []
        self.thumbnail_pixmaps = []
       
        for x in range(0, 5):
            self.thumbnail_labels.append(QLabel(self))

        # set initial thumbnail images
        self.load_thumbnails()

        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, CONST_WIDTH, CONST_HEIGHT)

        stylesheet = '''
                     border: 20px solid black;
                     background: black;
                     '''

        self.pixmap = QPixmap(self.model.get_current_filename())

        self.label = QLabel(self)
        self.label.setStyleSheet(stylesheet)
        #self.label.setFrameShape(QFrame.StyledPanel)

        # hbox for fullscreen
        self.hbox = QHBoxLayout(self)
        self.hbox.addWidget(self.label)

        # set thumbnail QLabels
        offset = 30

        for label in self.thumbnail_labels:
            label.setStyleSheet(stylesheet)
            # label.resize(100, 100)
            # label.move(offset, 50)
            offset += 20

        self.setLayout(self.hbox)

        self.show_image()
        #self.label.hide()

        #self.show_thumbnails()


    def keyPressEvent(self, event):
        key_pressed = event.key()

        if key_pressed == Qt.Key_Right: 
        	self.next_image()
        elif key_pressed == Qt.Key_Left: 
        	self.prev_image()


    def show_image(self):
        self.pixmap = QPixmap(self.model.get_current_filename())       
        self.pixmap = self.pixmap.scaled(CONST_WIDTH, CONST_HEIGHT, Qt.KeepAspectRatio)
        
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignCenter)

        self.model.next_filename()
        self.show()


    def next_image(self):
        self.model.next_filename()
        self.show_image()


    def prev_image(self):
    	self.model.prev_filename()
    	self.show_image()


    def load_thumbnails(self):
        for index in range(0, 5):
            self.thumbnail_pixmaps.append(QPixmap(self.model.get_current_filename()))
            self.model.next_filename()
    
    def show_thumbnails(self):
    	for index in range(0, 5):
    		self.thumbnail_labels[index].setPixmap(self.thumbnail_pixmaps[index]).layout().addWidget(index, index * 10, 50)

    	self.show()

    		
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
