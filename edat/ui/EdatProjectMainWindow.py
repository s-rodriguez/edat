#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui

from edat.ui.EdatNewProjectDialog import EdatNewProjectDialog
from edat.ui.ImportDbWizard import IntroductionPage, SelectDbPage, SelectTablePage
import edat.utils.ui as utils_ui


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

        save_project_action = file_menu.addAction('Export Configuration')
        save_project_action.setShortcut('Ctrl+E')
        save_project_action.setStatusTip('Export Configuration')
        save_project_action.triggered.connect(self.export_configuration)

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
        select_table_page = SelectTablePage(wizard)
        wizard.addPage(select_table_page)
        wizard.exec_()

        db_type = 'sqlite' if wizard.field("SQLiteButton").toPyObject() else 'csv'
        db_project_directory = str(select_table_page.selected_db)
        db_table_selected = str(select_table_page.selected_table.accessibleText())
        self.project_controller.add_config_data_to_project(db_project_directory, db_type, db_table_selected)

    def save_project(self, parent=None, name=None, location_path=None):
        self.project_controller.save_project(name, location_path)

    def save_project_as(self):
        new_project_dialog = EdatNewProjectDialog(self)
        new_project_dialog.exec_()

        if new_project_dialog.result() == QtGui.QDialog.Accepted:
            name, path = new_project_dialog.get_project_name()
            try:
                return self.save_project(name=name, location_path=path)
            except Exception as info_exception:
                utils_ui.showMessageAlertBox(parent=self, title="Save Project As Error", message=info_exception.message)

    def export_configuration(self):
        new_config_dialog = EdatNewProjectDialog(self)
        new_config_dialog.exec_()

        if new_config_dialog.result() == QtGui.QDialog.Accepted:
            name, path = new_config_dialog.get_project_name()
            try:
                return self.project_controller.export_configuration(name=name, location_path=path)
            except Exception as info_exception:
                utils_ui.showMessageAlertBox(parent=self, title="Could not export configuration", message=info_exception.message)

    def close_application(self):
        if self.project_controller.unsaved_changes:
            quit_msg = "All unsaved changes will be lost. Do you want to save them?"
            reply = QtGui.QMessageBox.question(self, 'Save last changes',
                                               quit_msg, QtGui.QMessageBox.Save, QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Save:
                self.save_project()

        self.close()
