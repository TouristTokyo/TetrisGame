from PyQt5.QtWidgets import QApplication
import sys
from menu_tetris import *


def main():
    app = QApplication(sys.argv)
    window = MainWindowUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
