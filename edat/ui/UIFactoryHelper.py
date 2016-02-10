from edat.ui.SQLUIFactory import SQLUiFactory
from edat.ui.CSVUIFactory import CSVUIFactory

class UIFactoryHelper:

    @staticmethod
    def get_factory(data_type):
        if data_type == 'sqlite':
            return SQLUiFactory()
        if data_type == 'csv':
            return CSVUIFactory()
        # TODO: raise exception data type not supported
