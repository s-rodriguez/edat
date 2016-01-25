from PyQt4.QtGui import QStandardItemModel, QStandardItem
from af.controller.data.CSVController import CSVController

from edat.ui.DataTableView import DataTableView

class CSVTableView(DataTableView):

    def __init__(self, project_data_controller):
        super(CSVTableView, self).__init__(project_data_controller)

    def create_model(self):
        csv_controller = CSVController(self.project_data_controller.project.data_config.location)
        columns = csv_controller.table_columns_info()
        rows_size = csv_controller.amount_of_rows()
        columns_size = len(columns)
        model = QStandardItemModel(columns_size, rows_size)
        model.setHorizontalHeaderLabels(columns)

        table_date = csv_controller.get_table_data()
        for row in range(rows_size):
            for column in range(columns_size):
                model.setItem(row, column, QStandardItem(table_date[row][column]))
        return model
