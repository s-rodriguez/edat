from PyQt4 import QtGui

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFormLayout, QFrame

from edat.utils.ui.TextUtils import TextUtils

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

        # TODO: fill combo
        self.privacy_model_combo = QtGui.QComboBox()
        form_layout.addRow("Privacy Model: ", self.privacy_model_combo)

        # TODO: fill combo
        self.algorithm_combo = QtGui.QComboBox()
        form_layout.addRow("Model Algorithm: ", self.algorithm_combo)

        self.privacy_configuration_frame = QFrame()
        self.privacy_configuration_frame.setLayout(form_layout)
        main_layout.addWidget(self.privacy_configuration_frame, 0, Qt.AlignCenter)

        # TODO: connect button
        self.add_privacy_model_button = QtGui.QPushButton("Add Privacy Model")
        self.add_privacy_model_button.setMaximumSize(200, 30)
        main_layout.addWidget(self.add_privacy_model_button, 0, Qt.AlignCenter)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLayout(main_layout)
