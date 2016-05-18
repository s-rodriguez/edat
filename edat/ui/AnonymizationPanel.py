from PyQt4 import QtGui

from PyQt4.QtCore import (
    Qt,
)
from PyQt4.QtGui import (
    QMessageBox,
    QSlider,
)

from af.controller.hierarchies.BaseHierarchyController import BaseHierarchyController
from af.model.AfManager import AfManager
from af.utils import (
    HIERARCHY_TYPE_SUPPRESSION,
    HIERARCHY_TYPE_GENERALIZATION,
)

from edat.ui.HierarchyDisplayView import HierarchyDisplayView
from edat.ui.HierarchyView import HierarchyView
from edat.ui.LoadAttributeValuesThread import LoadAttributeValuesThread
from edat.utils.ui.TextUtils import TextUtils
import edat.utils.ui as utils_ui
from edat.utils import strings


NO_SELECTED_SLIDER_VALUE = 1

SUPPRESSION_SLIDER_VALUE = 0

GENERALIZATION_SLIDER_VALUE = 2


class AnonymizationPanel(QtGui.QFrame):

    def __init__(self, project_controller, attribute_view, parent=None):
        super(QtGui.QFrame, self).__init__(parent)
        self.af_manager = AfManager()

        self.attribute_view = attribute_view
        self.project_controller = project_controller

        self.vertical_layout = QtGui.QVBoxLayout()

        self.add_transformation_frame()
        self.add_generalization_related_objects()
        self.add_suppression_related_objects()

        self.update_view()
        self.setLayout(self.vertical_layout)

    def add_transformation_frame(self):
        self.transformation_frame = QtGui.QFrame()
        horizontal_layout = QtGui.QHBoxLayout()

        self.supression_label = TextUtils.get_caption_styled_text('Suppression')
        self.generalization_label = TextUtils.get_caption_styled_text('Generalization')

        self.privacy_slider = QSlider(Qt.Horizontal)
        self.privacy_slider.setMinimum(0)
        self.privacy_slider.setMaximum(2)
        self.privacy_slider.setTickInterval(QSlider.TicksBothSides)
        self.privacy_slider.setValue(NO_SELECTED_SLIDER_VALUE)
        self.privacy_slider.valueChanged.connect(self.slider_value_changed)

        horizontal_layout.addStretch(1)
        horizontal_layout.addWidget(self.supression_label)
        horizontal_layout.addWidget(self.privacy_slider)
        horizontal_layout.addWidget(self.generalization_label)
        horizontal_layout.addStretch(1)

        self.transformation_frame.setLayout(horizontal_layout)
        self.vertical_layout.addWidget(self.transformation_frame, 0, Qt.AlignVCenter)

    def add_generalization_related_objects(self):
        self.generalization_frame = QtGui.QFrame()
        horizontal_layout = QtGui.QHBoxLayout()
        horizontal_layout.addStretch(1)

        self.hierarchy_button = QtGui.QPushButton("Create Hierarchy")
        self.hierarchy_button.clicked.connect(self.create_generalization_hierarchy)
        horizontal_layout.addWidget(self.hierarchy_button)

        self.status_button_generalization = QtGui.QPushButton("Hierarchy Status")
        self.status_button_generalization.setFlat(True)
        self.status_button_generalization.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.status_button_generalization.setStyleSheet('QPushButton {color: blue; text-decoration: underline;}')
        self.status_button_generalization.clicked.connect(self.display_hierarchy)
        horizontal_layout.addWidget(self.status_button_generalization)
        horizontal_layout.addStretch(1)

        self.generalization_frame.setLayout(horizontal_layout)
        self.generalization_frame.hide()
        self.vertical_layout.addWidget(self.generalization_frame)

    def add_suppression_related_objects(self):
        self.suppression_frame = QtGui.QFrame()
        v_layout = QtGui.QVBoxLayout(self.suppression_frame)

        frame_1 = QtGui.QFrame()
        horizontal_layout_1 = QtGui.QHBoxLayout(frame_1)
        horizontal_layout_1.addStretch(1)

        self.supression_type_label = TextUtils.get_caption_styled_text('Suppression Type')
        self.supression_type_label = QtGui.QLabel("Suppression Type")
        horizontal_layout_1.addWidget(self.supression_type_label)

        self.automatic_dimensions_combo = QtGui.QComboBox()
        self.automatic_dimensions_combo.currentIndexChanged['QString'].connect(self.refresh_ad_info)
        horizontal_layout_1.addWidget(self.automatic_dimensions_combo)

        self.suppression_info = QtGui.QLabel("?")
        self.suppression_info.setStyleSheet('QLabel {color: blue; text-decoration: underline;}')
        horizontal_layout_1.addWidget(self.suppression_info)

        self.ad_arguments_frame = QtGui.QFrame()
        self.ad_arguments_layout = QtGui.QGridLayout(self.ad_arguments_frame)

        horizontal_layout_1.addWidget(self.ad_arguments_frame)

        horizontal_layout_1.addStretch(1)

        v_layout.addWidget(frame_1)

        frame_2 = QtGui.QFrame()
        horizontal_layout_2 = QtGui.QHBoxLayout(frame_2)
        horizontal_layout_2.addStretch(1)

        self.supression_button = QtGui.QPushButton("Create Hierarchy")
        self.supression_button.clicked.connect(self.create_automatic_hierarchy)
        horizontal_layout_2.addWidget(self.supression_button)

        self.status_button_automatic_dimension = QtGui.QPushButton("Hierarchy Status")
        self.status_button_automatic_dimension.setFlat(True)
        self.status_button_automatic_dimension.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.status_button_automatic_dimension.setStyleSheet('QPushButton {color: blue; text-decoration: underline;}')
        self.status_button_automatic_dimension.clicked.connect(self.display_hierarchy)
        horizontal_layout_2.addWidget(self.status_button_automatic_dimension)
        horizontal_layout_2.addStretch(1)

        v_layout.addWidget(frame_2)

        self.suppression_frame.hide()
        self.vertical_layout.addWidget(self.suppression_frame)

        self.refresh_automatic_dimensions()

    @staticmethod
    def create_horizontal_frame(widget):
        frame = QtGui.QFrame()
        layout = QtGui.QHBoxLayout()

        layout.addStretch(1)
        layout.addWidget(widget)
        layout.addStretch(1)

        frame.setLayout(layout)
        return frame

    def slider_value_changed(self):
        slider_value = self.privacy_slider.value()
        attribute = self.attribute_view.get_current_attribute()
        if slider_value == SUPPRESSION_SLIDER_VALUE:
            selected = 'Suppression'
            if attribute.hierarchy and attribute.hierarchy.hierarchy_type == HIERARCHY_TYPE_GENERALIZATION:
                attribute.hierarchy = None
            self.show_suppression_panel()
        elif slider_value == GENERALIZATION_SLIDER_VALUE:
            if attribute.hierarchy and attribute.hierarchy.hierarchy_type == HIERARCHY_TYPE_SUPPRESSION:
                attribute.hierarchy = None
            selected = 'Generalization'
            self.show_generalization_panel()
        else:
            selected = None
            if attribute.is_qi_attribute():
                attribute.hierarchy = None
            self.hide_anonymization_panels()
        for label in (self.supression_label, self.generalization_label):
            bold_text = QtGui.QFont.Bold if selected == label.text() else QtGui.QFont.Normal
            label.setFont(TextUtils.get_caption_text_font(weight=bold_text))

    def create_generalization_hierarchy(self):
        self.hierarchy_view = HierarchyView(self.project_controller, self.attribute_view.get_current_attribute(), self)

    def show_suppression_panel(self):
        if self.suppression_frame:
            self.suppression_frame.show()
        if self.generalization_frame:
            self.generalization_frame.hide()

    def show_generalization_panel(self):
        if self.generalization_frame:
           self.generalization_frame.show()
        if self.suppression_frame:
            self.suppression_frame.hide()

    def hide_anonymization_panels(self):
        if self.generalization_frame:
            self.generalization_frame.hide()
        if self.suppression_frame:
            self.suppression_frame.hide()

    def update_view(self):
        current_attribute = self.attribute_view.get_current_attribute()
        if current_attribute.hierarchy:
            if current_attribute.hierarchy.is_generalization_hierarchy():
                self.privacy_slider.setValue(GENERALIZATION_SLIDER_VALUE)
            else:
                self.privacy_slider.setValue(SUPPRESSION_SLIDER_VALUE)
        else:
            self.privacy_slider.setValue(NO_SELECTED_SLIDER_VALUE)

        self.slider_value_changed()

    def refresh_automatic_dimensions(self):
        current_attribute = self.attribute_view.get_current_attribute()
        dimensions = self.af_manager.get_automatic_dimensions_names(current_attribute.basic_type)
        self.automatic_dimensions_combo.clear()
        self.automatic_dimensions_combo.addItems(dimensions)

    def refresh_ad_info(self):
        # Refresh Automatic Dimension Description Tooltip
        ad_selected = str(self.automatic_dimensions_combo.currentText())
        ad_description = self.af_manager.get_automatic_dimension_description(ad_selected)
        self.suppression_info.setToolTip('' if ad_description is None else ad_description)

        # Refresh Automatic Dimension Arguments
        ad_parameters = self.af_manager.get_automatic_dimension_parameters(ad_selected)
        if ad_parameters is not None:
            utils_ui.clean_layout(self.ad_arguments_layout)
            amount_of_parameters = len(ad_parameters)
            amount_of_rows = (amount_of_parameters+1)/2
            positions = [(row, col) for row  in range(amount_of_rows) for col in range(0,4,2)]
            for position, parameter in zip(positions, ad_parameters):
                self.ad_arguments_layout.addWidget(QtGui.QLabel(parameter), position[0], position[1])
                self.ad_arguments_layout.addWidget(QtGui.QLineEdit(), position[0], position[1]+1)
            self.ad_arguments_frame.show()
        else:
            self.ad_arguments_frame.hide()


    def create_automatic_hierarchy(self):
        self.load_attributes_values_thread = LoadAttributeValuesThread(self.project_controller, self.attribute_view.get_current_attribute())
        self.load_attributes_values_thread.load_attribute_values_finished.connect(self.load_attributes_finished_update)
        self.load_attributes_values_thread.start()

    def display_hierarchy(self):
        current_attribute = self.attribute_view.get_current_attribute()
        if current_attribute.hierarchy is not None:
            HierarchyDisplayView(current_attribute, self)
        else:
            utils_ui.showMessageAlertBox(parent=self, title=strings.HIERARCHY_STATUS, message=strings.HIERARCHY_NOT_CREATED)

    def reset_slider(self):
        self.privacy_slider.setValue(NO_SELECTED_SLIDER_VALUE)

    def load_attributes_finished_update(self, values):
        try:
            current_attribute = self.attribute_view.get_current_attribute()
            hierarchy_controller = BaseHierarchyController()
            automatic_dimension_params = {}
            for i in range(0, self.ad_arguments_layout.count(), 2):
                parameter_value = str(self.ad_arguments_layout.itemAt(i+1).widget().text())
                if len(parameter_value) > 0:
                    parameter_name = str(self.ad_arguments_layout.itemAt(i).widget().text())
                    automatic_dimension_params[parameter_name] = parameter_value

            current_attribute.hierarchy = hierarchy_controller.create_automatic_dimension_hierarchy(str(self.automatic_dimensions_combo.currentText()), automatic_dimension_params, values, attribute_type=current_attribute.basic_type)

            title = 'Finished'
            text_message = 'Hierarchy Created!'
            icon = QMessageBox.Information
            detailed_text = ''
        except Exception, e:
            title = 'An error occured!'
            text_message = 'An error occured while creating the hierarchy'
            icon = QMessageBox.Critical
            detailed_text = e.message

        msg_box = utils_ui.create_message_box(title, text_message, icon)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.setDetailedText(detailed_text)
        msg_box.exec_()
