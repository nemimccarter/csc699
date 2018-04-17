from PyQt5.QtGui import QPixmap
from PyQt5 import QtGui
from os import listdir, walk
import os
import sys
import click
import json
from flickrapi import FlickrAPI
import urllib.request

CONST_FLICKR_KEY = '68bb2464e8b9435179751681b0fe46de'
CONST_FLICKR_SECRET = 'b04691a0177e2bbb'

flickr = FlickrAPI(CONST_FLICKR_KEY, CONST_FLICKR_SECRET, format = 'parsed-json')
extras='url_sq,url_t,url_s,url_q,url_m,url_n,url_z,url_c,url_l,url_o'
# Search format: cats = flickr.photos.search(text='kitten', per_page=5, extras=extras)

class Image_Node():
    def __init__(self, image, index, tags):
        self.image = QPixmap(image)
        self.tags = []

        self.add_tag(tags)


    def add_tag(self, tag):
        self.tags.append(tag)


    def get_image(self):
        return self.image


    def get_tags(self):
        return self.tags


    def set_image(self, image_filename):
        self.image = QPixmap(image_filename)




class Model():
    def __init__(self, dir_name):
        self.image_files = []
        self.nodes = []

        self.current_index = 0
        self.leftmost_index = 0
        
        self.dir_name = dir_name
        self.all_tags = []

        # load images into self.image_files
        for (dirpath, dirnames, filenames) in walk(dir_name):
            self.image_files.extend(filenames)
            break
        
        self.image_files.sort()

        # WARNING: Tags may only be one word
        saved_tags_string = self.load_tags('tags.txt')
        saved_tags = saved_tags_string.split('\n')

        # append empty strings to match length of image_files
        if len(self.image_files) > len(saved_tags):
            for index in range(len(saved_tags) - 1, len(self.image_files) - 1):
                saved_tags.append('')

        # create self.nodes from self.image_files
        index = 0
        for image, tag_string in zip(self.image_files, saved_tags):
            new_node = Image_Node(self.dir_name + image, index, '')
            
            for tag in tag_string.split(', '):
                new_node.add_tag(tag)
            
            self.add_node(new_node)
            index += 1

        for tag in self.all_tags:
            self.add_tags(tag)


    def add_node(self, node):
        self.nodes.append(node)


    # adds tags to current node
    def add_tag(self, tag):
        self.nodes[self.get_current_index()].add_tag(tag)


    # def check_index_bounds(self, temp_index):
    #     if temp_index - self.get_leftmost_index() > 4:
    #         if (self.get_current_index() >= len(self.image_files)):
    #             self.set_current_index(0)

    #         self.set_leftmost_index(self.get_current_index())
    #         temp_index = self.get_current_index()
    #     if temp_index < self.get_leftmost_index() and self.get_leftmost_index() == len(self.image_files) - 1:


    #     return temp_index


    def check_index_bounds(self, temp_index):
        if temp_index >= len(self.nodes):
            temp_index = 0
        elif temp_index < 0:
            temp_index = len(self.nodes) - 1
        return temp_index
        # if temp_index < self.get_leftmost_index():
        #     if temp_index == 4:
        #         temp_index = 3
        #     elif temp_index == 0:
        #         temp_index = self.get_current_index()

        # if temp_index >= len(self.nodes):
        #     self.set_current_index(0)
        #     temp_index = 0
        # elif temp_index < 0:
        #     temp_index = self.get_current_index()

        return temp_index


    def delete(self):
        del self.nodes[self.get_current_index()]
        if self.get_current_index() == len(self.nodes) - 1:
            self.set_current_index(0)


    def get_current_node(self):
        return self.nodes[self.current_index]


    def get_current_filename(self):
        return self.dir_name + self.image_files[self.current_index]


    def get_current_index(self):
        return self.current_index


    def get_leftmost_index(self):
        return self.leftmost_index


    def get_tags(self):
        return self.get_current_node().get_tags()
        # tags_string = ''
        # for tag in self.get_current_node().tags:
        #     tags_string += str(tag)
        #     tags_string += ' '
        # return tags_string


    def load_tags(self, save_filename):
        save_filename = open(save_filename, 'r')
        all_tags = save_filename.read()

        return all_tags
        #for tag, node in zip(all_tags, self.nodes):
        #    node.add_tag(tag)    def next_filename(self):
        self.current_index += 1

        if self.current_index >= len(self.nodes):
            self.current_index = 0


    def save_nodes(self):
        index = 0

        # clear contents of image directory
        filelist = [ f for f in os.listdir("./data") if f.endswith(".png") ]
        for f in filelist:
            os.remove('./data/' + f)
            print('removed ' + f)
        
        for node in self.nodes:
            if node.get_tags() != '':
                if index <= 9:
                    index = '0' + str(index)
                node.get_image().save('./data/image' + str(index) + '.png', format='PNG', quality=1)
                index = int(index)
            index += 1

        self.save_tags('tags.txt')


    def save_tags(self, save_filename):
        save_file = open(save_filename, 'w')
        tags_list = ''

        for node in self.nodes:
            node_tags = node.get_tags()
            #node_tags.remove('')
            
            node_tags_string = ', '.join(str(tag) for tag in node_tags)
            tags_list += node_tags_string + '\n'

        save_file.write("%s\n" % tags_list)

        save_file.close()
        print("Tags saved")


    def set_current_index(self, new_index):
        self.current_index = new_index    


    def set_leftmost_index(self, new_index):
        # if new_index > len(self.image_files):
        #     new_index = 4
        # elif new_index < 0:
        #     new_index = len(self.image_files) - 5

        self.leftmost_index = new_index


    # searches flickr for num_results tags matching search_string
    # appends results to model 
    def search_flickr(self, search_string, num_results):
        results = flickr.photos.search(text=search_string, per_page=num_results, extras=extras)
        print('Searching for ' + search_string)

        for result in results["photos"]["photo"]:
            image_url = result["url_c"]
            print(image_url)

            image_data = urllib.request.urlopen(image_url).read()
            image = QtGui.QImage()
            image.loadFromData(image_data)
            
            node = Image_Node(image, len(self.nodes), '')
            self.nodes.append(node)

        self.set_current_index(len(self.nodes) - int(num_results))
        self.set_leftmost_index(self.get_current_index())

    def select_next_node(self):
        self.current_index += 1

        if self.get_current_index() >= len(self.nodes):
            print("current index reset")
            self.current_index = 0


    def select_prev_node(self):
        self.current_index -= 1

        if self.get_current_index() < 0:
            self.current_index = len(self.nodes) - 1


    # def prev_filename(self):
    #     self.current_index -= 1

    #     if (self.current_index < 0):
    #         self.current_index = len(self.image_files) - 1