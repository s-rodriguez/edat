from PyQt4 import QtGui

from PyQt4.QtCore import Qt

from PyQt4.QtGui import QWidget, QFormLayout

from af.controller.data.DataFactory import DataFactory
from edat.ui.AnonymizationPanel import SuppressionPanel, GeneralizationPanel


class AttributeConfigurationView(QtGui.QWidget):

    def __init__(self, project_controller):
        super(QWidget, self).__init__()
        data_factory = DataFactory()
        controller = data_factory.create_controller(project_controller.project.data_config.location, project_controller.project.data_config.type)

        attr_layout = QtGui.QFormLayout()

        attr_layout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        attr_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        attr_layout.setFormAlignment(Qt.AlignHCenter | Qt.AlignTop)
        attr_layout.setLabelAlignment(Qt.AlignRight)

        self.attributes_combo = QtGui.QComboBox()

        self.attributes_combo.addItems(controller.table_columns_info(project_controller.project.data_config.table))
        attr_layout.addRow("Attribute: ", self.attributes_combo)

        # TODO: fill combos
        attr_layout.addRow("Category: ", QtGui.QComboBox())
        attr_layout.addRow("Type: ", QtGui.QComboBox())
        attr_layout.addRow("Weight", QtGui.QComboBox())

        self.suppression_panel = SuppressionPanel()
        self.generalization_panel = GeneralizationPanel()

        attr_layout.addRow(self.suppression_panel, self.generalization_panel)
        self.setLayout(attr_layout)
