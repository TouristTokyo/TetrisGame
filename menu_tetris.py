from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5 import QtGui
from game_tetris import *
from settings import SettingsWindowUI
from author_info import InformationWindowUI
from rules import RulesWindowUI

size = (804, 612)


class MainWindowUI(QMainWindow):

    def __init__(self):
        super(MainWindowUI, self).__init__()

        uic.loadUi('ui/menu_tetris.ui', self)
        self.setWindowTitle('Tetris[Menu]')
        self.setStyleSheet('.QWidget {background-image: url(images/menu_bg.jpg);}')
        self.setWindowIcon(QtGui.QIcon('images/icon_tetris.png'))
        self.setFixedSize(size[0], size[1])

        self.win_settings = SettingsWindowUI(self)
        self.win_info = InformationWindowUI(self)
        self.win_rules = RulesWindowUI(self)

        self.win_settings.config_default()

        self.pushButtonStart = self.findChild(QPushButton, "pushButtonStart")
        self.pushButtonStart.clicked.connect(self.on_click_start)

        self.pushButtonInfo = self.findChild(QPushButton, "pushButtonInfo")
        self.pushButtonInfo.clicked.connect(self.on_click_info)

        self.pushButtonSettings = self.findChild(QPushButton, "pushButtonSettings")
        self.pushButtonSettings.clicked.connect(self.on_click_settings)

        self.pushButtonRules = self.findChild(QPushButton, "pushButtonRules")
        self.pushButtonRules.clicked.connect(self.on_click_rules)

    def on_click_start(self):
        self.setVisible(False)
        speed = 0
        if self.win_settings.is_level_easy():
            speed = 60
        elif self.win_settings.is_level_normal():
            speed = 300
        elif self.win_settings.is_level_hard():
            speed = 600
        win_game = Game(speed, self.win_settings.is_music_play())
        win_game.start_game()
        self.setVisible(True)

    def on_click_info(self):
        self.win_info.show()
        self.close()

    def on_click_settings(self):
        self.win_settings.show()
        self.close()

    def on_click_rules(self):
        self.win_rules.show()
        self.close()
