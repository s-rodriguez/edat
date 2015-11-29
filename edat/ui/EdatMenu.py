import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import os
from EdatMainWindow import MainWindow

class EdatMenu(QDialog):
    def __init__(self, parent=None):
        super(EdatMenu, self).__init__(parent)

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

        self.mainWindow = MainWindow()
        self.mainWindow.hide()

        self.show()

    def new_project(self):
        self.mainWindow.showMaximized()

    def import_project(self):
        filename = QFileDialog.getOpenFileName(self, 'Import Project', os.getenv('HOME'))
        f = open(filename, 'r')
        filedata = f.read()
        f.close()

    def user_manual(self):
        QMessageBox.information(self, 'User Manual', '''https://github.com/s-rodriguez/edat''',
                                QMessageBox.Ok)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = EdatMenu()
    form.exec_()


