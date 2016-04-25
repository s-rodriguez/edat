from PyQt4 import QtGui

from PyQt4.QtCore import Qt
from af.exceptions import DuplicatedValueInHierarchyException
import edat.utils.ui as utils_ui
from edat.utils import strings


class HierarchyLevelDialog(QtGui.QDialog):

    def __init__(self, existing_item_values, parent=None):
        super(QtGui.QDialog, self).__init__(parent)
        self.existing_item_values = existing_item_values

        main_layout = QtGui.QVBoxLayout()

        level_name_form_view = QtGui.QFormLayout()
        self.level_name_edit_text = QtGui.QLineEdit()
        level_name_form_view.addRow("Level Name: ", self.level_name_edit_text)
        main_layout.addLayout(level_name_form_view)

        self.level_items_view = QtGui.QListWidget()
        self.level_items_view.itemChanged.connect(self.pepe)
        main_layout.addWidget(self.level_items_view)

        add_or_remove_item_layout = QtGui.QHBoxLayout()

        self.item_name = QtGui.QLineEdit()
        add_or_remove_item_layout.addWidget(self.item_name)

        add_item_button = QtGui.QPushButton("Add")
        add_item_button.clicked.connect(self.add_item)
        add_or_remove_item_layout.addWidget(add_item_button)

        remove_item_button = QtGui.QPushButton("Remove")
        remove_item_button.clicked.connect(self.remove_item)
        add_or_remove_item_layout.addWidget(remove_item_button)

        main_layout.addLayout(add_or_remove_item_layout)

        self.button_box = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.button(QtGui.QDialogButtonBox.Ok).setEnabled(False)
        self.button_box.rejected.connect(self.reject)

        main_layout.addWidget(self.button_box)

        self.setLayout(main_layout)
        if len(self.existing_item_values) == 0:
            self.setWindowTitle("Create Hierarchy Level")
        else:
            # Load the existing values
            self.setWindowTitle("Edit Hierarchy Level")
            for item in self.existing_item_values:
                list_item = QtGui.QListWidgetItem(item)
                list_item.setFlags(list_item.flags() | Qt.ItemIsEditable)
                self.level_items_view.addItem(list_item)

        self.show()

    def add_item(self):
        item_name = self.item_name.text()
        if item_name:
            try:
                for i in range(self.level_items_view.count()):
                    if item_name == self.level_items_view.item(i).text():
                        raise DuplicatedValueInHierarchyException("Duplicated value in hierarchy : %s" % item_name)

                if str(item_name) in self.existing_item_values:
                    raise DuplicatedValueInHierarchyException("Duplicated value in hierarchy : %s" % item_name)
            except DuplicatedValueInHierarchyException as e:
                utils_ui.showMessageAlertBox(parent=self, title=strings.CREATE_HIERARCHY_ITEM_ERROR, message=e.message)
                return

            self.item_name.clear()
            list_item = QtGui.QListWidgetItem(item_name)
            list_item.setFlags(list_item.flags() | Qt.ItemIsEditable)
            self.level_items_view.addItem(list_item)
            self.button_box.button(QtGui.QDialogButtonBox.Ok).setEnabled(True)

    def remove_item(self):
        for item in self.level_items_view.selectedItems():
            self.level_items_view.takeItem(self.level_items_view.row(item))
        self.button_box.button(QtGui.QDialogButtonBox.Ok).setEnabled(self.level_items_view.count() != 0)

    def get_level_items(self):
        items = []
        for i in range(self.level_items_view.count()):
            items.append(str(self.level_items_view.item(i).text()))
        return items

    def get_level_name(self):
        return str(self.level_name_edit_text.text())

    def pepe(self):
        self.button_box.button(QtGui.QDialogButtonBox.Ok).setEnabled(self.level_items_view.count() != 0)



