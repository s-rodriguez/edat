from edat.ui.db.AbstractDataTableView import AbstractDataTableView
from edat.ui.db.DictionaryTableModel import DictionaryTableModel


class MetricsTableView(AbstractDataTableView):

    def __init__(self, header_values, dictionary_values, parent=None):
        self.header_values = header_values
        self.dictionary_values = dictionary_values
        super(MetricsTableView, self).__init__(None, None)

    def create_model(self):
        return DictionaryTableModel(self.header_values, self.dictionary_values, self)
