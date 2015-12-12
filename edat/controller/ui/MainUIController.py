import sys

from edat.ui.EdatMainWindow import MainWindow
from edat.ui.EdatMenu import EdatMenu


class MainUiController:
    def __init__(self):
        self.edat_menu = EdatMenu(self)
        self.edat_main_window = None

    def show_main_window(self):
        self.edat_menu.close()
        self.edat_main_window = MainWindow()