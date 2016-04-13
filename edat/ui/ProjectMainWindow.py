#!/usr/bin/python
# -*- coding: utf-8 -*-


import os
import webbrowser

from PyQt4.QtWebKit import QWebView
from PyQt4.QtCore import Qt
from PyQt4.QtGui import (
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QWizard,
)

from af.exceptions import InfoException, ImportException
from af.utils.FileUtils import FileUtils

from edat.controller.ProjectController import ProjectController
from edat.ui.AttributeConfigurationView import AttributeConfigurationView
from edat.ui.EdatMenuBar import EdatMenuBar
from edat.ui.EdatNewProjectDialog import EdatNewProjectDialog
from edat.ui.ImportDbWizard import IntroductionPage, SelectDbPage, SelectTablePage
from edat.ui.InputDataView import InputDataView
from edat.ui.PrivacyConfigurationModelView import PrivacyModelConfigurationView
import edat.utils.ui as utils_ui


from edat.utils import strings


class ProjectMainWindow(QMainWindow):

    def __init__(self, main_ui_controller):
        super(ProjectMainWindow, self).__init__()

        self.main_ui_controller = main_ui_controller
        self.project_controller = self.main_ui_controller.get_project_controller()

        self.menu = EdatMenuBar(self)

        self.tab_widget = QTabWidget()

        self.create_input_and_configuration_tab()
        self.create_output_and_metrics_tab()

        self.mainLayout = QVBoxLayout()
        self.mainLayout.addWidget(self.tab_widget)

        self.ctr_frame = QWidget(self)
        self.ctr_frame.setLayout(self.mainLayout)
        self.setCentralWidget(self.ctr_frame)

        self.init_ui()
        self.update_view()

    def create_input_and_configuration_tab(self):
        self.input_and_configuration_tab = QWidget()
        layout = QHBoxLayout(self.input_and_configuration_tab)

        self.input_data_layout = QVBoxLayout()
        layout.addLayout(self.input_data_layout, 1)
        self.configuration_layout = QVBoxLayout()
        layout.addLayout(self.configuration_layout, 1)

        self.tab_widget.addTab(self.input_and_configuration_tab, strings.CONFIGURATION_TAB)

    def create_output_and_metrics_tab(self):
        self.output_and_metrics_tab = QWidget()
        layout = QHBoxLayout(self.output_and_metrics_tab)

        self.output_data_layout = QVBoxLayout()
        layout.addLayout(self.output_data_layout, 1)
        self.metrics_layout = QVBoxLayout()
        layout.addLayout(self.metrics_layout, 1)

        self.tab_widget.addTab(self.output_and_metrics_tab, strings.METRICS_TAB)

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
                error_message.setWindowTitle(strings.CREATE_PROJECT_ERROR)
                error_message.setText(e.message)
                error_message.exec_()

    def import_project(self):
        q_file_dialog = QFileDialog()
        filename = str(q_file_dialog.getOpenFileName(self, strings.IMPORT_PROJECT, os.getcwd()))
        if filename:
            self.project_controller = ProjectController()
            try:
                self.project_controller.load_project(FileUtils.get_file_name(filename), FileUtils.get_file_directory(filename))
                self.update_view()
                self.main_ui_controller.update_edat_config(self.project_controller.project.name, self.project_controller.project.path_location)
            except ImportException, e:
                error_message = QMessageBox(self)
                error_message.setWindowTitle(strings.IMPORT_PROJECT_ERROR)
                error_message.setText(e.message)
                error_message.exec_()

    def show_import_db_wizard(self):
        wizard = QWizard(self)
        wizard.setWindowTitle(strings.IMPORT_DB_WIZARD)
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
            self.update_input_and_configuration_tab()
            if self.anonymized_db_exists():
                self.update_output_and_metrics_tab()

    def build_window_title(self):
        title = strings.WINDOW_TITLE
        if self.is_project_open():
            title += ' - ' + self.project_controller.project.name + ' - ' + self.project_controller.project.path_location
        return title

    def update_input_and_configuration_tab(self):
        self.update_input_data_view()
        self.update_attribute_view()
        self.update_privacy_model_configuration_view()
        self.update_anonymize_view()

    def update_output_and_metrics_tab(self):
        self.update_output_data_view()
        self.update_report_metrics_view()

    def update_input_data_view(self):
        self.clean_layout(self.input_data_layout)
        input_data_view = InputDataView(self.project_controller)
        self.input_data_layout.addWidget(input_data_view)

    def update_attribute_view(self):
        self.clean_layout(self.configuration_layout)
        attribute_configuration_view = AttributeConfigurationView(self.project_controller)
        self.configuration_layout.addWidget(attribute_configuration_view, )

    def update_privacy_model_configuration_view(self):
        privacy_model_configuration_view = PrivacyModelConfigurationView()
        self.configuration_layout.addWidget(privacy_model_configuration_view, 3)

    def update_anonymize_view(self):
        # TODO: connect button
        self.anonymize_button = QPushButton(strings.ANONYMIZE)
        self.anonymize_button.setMaximumSize(200, 150)
        self.anonymize_button.setStyleSheet('font-size: 18pt; border-width: 2px;')
        self.configuration_layout.addWidget(self.anonymize_button, 1, Qt.AlignCenter)

    def update_output_data_view(self):
        pass

    def update_report_metrics_view(self):
        self.clean_layout(self.metrics_layout)
        # TODO: look for the report
        # or data config should save the location, or it should be created again
        with open('/home/ubuntu/af/reports/my_report.html') as f:
            report_html = f.read()
            web_view = QWebView()
            web_view.setHtml(report_html)
            self.metrics_layout.addWidget(web_view)

    def clean_layout(self, layout):
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def clean_project_view(self):
        layouts = (
            self.input_data_layout,
            self.configuration_layout,
            self.metrics_layout
        )
        for l in layouts:
            self.clean_layout(l)

    def save_project(self, widget=False, name=None, location_path=None):
        self.project_controller.save_project(name, location_path)

    def save_project_as(self):
        new_project_dialog = EdatNewProjectDialog(self)
        new_project_dialog.exec_()

        if new_project_dialog.result() == QDialog.Accepted:
            name, path = new_project_dialog.get_project_name()
            try:
                return self.save_project(name=name, location_path=path)
            except Exception as info_exception:
                utils_ui.showMessageAlertBox(parent=self, title=strings.SAVE_PROJECT_AS_ERROR, message=info_exception.message)

    def export_configuration(self):
        new_config_dialog = EdatNewProjectDialog(self)
        new_config_dialog.exec_()

        if new_config_dialog.result() == QDialog.Accepted:
            name, path = new_config_dialog.get_project_name()
            try:
                return self.project_controller.export_configuration(name=name, location_path=path)
            except Exception as info_exception:
                utils_ui.showMessageAlertBox(parent=self, title=strings.EXPORT_CONFIG_ERROR, message=info_exception.message)

    def close_application(self):
        if self.project_controller and self.project_controller.unsaved_changes:
            quit_msg = "All unsaved changes will be lost. Do you want to save them?"
            reply = QMessageBox.question(self, strings.SAVE_CHANGES,
                                               quit_msg, QMessageBox.Save, QMessageBox.Cancel)
            if reply == QMessageBox.Save:
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

    def anonymized_db_exists(self):
        data_config = self.project_controller.project.data_config
        return data_config.anonymized_db_location is not None

    def close_project(self):
        self.project_controller = None
        self.clean_project_view()
        self.update_view()
        self.main_ui_controller.update_edat_config()
