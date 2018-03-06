from PyQt5.QtGui import QPixmap
from os import listdir, walk
from os.path import isfile, join
import sys
import click


class Image_Node():
    def __init__(self, image, index, tags):
        self.image = image
        self.tags = []

        self.add_tags(tags)


    def add_tags(self, tags):
        for tag in tags:
            self.tags.append(tag)


    def get_tags(self, filename):
        return self.tags


    def set_image(self, image_filename):
        self.image = QPixmap(image_filename)


    def get_image(self):
        return self.image




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
        #   self.add_node_image(image)

        for tag in self.all_tags:
            self.add_tags(tag)


    def get_current_node(self):
        return self.nodes[self.current_index]


    def selet_next_node(self):
        self.current_index += 1


    def select_prev_node(self):
        self.current_index += 1


    def add_node(self, node):
        self.nodes.append(node)


    # adds tags to current node
    def add_tags(tags):
        self.nodes[self.current_index].add_tags(tags)


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


    def set_current_index(self, new_index):
        self.current_index = new_index


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
        #   node.add_tags(all_tags)


    def get_leftmost_index(self):
        return self.leftmost_index


    def set_leftmost_index(self, new_index):
        if new_index > len(self.image_files) - 6:
            new_index = 0
        elif new_index < 0:
            new_index = len(self.image_files) - 6

        self.leftmost_index = new_index