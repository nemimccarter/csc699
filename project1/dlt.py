from os import listdir, walk
from os.path import isfile, join
import sys

data_files = []
for (dirpath, dirnames, filenames) in walk("./data"):
    data_files.extend(filenames)
    break
print(data_files)

