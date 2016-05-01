from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QSlider

from af.model.AfManager import AfManager

from edat.ui.HierarchyView import HierarchyView
from edat.utils.ui.TextUtils import TextUtils

NO_SELECTED_SLIDER_VALUE = 1

SUPPRESSION_SLIDER_VALUE = 0

GENERALIZATION_SLIDER_VALUE = 2


class AnonymizationPanel(QtGui.QFrame):

    def __init__(self, project_controller, attribute_view):
        super(QtGui.QFrame, self).__init__()
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

        self.supression_label = TextUtils.get_caption_styled_text('Supression')
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
        horizontal_layout.addWidget(self.status_button_generalization)
        horizontal_layout.addStretch(1)

        self.generalization_frame.setLayout(horizontal_layout)
        self.generalization_frame.hide()
        self.vertical_layout.addWidget(self.generalization_frame)

    def add_suppression_related_objects(self):
        self.suppression_frame = QtGui.QFrame()
        horizontal_layout = QtGui.QHBoxLayout()
        horizontal_layout.addStretch(1)

        self.supression_type_label = TextUtils.get_caption_styled_text('Supression Type')
        horizontal_layout.addWidget(self.supression_type_label)

        self.automatic_dimensions_combo = QtGui.QComboBox()
        self.automatic_dimensions_combo.currentIndexChanged['QString'].connect(self.refresh_ad_description)
        horizontal_layout.addWidget(self.automatic_dimensions_combo)

        self.suppression_info = QtGui.QLabel("?")
        self.suppression_info.setStyleSheet('QLabel {color: blue; text-decoration: underline;}')
        horizontal_layout.addWidget(self.suppression_info)

        horizontal_layout.addStretch(1)

        self.supression_button = QtGui.QPushButton("Create Hierarchy")
        self.supression_button.clicked.connect(self.create_automatic_hierarchy)
        horizontal_layout.addWidget(self.supression_button)

        self.status_button_automatic_dimension = QtGui.QPushButton("Hierarchy Status")
        self.status_button_automatic_dimension.setFlat(True)
        self.status_button_automatic_dimension.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.status_button_automatic_dimension.setStyleSheet('QPushButton {color: blue; text-decoration: underline;}')
        horizontal_layout.addWidget(self.status_button_automatic_dimension)
        horizontal_layout.addStretch(1)

        self.suppression_frame.setLayout(horizontal_layout)
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
        if slider_value == SUPPRESSION_SLIDER_VALUE:
            selected = 'Supression'
            self.show_suppression_panel()
        elif slider_value == GENERALIZATION_SLIDER_VALUE:
            selected = 'Generalization'
            self.show_generalization_panel()
        else:
            selected = None
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
            # TODO: agregar logica para saber si la jerarquia existente se debe a generalizacion o supresion
            self.privacy_slider.setValue(GENERALIZATION_SLIDER_VALUE)
        else:
            self.privacy_slider.setValue(NO_SELECTED_SLIDER_VALUE)

    def refresh_automatic_dimensions(self):
        current_attribute = self.attribute_view.get_current_attribute()
        dimensions = self.af_manager.get_automatic_dimensions_names(current_attribute.basic_type)
        self.automatic_dimensions_combo.clear()
        self.automatic_dimensions_combo.addItems(dimensions)

    def refresh_ad_description(self):
        ad_selected = str(self.automatic_dimensions_combo.currentText())
        ad_description = self.af_manager.get_automatic_dimension_description(ad_selected)
        self.suppression_info.setToolTip('' if ad_description is None else ad_description)

    def create_automatic_hierarchy(self):
        # TODO: connect automatic dimension with base hierarchy controller and create hierarchy
        pass
