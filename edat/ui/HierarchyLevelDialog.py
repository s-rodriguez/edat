from PyQt4 import QtGui

from PyQt4.QtCore import Qt


class HierarchyLevelDialog(QtGui.QDialog):

    def __init__(self, parent=None):
        super(QtGui.QDialog, self).__init__(parent)

        main_layout = QtGui.QVBoxLayout()

        level_name_form_view = QtGui.QFormLayout()
        self.level_name_edit_text = QtGui.QLineEdit()
        level_name_form_view.addRow("Level Name: ", self.level_name_edit_text)
        main_layout.addLayout(level_name_form_view)

        self.level_items_view = QtGui.QListWidget()
        self.level_items_view.edit
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

        ok_and_cancel_buttons = QtGui.QDialogButtonBox(
            QtGui.QDialogButtonBox.Ok | QtGui.QDialogButtonBox.Cancel,
            Qt.Horizontal, self)
        ok_and_cancel_buttons.accepted.connect(self.accept)
        ok_and_cancel_buttons.rejected.connect(self.reject)

        main_layout.addWidget(ok_and_cancel_buttons)

        self.setLayout(main_layout)
        self.setWindowTitle("Create Hierarchy Level")

        self.show()

    def add_item(self):
        item_name = self.item_name.text()
        if item_name:
            for i in range(self.level_items_view.count()):
                if item_name == self.level_items_view.item(i).text():
                    return
            self.item_name.clear()
            list_item = QtGui.QListWidgetItem(item_name)
            list_item.setFlags(list_item.flags() | Qt.ItemIsEditable)
            self.level_items_view.addItem(list_item)

    def remove_item(self):
        for item in self.level_items_view.selectedItems():
            self.level_items_view.takeItem(self.level_items_view.row(item))

    def get_level_items(self):
        items = []
        for i in range(self.level_items_view.count()):
            items.append(str(self.level_items_view.item(i).text()))
        return items

    def get_level_name(self):
        return str(self.level_name_edit_text.text())



