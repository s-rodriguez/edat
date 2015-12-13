#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from edat.ui.ImportDbWizard import IntroductionPage, SelectDbPage, SelectTablePage


class EdatProjectMainWindow(QtGui.QMainWindow):

    def __init__(self, project_controller):
        super(EdatProjectMainWindow, self).__init__()

        self.project_controller = project_controller

        self.init_ui()

    def init_ui(self):
        self.showMaximized()

        text_edit = QtGui.QTextEdit()
        self.setCentralWidget(text_edit)

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')

        import_action = file_menu.addAction('Import DB')
        import_action.triggered.connect(self.import_db)

        exit_action = QtGui.QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle(self.project_controller.project.name + ' - ' + self.project_controller.project.path_location)

        self.show()

    def import_db(self):
        wizard = QtGui.QWizard(self)
        wizard.setWindowTitle('Import DB Wizard')
        wizard.addPage(IntroductionPage(wizard))
        wizard.addPage(SelectDbPage(wizard))
        wizard.addPage(SelectTablePage(wizard))
        wizard.exec_()
