from PyQt4 import QtGui

from PyQt4.QtGui import QTableWidgetItem

from af.controller.data.SqliteController import SqliteController


class HierarchyView(QtGui.QDialog):

    def __init__(self, project_controller, attribute, parent=None):
        super(QtGui.QDialog, self).__init__(parent)

        self.project_controller = project_controller
        self.attribute = attribute
        # TODO:  se crea el SqliteController en vez de usar la factory,
        # ya que el Csvcontroller no tiene implementado el get_distinct_qi_values
        # una vez implementado, usar la factory
        self.db_controller = SqliteController(self.project_controller.project.data_config.location)

        attribute_values = []
        for value in self.db_controller.get_distinct_qi_values(self.project_controller.project.data_config.table, self.attribute.name):
            attribute_values.append(str(value))

        layout = QtGui.QHBoxLayout()
        self.setLayout(layout)

        self.table_view = QtGui.QTableWidget()
        self.table_view.setColumnCount(2)
        self.table_view.setRowCount(len(attribute_values))
        self.fill_values(attribute_values)
        self.build_columns_headers()

        layout.addWidget(self.table_view)

        self.setWindowTitle(self.attribute.name + ' Hierarchy')
        self.table_view.resizeColumnsToContents()
        self.table_view.resizeRowsToContents()

        self.setMinimumSize(600, 600)

        self.show()

    def fill_values(self, attribute_values):

        for n_row in range(0, len(attribute_values)):
            for n_col in range(0, self.table_view.colorCount()):
                if n_col == 0:
                    widget = QtGui.QLabel()
                    self.table_view.setItem(n_row, n_col, QTableWidgetItem(attribute_values[n_row]))
                else:
                    widget = QtGui.QComboBox()
                self.table_view.setCellWidget(n_row, n_col, widget)

    def build_columns_headers(self):
        for n_col in range(0, self.table_view.columnCount()):
            if n_col == 0:
                column_name = 'Leaf level'
            else:
                column_name = 'Level ' + str(n_col)
            self.table_view.setHorizontalHeaderItem(n_col, QtGui.QTableWidgetItem(column_name))




