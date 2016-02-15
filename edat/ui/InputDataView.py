from PyQt4 import QtGui
from PyQt4.QtGui import QWidget
from edat.utils.FileUtils import FileUtils
from edat.ui.UIFactoryHelper import UIFactoryHelper


class InputDataViewWidget(QtGui.QWidget):

    def __init__(self, project_data_controller):
        super(QWidget, self).__init__()
        layout = QtGui.QVBoxLayout()
        table_name_label = QtGui.QLabel()
        table_name_label.setText(
            "Table: " + project_data_controller.project.data_config.table + " (Database: " +
            FileUtils.get_file_name(project_data_controller.project.data_config.location) + " )")
        layout.addWidget(table_name_label)
        ui_factory = UIFactoryHelper.get_factory(project_data_controller.project.data_config.type)
        layout.addWidget(ui_factory.create_table_view(project_data_controller))
        self.setLayout(layout)
