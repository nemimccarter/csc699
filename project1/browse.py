from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QFrame, QHBoxLayout, QVBoxLayout, QApplication)
from PyQt5.QtGui import QPixmap
import json

from Model import *


CONST_BORDER = 20
CONST_THUMBNAIL_COUNT = 5
CONST_THUMBNAIL_SIZE = 100
CONST_NUM_TAGS = 10


class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.title = 'CSC 690 - Project 1'
        self.model = Model('./data/')
        self.view_mode = 'thumbnails'
        self.mode = 'thumbnails'
        self.stylesheet = ''
        self.selected_thumbnail_stylesheet = 'border: 5px solid red;'
        
        self.window_width = 800
        self.window_height = 600

        if len(sys.argv) > 1:
        	self.window_width = int(sys.argv[1])
        	self.window_height = self.window_width * (3/4)

        self.thumbnail_labels = []
        self.thumbnail_pixmaps = []
        self.tag_labels = []
        
        self.init_labels()
        self.init_controls()
        self.init_UI()


    def init_UI(self):
        self.fullscreen_pixmap = QPixmap(self.model.get_current_filename())

        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, self.window_width, self.window_height)
        self.setStyleSheet('background: #00C0FF;')

        self.load_thumbnails()

        # start with first thumbnail selected
        self.thumbnail_labels[0].setStyleSheet(self.selected_thumbnail_stylesheet)

        self.fullscreen_label.hide()
        self.hide_tags()
        self.show()


    def init_labels(self):
        self.fullscreen_label = QLabel(self)

        self.fullscreen_label.resize(self.window_width / 2, self.window_height / 2)
        self.fullscreen_label.setStyleSheet(self.selected_thumbnail_stylesheet)
        self.fullscreen_label.setAlignment(Qt.AlignCenter)
        self.fullscreen_label.setFocusPolicy(Qt.StrongFocus)
        self.fullscreen_label.move((self.window_width - (self.window_width / 2)) / 2, (self.window_height - (self.window_height/ 2)) /2)


        for index in range(0, CONST_NUM_TAGS):
        	temp_label = QLabel(self)
        	temp_label.move(650, 400 - (index * 30))
        	
        	self.tag_labels.append(temp_label)
        	
        	temp_label.hide()


    def init_controls(self):
        self.add_tag_button = QPushButton('Add tag', self)
        self.add_tag_button.setFocusPolicy(Qt.ClickFocus)
        self.add_tag_button.move(300, 550)
        self.add_tag_button.clicked.connect(self.add_tag)

        self.add_tag_button.hide()

        self.save_tags_button = QPushButton('Save all tags', self)
        self.save_tags_button.setFocusPolicy(Qt.ClickFocus)
        self.save_tags_button.move(400, 550)
        self.save_tags_button.clicked.connect(self.save_tags)

        self.save_tags_button.hide()

        self.tag_field = QLineEdit(self)
        self.tag_field.setFocusPolicy(Qt.ClickFocus)
        self.tag_field.move(self.window_width - 300, self.window_height - 100)

        self.tag_field.hide()


    def add_tag(self):
        self.model.add_tag(self.tag_field.text())
        self.setFocusPolicy(Qt.ClickFocus)
        self.show_tags()


    def save_tags(self):
    	self.model.save_tags('tags.txt')


    def keyPressEvent(self, event):
        key_pressed = event.key()

        if key_pressed == Qt.Key_Right:
            
            if self.mode == 'thumbnails':
                self.next_image()

            elif self.mode == 'fullscreen':
                self.next_image()
                self.show_fullscreen()
                self.show_tags()
        
        elif key_pressed == Qt.Key_Left:
            
            if self.mode == 'thumbnails':
                self.prev_image()
          
            elif self.mode == 'fullscreen':
                self.prev_image()
                self.show_fullscreen()
                self.show_tags()
        
        elif key_pressed == Qt.Key_Up: 
            
            if self.mode == 'thumbnails':
                self.mode = 'fullscreen'

                self.show_fullscreen()
                self.show_tags()

                self.add_tag_button.show()
                self.save_tags_button.show()
                self.tag_field.show()
            
                for label in self.thumbnail_labels:
                    label.hide()
        
        elif key_pressed == Qt.Key_Down:

            if self.mode == 'fullscreen':
                self.mode = 'thumbnails'
                self.fullscreen_label.hide()

                self.add_tag_button.hide()
                self.save_tags_button.hide()
                self.tag_field.hide()

                self.hide_tags()

                for label in self.thumbnail_labels:
                    label.show()
        
        elif key_pressed == 46:
            if self.mode == 'thumbnails':

                for _ in range(0, CONST_THUMBNAIL_COUNT):
                    self.next_image()

                self.thumbnail_labels[self.model.get_current_index() - self.model.get_leftmost_index()].setStyleSheet('')
                self.model.set_current_index(self.model.get_leftmost_index())
                self.thumbnail_labels[self.model.get_current_index() - self.model.get_leftmost_index()].setStyleSheet(self.selected_thumbnail_stylesheet)

        elif key_pressed == 44:
            if self.mode == 'thumbnails':

                for _ in range(0, CONST_THUMBNAIL_COUNT):
                    self.prev_image()

                self.thumbnail_labels[self.model.get_current_index() - self.model.get_leftmost_index()].setStyleSheet('')
                self.model.set_current_index(self.model.get_leftmost_index())
                self.thumbnail_labels[self.model.get_current_index() - self.model.get_leftmost_index()].setStyleSheet(self.selected_thumbnail_stylesheet)


    def show_fullscreen(self):
        self.fullscreen_pixmap = QPixmap(self.model.get_current_filename())       
        self.fullscreen_pixmap = self.fullscreen_pixmap.scaled(self.window_width / 2, self.window_height / 2, Qt.KeepAspectRatio)
        
        self.fullscreen_label.setPixmap(self.fullscreen_pixmap)
        self.fullscreen_label.show()

        self.show_tags()
        

    def show_tags(self):
        tags = self.model.get_tags()

        for label in self.tag_labels:
            label.setText('')

        for label, tag in zip(self.tag_labels, tags):
            label.hide()
            label.setText(str(tag))
            label.show()


    def hide_tags(self):
        for label in self.tag_labels:
            label.hide()


    def next_image(self):
        # remove red highlight from current selection
        self.thumbnail_labels[self.model.get_current_index() - self.model.get_leftmost_index()].setStyleSheet('')
        self.model.set_current_index(self.model.get_current_index() + 1)

        self.check_index_bounds()
        self.reload_thumbnails()

        print("Current index: " + str(self.model.get_current_index()))
        print("Leftmost index: " + str(self.model.get_leftmost_index()))
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
        current_index = self.model.get_current_index()
        leftmost_index = self.model.get_leftmost_index()

        if current_index > leftmost_index + 4:

        	# check if we've reached end of list
            if current_index >= len(self.model.nodes) - 1:
                self.model.set_current_index(0)

            self.model.set_leftmost_index(self.model.get_current_index())
        
        elif current_index < leftmost_index:
            self.model.set_leftmost_index(current_index - 4)
            self.model.set_current_index(self.model.get_leftmost_index() + 4)


    def load_thumbnails(self):
        # load images into pixmap array
        for _ in self.model.image_files:
            self.thumbnail_pixmaps.append(QPixmap(self.model.get_current_filename()).scaled(CONST_THUMBNAIL_SIZE, CONST_THUMBNAIL_SIZE, Qt.KeepAspectRatio))
            self.model.next_filename()

        for index in range(0, CONST_THUMBNAIL_COUNT):
            # init thumbnail labels with corresponding pixmap
            self.thumbnail_labels.append(QLabel(self))
            self.thumbnail_labels[index].setPixmap(self.thumbnail_pixmaps[index])

            # positioning labels
            self.thumbnail_labels[index].resize(CONST_THUMBNAIL_SIZE, CONST_THUMBNAIL_SIZE)
            self.thumbnail_labels[index].setAlignment(Qt.AlignCenter)
            # TODO: remove magic numbers below
            self.thumbnail_labels[index].move(10 + index * 150 + (index * 20), (self.window_height - CONST_THUMBNAIL_SIZE) / 2)


    def reload_thumbnails(self):
        temp_index = self.model.get_leftmost_index()

        for label in self.thumbnail_labels:
            label.setPixmap(self.thumbnail_pixmaps[temp_index])
            temp_index += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
