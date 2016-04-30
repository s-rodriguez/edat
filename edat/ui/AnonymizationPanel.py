from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QSlider

from edat.ui.HierarchyView import HierarchyView
from edat.utils.ui.TextUtils import TextUtils


class AnonymizationPanel(QtGui.QFrame):

    def __init__(self, project_controller, attribute_view):
        super(QtGui.QFrame, self).__init__()

        self.attribute_view = attribute_view
        self.project_controller = project_controller

        self.vertical_layout = QtGui.QVBoxLayout()

        self.add_transformation_frame()
        self.add_generalization_related_objects()
        self.add_suppression_related_objects()

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
        self.privacy_slider.setValue(1)
        self.privacy_slider.valueChanged.connect(self.slider_value_changed)
        self.slider_value_changed()

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
        self.hierarchy_button.clicked.connect(self.create_hierarchy)
        horizontal_layout.addWidget(self.hierarchy_button)

        self.status_button = QtGui.QPushButton("Hierarchy Status")
        self.status_button.setFlat(True)
        self.status_button.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.status_button.setStyleSheet('QPushButton {color: blue; text-decoration: underline;}')
        horizontal_layout.addWidget(self.status_button)
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

        self.suppression_type = QtGui.QComboBox()
        horizontal_layout.addWidget(self.suppression_type)

        self.suppression_info = QtGui.QPushButton("Suppression Information")
        self.suppression_info.setFlat(True)
        self.suppression_info.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.suppression_info.setStyleSheet('QPushButton {color: blue; text-decoration: underline;}')
        horizontal_layout.addWidget(self.suppression_info)
        horizontal_layout.addStretch(1)

        self.suppression_frame.setLayout(horizontal_layout)
        self.suppression_frame.hide()
        self.vertical_layout.addWidget(self.suppression_frame)

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
        if slider_value == 0:
            selected = 'Supression'
            self.show_suppression_panel()
        elif slider_value == 2:
            selected = 'Generalization'
            self.show_generalization_panel()
        else:
            selected = None
        for label in (self.supression_label, self.generalization_label):
            bold_text = QtGui.QFont.Bold if selected == label.text() else QtGui.QFont.Normal
            label.setFont(TextUtils.get_caption_text_font(weight=bold_text))

    def create_hierarchy(self):
        if self.privacy_slider.value() == 1:
            self.hierarchy_view = HierarchyView(self.project_controller, self.attribute_view.get_current_attribute(), self)
        else:
            print "Create supression hierarchy for attribute!!"

    def show_suppression_panel(self):
        self.suppression_frame.show()
        self.generalization_frame.hide()

    def show_generalization_panel(self):
        self.generalization_frame.show()
        self.suppression_frame.hide()
