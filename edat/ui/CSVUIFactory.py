from edat.ui.UIFactory import UIFactory
from edat.ui.CSVTableView import CSVTableView

class CSVUIFactory(UIFactory):

    def create_table_view(self, controller):
        return CSVTableView(controller)
