###############################################
# File: McCarter-RibakoffNP1.py               #
# By: Nehemya McCarter-Ribakoff               #  
# Date: [date last revised]                   #
# Usage: python McCarter-RibakoffP1.py        #
# System: Linux Debian 9.2                    #
# Description: Simple image browser. User may #
#              view five consecutive images   #
#              from a folder or select one to #
#              view                           # 
###############################################

import sys
from PyQt5.QtWidgets import QApplication, QWidget

if __name__ == '__main__':

    # create window
    app = QApplication(sys.argv)

    w = QWidget()
    w.resize(800, 600)
    w.move(300, 100)
    w.setWindowTitle('I am a window')
    w.show()

    sys.exit(app.exec_())
