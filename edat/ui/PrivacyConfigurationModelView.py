from PyQt4 import QtGui

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFormLayout, QFrame, QFont, QSizePolicy
from edat.utils.ui.TextUtils import TextUtils

class PrivacyModelConfigurationView(QtGui.QFrame):

    def __init__(self):
        super(QFrame, self).__init__()

        main_layout = QtGui.QVBoxLayout()

        main_layout.addWidget(TextUtils.get_header_styled_text("Privacy Model Configuration"))

        form_layout = QtGui.QFormLayout()
        form_layout.setRowWrapPolicy(QFormLayout.DontWrapRows)
        form_layout.setFieldGrowthPolicy(QFormLayout.FieldsStayAtSizeHint)
        form_layout.setFormAlignment(Qt.AlignCenter)
        form_layout.setLabelAlignment(Qt.AlignLeft)

        # TODO: fill combo
        self.privacy_model_combo = QtGui.QComboBox()
        form_layout.addRow("Privacy Model: ", self.privacy_model_combo)

        # TODO: fill combo
        self.algorithm_combo = QtGui.QComboBox()
        form_layout.addRow("Model Algorithm: ", self.algorithm_combo)

        # # TODO: connect button
        self.add_privacy_model_button = QtGui.QPushButton("Add Privacy Model")
        self.add_privacy_model_button.setMaximumSize(250, 100)
        form_layout.addRow(self.add_privacy_model_button)

        main_layout.addLayout(form_layout)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        # TODO: remove when panel is finish
        # self.setStyleSheet("border: 1px solid red")

        self.setLayout(main_layout)
