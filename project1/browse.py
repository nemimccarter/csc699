from PyQt5.QtCore import (Qt, QUrl)
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QPushButton, QFrame, QHBoxLayout, QVBoxLayout, QApplication)
from PyQt5.QtGui import QPixmap
from PyQt5.QtMultimedia import QSoundEffect

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

        self.window_width = 800
        self.window_height = 600

        if len(sys.argv) > 1:
        	if int(sys.argv[1]) >= 600 and int(sys.argv[1]) <= 1200:
        		self.window_width = int(sys.argv[1])
        		self.window_height = self.window_width * (3/4)
        	else:
        		print("Given width out of range. Defaulting to 600.")
        
        self.init_labels()
        self.init_controls()
        self.init_UI()
        self.init_sounds()


    def init_UI(self):
        self.fullscreen_pixmap = QPixmap(self.model.get_current_filename())

        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, self.window_width, self.window_height)
        self.setStyleSheet('background: #00C0FF;')

        self.load_thumbnails()

        # start with first thumbnail selected
        self.thumbnail_labels[0].setStyleSheet(self.selected_thumbnail_stylesheet)

        self.fullscreen_label.hide()
        for label in self.tag_labels:
            label.hide()
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
        self.add_tag_button.move((self.window_width / 2) - 180, self.window_height - 50)
        self.add_tag_button.clicked.connect(self.add_tag)

        self.add_tag_button.hide()

        self.search_button = QPushButton('Search', self)
        self.search_button.setFocusPolicy(Qt.ClickFocus)
        self.search_button.move(self.window_width / 3.7, self.window_height - (self.window_height / 10))
        self.search_button.clicked.connect(self.search_flickr)

        self.save_tags_button = QPushButton('Save all tags', self)
        self.save_tags_button.setFocusPolicy(Qt.ClickFocus)
        self.save_tags_button.move((self.window_width / 2) - 10, self.window_height - 50)
        self.save_tags_button.clicked.connect(self.save_tags)

        self.save_tags_button.hide()

        self.tag_field = QLineEdit(self)
        self.tag_field.setFocusPolicy(Qt.ClickFocus)
        self.tag_field.setAlignment(Qt.AlignCenter)
        self.tag_field.move((self.window_width / 2) - 90, self.window_height - 100)

        self.tag_field.hide()

        self.search_text_field = QLineEdit(self)
        self.search_text_field.setFocusPolicy(Qt.ClickFocus)
        self.search_text_field.move(self.window_width / 28, self.window_height - (self.window_height / 10))

        self.search_number_field = QLineEdit(self)
        self.search_number_field.setFocusPolicy(Qt.ClickFocus)
        self.search_number_field.move(self.window_width / 2.5, self.window_height - (self.window_height / 10))
        self.search_number_field.setFixedWidth(60)

        self.test_button = QPushButton('Test', self)
        self.test_button.setFocusPolicy(Qt.ClickFocus)
        self.test_button.move(self.window_width / 28, self.window_height - (self.window_height / 19))
        self.test_button.clicked.connect(self.test)

        self.save_photos_button = QPushButton('Save', self)
        self.save_photos_button.setFocusPolicy(Qt.ClickFocus)
        self.save_photos_button.move(self.window_width / 7.3, self.window_height - (self.window_height / 19))
        self.save_photos_button.clicked.connect(self.save_photos)

        self.exit_button = QPushButton('Exit', self)
        self.exit_button.setFocusPolicy(Qt.ClickFocus)
        self.exit_button.move(self.window_width / 4.2, self.window_height - (self.window_height / 19))
        self.exit_button.clicked.connect(self.close)

        self.delete_button = QPushButton('Delete', self)
        self.delete_button.setFocusPolicy(Qt.ClickFocus)
        self.delete_button.move(self.window_width / 2.95, self.window_height - (self.window_height / 19))
        self.delete_button.clicked.connect(self.delete)


    def init_sounds(self):
        self.train_sound = QSoundEffect()
        self.train_sound.setSource(QUrl.fromLocalFile('./audio/TRAIN06.WAV'))
        self.train_sound.setVolume(0.5)

        self.conk_sound = QSoundEffect()
        self.conk_sound.setSource(QUrl.fromLocalFile('./audio/CONK.WAV'))
        self.conk_sound.setVolume(0.5)
    

    def add_tag(self):
        self.model.add_tag(self.tag_field.text())
        self.setFocusPolicy(Qt.ClickFocus)
        self.show_tags()

    def delete(self):
        pass


    def hide_thumbnail_controls(self):
        self.search_text_field.hide()
        self.search_number_field.hide()


    def keyPressEvent(self, event):
        key_pressed = event.key()

        if key_pressed == Qt.Key_Right:
            
            if self.mode == 'thumbnails':
                self.next_image()

            elif self.mode == 'fullscreen':
                self.next_image()
                self.show_fullscreen_image()
                self.show_tags()
        
        elif key_pressed == Qt.Key_Left:
            
            if self.mode == 'thumbnails':
                self.prev_image()
          
            elif self.mode == 'fullscreen':
                self.prev_image()
                self.show_fullscreen_image()
                self.show_tags()
        
        elif key_pressed == Qt.Key_Up: 
            
            if self.mode == 'thumbnails':
                self.mode = 'fullscreen'

                self.conk_sound.play()

                self.show_fullscreen_image()
                self.show_fullscreen_view()

        
        elif key_pressed == Qt.Key_Down:

            if self.mode == 'fullscreen':
                self.mode = 'thumbnails'

                self.conk_sound.play()

                self.fullscreen_label.hide()
                self.show_thumbnails_view()
        
        elif key_pressed == 46:
            if self.mode == 'thumbnails':

                self.train_sound.play()

                for _ in range(0, CONST_THUMBNAIL_COUNT):
                    self.next_image()

                self.thumbnail_labels[self.model.get_current_index() % 5].setStyleSheet('')
                self.model.set_current_index(self.model.get_leftmost_index())
                self.thumbnail_labels[self.model.get_current_index() % 5].setStyleSheet(self.selected_thumbnail_stylesheet)

        elif key_pressed == 44:
            if self.mode == 'thumbnails':

                self.train_sound.play()

                for _ in range(0, CONST_THUMBNAIL_COUNT):
                    self.prev_image()

                self.thumbnail_labels[self.model.get_current_index() % 5].setStyleSheet('')
                self.model.set_current_index(self.model.get_leftmost_index())
                self.thumbnail_labels[self.model.get_current_index() % 5].setStyleSheet(self.selected_thumbnail_stylesheet)


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

            self.thumbnail_labels[index].move(self.window_width / (self.window_width / 30) + (index * self.window_width / 5), (self.window_height - CONST_THUMBNAIL_SIZE) / 2)
            #self.thumbnail_labels[index].move((self.window_width / (self.window_width / 10)) + index * self.window_width / 5, (self.window_height - CONST_THUMBNAIL_SIZE) / 2)


    def next_image(self):
        # remove red highlight from current selection
        self.thumbnail_labels[self.model.get_current_index() % 5].setStyleSheet('')

        self.model.select_next_node()

        self.reload_thumbnails()


    def prev_image(self):       
        # remove red highlight from current 
        self.thumbnail_labels[self.model.get_current_index() % 5].setStyleSheet('')

        self.model.select_prev_node()

        self.reload_thumbnails()


    def reload_thumbnails(self):
        print("current: " + str(self.model.get_current_index()))
        print("leftmost: " + str(self.model.get_leftmost_index()))
        print("current - leftmost: " + str(self.model.get_current_index() % 5))

        if (self.model.get_current_index() > self.model.get_leftmost_index() + 4):
            self.model.set_leftmost_index(self.model.get_current_index())
        elif (self.model.get_current_index() < self.model.get_leftmost_index() and self.model.get_leftmost_index() != len(self.model.nodes) - 1):
            self.model.set_leftmost_index(self.model.get_leftmost_index() - 5)
        elif (self.model.get_leftmost_index() == len(self.model.nodes) - 1 and self.model.get_current_index() == 4):
            self.model.set_leftmost_index(self.model.get_current_index())

        temp_index = self.model.get_leftmost_index()

        for label in self.thumbnail_labels:
            temp_index = self.model.check_index_bounds(temp_index)

            label.setPixmap(self.thumbnail_pixmaps[temp_index])
            
            temp_index += 1

        self.thumbnail_labels[self.model.get_current_index() % 5].setStyleSheet(self.selected_thumbnail_stylesheet)


    def save_photos(self):
        pass


    def save_tags(self):
        self.model.save_tags('tags.txt')


    def search_flickr(self):
        results = self.model.search_flickr(self.search_text_field, self.search_text_field.text())
        print(results)
        
        self.setFocusPolicy(Qt.ClickFocus)


    def show_fullscreen_image(self):
        self.fullscreen_pixmap = QPixmap(self.model.get_current_filename())       
        self.fullscreen_pixmap = self.fullscreen_pixmap.scaled(self.window_width / 2, self.window_height / 2, Qt.KeepAspectRatio)
        
        self.fullscreen_label.setPixmap(self.fullscreen_pixmap)
        self.fullscreen_label.show()

        self.show_tags()


    def show_fullscreen_view(self):
        self.add_tag_button.show()
        self.save_tags_button.show()
        self.tag_field.show()
        self.show_tags()
            
        for label in self.thumbnail_labels:
            label.hide()

        self.search_button.hide()
        self.search_text_field.hide()
        self.search_number_field.hide()
        self.test_button.hide()
        self.save_photos_button.hide()
        self.exit_button.hide()
        self.delete_button.hide()        


    def show_tags(self):
        tags = self.model.get_tags()

        for label in self.tag_labels:
            label.setText('')

        for label, tag in zip(self.tag_labels, tags):
            label.hide()
            label.setText(str(tag))
            label.show()


    def show_thumbnail_controls(self):
    	self.search_text_field.show()
    	self.search_number_field.show()


    def show_thumbnails_view(self):
        for label in self.thumbnail_labels:
            label.show()

        self.add_tag_button.hide()
        self.save_tags_button.hide()
        self.tag_field.hide()
        for label in self.tag_labels:
            label.hide()

        self.search_button.show()
        self.search_text_field.show()
        self.search_number_field.show()
        self.search_button.show()
        self.search_text_field.show()
        self.search_number_field.show()
        self.test_button.show()
        self.save_photos_button.show()
        self.exit_button.show()
        self.delete_button.show()


    def test(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())
