from PyQt4 import QtGui

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFormLayout, QFrame, QLineEdit, QLabel

import edat.utils.ui as utils_ui
from edat.utils.ui.TextUtils import TextUtils
from af.model.AfManager import AfManager


class PrivacyModelConfigurationView(QtGui.QFrame):

    def __init__(self, parent=None):
        super(QFrame, self).__init__(parent)
        self.af_manager = AfManager()

        self.main_layout = QtGui.QVBoxLayout()

        self.set_title_header()
        self.set_model_and_algorithms_box()
        self.set_algorithm_arguments_grid()
        self.set_extra_options_form()

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLayout(self.main_layout)

    def set_title_header(self):
        header_label = TextUtils.get_header_styled_text("Privacy Model Configuration")
        header_label.setAlignment(Qt.AlignVCenter)
        header_label.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.main_layout.addWidget(header_label, 0, Qt.AlignHCenter)

    def set_model_and_algorithms_box(self):
        self.model_and_algoritms_layout = QtGui.QHBoxLayout()
        self.add_models_and_algorithms()
        self.model_and_algoritms_frame = QFrame()
        self.model_and_algoritms_frame.setLayout(self.model_and_algoritms_layout)
        self.main_layout.addWidget(self.model_and_algoritms_frame, 0, Qt.AlignCenter)

    def add_models_and_algorithms(self):
        self.add_privacy_models()
        spacing_label = QLabel()
        spacing_label.setFixedWidth(100)
        self.model_and_algoritms_layout.addWidget(spacing_label)
        self.add_model_algorithms()

    def add_privacy_models(self):
        self.privacy_model_combo = QtGui.QComboBox()
        self.privacy_model_combo.addItems(list(self.af_manager.privacy_models))
        self.privacy_model_combo.currentIndexChanged['QString'].connect(self.refresh_algorithms)
        self.model_and_algoritms_layout.addWidget(TextUtils.get_caption_styled_text('Privacy Model'))
        self.model_and_algoritms_layout.addWidget(self.privacy_model_combo)

    def add_model_algorithms(self):
        self.algorithm_combo = QtGui.QComboBox()
        algorithms = self.af_manager.get_algorithms(str(self.privacy_model_combo.currentText()))
        self.algorithm_combo.addItems(list(algorithms))
        self.algorithm_combo.currentIndexChanged['QString'].connect(self.refresh_arguments)
        self.model_and_algoritms_layout.addWidget(TextUtils.get_caption_styled_text('Algorithm'))
        self.model_and_algoritms_layout.addWidget(self.algorithm_combo)

    def refresh_algorithms(self, model_selected):
        algorithms = self.af_manager.get_algorithms(model_selected)
        self.algorithm_combo.clear()
        self.algorithm_combo.addItems(list(algorithms))

    def set_algorithm_arguments_grid(self):
        self.algorithm_arguments_layout = QtGui.QGridLayout()
        self.refresh_arguments(self.algorithm_combo.currentText())
        self.algorithm_arguments_frame = QFrame()
        self.algorithm_arguments_frame.setLayout(self.algorithm_arguments_layout)
        self.main_layout.addWidget(self.algorithm_arguments_frame, 0, Qt.AlignCenter)

    def refresh_arguments(self, algorithm_selected):
        utils_ui.clean_layout(self.algorithm_arguments_layout)
        algorithm_parameters = self.af_manager.get_algoritm_parameters(algorithm_selected)
        if algorithm_parameters is not None:
            amount_of_parameters = len(algorithm_parameters)
            amount_of_rows = (amount_of_parameters+1)/2
            positions = [(row, col) for row  in range(amount_of_rows) for col in range(0,4,2)]
            for position, parameter in zip(positions, algorithm_parameters):
                self.algorithm_arguments_layout.addWidget(QLabel(parameter), position[0], position[1])
                self.algorithm_arguments_layout.addWidget(QLineEdit(), position[0], position[1]+1)

    def set_extra_options_form(self):
        self.extra_options_layout = QtGui.QFormLayout()
        self.add_extra_options()
        self.extra_options_frame = QFrame()
        self.extra_options_frame.setLayout(self.extra_options_layout)
        self.main_layout.addWidget(self.extra_options_frame, 0, Qt.AlignCenter)

    def add_extra_options(self):
        self.optimization_check_box = QtGui.QCheckBox("Optimize algorithm if possible")
        self.extra_options_layout.addRow(self.optimization_check_box)

    def get_config(self):
        algorithm_name = self.algorithm_combo.currentText()
        optimized_processing = self.optimization_check_box.isChecked()

        algorithm_parameters = {}
        for i in range(0, self.algorithm_arguments_layout.count(), 2):
            parameter_name = str(self.algorithm_arguments_layout.itemAt(i).widget().text())
            parameter_value = str(self.algorithm_arguments_layout.itemAt(i+1).widget().text())
            algorithm_parameters[parameter_name] = parameter_value

        return algorithm_name, algorithm_parameters, optimized_processing
