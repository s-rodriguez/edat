from UIFactory import UIFactory
from ui.SQLTableView import SQLTableView


class SQLUiFactory(UIFactory):

    def create_table_view(self, controller):
        return SQLTableView(controller)