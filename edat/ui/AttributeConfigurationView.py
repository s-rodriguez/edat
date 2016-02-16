from PyQt4 import QtGui

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFormLayout, QFrame

from af.controller.data.DataFactory import DataFactory
from edat.ui.AnonymizationPanel import SuppressionPanel, GeneralizationPanel
from edat.utils.ui.TextUtils import TextUtils

class AttributeConfigurationView(QtGui.QFrame):

    def __init__(self, project_controller):
        super(QFrame, self).__init__()
        data_factory = DataFactory()
        controller = data_factory.create_controller(project_controller.project.data_config.location, project_controller.project.data_config.type)

        main_layout = QtGui.QVBoxLayout()

        main_layout.addWidget(TextUtils.get_header_styled_text("Attributes Configuration"))

        attr_layout = QtGui.QFormLayout()

        attr_layout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        attr_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        attr_layout.setFormAlignment(Qt.AlignCenter)
        attr_layout.setLabelAlignment(Qt.AlignLeft)

        self.attributes_combo = QtGui.QComboBox()

        self.attributes_combo.addItems(controller.table_columns_info(project_controller.project.data_config.table))
        attr_layout.addRow("Attribute: ", self.attributes_combo)

        # TODO: fill combo
        self.category_combo = QtGui.QComboBox()
        attr_layout.addRow("Category: ", self.category_combo)

        # TODO: fill combo
        self.type_combo = QtGui.QComboBox()
        attr_layout.addRow("Type: ", self.type_combo)

        # TODO: fill combo
        self.weight_combo = QtGui.QComboBox()
        attr_layout.addRow("Weight", self.weight_combo)

        self.suppression_panel = SuppressionPanel()
        self.generalization_panel = GeneralizationPanel()

        attr_layout.addRow(self.suppression_panel, self.generalization_panel)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)

        main_layout.addLayout(attr_layout)
        self.setLayout(main_layout)
