import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import webbrowser
import os
from EdatOpenProjectDialog import EdatOpenProjectDialog

class EdatMenu(QDialog):
    def __init__(self, controller, parent=None):
        super(EdatMenu, self).__init__(parent)

        self.controller = controller
        self.new_project_dialog = None

        self.init_ui()

    def init_ui(self):
        self.resize(260, 160)
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
        self.new_project_dialog = EdatOpenProjectDialog(self)
        self.new_project_dialog.show()
        # self.controller.show_main_window()

    def import_project(self):
        filename = QFileDialog.getOpenFileName(self, 'Import Project', os.getenv('HOME'))

    def user_manual(self):
        url = "https://github.com/s-rodriguez/edat"
        webbrowser.open(url, 2)



