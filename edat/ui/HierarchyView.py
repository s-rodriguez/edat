from PyQt4 import QtGui

from PyQt4.QtCore import Qt

from af.controller.data.SqliteController import SqliteController
from edat.ui.HierarchyLevelDialog import HierarchyLevelDialog


class HierarchyView(QtGui.QMainWindow):

    def __init__(self, project_controller, attribute, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)

        self.project_controller = project_controller
        self.attribute = attribute
        self.hierarchy_levels = []
        # TODO:  se crea el SqliteController en vez de usar la factory,
        # ya que el Csvcontroller no tiene implementado el get_distinct_qi_values
        # una vez implementado, usar la factory
        self.db_controller = SqliteController(self.project_controller.project.data_config.location)

        self.leaf_values = []
        for value in self.db_controller.get_distinct_qi_values(self.project_controller.project.data_config.table, self.attribute.name):
            self.leaf_values.append(str(value))

        self.hierarchy_levels.append(self.leaf_values)

        self.mainLayout = QtGui.QVBoxLayout()

        self.ctr_frame = QtGui.QWidget(self)
        self.ctr_frame.setLayout(self.mainLayout)
        self.setCentralWidget(self.ctr_frame)

        self.hierarchy_table_view = QtGui.QTableWidget()
        self.update_table_view()

        self.mainLayout.addWidget(self.hierarchy_table_view)

        self.hierarchy_table_view.resizeColumnsToContents()
        self.hierarchy_table_view.resizeRowsToContents()

        self.add_level_button = QtGui.QPushButton("New level")
        self.add_level_button.setMaximumSize(100, 60)
        self.add_level_button.clicked.connect(self.on_new_level)

        self.mainLayout.addWidget(self.add_level_button, 0, Qt.AlignCenter)

        self.setWindowTitle(self.attribute.name + ' Hierarchy')
        self.showMaximized()

        self.show()

    def update_table_view(self):
        self.hierarchy_table_view.setColumnCount(len(self.hierarchy_levels))
        self.hierarchy_table_view.setRowCount(len(self.leaf_values))
        self.fill_values()
        self.build_columns_headers()

    def fill_values(self):
        for n_row in range(0, len(self.leaf_values)):
            for n_col in range(0, len(self.hierarchy_levels)):
                if n_col == 0:
                    self.hierarchy_table_view.setCellWidget(n_row, n_col, QtGui.QLabel(self.leaf_values[n_row]))
                else:
                    widget = QtGui.QComboBox()
                    widget.addItems(list(self.hierarchy_levels[n_col]))
                    self.hierarchy_table_view.setCellWidget(n_row, n_col, widget)

    def build_columns_headers(self):
        for n_col in range(0, len(self.hierarchy_levels)):
            if n_col == 0:
                column_name = 'Leaf level'
            else:
                column_name = 'Level ' + str(n_col)
            self.hierarchy_table_view.setHorizontalHeaderItem(n_col, QtGui.QTableWidgetItem(column_name))

    def on_new_level(self):
        self.new_level_dialog = HierarchyLevelDialog(self)
        if self.new_level_dialog.exec_():
            level_items = self.new_level_dialog.get_level_items()
            if level_items:
                self.hierarchy_levels.append(level_items)
                self.update_table_view()





