#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import os
import webbrowser

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMessageBox, QDialog, QFileDialog
from af.utils.FileUtils import FileUtils

from edat.controller.ProjectController import ProjectController
from edat.ui.EdatNewProjectDialog import EdatNewProjectDialog
from edat.ui.ImportDbWizard import IntroductionPage, SelectDbPage, SelectTablePage
import edat.utils.ui as utils_ui
from edat.ui.AttributeConfigurationView import AttributeConfigurationView
from edat.ui.InputDataView import InputDataView
from edat.ui.PrivacyConfigurationModelView import PrivacyModelConfigurationView
from af.exceptions import InfoException, ImportException
from edat.ui.EdatMenuBar import EdatMenuBar


class ProjectMainWindow(QtGui.QMainWindow):

    def __init__(self, main_ui_controller):
        super(ProjectMainWindow, self).__init__()

        self.main_ui_controller = main_ui_controller
        self.project_controller = self.main_ui_controller.get_project_controller()

        self.menu = EdatMenuBar(self)

        self.layout = QtGui.QHBoxLayout()
        self.ctr_frame = QtGui.QWidget(self)
        self.ctr_frame.setLayout(self.layout)
        self.setCentralWidget(self.ctr_frame)

        self.input_data_layout = QtGui.QVBoxLayout()
        self.layout.addLayout(self.input_data_layout, 1)
        self.configuration_layout = QtGui.QVBoxLayout()
        self.layout.addLayout(self.configuration_layout, 1)

        self.init_ui()
        self.update_view()

    def init_ui(self):
        self.setMenuBar(self.menu)
        self.showMaximized()
        self.setGeometry(300, 300, 350, 250)
        self.show()

    def new_project(self):
        new_project_dialog = EdatNewProjectDialog(self)
        new_project_dialog.exec_()

        if new_project_dialog.result() == QDialog.Accepted:
            self.project_controller = ProjectController()
            name, path = new_project_dialog.get_project_name()
            try:
                self.project_controller.create_project(name, path)
                self.update_view()
                self.main_ui_controller.update_edat_config(name, path)
            except InfoException, e:
                error_message = QMessageBox(self)
                error_message.setWindowTitle("Create Project Error")
                error_message.setText(e.message)
                error_message.exec_()

    def import_project(self):
        q_file_dialog = QFileDialog()
        filename = str(q_file_dialog.getOpenFileName(self, 'Import Project', os.getcwd()))
        if filename:
            self.project_controller = ProjectController()
            try:
                self.project_controller.load_project(FileUtils.get_file_name(filename), FileUtils.get_file_directory(filename))
                self.update_view()
                self.main_ui_controller.update_edat_config(self.project_controller.project.name, self.project_controller.project.path_location)
            except ImportException, e:
                error_message = QMessageBox(self)
                error_message.setWindowTitle("Import Project Error")
                error_message.setText(e.message)
                error_message.exec_()

    def show_import_db_wizard(self):
        wizard = QtGui.QWizard(self)
        wizard.setWindowTitle('Import DB Wizard')
        wizard.addPage(IntroductionPage(wizard))
        wizard.addPage(SelectDbPage(wizard))
        select_table_page = SelectTablePage(wizard)
        wizard.addPage(select_table_page)

        if wizard.exec_():
            db_path = str(select_table_page.selected_db)
            db_table_selected = str(select_table_page.selected_table.accessibleText())
            self.project_controller.add_config_data_to_project(db_path, select_table_page.controller.CONTROLLER_TYPE,
                                                               db_table_selected)
            self.update_view()

    def update_view(self):
        self.setWindowTitle(self.build_window_title())
        self.menu.update_menu()
        if self.is_project_open() and self.is_db_open():
            self.update_input_data_view()
            self.update_attribute_view()
            self.update_privacy_model_configuration_view()
            self.update_anonymize_view()

    def build_window_title(self):
        title = 'EDAT'
        if self.is_project_open():
            title += ' - ' + self.project_controller.project.name + ' - ' + self.project_controller.project.path_location
        return title

    def update_attribute_view(self):
        self.clean_attribute_view()
        attribute_configuration_view = AttributeConfigurationView(self.project_controller)
        self.configuration_layout.addWidget(attribute_configuration_view, )

    def update_anonymize_view(self):
        # TODO: connect button
        self.anonymize_button = QtGui.QPushButton("Anonymize")
        self.anonymize_button.setMaximumSize(200, 150)
        self.anonymize_button.setStyleSheet('font-size: 18pt; border-width: 2px;')
        self.configuration_layout.addWidget(self.anonymize_button, 1, Qt.AlignCenter)


    def clean_attribute_view(self):
        for i in reversed(range(self.configuration_layout.count())):
            self.configuration_layout.itemAt(i).widget().setParent(None)

    def update_input_data_view(self):
        self.clean_input_data_view()
        input_data_view = InputDataView(self.project_controller)
        self.input_data_layout.addWidget(input_data_view)

    def clean_input_data_view(self):
        for i in reversed(range(self.input_data_layout.count())):
            self.input_data_layout.itemAt(i).widget().setParent(None)

    def clean_project_view(self):
        self.clean_attribute_view()
        self.clean_input_data_view()

    def update_privacy_model_configuration_view(self):
        privacy_model_configuration_view = PrivacyModelConfigurationView()
        self.configuration_layout.addWidget(privacy_model_configuration_view, 3)

    def save_project(self, widget=False, name=None, location_path=None):
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
        if self.project_controller and self.project_controller.unsaved_changes:
            quit_msg = "All unsaved changes will be lost. Do you want to save them?"
            reply = QtGui.QMessageBox.question(self, 'Save last changes',
                                               quit_msg, QtGui.QMessageBox.Save, QtGui.QMessageBox.Cancel)
            if reply == QtGui.QMessageBox.Save:
                self.save_project()

        self.close()

    @staticmethod
    def user_manual():
        url = "https://github.com/s-rodriguez/edat"
        webbrowser.open(url, 2)

    def is_project_open(self):
        return self.project_controller is not None

    def is_db_open(self):
        return self.project_controller.project.data_config is not None

    def close_project(self):
        self.project_controller = None
        self.clean_project_view()
        self.update_view()
        self.main_ui_controller.update_edat_config()
