from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from PyQt4.QtGui import QFrame

from edat.ui.db.UIFactoryHelper import UIFactoryHelper
from edat.utils.ui.TextUtils import TextUtils


class TableDataView(QtGui.QFrame):

    def __init__(self, db_type, table_name, db_location, header):
        super(QFrame, self).__init__()
        ui_factory = UIFactoryHelper.get_factory(db_type)

        layout = QtGui.QVBoxLayout()

        layout.addWidget(TextUtils.get_header_styled_text(header))
        data_info = ui_factory.get_table_view_caption(table_name, db_location)
        data_info.setAlignment(Qt.AlignLeft)
        layout.addWidget(data_info)

        table_view = ui_factory.create_table_view(table_name, db_location)
        layout.addWidget(table_view)

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLayout(layout)
