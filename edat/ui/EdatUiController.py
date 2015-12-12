import sys

from PyQt4.QtGui import *

from EdatMainWindow import MainWindow
from EdatMenu import EdatMenu


class EdatUiController:
    def __init__(self):
        self.edat_menu = EdatMenu(self)
        self.edat_main_window = None

    def show_main_window(self):
        self.edat_menu.close()
        self.edat_main_window = MainWindow()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = EdatUiController()
    sys.exit(app.exec_())

