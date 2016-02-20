from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from PyQt4.QtGui import QFrame

from edat.ui.UIFactoryHelper import UIFactoryHelper
from edat.utils.ui.TextUtils import TextUtils


class InputDataView(QtGui.QFrame):

    def __init__(self, project_data_controller):
        super(QFrame, self).__init__()
        ui_factory = UIFactoryHelper.get_factory(project_data_controller.project.data_config.type)

        layout = QtGui.QVBoxLayout()

        layout.addWidget(TextUtils.get_header_styled_text("Input Data"))
        data_info = ui_factory.get_table_view_caption(project_data_controller)
        data_info.setAlignment(Qt.AlignLeft)
        layout.addWidget(data_info)
        layout.addWidget(ui_factory.create_table_view(project_data_controller))

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLayout(layout)
