from PyQt4 import QtGui

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFormLayout, QFrame

from af.controller.data.DataFactory import DataFactory
from edat.ui.AnonymizationPanel import AnonymizationPanel
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

        grid_frame = QtGui.QFrame()
        grid_layout = QtGui.QGridLayout()
        grid_layout.setSpacing(20)
        row = 0


        self.attributes_combo = QtGui.QComboBox()
        self.load_attributes()
        grid_layout.addWidget(TextUtils.get_caption_styled_text('Attribute'), row, 0)
        grid_layout.addWidget(self.attributes_combo, row, 1)

        self.category_combo = QtGui.QComboBox()
        self.category_combo.addItems(list(af_manager.privacy_types))
        self.category_combo.currentIndexChanged['QString'].connect(self.save_attribute_info)
        grid_layout.addWidget(TextUtils.get_caption_styled_text('Category'), row, 2)
        grid_layout.addWidget(self.category_combo, row, 3)

        row += 1

        self.type_combo = QtGui.QComboBox()
        self.type_combo.addItems(list(af_manager.data_types))
        self.type_combo.currentIndexChanged['QString'].connect(self.save_attribute_info)
        grid_layout.addWidget(TextUtils.get_caption_styled_text('Type'), row, 0)
        grid_layout.addWidget(self.type_combo, row, 1)


        self.weight_spin_box = QtGui.QSpinBox()
        self.weight_spin_box.setMaximum(10)
        self.weight_spin_box.setMinimum(0)
        self.weight_spin_box.setSingleStep(1)
        self.weight_spin_box.setValue(5)
        self.weight_spin_box.valueChanged.connect(self.save_attribute_info)
        grid_layout.addWidget(TextUtils.get_caption_styled_text('Weight'), row, 2)
        grid_layout.addWidget(self.weight_spin_box, row, 3)
        row += 1

        grid_frame.setLayout(grid_layout)
        main_layout.addWidget(grid_frame)

        self.anonymization_panel = AnonymizationPanel(self.project_controller, self)
        main_layout.addWidget(self.anonymization_panel)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)

        self.attributes_combo.setCurrentIndex(0)
        self.refresh_attribute(self.attributes_combo.currentText())

        main_layout.addLayout(attr_layout)
        self.setLayout(main_layout)

    @staticmethod
    def create_horizontal_frame(text, widget):
        frame = QtGui.QFrame()
        layout = QtGui.QHBoxLayout()
        layout.addStretch(1)
        layout.addWidget(TextUtils.get_caption_styled_text(text), 0, Qt.AlignVCenter)
        layout.addWidget(widget, 0, Qt.AlignVCenter)
        layout.addStretch(1)
        frame.setLayout(layout)
        return frame

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

                self.enable_anonymization_panels(att)
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
        self.anonymization_panel.setEnabled(enabled)
