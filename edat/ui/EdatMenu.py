import webbrowser
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from edat.ui.EdatNewProjectDialog import EdatNewProjectDialog
from edat.controller.ProjectController import ProjectController
from edat.utils.FileUtils import FileUtils


class EdatMenu(QDialog):
    def __init__(self, controller, parent=None):
        super(EdatMenu, self).__init__(parent)

        self.controller = controller
        self.new_project_dialog = None

        self.init_ui()

    def init_ui(self):
        self.setFixedSize(260, 160)

        # main actions
        layout = QVBoxLayout()
        for text, slot in (("New Project", self.new_project),
                           ("Import Project", self.import_project),
                           ("User Manual", self.user_manual)):
            button = QPushButton(text)
            layout.addWidget(button)
            self.connect(button, SIGNAL("clicked()"), slot)
        self.setLayout(layout)

        self.setWindowTitle('EDAT')
        self.show()

    def new_project(self):
        self.new_project_dialog = EdatNewProjectDialog(self)
        self.new_project_dialog.exec_()

        if self.new_project_dialog.result() == QDialog.Accepted:
            project_controller = ProjectController()
            name, path = self.new_project_dialog.get_project_name()
            project_controller.create_project(name, path)
            self.controller.show_project_main_window(project_controller)

    def import_project(self):
        q_file_dialog = QFileDialog()
        filename = str(q_file_dialog.getOpenFileName(self, 'Import Project', os.getcwd()))
        if filename:
            project_controller = ProjectController()
            project_controller.load_project(FileUtils.get_file_name(filename), FileUtils.get_file_directory(filename))
            self.controller.show_project_main_window(project_controller)

    @staticmethod
    def user_manual():
        url = "https://github.com/s-rodriguez/edat"
        webbrowser.open(url, 2)



