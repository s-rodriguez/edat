from edat.ui.UIFactory import UIFactory
from edat.ui.CSVTableView import CSVTableView
from edat.utils.ui.TextUtils import TextUtils

class CSVUIFactory(UIFactory):

    def get_table_view_caption(self, table_name, db_location):
        table_name_label = "CSV file: {0} (Location: {1})".format(table_name, db_location)
        return table_name_label

    def create_table_view(self, controller):
        return CSVTableView(table_name, db_location)
