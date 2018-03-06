from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QFrame, QHBoxLayout, QApplication)
from PyQt5.QtGui import QPixmap
import json

from os import listdir, walk
from os.path import isfile, join
import sys
import click

from Model import *

CONST_WIDTH = 800
CONST_HEIGHT = 600
CONST_BORDER = 20
CONST_THUMBNAIL_COUNT = 5


class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.title = 'CSC 690 - Project 1'
        self.model = Model('./data/')
        
        self.thumbnail_labels = []
        self.thumbnail_pixmaps = []
        
        self.view_mode = 'thumbnails'
        self.mode = 'thumbnails'
        
        self.tag_field = QLineEdit(self)
        self.tag_field.setFocusPolicy(Qt.ClickFocus)
        self.tags_label = QLabel(self)        

        self.stylesheet = 'background: solid black;'
        self.selected_thumbnail_stylesheet = 'border: 5px solid red;'

        self.initUI()


    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, CONST_WIDTH, CONST_HEIGHT)

        # load pixmaps
        self.pixmap = QPixmap(self.model.get_current_filename())
        self.load_thumbnails()

        self.label = QLabel(self)
        self.label.setStyleSheet(self.stylesheet)
        self.label.setFrameShape(QFrame.StyledPanel)
        self.label.resize(CONST_WIDTH, CONST_HEIGHT)
        self.label.setAlignment(Qt.AlignCenter)

        self.thumbnail_labels[0].setStyleSheet(self.selected_thumbnail_stylesheet)

        # hbox for fullscreen
        self.hbox = QHBoxLayout(self)

        self.setLayout(self.hbox)

        self.show_fullscreen()
        self.label.hide()

        self.tags_label.move(600, 400)
        self.tag_field.move(300, 500)

        self.show()


    def keyPressEvent(self, event):
        key_pressed = event.key()

        if key_pressed == Qt.Key_Right:
            
            if self.mode == 'thumbnails':
                self.next_image()

            elif self.mode == 'fullscreen':
                self.next_image()
                self.show_fullscreen()
        
        elif key_pressed == Qt.Key_Left:
            
            if self.mode == 'thumbnails':
                self.prev_image()
          
            elif self.mode == 'fullscreen':
                self.prev_image()
                self.show_fullscreen()
        
        elif key_pressed == Qt.Key_Up: 
            
            if self.mode == 'thumbnails':
                self.mode = 'fullscreen'
                self.show_fullscreen()
            
                for label in self.thumbnail_labels:
                    label.hide()
        
        elif key_pressed == Qt.Key_Down:
            
            if self.mode == 'fullscreen':
                self.mode = 'thumbnails'
                self.label.hide()
                # select middle thumbnail
                # self.select_thumbnail(self.model.get_leftmost_index() + 2)

                for label in self.thumbnail_labels:
                    label.show()
        
        elif key_pressed == 46:
            if self.mode == 'thumbnails':

                for _ in range(0, 5):
                    self.next_image()

                self.thumbnail_labels[self.model.get_current_index() - self.model.get_leftmost_index()].setStyleSheet('')
                self.model.set_current_index(self.model.get_leftmost_index())
                self.thumbnail_labels[self.model.get_current_index() - self.model.get_leftmost_index()].setStyleSheet(self.selected_thumbnail_stylesheet)

        elif key_pressed == 44:
            if self.mode == 'thumbnails':

                for _ in range(0, 5):
                    self.prev_image()

                self.thumbnail_labels[self.model.get_current_index() - self.model.get_leftmost_index()].setStyleSheet('')
                self.model.set_current_index(self.model.get_leftmost_index())
                self.thumbnail_labels[self.model.get_current_index() - self.model.get_leftmost_index()].setStyleSheet(self.selected_thumbnail_stylesheet)


    def show_fullscreen(self):
        self.pixmap = QPixmap(self.model.get_current_filename())       
        self.pixmap = self.pixmap.scaled(CONST_WIDTH, CONST_HEIGHT, Qt.KeepAspectRatio)
        
        self.label.setPixmap(self.pixmap)
        self.label.show()


    def next_image(self):
        # remove red highlight from current selection
        self.thumbnail_labels[self.model.get_current_index() - self.model.get_leftmost_index()].setStyleSheet('')
        self.model.set_current_index(self.model.get_current_index() + 1)

        self.check_index_bounds()
        self.reload_thumbnails()

        self.thumbnail_labels[self.model.get_current_index() - self.model.get_leftmost_index()].setStyleSheet(self.selected_thumbnail_stylesheet)


    def prev_image(self):       
        # remove red highlight from current 
        self.thumbnail_labels[self.model.get_current_index() - self.model.get_leftmost_index()].setStyleSheet('')
        self.model.set_current_index(self.model.get_current_index() - 1)

        self.check_index_bounds()
        self.reload_thumbnails()

        self.thumbnail_labels[self.model.get_current_index() - self.model.get_leftmost_index()].setStyleSheet(self.selected_thumbnail_stylesheet)


    def select_thumbnail(self, thumbnail_index):
        self.thumbnail_labels[self.model.get_current_index()].setStyleSheet('')
        self.model.set_current_index(thumbnail_index)
        self.check_index_bounds()

        self.thumbnail_labels[self.model.get_current_index()].setStyleSheet(self.selected_thumbnail_stylesheet)
        self.reload_thumbnails()


    def check_index_bounds(self):
        if self.model.get_current_index() > self.model.get_leftmost_index() + 4:

            if self.model.get_current_index() >= len(self.model.image_files) - 1:
                self.model.set_current_index(0)

            self.model.set_leftmost_index(self.model.get_current_index())
        
        elif self.model.get_current_index() < self.model.get_leftmost_index():
            self.model.set_leftmost_index(self.model.get_current_index() - 4)
            self.model.set_current_index(self.model.get_leftmost_index() + 4)


    def load_thumbnails(self):
        # load images into pixmap array
        for _ in self.model.image_files:
            self.thumbnail_pixmaps.append(QPixmap(self.model.get_current_filename()).scaled(100, 100, Qt.KeepAspectRatio))
            self.model.next_filename()

        for index in range(0, 5):
            # init thumbnail labels with corresponding pixmap
            self.thumbnail_labels.append(QLabel(self))
            self.thumbnail_labels[index].setPixmap(self.thumbnail_pixmaps[index])

            # positioning labels
            self.thumbnail_labels[index].resize(100,100)
            self.thumbnail_labels[index].setAlignment(Qt.AlignCenter)
            # TODO: remove magic numbers below
            self.thumbnail_labels[index].move(20 + index * 150 + (index * 20), (CONST_HEIGHT - 100) / 2)


    def reload_thumbnails(self):
        temp_index = self.model.get_leftmost_index()

        for label in self.thumbnail_labels:
            label.setPixmap(self.thumbnail_pixmaps[temp_index])
            temp_index += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
