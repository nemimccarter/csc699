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
        self.image_files = []
        self.fullscreen_index = 0
        self.dir_name = dir_name
        
        for (dirpath, dirnames, filenames) in walk(dir_name):
            self.image_files.extend(filenames)
            break
        
        self.image_files.sort()


    def next_filename(self):
        self.fullscreen_index = self.fullscreen_index + 1

        if (self.fullscreen_index >= len(self.image_files)):
            self.fullscreen_index = 0


    def prev_filename(self):
        self.fullscreen_index = self.fullscreen_index - 1

        if (self.fullscreen_index < 0):
            self.fullscreen_index = len(self.image_files) - 1


    def get_current_filename(self):
        return self.dir_name + self.image_files[self.fullscreen_index]


class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.title = 'CSC 690 - Project 1'
        self.image_files = []
        self.fullscreen_index = 0
        self.model = Model('./data/')
        self.thumbnail_labels = []
        self.thumbnail_pixmaps = []
        self.view_mode = 'thumbnails'
        self.thumbnail_index = 0

        self.load_thumbnails()
        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, CONST_WIDTH, CONST_HEIGHT)

        stylesheet = '''
                     border: 20px solid black;
                     background: black;
                     '''

        # load pixmaps
        self.pixmap = QPixmap(self.model.get_current_filename())
        self.load_thumbnails()

        self.label = QLabel(self)
        self.label.setStyleSheet(stylesheet)
        #self.label.setFrameShape(QFrame.StyledPanel)

        # hbox for fullscreen
        self.hbox = QHBoxLayout(self)

        self.setLayout(self.hbox)

        #self.show_image()
        #self.label.hide()

        self.load_thumbnails()

        self.show()


    def keyPressEvent(self, event):
        key_pressed = event.key()

        if key_pressed == Qt.Key_Right:
        	self.next_image()
        elif key_pressed == Qt.Key_Left: 
        	self.prev_image()
        elif key_pressed == Qt.Key_Up: 
        	print("up hit")
        elif key_pressed == Qt.Key_Down: 
        	print('thumbnails hit')
        elif key_pressed == 46:
        	print('>')

        	self.next_thumbnails()
        	self.show()
        elif key_pressed == 44:
        	print('<')

        	self.prev_thumbnails()
        	self.show()


    def show_image(self):
        self.pixmap = QPixmap(self.model.get_current_filename())       
        self.pixmap = self.pixmap.scaled(CONST_WIDTH, CONST_HEIGHT, Qt.KeepAspectRatio)
        
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignCenter)

        self.show()


    def next_image(self):
        self.model.next_filename()
        #self.show_image()


    def prev_image(self):
    	self.model.prev_filename()
    	#self.show_image()


    def load_thumbnails(self):
    	# load images into pixmap array
    	for _ in self.model.image_files:
    		self.thumbnail_pixmaps.append(QPixmap(self.model.get_current_filename()))
    		self.model.next_filename()

    	for index in range(0, 5):
    		# scale pixmaps
    		self.thumbnail_pixmaps[index] = self.thumbnail_pixmaps[index].scaled(100, 100, Qt.KeepAspectRatio)

    		self.next_image()

    		# init thumbnail labels with corresponding pixmap
    		self.thumbnail_labels.append(QLabel(self))
    		self.thumbnail_labels[index].setPixmap(self.thumbnail_pixmaps[index])

    		# positioning labels
    		self.thumbnail_labels[index].resize(100,100)
    		self.thumbnail_labels[index].setAlignment(Qt.AlignCenter)
    		# TODO: remove magic numbers below
    		self.thumbnail_labels[index].move(20 + index * 150 + (index * 20), (CONST_HEIGHT - 100) / 2)

    		self.thumbnail_index = 4

    	self.show()


    def prev_thumbnails(self):
    	self.thumbnail_index -= 5
    	if self.thumbnail_index < 0:
    		self.thumbnail_index = len(self.thumbnail_pixmaps) - 1
    	for label in self.thumbnail_labels:
	        label.setPixmap(self.thumbnail_pixmaps[self.thumbnail_index])
	        self.thumbnail_index -= 1
	        if self.thumbnail_index < 0:
	        	self.thumbnail_index = len(self.thumbnail_pixmaps) - 1


    def next_thumbnails(self):
	    for label in self.thumbnail_labels:
	    	label.setPixmap(self.thumbnail_pixmaps[self.thumbnail_index])
	    	self.thumbnail_index += 1

	    	if self.thumbnail_index >= len(self.thumbnail_pixmaps):
	    		self.thumbnail_index = 0


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
