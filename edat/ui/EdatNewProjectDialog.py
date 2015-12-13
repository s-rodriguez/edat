__author__ = 'gustavo'
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class EdatNewProjectDialog(QDialog):
    def __init__(self, parent=None):
        super(EdatNewProjectDialog, self).__init__(parent)

        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        # project name input text
        self.project_name_edit_text = QLineEdit(self)
        self.project_name_edit_text.setText("New Project")
        self.form_layout.addRow('Name:', self.project_name_edit_text)

        # project directory input text
        self.project_directory_edit_text = QLineEdit(self)
        self.project_directory_edit_text.setText(os.getcwd())
        self.project_directory_edit_text.setEnabled(False)
        self.form_layout.addRow('Directory:', self.project_directory_edit_text)

        self.layout.addLayout(self.form_layout)
        self.layout.addStretch(1)

        # directory explorer button
        self.import_button_box = QHBoxLayout()
        self.import_button_box.addStretch(1)
        self.import_button = QPushButton('...', self)
        self.connect(self.import_button, SIGNAL("clicked()"), self.show_directory)
        self.import_button_box.addWidget(self.import_button)
        self.layout.addLayout(self.import_button_box)

        # ok and cancel buttons
        self.action_button_box = QHBoxLayout()
        self.action_button_container = QDialogButtonBox(self)
        self.action_button_container.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)

        self.connect(self.action_button_container.button(QDialogButtonBox.Ok), SIGNAL("clicked()"), self.accept)
        self.connect(self.action_button_container.button(QDialogButtonBox.Cancel), SIGNAL("clicked()"), self.close)
        self.action_button_box.addWidget(self.action_button_container)
        self.layout.addLayout(self.action_button_box)

        self.setLayout(self.layout)

        self.setWindowTitle('New Project')
        # self.resize(300, 300)
        self.show()

    def show_directory(self):
        file_dialog = QFileDialog()
        filename = file_dialog.getExistingDirectory(self, 'Import Project', os.getenv('HOME'))
        self.project_directory_edit_text.setText(filename)

    def get_project_name(self):
        return str(self.project_name_edit_text.text()), str(self.project_directory_edit_text.text())

    def cancel_create_project(self):
        self.close()


