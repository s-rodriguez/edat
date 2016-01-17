from PyQt4 import QtGui
import os

from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtGui import QFileDialog, QPushButton, QHBoxLayout, QVBoxLayout, QLineEdit, QFormLayout, QLabel, QRadioButton, \
    QTreeView, QAbstractItemView, QStandardItemModel, QStandardItem, QItemSelectionModel

from af.controller.data.DataFactory import DataFactory


class IntroductionPage(QtGui.QWizardPage):
    def __init__(self, parent):
        super(IntroductionPage, self).__init__(parent)
        layout = QVBoxLayout()

        self.setTitle(self.tr("Introduction"))
        top_label = QLabel(self.tr('This Wizard will help you to import a table from a DB. Please select the extension of your DB'))
        top_label.setWordWrap(True)
        layout.addWidget(top_label)

        sqlite_button = QRadioButton(self.tr("SQLite"))
        sqlite_button.setChecked(True)
        self.registerField("SQLiteButton", sqlite_button)
        layout.addWidget(sqlite_button)

        csv_button = QRadioButton(self.tr("CSV"))
        self.registerField("CSVbutton", csv_button)
        layout.addWidget(csv_button)

        self.setLayout(layout)


class SelectDbPage(QtGui.QWizardPage):
    def __init__(self, parent):
        super(SelectDbPage, self).__init__(parent)
        self.setTitle('Select DB File')

        self.file_extension = None

        self.layout = QVBoxLayout()
        self.form_layout = QFormLayout()

        # project directory input text
        self.project_directory_edit_text = QLineEdit(self)
        self.project_directory_edit_text.setEnabled(False)
        self.form_layout.addRow('File:', self.project_directory_edit_text)

        self.registerField("ProjectDirectory*", self.project_directory_edit_text)

        self.layout.addLayout(self.form_layout)
        self.layout.addStretch(1)

        # directory explorer button
        self.import_button_box = QHBoxLayout()
        self.import_button_box.addStretch(1)
        self.import_button = QPushButton('...', self)
        self.connect(self.import_button, SIGNAL("clicked()"), self.show_directory)
        self.import_button_box.addWidget(self.import_button)
        self.layout.addLayout(self.import_button_box)

        self.setLayout(self.layout)

        self.setWindowTitle('Select DB')
        # self.resize(300, 300)
        self.show()

    def initializePage(self):
        sqlite_option = self.field("SQLiteButton").toPyObject()
        if sqlite_option:
            self.file_extension = 'SQLite (*.sqlite3 *.db *.sqlite)'
        else:
            self.file_extension = 'CSV (*.csv)'

    def show_directory(self):
        q_file_dialog = QFileDialog()
        filename = str(q_file_dialog.getOpenFileName(self,
                                                     'Select file', os.getcwd(), self.file_extension))
        self.project_directory_edit_text.setText(filename)


class SelectTablePage(QtGui.QWizardPage):
    def __init__(self, parent):
        super(SelectTablePage, self).__init__(parent)

        self.selected_db = None
        self.tables = None
        self.layout = None
        self.view = None
        self.model = None
        self.last_selection = -1
        self.selected_table = None

        self.setTitle('Select table')

        self.show()

    def initializePage(self):

        self.selected_db = str(self.field("ProjectDirectory").toPyObject())
        db_type = 'sqlite' if self.field("SQLiteButton").toPyObject() else 'csv'
        controller = DataFactory.create_controller(self.selected_db, db_type)
        self.tables = controller.db_available_tables()

        view = QTreeView()
        view.setSelectionBehavior(QAbstractItemView.SelectRows)
        view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.init_model(controller, view)

        self.layout = QVBoxLayout()
        self.layout.addWidget(view)
        self.setLayout(self.layout)

    def init_model(self, controller, view):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Table Name'])
        self.model.itemChanged.connect(self.on_item_changed)
        view.setModel(self.model)
        view.setUniformRowHeights(True)
        for table in self.tables:
            for name in table:
                table_name = str(name)
                root_table_item = QStandardItem(table_name)
                root_table_item.setAccessibleText(table_name)
                root_table_item.setCheckable(True)
                root_table_caption = QStandardItem("Columns:")
                root_table_item.appendRow(root_table_caption)

                table_columns = controller.table_columns_info(table_name)
                for column in table_columns:
                    child = QStandardItem(str(column))
                    child.setSelectable(False)
                    root_table_caption.appendRow(child)
                self.model.appendRow(root_table_item)

    def isComplete(self):
        return self.selected_table is not None

    def on_item_changed(self):
        for x in range(0, self.model.rowCount()):
            item = self.model.item(x, 0)
            if item.checkState() == Qt.Checked and self.last_selection != x:
                self.last_selection = x
                break

        self.selected_table = None

        for y in range(0, self.model.rowCount()):
            item = self.model.item(y, 0)
            if item.checkState() == Qt.Checked:
                if self.last_selection != y:
                    item.setCheckState(Qt.Unchecked)
                else:
                    self.selected_table = item

        self.completeChanged.emit()
