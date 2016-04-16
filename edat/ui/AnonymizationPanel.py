from PyQt4 import QtGui

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFormLayout
from PyQt4.QtGui import QSlider

from edat.ui.HierarchyView import HierarchyView


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
        self.hierarchy_view = HierarchyView(self.project_controller, self.attribute_view.get_current_attribute())



