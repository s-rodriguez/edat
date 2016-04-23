from PyQt4 import QtGui

from PyQt4.QtCore import (
    QThread,
    pyqtSignal,
)
from PyQt4.QtCore import Qt

from af.controller.data.DataFactory import DataFactory
from edat.ui.HierarchyLevelDialog import HierarchyLevelDialog

SELECT_VALUE_DEFAULT = "-- Select a value --"


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
        self.hierarchy_table_view.setRowCount(len(self.leaf_items))
        self.fill_values()
        self.build_columns_headers()
        self.hierarchy_table_view.resizeColumnsToContents()
        self.hierarchy_table_view.resizeRowsToContents()

    def add_column(self, n_col):
        for n_row in range(0, len(self.leaf_items)):
            if n_col == 0:
                self.hierarchy_table_view.setCellWidget(n_row, n_col, QtGui.QLabel(self.leaf_items[n_row]))
            else:
                level_value_combo_box = QtGui.QComboBox(self.hierarchy_table_view)
                level_value_combo_box.setProperty("row", n_row)
                level_value_combo_box.setProperty("col", n_col)
                level_value_combo_box.addItems(list(self.hierarchy_levels[n_col].items))
                level_value_combo_box.currentIndexChanged.connect(self.on_level_value_updated)
                self.hierarchy_table_view.setCellWidget(n_row, n_col, level_value_combo_box)

    def fill_values(self):
        level_count = len(self.hierarchy_levels)
        table_column_count = self.hierarchy_table_view.columnCount()

        if level_count == table_column_count:
            return

        self.hierarchy_table_view.setColumnCount(level_count)

        if level_count > table_column_count:
            while table_column_count < level_count:
                self.add_column(table_column_count)
                table_column_count += 1

    def on_level_value_updated(self):
        sender = self.sender()
        if sender.itemText(0) == SELECT_VALUE_DEFAULT:
            sender.removeItem(0)
            return

        n_row_updated = sender.property("row").toInt()[0]
        n_col_updated = sender.property("col").toInt()[0]
        if n_col_updated < 2:
            return

        n_col_to_update = n_col_updated - 1

        item_new_value = self.hierarchy_table_view.cellWidget(n_row_updated, n_col_updated).currentText()
        item_value_to_update = self.hierarchy_table_view.cellWidget(n_row_updated, n_col_to_update).currentText()

        if item_value_to_update == SELECT_VALUE_DEFAULT:
            return

        for n_row in range(0, len(self.leaf_items)):
            item = self.hierarchy_table_view.cellWidget(n_row, n_col_to_update)
            if item.currentText() == item_value_to_update:
                combo_box = self.hierarchy_table_view.cellWidget(n_row, n_col_updated)
                for i in range(combo_box.count()):
                    if combo_box.itemText(i) == item_new_value:
                        combo_box.setCurrentIndex(i)
                        break

    def build_columns_headers(self):
        for n_col in range(0, len(self.hierarchy_levels)):
            self.hierarchy_table_view.setHorizontalHeaderItem(n_col, QtGui.QTableWidgetItem(self.hierarchy_levels[n_col].name))

    def on_new_level(self):
        self.new_level_dialog = HierarchyLevelDialog(self)
        if self.new_level_dialog.exec_():
            level_items = self.new_level_dialog.get_level_items()
            if level_items:
                level_name = 'Level ' + str(len(self.hierarchy_levels)) + ' ' + self.new_level_dialog.get_level_name()
                level_items.insert(0, SELECT_VALUE_DEFAULT)
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
        controller = DataFactory.create_controller(self.project_controller.project.data_config.location, self.project_controller.project.data_config.type)
        values = []
        for value in controller.get_distinct_qi_values(self.project_controller.project.data_config.table,
                                                               self.attribute.name):
            values.append(str(value))
        self.load_attribute_values_finished.emit(values)


class HierachyLevel:
    def __init__(self, name, items, position):
        self.name = name
        self.items = items
        self.position = position

