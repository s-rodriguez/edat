from PyQt4 import QtGui

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFormLayout
from PyQt4.QtGui import QSlider

from edat.ui.HierarchyView import HierarchyView
from edat.utils.ui.TextUtils import TextUtils


class AnonymizationPanel(QtGui.QFrame):

    def __init__(self, project_controller, attribute_view):
        super(QtGui.QFrame, self).__init__()

        self.attribute_view = attribute_view
        self.project_controller = project_controller

        layout = QFormLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(1)
        self.slider.setValue(0)
        self.slider.setTickInterval(1)
        self.slider.setToolTip("On/Off")
        layout.addRow(self.get_slider_text(), self.slider)

        self.status_button = QtGui.QPushButton("status_information")
        self.status_button.setFlat(True)
        self.status_button.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.status_button.setStyleSheet('QPushButton {color: blue; text-decoration: underline;}')
        layout.addRow("Status:", self.status_button)

        self.action_button = QtGui.QPushButton(self.get_push_button_text())
        self.action_button.clicked.connect(self.on_push_button_clicked)

        layout.addRow(self.action_button)

        self.setLayout(layout)

    def get_slider_text(self):
        pass

    def get_push_button_text(self):
        pass

    def on_push_button_clicked(self):
        pass

class SuppressionPanel(AnonymizationPanel):

    def get_slider_text(self):
        return "Suppression"

    def get_push_button_text(self):
        return "Suppress"


class GeneralizationPanel(AnonymizationPanel):

    def get_slider_text(self):
        return "Generalization"

    def get_push_button_text(self):
        return "Generalize"

    def on_push_button_clicked(self):
        self.hierarchy_view = HierarchyView(self.project_controller, self.attribute_view.get_current_attribute(), self)


class ReadOnlyCheck(QtGui.QCheckBox):
    def __init__(self, parent=None, *args):
        QtGui.QCheckBox.__init__(self, parent, *args)

    def mousePressEvent(self, event):
        event.ignore()


class AnonymizationPanel2(QtGui.QFrame):

    def __init__(self, project_controller, attribute_view):
        super(QtGui.QFrame, self).__init__()

        self.attribute_view = attribute_view
        self.project_controller = project_controller

        self.vertical_layout = QtGui.QVBoxLayout()

        self.add_transformation_frame()
        self.add_hierarchy_related_objects()

        self.setLayout(self.vertical_layout)

    def add_transformation_frame(self):
        self.transformation_frame = QtGui.QFrame()
        horizontal_layout = QtGui.QHBoxLayout()

        self.supression_label = TextUtils.get_caption_styled_text('Supression')
        self.generalization_label = TextUtils.get_caption_styled_text('Generalization')

        self.privacy_slider = QSlider(Qt.Horizontal)
        self.privacy_slider.setMinimum(0)
        self.privacy_slider.setMaximum(1)
        self.privacy_slider.setTickInterval(1)
        self.privacy_slider.setValue(0)
        self.privacy_slider.valueChanged.connect(self.slider_value_changed)
        self.slider_value_changed()

        horizontal_layout.addStretch(1)
        horizontal_layout.addWidget(self.supression_label)
        horizontal_layout.addWidget(self.privacy_slider)
        horizontal_layout.addWidget(self.generalization_label)
        horizontal_layout.addStretch(1)

        self.transformation_frame.setLayout(horizontal_layout)
        self.vertical_layout.addWidget(self.transformation_frame, 0, Qt.AlignVCenter)

    def add_hierarchy_related_objects(self):

        self.status_button = QtGui.QPushButton("status_information")
        self.status_button.setFlat(True)
        self.status_button.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.status_button.setStyleSheet('QPushButton {color: blue; text-decoration: underline;}')
        status_frame = self.create_horizontal_frame(self.status_button)
        self.vertical_layout.addWidget(status_frame, 0, Qt.AlignVCenter)

        self.hierarchy_button = QtGui.QPushButton("Create Hierarchy")
        self.hierarchy_button.clicked.connect(self.create_hierarchy)
        hierarchy_frame = self.create_horizontal_frame(self.hierarchy_button)
        self.vertical_layout.addWidget(hierarchy_frame, 0, Qt.AlignVCenter)

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
        selected = 'Supression' if self.privacy_slider.value() == 0 else 'Generalization'
        for label in (self.supression_label, self.generalization_label):
            bold_text = QtGui.QFont.Bold if selected == label.text() else QtGui.QFont.Normal
            label.setFont(TextUtils.get_caption_text_font(weight=bold_text))

    def create_hierarchy(self):
        if self.privacy_slider.value() == 1:
            self.hierarchy_view = HierarchyView(self.project_controller, self.attribute_view.get_current_attribute(), self)
        else:
            print "Create supression hierarchy for attribute!!"
