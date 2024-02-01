from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5 import QtWidgets
from PyQt5 import QtGui 
import os, sys
from sys import platform as _platform

from MainWindow import MainWindow as mw

def info():
    print("ParrotBrowser - A simple web browser made with PyQt5")
    print("OS: " + _platform)
    print("Python: " + sys.version)
    print("PyQt5: " + str(QtWidgets.QStyleFactory.keys()))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mw()
    app.exec_()