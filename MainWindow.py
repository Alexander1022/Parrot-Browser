from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5 import QtWidgets
from PyQt5 import QtGui
from SettingsWindow import SettingsWindow as sw
import configparser
import os.path

PARROT_ICON = "./assets/parrot.png"
BACK_ICON = "./assets/back.png"
FORWARD_ICON = "./assets/forward.png"
RELOAD_ICON = "./assets/reload.png"
CONFIG_FILE = "config.ini"
DEFAULT_HOMEPAGE = "https://www.duckduckgo.com"

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow,self).__init__(*args, **kwargs)
        self.config = configparser.ConfigParser()
        self.default_url = None
        self.read_url()
        self.settings = QSettings("Xander", "ParrotBrowser")
        self.setMinimumSize(QSize(1000, 600))
        self.setWindowTitle("ParrotBrowser")
        self.setWindowIcon(QtGui.QIcon(PARROT_ICON))
        self.setStyleSheet("background-color: white;")

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl(self.default_url))
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
        navtb.setIconSize(QSize(20, 20))
        self.addToolBar(navtb)

        navtb.setStyleSheet(
            "QToolBar { background-color: #2c3e50; border: 1px solid #34495e; border-radius: 5px; }"
            "QToolButton { background-color: transparent; border: none; }"
            "QToolButton:hover { background-color: #34495e; }"
        )

        back_icon = QIcon(BACK_ICON)
        forward_icon = QIcon(FORWARD_ICON)
        reload_icon = QIcon(RELOAD_ICON)

        back_btn = QAction(QIcon(BACK_ICON), "Back", self)
        back_btn.setStatusTip("Back button")
        back_btn.triggered.connect(lambda: self.tabs.currentWidget().back())
        navtb.addAction(back_btn)

        forward_btn = QAction(QIcon(FORWARD_ICON), "Forward", self)
        forward_btn.setStatusTip("Forward button")
        forward_btn.triggered.connect(lambda: self.tabs.currentWidget().forward())
        navtb.addAction(forward_btn)

        reload_btn = QAction(QIcon(RELOAD_ICON), "Reload", self)
        reload_btn.setStatusTip("Reload button")
        reload_btn.triggered.connect(self.browser.reload)
        navtb.addAction(reload_btn)

        self.urlbar = QLineEdit(self)
        self.urlbar.setStyleSheet(
            "QLineEdit { background-color: #34495e; color: #ecf0f1; border: 1px solid #2c3e50; border-radius: 5px; padding: 5px; }"
        )
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

        settings_btn = QAction("Settings", self)
        settings_btn.setStatusTip("Settings button")
        settings_btn.triggered.connect(self.open_settings_window)
        navtb.addAction(settings_btn)

        self.add_new_tab(QUrl(self.default_url), "Homepage")
        self.show()

    def open_settings_window(self, checked):
        self.s = sw()
        self.s.show()

    def navigate_to_url(self):
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
            url = QUrl(DEFAULT_HOMEPAGE)

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

    def create_config(self):
        if 'DEFAULT' not in self.config:
            self.config['DEFAULT'] = {}

        if 'homepage' not in self.config['DEFAULT']:
            self.config['DEFAULT']['homepage'] = DEFAULT_HOMEPAGE

        with open(CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)
            print("Config file created")

    def read_url(self):
        if not os.path.isfile(CONFIG_FILE):
            self.create_config()

        self.config.read(CONFIG_FILE)
        self.default_url = self.config['DEFAULT']['homepage']
