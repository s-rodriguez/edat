__author__ = 'gustavo'
import os
from PyQt4.QtGui import *
from PyQt4.QtCore import *

class EdatOpenProjectDialog(QDialog):
    def __init__(self,parent=None):
        super(EdatOpenProjectDialog, self).__init__(parent)

        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        self.project_name = QLineEdit(self)
        self.form_layout.addRow('Name:', self.project_name)

        self.project_directory = QLineEdit(self)
        self.form_layout.addRow('Directory:', self.project_directory)

        self.layout.addLayout(self.form_layout)
        self.layout.addStretch(1)

        self.import_button_box = QHBoxLayout()
        self.import_button_box.addStretch(1)
        self.import_button = QPushButton('...', self)
        self.connect(self.import_button, SIGNAL("clicked()"), self.show_directory)
        self.import_button_box.addWidget(self.import_button)
        self.layout.addLayout(self.import_button_box)

        self.action_button_box = QHBoxLayout()
        self.action_button_container = QDialogButtonBox(self)
        self.action_button_container.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.action_button_box.addWidget(self.action_button_container)
        self.layout.addLayout(self.action_button_box)

        self.setLayout(self.layout)

        self.setWindowTitle('New Project')
        # self.resize(300, 300)
        self.show()

    def show_directory(self):
        filename = QFileDialog.getOpenFileName(self, 'Import Project', os.getenv('HOME'))
        self.project_directory.setText(filename)


