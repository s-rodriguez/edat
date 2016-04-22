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
        self.hierarchy_frame = QtGui.QFrame()
        horizontal_layout = QtGui.QHBoxLayout()

        self.hierarchy_button = QtGui.QPushButton("Create Hierarchy")
        self.hierarchy_button.clicked.connect(self.create_hierarchy)
        self.hierarchy_button.setMaximumSize(200, 50)
        self.hierarchy_button.setStyleSheet('font-size: 18pt; border-width: 2px;')

        self.valid_hierarchy_checkbox = ReadOnlyCheck()
        self.valid_hierarchy_checkbox.setCheckState(Qt.Checked)
        self.valid_hierarchy_checkbox.setStyleSheet("QPushButton#DCButton:checked {color: green;")

        horizontal_layout.addStretch(1)
        horizontal_layout.addWidget(self.hierarchy_button)
        horizontal_layout.addWidget(self.valid_hierarchy_checkbox)
        horizontal_layout.addStretch(1)

        self.hierarchy_frame.setLayout(horizontal_layout)
        self.vertical_layout.addWidget(self.hierarchy_frame, 0, Qt.AlignVCenter)

    def slider_value_changed(self):
        selected = 'Supression' if self.privacy_slider.value() == 0 else 'Generalization'
        for label in (self.supression_label, self.generalization_label):
            bold_text = QtGui.QFont.Bold if selected == label.text() else QtGui.QFont.Normal
            label.setFont(TextUtils.get_caption_text_font(weight=bold_text))

    def create_hierarchy(self):
        print 123123123123
