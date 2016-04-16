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
        self.data_config = self.project_controller.project.data_config

        data_factory = DataFactory()
        af_manager = AfManager()

        self.db_controller = data_factory.create_controller(self.data_config.location,
                                                            self.data_config.type)

        main_layout = QtGui.QVBoxLayout()

        main_layout.addWidget(TextUtils.get_header_styled_text("Attributes Configuration"))

        attr_layout = QtGui.QFormLayout()

        attr_layout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        attr_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        attr_layout.setFormAlignment(Qt.AlignCenter)
        attr_layout.setLabelAlignment(Qt.AlignLeft)
        attr_layout.setVerticalSpacing(20)

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

        self.suppression_panel = SuppressionPanel(self.project_controller, self)
        self.generalization_panel = GeneralizationPanel(self.project_controller, self)

        attr_layout.addRow(self.suppression_panel, self.generalization_panel)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)

        self.attributes_combo.setCurrentIndex(0)
        self.refresh_attribute(self.attributes_combo.currentText())

        main_layout.addLayout(attr_layout)
        self.setLayout(main_layout)

    def load_attributes(self):
        if len(self.data_config.attributes_list) == 0:
            attributes = self.db_controller.table_columns_info(self.project_controller.project.data_config.table)
            for att_name in attributes:
                self.data_config.attributes_list.append(Attribute(name=att_name))
        else:
            attributes = [att.name for att in self.data_config.attributes_list]

        self.attributes_combo.addItems(attributes)
        self.attributes_combo.currentIndexChanged['QString'].connect(self.refresh_attribute)

    def refresh_attribute(self, attribute_name):
        selected_attribute = str(self.attributes_combo.currentText())

        for att in self.data_config.attributes_list:
            if att.name == selected_attribute:
                combos = (self.type_combo, self.category_combo, self.weight_spin_box)
                self.block_objects_signals(combos, True)

                self.type_combo.setCurrentIndex(self.type_combo.findText(att.basic_type))
                self.category_combo.setCurrentIndex(self.category_combo.findText(att.privacy_type))
                self.weight_spin_box.setValue(att.weight)

                self.block_objects_signals(combos, False)

                break

    def save_attribute_info(self, text):
        selected_attribute = str(self.attributes_combo.currentText())
        basic_type = str(self.type_combo.currentText())
        privacy_category = str(self.category_combo.currentText())
        weight = self.weight_spin_box.value()

        for att in self.data_config.attributes_list:
            if att.name == selected_attribute:
                att.basic_type = basic_type
                att.privacy_type = privacy_category
                att.weight = weight
                self.enable_anonymization_panels(att)
                break


    @staticmethod
    def block_objects_signals(objects_list, block=True):
        for ob in objects_list:
            ob.blockSignals(block)

    def get_current_attribute(self):
        selected_attribute = str(self.attributes_combo.currentText())
        for att in self.data_config.attributes_list:
            if att.name == selected_attribute:
                return att

    def enable_anonymization_panels(self, att):
        enabled = att.is_qi_attribute()
        self.suppression_panel.setEnabled(enabled)
        self.generalization_panel.setEnabled(enabled)

