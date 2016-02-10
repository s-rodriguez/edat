from edat.ui.UIFactory import UIFactory
from edat.ui.SQLTableView import SQLTableView


class SQLUiFactory(UIFactory):

    def create_table_view(self, controller):
        return SQLTableView(controller)