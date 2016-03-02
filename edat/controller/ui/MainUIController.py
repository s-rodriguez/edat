from PyQt4.QtGui import QMessageBox
from edat.controller.ProjectController import ProjectController
from edat.ui.ProjectMainWindow import ProjectMainWindow
from edat.model.EdatConfig import EdatConfig
from af.exceptions import ImportException


class MainUiController:
    def __init__(self):
        self.edat_config = EdatConfig()
        self.edat_project_main_window = ProjectMainWindow(self)
        self.edat_project_main_window.show()

    def get_project_controller(self):
        self.edat_config.load()
        project_controller = None
        if self.edat_config.exists_config_file():
            project_controller = ProjectController()
            try:
                project_controller.load_project(self.edat_config.project, self.edat_config.location)
            except ImportException, e:
                error_message = QMessageBox()
                error_message.setWindowTitle("Import Project Error")
                error_message.setText(e.message)
                error_message.exec_()
            finally:
                project_controller = None

        return project_controller

    def update_edat_config(self, project=None, location=None):
        self.edat_config.save(project, location)
