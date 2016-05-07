import abc
from PyQt4 import QtGui
from PyQt4.QtGui import QAbstractItemView, QHeaderView


class AbstractDataTableView(QtGui.QTableView):

    def __init__(self, table_name, db_location):
        super(AbstractDataTableView, self).__init__()

        self.table_name = table_name
        self.db_location = db_location

        self.setModel(self.create_model())
        self.setAlternatingRowColors(True)
        self.setVisible(False)

        self.resizeColumnsToContents()
        self.resizeRowsToContents()

        self.setVisible(True)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    @abc.abstractmethod
    def create_model(self):
        return
