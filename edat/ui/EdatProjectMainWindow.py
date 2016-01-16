#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from edat.ui.EdatNewProjectDialog import EdatNewProjectDialog
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
        import_action.setShortcut('Ctrl+I')
        import_action.triggered.connect(self.import_db)

        save_project_action = file_menu.addAction('Save')
        save_project_action.setShortcut('Ctrl+S')
        save_project_action.setStatusTip('Save Project')
        save_project_action.triggered.connect(self.save_project)

        save_project_action = file_menu.addAction('Save As')
        save_project_action.setShortcut('Ctrl+Shift+S')
        save_project_action.setStatusTip('Save Project As')
        save_project_action.triggered.connect(self.save_project_as)

        exit_action = QtGui.QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close_application)
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

        db_type = 'sqlite' if wizard.field("SQLiteButton").toPyObject() else 'csv'
        db_project_directory = str(wizard.field("ProjectDirectory").toPyObject())
        db_table_selected = 'Cars' #TODO
        self.project_controller.add_config_data_to_project(db_project_directory, db_type, db_table_selected)

    def save_project(self, parent=None, name=None, location_path=None):
        self.project_controller.save_project(name, location_path)

    def save_project_as(self):
        new_project_dialog = EdatNewProjectDialog(self)
        new_project_dialog.exec_()

        if new_project_dialog.result() == QtGui.QDialog.Accepted:
            name, path = new_project_dialog.get_project_name()
            try:
                return self.save_project(name, path)
            except Exception as info_exception:
                error_message = QtGui.QMessageBox(self)
                error_message.setWindowTitle("Save Project As Error")
                error_message.setText(info_exception.message)
                error_message.exec_()

    def close_application(self):
        if self.project_controller.unsaved_changes:
            quit_msg = "All unsaved changes will be lost. Do you want to save them?"
            reply = QtGui.QMessageBox.question(self, 'Save last changes',
                                               quit_msg, QtGui.QMessageBox.Save, QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Save:
                self.save_project()

        self.close()
