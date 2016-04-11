from PyQt4 import QtGui

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFormLayout, QFrame

from af.controller.data.DataFactory import DataFactory
from edat.ui.AnonymizationPanel import SuppressionPanel, GeneralizationPanel
from edat.utils.ui.TextUtils import TextUtils
from af.model.algorithms.AfManager import AfManager
from af.model.Attribute import Attribute

class AttributeConfigurationView(QtGui.QFrame):

    def __init__(self, project_controller):
        super(QFrame, self).__init__()
        self.project_controller = project_controller
        self.attributes = []

        data_factory = DataFactory()
        af_manager = AfManager()

        self.db_controller = data_factory.create_controller(self.project_controller.project.data_config.location,
                                                            self.project_controller.project.data_config.type)

        main_layout = QtGui.QVBoxLayout()

        main_layout.addWidget(TextUtils.get_header_styled_text("Attributes Configuration"))

        attr_layout = QtGui.QFormLayout()

        attr_layout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        attr_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        attr_layout.setFormAlignment(Qt.AlignCenter)
        attr_layout.setLabelAlignment(Qt.AlignLeft)

        self.attributes_combo = QtGui.QComboBox()
        self.load_attributes()
        attr_layout.addRow("Attribute: ", self.attributes_combo)

        self.category_combo = QtGui.QComboBox()
        self.category_combo.addItems(list(af_manager.privacy_types))
        attr_layout.addRow("Category: ", self.category_combo)
        self.category_combo.currentIndexChanged['QString'].connect(self.save_attribute_info)

        self.type_combo = QtGui.QComboBox()
        self.type_combo.addItems(list(af_manager.data_types))
        attr_layout.addRow("Type: ", self.type_combo)
        self.type_combo.currentIndexChanged['QString'].connect(self.save_attribute_info)

        self.weight_spin_box = QtGui.QSpinBox()
        self.weight_spin_box.setMaximum(10)
        self.weight_spin_box.setMinimum(0)
        self.weight_spin_box.setSingleStep(1)
        self.weight_spin_box.setValue(5)
        attr_layout.addRow("Weight", self.weight_spin_box)
        self.weight_spin_box.valueChanged.connect(self.save_attribute_info)

        self.suppression_panel = SuppressionPanel()
        self.generalization_panel = GeneralizationPanel()

        attr_layout.addRow(self.suppression_panel, self.generalization_panel)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)

        main_layout.addLayout(attr_layout)
        self.setLayout(main_layout)

    def load_attributes(self):
        attributes = self.db_controller.table_columns_info(self.project_controller.project.data_config.table)
        self.attributes_combo.addItems(attributes)
        self.attributes_combo.currentIndexChanged['QString'].connect(self.refresh_attribute)
        for att_name in attributes:
            self.attributes.append(Attribute(name=att_name))

    def refresh_attribute(self, attribute_name):
        selected_attribute = str(self.attributes_combo.currentText())

        for att in self.attributes:
            if att.name == selected_attribute:
                for combo in (self.type_combo, self.category_combo, self.weight_spin_box):
                    combo.blockSignals(True)

                self.type_combo.setCurrentIndex(self.type_combo.findText(att.basic_type))
                self.category_combo.setCurrentIndex(self.category_combo.findText(att.privacy_type))
                self.weight_spin_box.setValue(att.weight)

                for combo in (self.type_combo, self.category_combo, self.weight_spin_box):
                    combo.blockSignals(False)
                break

    def save_attribute_info(self, text):
        selected_attribute = str(self.attributes_combo.currentText())
        basic_type = str(self.type_combo.currentText())
        privacy_category = str(self.category_combo.currentText())
        weight = self.weight_spin_box.value()

        for att in self.attributes:
            if att.name == selected_attribute:
                att.basic_type = basic_type
                att.privacy_type = privacy_category
                att.weight = weight
                break
