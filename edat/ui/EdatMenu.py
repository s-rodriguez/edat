from PyQt4.QtCore import *
from PyQt4.QtGui import *
import webbrowser
import os
from EdatNewProjectDialog import EdatNewProjectDialog

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
            self.new_project_dialog.get_project_name()

    def import_project(self):
        filename = QFileDialog.getOpenFileName(self, 'Import Project', os.getenv('HOME'))
        self.controller.show_main_window()

    def user_manual(self):
        url = "https://github.com/s-rodriguez/edat"
        webbrowser.open(url, 2)



