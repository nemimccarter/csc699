###############################################
# File: model.py                              #
# By: Nehemya McCarter-Ribakoff               #  
# Date: [date last revised]                   #
# Usage: python McCarter-RibakoffP1.py        #
# System: Linux Debian 9.2                    #
# Description: Data model for main program.   #
#              Stores images in a circular    #
#              linked list.                   # 
###############################################

from os import listdir
from PIL import Image as PImage

#TODO: ask Hsu if it's ok to have both classes in 1 file
class Node:
    def __init__(self, data, next):
        self.data = data
        self.next = next

class List:
    def __init__(self):
        self.head = Link(None, None) # sentinel node
        self.head.next = self.head   # list initially empty

    def add_node(self, data):
        self.head.next = Link(self, self.head.next)
