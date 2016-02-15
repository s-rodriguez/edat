from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFormLayout
from PyQt4.QtGui import QSlider


class AnonymizationPanel(QtGui.QWidget):

    def __init__(self):
        super(QtGui.QWidget, self).__init__()
        layout = QFormLayout()
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setMinimum(0)
        self.slider.setMaximum(1)
        self.slider.setValue(0)
        self.slider.setTickInterval(1)
        layout.addRow(self.get_slider_text(), self.slider)

        self.status_button = QtGui.QPushButton("status_information")
        self.status_button.setFlat(True)
        self.status_button.setSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.status_button.setStyleSheet('QPushButton {color: blue; text-decoration: underline;}')

        layout.addRow("Status:", self.status_button)
        layout.addRow(QtGui.QPushButton(self.get_push_button_text()))
        self.setLayout(layout)

    def get_slider_text(self):
        pass

    def get_push_button_text(self):
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

