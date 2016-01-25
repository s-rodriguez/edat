import abc
from PyQt4 import QtGui
from PyQt4.QtGui import QAbstractItemView


class DataTableView(QtGui.QTableView):

    def __init__(self, project_data_controller):
        super(DataTableView, self).__init__()
        self.project_data_controller = project_data_controller
        self.setModel(self.create_model())
        self.setAlternatingRowColors(True)
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    @abc.abstractmethod
    def create_model(self):
        return
