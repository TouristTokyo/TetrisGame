from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5 import QtGui

size = (804, 612)


class SettingsWindowUI(QMainWindow):
    def __init__(self, window_parent):
        super(SettingsWindowUI, self).__init__()

        self.win_old = window_parent
        uic.loadUi('ui/settings.ui', self)
        self.setWindowTitle('Tetris[Settings]')
        self.setStyleSheet('.QWidget {background-image: url(images/menu_bg.jpg);}')
        self.setWindowIcon(QtGui.QIcon('images/icon_tetris.png'))
        self.setFixedSize(size[0], size[1])

        self.speed_rb = QButtonGroup()
        self.music_rb = QButtonGroup()

        self.radioButtonEasy = self.findChild(QRadioButton, "radioButtonEasy")
        self.radioButtonNormal = self.findChild(QRadioButton, "radioButtonNormal")
        self.radioButtonHard = self.findChild(QRadioButton, "radioButtonHard")

        self.speed_rb.addButton(self.radioButtonEasy)
        self.speed_rb.addButton(self.radioButtonNormal)
        self.speed_rb.addButton(self.radioButtonHard)

        self.music_rb.addButton(self.radioButtonOn)
        self.music_rb.addButton(self.radioButtonOff)

        self.radioButtonOn = self.findChild(QRadioButton, "radioButtonOn")
        self.radioButtonOff = self.findChild(QRadioButton, "radioButtonOff")

        self.pushButtonApply = self.findChild(QPushButton, "pushButtonApply")
        self.pushButtonApply.clicked.connect(self.on_click_apply)

    def on_click_apply(self):
        self.win_old.show()
        self.close()

    def config_default(self):
        self.radioButtonEasy.setChecked(True)
        self.radioButtonOn.setChecked(True)
    
    def is_level_easy(self):
        return self.radioButtonEasy.isChecked()

    def is_level_normal(self):
        return self.radioButtonNormal.isChecked()

    def is_level_hard(self):
        return self.radioButtonHard.isChecked()

    def is_music_play(self):
        return self.radioButtonOn.isChecked()
