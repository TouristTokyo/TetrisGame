from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import uic
from PyQt5 import QtGui

size = (804, 612)


class RulesWindowUI(QMainWindow):
    def __init__(self, window_parent):
        super(RulesWindowUI, self).__init__()

        self.win_old = window_parent
        uic.loadUi('ui/rules.ui', self)
        self.setWindowTitle('Tetris[Rules]')
        self.setStyleSheet('.QWidget {background-image: url(images/menu_bg.jpg);}')
        self.setWindowIcon(QtGui.QIcon('images/icon_tetris.png'))
        self.setFixedSize(size[0], size[1])

        self.pushButtonBack = self.findChild(QPushButton, "pushButtonBack")
        self.pushButtonBack.clicked.connect(self.on_click_back)

    def on_click_back(self):
        self.win_old.show()
        self.close()
