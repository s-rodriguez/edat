import sys

from edat.ui.EdatProjectMainWindow import EdatProjectMainWindow
from edat.ui.EdatMenu import EdatMenu


class MainUiController:
    def __init__(self):
        self.edat_menu = EdatMenu(self)
        self.edat_project_main_window = None

    def show_project_main_window(self, project_controller):
        self.edat_menu.close()
        self.edat_project_main_window = EdatProjectMainWindow(project_controller)
