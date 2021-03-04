from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5 import QtWidgets
from PyQt5 import QtGui 
import os, sys
from sys import platform as _platform

def info():
    if _platform == "linux" or _platform == "linux2":
        return "linux"
    elif _platform == "darwin":
        return "macos"
    elif _platform == "win32":
        return "windows"
    elif _platform == "win64":
        return "windows"

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        #self.setMinimumSize(QSize(500, 200)) 
        self.setFixedHeight(300)
        self.setFixedWidth(600)
        self.setWindowTitle("ParrotBrowser - Settings") 
        self.setWindowIcon(QtGui.QIcon('parrot.png')) 
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.textbox = QLineEdit(self)
        self.button = QPushButton("Change", self)
         
class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)

        self.settings = QSettings("Xander", "ParrotBrowser")
        self.setMinimumSize(QSize(1000, 600))    
        self.setWindowTitle("ParrotBrowser") 
        self.setWindowIcon(QtGui.QIcon('parrot.png')) 
        self.setStyleSheet("background-color: white;")

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://duckduckgo.com/"))
        self.setCentralWidget(self.browser)

        self.tabs = QTabWidget() 
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True) 
        self.tabs.tabBarDoubleClicked.connect(self.tab_opened) 
        self.tabs.currentChanged.connect(self.tab_changed) 
        self.tabs.tabCloseRequested.connect(self.close_tab) 
        self.setCentralWidget(self.tabs) 

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        navtb = QToolBar("Navigation")
        navtb.setIconSize(QSize(30, 30))
        self.addToolBar(navtb)

        back_btn = QAction(QIcon('back.png'), "Back", self)
        back_btn.setStatusTip("Back button")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        forward_btn = QAction(QIcon('forward.png'), "Forward", self)
        forward_btn.setStatusTip("Forward button") 
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(forward_btn)

        reload_btn = QAction(QIcon('reload.png'), "Reload", self)
        reload_btn.setStatusTip("Reload button") 
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        self.urlbar = QLineEdit(self)
        self.urlbar.setStyleSheet("background-color: black; color: white;")
        self.urlbar.returnPressed.connect(self.goThere)
        navtb.addWidget(self.urlbar)

        settings_btn = QAction("Settings", self)
        settings_btn.setStatusTip("Settings button")
        settings_btn.triggered.connect(self.openSettingsWindows)
        navtb.addAction(settings_btn)

        self.add_new_tab(QUrl("https://duckduckgo.com/"), "Homepage")
        self.show()

    def openSettingsWindows(self, checked):
        self.s = SettingsWindow()
        self.s.show()

    def goThere(self):
        addr = QUrl(self.urlbar.text())

        if addr.scheme() == "":
            addr.setScheme("http")

        self.tabs.currentWidget().setUrl(addr)

    def close_tab(self, i):
        self.tabs.removeTab(i)

    def update_tab_info(self, browser): 
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("ParrotBrowser " + title)

    def tab_changed(self, i):
        url = self.tabs.currentWidget().url()

        self.update_urlbar(url, self. tabs.currentWidget())
        self.update_tab_info(self.tabs.currentWidget())

    def tab_opened(self, i):
        self.add_new_tab()

    def add_new_tab(self, url = None, label = "New tab"):
        if url is None:
            url = QUrl("https://duckduckgo.com/")

        browser = QWebEngineView()
        browser.setUrl(url)

        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda url, browser = browser:self.update_urlbar(url, browser))
        browser.loadFinished.connect(lambda _, i = i, browser = browser:self.tabs.setTabText(i, browser.page().title()))

    def update_urlbar(self, q, browser = None):
        if browser != self.tabs.currentWidget():
            return

        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

if __name__ == "__main__":
    print(info())
    app = QApplication(sys.argv)
    window = MainWindow()

    app.exec_()