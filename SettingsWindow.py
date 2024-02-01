from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtPrintSupport import *
from PyQt5 import QtWidgets
from PyQt5 import QtGui
import configparser

PARROT_ICON = "./assets/parrot.png"
CONFIG_FILE = "config.ini"

class SettingsWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.config = configparser.ConfigParser()

        self.setFixedSize(600, 300)
        self.setWindowTitle("ParrotBrowser - Settings")
        self.setWindowIcon(QtGui.QIcon(PARROT_ICON))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(2)

        label_url = QLabel("Default Homepage URL:")
        label_url.setStyleSheet("color: black;")

        self.textbox = QLineEdit(self)
        self.textbox.setStyleSheet("background-color: white; color: black;")

        self.button_save = QPushButton("Save Settings", self)
        self.button_save.setStyleSheet("background-color: #4CAF50; color: black;")

        self.button_save.clicked.connect(self.save_settings)

        self.load_settings()

        layout.addWidget(label_url)
        layout.addWidget(self.textbox)
        layout.addWidget(self.button_save)

        self.setLayout(layout)
        self.setStyleSheet(
                    "QWidget { background-color: #f0f0f0; }"
                    "QLabel { font-size: 16px; }"
                    "QLineEdit { font-size: 14px; }"
        )

    def load_settings(self):
        self.config.read(CONFIG_FILE)
        self.textbox.setText(self.config['DEFAULT']['homepage'])

    def save_settings(self):
        self.config['DEFAULT'] = {
            'homepage': self.textbox.text()
        }
        with open(CONFIG_FILE, 'w') as configfile:
            self.config.write(configfile)
