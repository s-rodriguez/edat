from PyQt4.QtGui import QStandardItemModel, QStandardItem
from af.controller.data.CSVController import CSVController

from edat.ui.db.DataTableView import DataTableView

class CSVTableView(DataTableView):

    def __init__(self, table_name, db_location):
        super(CSVTableView, self).__init__(table_name, db_location)

    def create_model(self):
        csv_controller = CSVController(self.db_location)
        columns = csv_controller.table_columns_info()
        rows_size = csv_controller.amount_of_rows()
        columns_size = len(columns)
        model = QStandardItemModel(rows_size, columns_size)
        model.setHorizontalHeaderLabels(columns)
        table_date = csv_controller.get_table_data()
        for column in range(columns_size):
            for row in range(rows_size):
                model.setItem(row, column, QStandardItem(table_date[row][column]))
        return model
