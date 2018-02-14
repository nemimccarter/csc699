###############################################
# File: model.py                              #
# By: Nehemya McCarter-Ribakoff               #  
# Date: [date last revised]                   #
# Usage: python browser.py                    #
# System: Linux Debian 9.2                    #
# Description: Data model for main program.   #
#              Stores images in a circular    #
#              list.                          # 
###############################################

from os import listdir, walk
from os.path import isfile, join
from itertools import cycle
import sys

class Model:
    data_files = []

    def __init__(self):
        for (dirpath, dirnames, filenames) in walk("./data"):
            self.data_files.extend(filenames)
            break
        self.data_files.sort()
        self.data_files = cycle(self.data_files)
    def get_image():
        return next(self.data_files)
