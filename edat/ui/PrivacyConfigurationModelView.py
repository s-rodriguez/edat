from PyQt4 import QtGui

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFormLayout, QFrame, QGridLayout, QLineEdit

import edat.utils.ui as utils_ui
from edat.utils.ui.TextUtils import TextUtils
from af.model.algorithms.AfManager import AfManager


class PrivacyModelConfigurationView(QtGui.QFrame):

    def __init__(self):
        super(QFrame, self).__init__()

        main_layout = QtGui.QVBoxLayout()

        header_label = TextUtils.get_header_styled_text("Privacy Model Configuration")
        header_label.setAlignment(Qt.AlignVCenter)
        header_label.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        main_layout.addWidget(header_label, 0, Qt.AlignHCenter)

        self.form_layout = self.get_form_layout()

        self.af_manager = AfManager()

        self.add_privacy_models()
        self.add_model_algorithms()
        self.add_algorithm_arguments()
        self.add_extra_options()

        self.privacy_configuration_frame = QFrame()
        self.privacy_configuration_frame.setLayout(self.form_layout)
        main_layout.addWidget(self.privacy_configuration_frame, 0, Qt.AlignCenter)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLayout(main_layout)

    def add_privacy_models(self):
        self.privacy_model_combo = QtGui.QComboBox()
        self.privacy_model_combo.addItems(list(self.af_manager.privacy_models))
        self.privacy_model_combo.currentIndexChanged['QString'].connect(self.refresh_algorithms)
        self.form_layout.addRow("Privacy Model: ", self.privacy_model_combo)

    def add_model_algorithms(self):
        self.algorithm_combo = QtGui.QComboBox()
        algorithms = self.af_manager.get_algorithms(str(self.privacy_model_combo.currentText()))
        self.algorithm_combo.addItems(list(algorithms))
        self.algorithm_combo.currentIndexChanged['QString'].connect(self.refresh_arguments)
        self.form_layout.addRow("Model Algorithm: ", self.algorithm_combo)

    def add_algorithm_arguments(self):
        self.arguments_layout = self.get_form_layout(vertical_spacing=5)
        self.arguments_frame = QFrame()
        self.arguments_frame.setLayout(self.arguments_layout)
        self.refresh_arguments(self.algorithm_combo.currentText())
        self.form_layout.addRow(self.arguments_frame)

    def add_extra_options(self):
        self.optimization_check_box = QtGui.QCheckBox("Optimize algorithm if possible")
        self.form_layout.addRow(self.optimization_check_box)

    def refresh_algorithms(self, model_selected):
        algorithms = self.af_manager.get_algorithms(model_selected)
        self.algorithm_combo.clear()
        self.algorithm_combo.addItems(list(algorithms))

    def refresh_arguments(self, algorithm_selected):
        # TODO: Review for large amount of arguments and their display on the panel
        utils_ui.clean_layout(self.arguments_layout)
        algorithm_parameters = self.af_manager.get_algoritm_parameters(algorithm_selected)
        if algorithm_parameters is not None:
            for parameter in algorithm_parameters:
                self.arguments_layout.addRow(parameter, QLineEdit())

    @staticmethod
    def get_form_layout(vertical_spacing=20):
        form_layout = QtGui.QFormLayout()
        form_layout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        form_layout.setFormAlignment(Qt.AlignLeft)
        form_layout.setLabelAlignment(Qt.AlignCenter)
        form_layout.setVerticalSpacing(vertical_spacing)
        return form_layout
