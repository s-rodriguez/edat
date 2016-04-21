from PyQt4 import QtGui

from PyQt4.QtCore import (
    QThread,
    pyqtSignal,
)
from PyQt4.QtCore import Qt

from af.controller.data.SqliteController import SqliteController
from edat.ui.HierarchyLevelDialog import HierarchyLevelDialog


class HierarchyView(QtGui.QMainWindow):

    def __init__(self, project_controller, attribute, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)

        self.project_controller = project_controller
        self.attribute = attribute
        self.hierarchy_levels = []
        self.leaf_items = []

        self.load_attributes_values_thread = LoadAttributeValuesThread(self.project_controller, attribute)
        self.load_attributes_values_thread.load_attribute_values_finished.connect(self.load_attributes_finished_update)
        self.load_attributes_values_thread.start()

        self.mainLayout = QtGui.QVBoxLayout()

        self.ctr_frame = QtGui.QWidget(self)
        self.ctr_frame.setLayout(self.mainLayout)
        self.setCentralWidget(self.ctr_frame)

        self.hierarchy_table_view = QtGui.QTableWidget()

        self.mainLayout.addWidget(self.hierarchy_table_view)

        self.add_level_button = QtGui.QPushButton("New level")
        self.add_level_button.setMaximumSize(100, 60)
        self.add_level_button.clicked.connect(self.on_new_level)

        self.mainLayout.addWidget(self.add_level_button, 0, Qt.AlignCenter)

        self.setWindowTitle(self.attribute.name + ' Hierarchy')
        self.showMaximized()

        self.show()

    def update_table_view(self):
        self.hierarchy_table_view.setColumnCount(len(self.hierarchy_levels))
        self.hierarchy_table_view.setRowCount(len(self.leaf_items))
        self.fill_values()
        self.build_columns_headers()
        self.hierarchy_table_view.resizeColumnsToContents()
        self.hierarchy_table_view.resizeRowsToContents()

    def fill_values(self):
        for n_row in range(0, len(self.leaf_items)):
            for n_col in range(0, len(self.hierarchy_levels)):
                if n_col == 0:
                    self.hierarchy_table_view.setCellWidget(n_row, n_col, QtGui.QLabel(self.leaf_items[n_row]))
                else:
                    widget = QtGui.QComboBox()
                    widget.addItems(list(self.hierarchy_levels[n_col].items))
                    self.hierarchy_table_view.setCellWidget(n_row, n_col, widget)

    def build_columns_headers(self):
        for n_col in range(0, len(self.hierarchy_levels)):
            self.hierarchy_table_view.setHorizontalHeaderItem(n_col, QtGui.QTableWidgetItem(self.hierarchy_levels[n_col].name))

    def on_new_level(self):
        self.new_level_dialog = HierarchyLevelDialog(self)
        if self.new_level_dialog.exec_():
            level_items = self.new_level_dialog.get_level_items()
            if level_items:
                level_name = 'Level ' + str(len(self.hierarchy_levels)) + ' ' + self.new_level_dialog.get_level_name()
                new_level = HierachyLevel(level_name, level_items, len(self.hierarchy_levels))
                self.hierarchy_levels.append(new_level)
                self.update_table_view()

    def load_attributes_finished_update(self, values):
        self.leaf_items = values
        leaf_level = HierachyLevel('Leaf Node', self.leaf_items, len(self.hierarchy_levels))
        self.hierarchy_levels.append(leaf_level)
        self.update_table_view()


class LoadAttributeValuesThread(QThread):

    load_attribute_values_finished = pyqtSignal(list)

    def __init__(self, project_controller, attribute):
        QThread.__init__(self)
        self.project_controller = project_controller
        self.attribute = attribute

    def __del__(self):
        self.wait()

    def run(self):
        # TODO:  se crea el SqliteController en vez de usar la factory,
        # ya que el Csvcontroller no tiene implementado el get_distinct_qi_values
        # una vez implementado, usar la factory
        db_controller = SqliteController(self.project_controller.project.data_config.location)
        values = []
        for value in db_controller.get_distinct_qi_values(self.project_controller.project.data_config.table,
                                                               self.attribute.name):
            values.append(str(value))
        self.load_attribute_values_finished.emit(values)

class HierachyLevel:
    def __init__(self, name, items, position):
        self.name = name
        self.items = items
        self.position = position

