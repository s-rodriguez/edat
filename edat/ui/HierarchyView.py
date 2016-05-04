from PyQt4 import QtGui

from PyQt4.QtCore import Qt
from PyQt4.QtGui import QMessageBox

import edat.utils.ui as utils_ui
from af.controller.hierarchies.BaseHierarchyController import BaseHierarchyController
from af.exceptions import InvalidValueInHierarchyException
from af.model.hierarchies.BaseHierarchy import BaseHierarchy
from edat.ui.HierarchyLevelDialog import HierarchyLevelDialog
from edat.utils import strings
from edat.ui.LoadAttributeValuesThread import LoadAttributeValuesThread

SELECT_VALUE_DEFAULT = "-- Select a value --"


class HierarchyView(QtGui.QMainWindow):

    def __init__(self, project_controller, attribute, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)

        self.project_controller = project_controller
        self.attribute = attribute
        self.hierarchy_levels = []
        self.leaf_items = []

        self.mainLayout = QtGui.QVBoxLayout()

        self.ctr_frame = QtGui.QWidget(self)
        self.ctr_frame.setLayout(self.mainLayout)
        self.setCentralWidget(self.ctr_frame)

        self.hierarchy_table_view = QtGui.QTableWidget()
        headers = self.hierarchy_table_view.horizontalHeader()
        headers.setContextMenuPolicy(Qt.CustomContextMenu)
        headers.customContextMenuRequested.connect(self.open_table_context_menu)

        self.mainLayout.addWidget(self.hierarchy_table_view)

        self.add_buttons()

        if self.attribute.hierarchy is None or len(self.attribute.hierarchy.leaf_nodes) == 0 or self.attribute.hierarchy.leaf_nodes[0].value == BaseHierarchy.supression_node().value:

            self.load_attributes_values_thread = LoadAttributeValuesThread(self.project_controller, self.attribute)
            self.load_attributes_values_thread.load_attribute_values_finished.connect(self.load_attributes_finished_update)
            self.load_attributes_values_thread.start()
        else:
            self.load_hierarchy()

        self.setWindowTitle(self.attribute.name + ' Hierarchy')
        self.showMaximized()

        self.show()

    def add_buttons(self):
        self.buttons_frame = QtGui.QFrame()
        horizontal_layout = QtGui.QHBoxLayout()

        self.add_level_button = QtGui.QPushButton("New level")
        self.add_level_button.setMaximumSize(100, 60)
        self.add_level_button.clicked.connect(self.on_new_level)
        horizontal_layout.addWidget(self.add_level_button)

        self.create_hiearchy_button = QtGui.QPushButton("Create Hierarchy")
        self.create_hiearchy_button.setMaximumSize(120, 60)
        self.create_hiearchy_button.clicked.connect(self.on_create_hierarchy)
        self.create_hiearchy_button.setEnabled(False)
        horizontal_layout.addWidget(self.create_hiearchy_button)

        self.buttons_frame.setLayout(horizontal_layout)

        self.mainLayout.addWidget(self.buttons_frame, 0, Qt.AlignCenter)


    def load_hierarchy(self):
        hierarchy_depth = self.attribute.hierarchy.get_hierarchy_depth()
        nodes_dimension_values = self.attribute.hierarchy.get_all_nodes_complete_transformation()

        hierarchy_levels = map(list, zip(*nodes_dimension_values))

        for col, level in enumerate(hierarchy_levels):
            if col < hierarchy_depth:

                distinct_level_values = []
                for i in level:
                    if i not in distinct_level_values:
                        distinct_level_values.append(i)

                if col == 0:
                    self.leaf_items = distinct_level_values
                    level_name = 'Leaf Node'
                else:
                    level_name = 'Level ' + str(len(self.hierarchy_levels))
                    distinct_level_values.insert(0, SELECT_VALUE_DEFAULT)

                new_level = HierachyLevel(level_name, distinct_level_values, len(self.hierarchy_levels))
                self.hierarchy_levels.append(new_level)

        self.update_table_view()

        for row_id, dimension_values in enumerate(nodes_dimension_values):
            for col_id, value in enumerate(dimension_values):
                if col_id != 0 and col_id < hierarchy_depth:
                    combo_box = self.hierarchy_table_view.cellWidget(row_id, col_id)
                    index = combo_box.findText(value, Qt.MatchFixedString)
                    if index >= 0:
                        combo_box.blockSignals(True)
                        combo_box.setCurrentIndex(index)
                        combo_box.blockSignals(False)

    def update_table_view(self):
        self.hierarchy_table_view.setRowCount(len(self.leaf_items))
        self.fill_values()
        self.build_columns_headers()
        self.hierarchy_table_view.resizeColumnsToContents()
        self.hierarchy_table_view.resizeRowsToContents()
        self.create_hiearchy_button.setEnabled(len(self.hierarchy_levels) > 1)

    def add_column(self, n_col):
        for n_row in range(0, len(self.leaf_items)):
            if n_col == 0:
                self.hierarchy_table_view.setCellWidget(n_row, n_col, QtGui.QLabel(self.leaf_items[n_row]))
            else:
                level_value_combo_box = QtGui.QComboBox(self.hierarchy_table_view)
                level_value_combo_box.setProperty("row", n_row)
                level_value_combo_box.setProperty("col", n_col)

                column_items = self.hierarchy_levels[n_col].items
                if (SELECT_VALUE_DEFAULT not in column_items) and (len(column_items) > 1):
                    column_items.insert(0, SELECT_VALUE_DEFAULT)

                level_value_combo_box.addItems(column_items)
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
        hierarchy_items = set()
        for level in range(1, len(self.hierarchy_levels)):
            hierarchy_items |= set(self.hierarchy_levels[level].items)

        self.new_level_dialog = HierarchyLevelDialog(hierarchy_items, self)
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

    def validate_hierarchy(self):
        model = self.hierarchy_table_view.model()
        for col_id in range(model.columnCount()):
            for row_id in range(1, model.rowCount()):
                cell_widget = self.hierarchy_table_view.cellWidget(row_id, col_id)
                cell_value = cell_widget.currentText() if col_id != 0 else cell_widget.text()
                if cell_value == SELECT_VALUE_DEFAULT:
                    raise InvalidValueInHierarchyException("Default value present in hierarchy")

    def on_create_hierarchy(self):
        reply = QtGui.QMessageBox.question(self,
                                           'Hierarchy Creation',
                                           'The creation of the new hierarchy will override the current hierarchy saved in the attribute configuration.\n\nDo you want to proceed anyway?',
                                           QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
                                           QtGui.QMessageBox.No
                                           )

        if reply == QtGui.QMessageBox.Yes:

            try:
                self.validate_hierarchy()

            except InvalidValueInHierarchyException as e:
                utils_ui.showMessageAlertBox(parent=self, title=strings.CREATE_HIERARCHY_ITEM_ERROR, message=e.message)
                return

            model = self.hierarchy_table_view.model()
            rows = []
            for row_id in range(model.rowCount()):
                row_data = []
                for col_id in range(model.columnCount()):
                    cell_widget = self.hierarchy_table_view.cellWidget(row_id, col_id)
                    cell_value = cell_widget.currentText() if col_id != 0 else cell_widget.text()
                    row_data.append(str(cell_value))

                if len(rows) > 0 and len(rows[0]) != len(row_data):
                    raise Exception("Hierarchy not well formed, different heights")
                rows.append(row_data)

            new_hierarchy = BaseHierarchyController.create_hierarchy_from_list_of_values(rows)
            self.attribute.hierarchy = new_hierarchy
            self.show_hierarchy_created_dialog()
            self.close()

    @staticmethod
    def show_hierarchy_created_dialog():
        title = 'Finished'
        text_message = 'Hierarchy Created!'
        icon = QMessageBox.Information

        msg_box = utils_ui.create_message_box(title, text_message, icon)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()

    def open_table_context_menu(self, position):
        level_id = self.hierarchy_table_view.columnAt(position.x())
        if level_id < 1:
            return
        menu = QtGui.QMenu()
        edit_level_action = menu.addAction("Edit Level")
        remove_level_action = menu.addAction("Remove Level")
        action = menu.exec_(self.hierarchy_table_view.mapToGlobal(position))
        if action == edit_level_action:
            self.edit_level(level_id)
        elif action == remove_level_action:
            self.remove_level(level_id)

    def edit_level(self, level_id):
        if level_id != 0:
            hierarchy_items = self.hierarchy_levels[level_id].items
            if SELECT_VALUE_DEFAULT in hierarchy_items:
                hierarchy_items.pop(0)

            update_level_dialog = HierarchyLevelDialog(set(hierarchy_items), self)
            if update_level_dialog.exec_():
                level_items = update_level_dialog.get_level_items()

                if level_items:
                    level_name = 'Level ' + str(len(self.hierarchy_levels)) + ' ' + update_level_dialog.get_level_name()

                    new_level = HierachyLevel(level_name, level_items, len(self.hierarchy_levels))
                    self.hierarchy_levels.insert(level_id, new_level)
                    self.hierarchy_levels.pop(level_id+1)

                    combo_items = list(level_items)
                    if SELECT_VALUE_DEFAULT not in combo_items:
                        combo_items.insert(0, SELECT_VALUE_DEFAULT)

                    model = self.hierarchy_table_view.model()
                    for row_id in range(model.rowCount()):
                        combo_box = self.hierarchy_table_view.cellWidget(row_id, level_id)
                        combo_box.blockSignals(True)
                        previous_value = combo_box.currentText()
                        combo_box.clear()
                        combo_box.addItems(combo_items)
                        index = combo_box.findText(previous_value, Qt.MatchFixedString)
                        if index < 0:
                            index = 0
                        combo_box.setCurrentIndex(index)
                        combo_box.blockSignals(False)

    def remove_level(self, level_id):
        if level_id != 0:
            self.hierarchy_table_view.removeColumn(level_id)
            self.hierarchy_levels.pop(level_id)
            self.update_table_view()


class HierachyLevel:
    def __init__(self, name, items, position):
        self.name = name
        self.items = items
        self.position = position

