from PyQt4 import QtGui

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFormLayout, QFrame

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

        form_layout = QtGui.QFormLayout()
        form_layout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        form_layout.setFormAlignment(Qt.AlignLeft)
        form_layout.setLabelAlignment(Qt.AlignCenter)
        form_layout.setVerticalSpacing(30)

        self.af_manager = AfManager()

        self.privacy_model_combo = QtGui.QComboBox()
        self.privacy_model_combo.addItems(list(self.af_manager.privacy_models))
        self.privacy_model_combo.currentIndexChanged['QString'].connect(self.refresh_algorithms)
        form_layout.addRow("Privacy Model: ", self.privacy_model_combo)

        self.algorithm_combo = QtGui.QComboBox()
        algorithms = self.af_manager.get_algorithms(str(self.privacy_model_combo.currentText()))

        self.algorithm_combo.addItems(list(algorithms))
        form_layout.addRow("Model Algorithm: ", self.algorithm_combo)

        self.optimization_check_box = QtGui.QCheckBox("Optimize algorithm if possible")
        form_layout.addRow(self.optimization_check_box)

        self.privacy_configuration_frame = QFrame()
        self.privacy_configuration_frame.setLayout(form_layout)
        main_layout.addWidget(self.privacy_configuration_frame, 0, Qt.AlignCenter)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLayout(main_layout)

    def refresh_algorithms(self, model_selected):
        algorithms = self.af_manager.get_algorithms(model_selected)
        self.algorithm_combo.clear()
        self.algorithm_combo.addItems(list(algorithms))
