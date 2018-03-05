from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QFrame, QHBoxLayout, QApplication)
from PyQt5.QtGui import QPixmap
import json

from os import listdir, walk
from os.path import isfile, join
import sys
import click

CONST_WIDTH = 800
CONST_HEIGHT = 600
CONST_BORDER = 20
CONST_THUMBNAIL_COUNT = 5


class Image_Node():
	def __init__(self, image, index, tags):
		self.image = image
		self.index = index
		self.tags = []

		self.add_tags(tags)


	def add_tags(self, tags):
		for tag in tags:
			self.tags.append(tag)

	def read_tags(self, filename):
		print("reading")

class Model():
    def __init__(self, dir_name):
        self.image_files = []
        self.nodes = []

        self.current_index = 0
        self.leftmost_index = 0
        
        self.dir_name = dir_name
        self.all_tags = []

        for (dirpath, dirnames, filenames) in walk(dir_name):
            self.image_files.extend(filenames)
            break
        
        self.image_files.sort()

        self.load_tags('tags.txt')
        #for image in image_files:
        #	self.add_node_image(image)

        for tag in self.all_tags:
        	self.add_tags(tag)


    def add_node_image(self, image):
    	self.nodes.append(image)


    def add_tags(tags):
    	for node in self.nodes:
    		node.add_tag(tag)


    def next_filename(self):
        self.current_index += 1

        if self.current_index >= len(self.image_files):
            self.current_index = 0


    def prev_filename(self):
        self.current_index -= 1

        if (self.current_index < 0):
            self.current_index = len(self.image_files) - 1

    def get_current_filename(self):
        return self.dir_name + self.image_files[self.current_index]


    def get_current_index(self):
        return self.current_index


    def get_tags(self, current_node):
    	return current_node.tags


    def save_tags(self, save_filename):
    	save_file = open(save_filename, 'w')

    	for node in nodes:
    		json.dump(node.get_tags, save_file)

    	save_file.close()


    def load_tags(self, save_filename):
    	save_file = open(save_filename, 'r')
    	#self.all_tags = json.load(save_file)

    	#for all_tags, node in zip(all_tags, self.nodes):
    	#	node.add_tags(all_tags)

    def get_leftmost_index(self):
        return self.leftmost_index

    def set_leftmost_index(self, new_index):
        if new_index > len(self.image_files) - 6:
            new_index = 0
        elif new_index < 0:
            new_index = len(self.image_files) - 6

        self.leftmost_index = new_index


class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        self.title = 'CSC 690 - Project 1'
        self.image_files = []
        self.current_index = 0
        self.model = Model('./data/')
        
        self.thumbnail_labels = []
        self.thumbnail_pixmaps = []
        self.thumbnail_index = 0
        
        self.view_mode = 'thumbnails'
        self.selected_thumbnail = 0
        self.mode = 'thumbnails'
        
        self.tag_field = QLineEdit(self)
        self.tag_field.setFocusPolicy(Qt.ClickFocus)
        self.tags_label = QLabel(self)        

        self.stylesheet = '''
                          background: solid black;
                          '''

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

        self.thumbnail_labels[0].setStyleSheet('border: 5px solid red;')

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
        		self.select_next_thumbnail()

        	self.next_image()
        
        elif key_pressed == Qt.Key_Left:
        	
        	if self.mode == 'thumbnails':
        		self.select_prev_thumbnail() 

        	self.prev_image()
        
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
        		#self.select_thumbnail(2)

        		for label in self.thumbnail_labels:
        			label.show()
        
        elif key_pressed == 46:
            if self.mode == 'thumbnails':
                for _ in range(0, 5):
                    self.select_next_thumbnail()

        elif key_pressed == 44:
            if self.mode == 'thumbnails':
                for _ in range(0, 5):
                    self.select_prev_thumbnail()

    def show_fullscreen(self):
        self.pixmap = QPixmap(self.model.get_current_filename())       
        self.pixmap = self.pixmap.scaled(CONST_WIDTH, CONST_HEIGHT, Qt.KeepAspectRatio)
        
        self.label.resize(CONST_WIDTH, CONST_HEIGHT)
        self.label.setPixmap(self.pixmap)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.show()


    def set_current_index(self, new_index):
        self.model.current_index = new_index

    
    def get_leftmost_index(self):
        return self.model.leftmost_index


    def set_leftmost_index(self, new_index):
        if new_index < 0:
            new_index = len(self.model.image_files - 5)
        self.model.leftmost_index = new_index


    def select_next_thumbnail(self):
        # remove red highlight from current selection
        self.thumbnail_labels[self.model.get_current_index() - self.model.get_leftmost_index()].setStyleSheet('')
        self.set_current_index(self.model.get_current_index() + 1)

        if self.model.get_current_index() > self.model.get_leftmost_index() + 4:

            if self.model.get_current_index() >= len(self.model.image_files) - 1:
                self.set_current_index(0)

            self.model.set_leftmost_index(self.model.get_current_index())

            self.reload_thumbnails()

        self.thumbnail_labels[self.model.get_current_index() - self.get_leftmost_index()].setStyleSheet('border: 5px solid red;')


    def select_prev_thumbnail(self):       
        # remove red highlight from current 
        self.thumbnail_labels[self.model.get_current_index() - self.model.get_leftmost_index()].setStyleSheet('')
        self.set_current_index(self.model.get_current_index() - 1)

        if self.model.get_current_index() < self.model.get_leftmost_index():
            self.model.set_leftmost_index(self.model.get_current_index() - 4)
            self.set_current_index(self.model.get_leftmost_index() + 4)
            self.reload_thumbnails()

        self.thumbnail_labels[self.model.get_current_index() - self.get_leftmost_index()].setStyleSheet('border: 5px solid red;')


    def select_thumbnail(self, thumbnail_index):
    	self.thumbnail_labels[self.selected_thumbnail].setStyleSheet('')
    	self.selected_thumbnail = thumbnail_index

    	self.thumbnail_labels[self.selected_thumbnail].setStyleSheet('border: 5px solid red;')
 

    def next_image(self):
        '''
        self.model.next_filename()
        
        if self.mode == 'fullscreen':
        	self.show_fullscreen()
        '''

    def prev_image(self):
        '''
    	self.model.prev_filename()
    	
    	if self.mode == 'fullscreen':
    		self.show_fullscreen()
        '''

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

    def cycle_thumbnails_prev(self):
    	# TODO: two sources of truth. make only one
    	
    	while self.selected_thumbnail >= 0:
    		self.thumbnail_index -= 1
    		self.prev_image()
    		self.selected_thumbnail -= 1

    	self.selected_thumbnail = 4

    	for label in self.thumbnail_labels:

    		if self.thumbnail_index >= len(self.thumbnail_pixmaps):
	    		self.thumbnail_index = 0

	    	label.setPixmap(self.thumbnail_pixmaps[self.thumbnail_index])
	    	self.thumbnail_index += 1
	    

    def cycle_thumbnails_next(self):
    	# TODO: two sources of truth. make only one
    	while self.selected_thumbnail < 5:
    		self.thumbnail_index += 1
    		self.next_image()
    		self.selected_thumbnail += 1

    	self.selected_thumbnail = 0

    	for label in self.thumbnail_labels:

    		if self.thumbnail_index >= len(self.thumbnail_pixmaps):
	    		self.thumbnail_index = 0

	    	label.setPixmap(self.thumbnail_pixmaps[self.thumbnail_index])
	    	self.thumbnail_index += 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
