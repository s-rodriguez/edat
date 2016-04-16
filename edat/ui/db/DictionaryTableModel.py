from PyQt4.QtCore import Qt, QAbstractTableModel, QVariant


class DictionaryTableModel(QAbstractTableModel):
    def __init__(self, header_values, dictionary_table_values, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.header_labels = header_values
        self.arraydata = []
        self._process_data_in(dictionary_table_values)

    def _process_data_in(self, dictionary_table_values):
        for key in sorted(dictionary_table_values.keys()):
            data = [key]
            values = dictionary_table_values[key]
            for value in values:
                data.append(value)
            self.arraydata.append(data)

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header_labels[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        return QVariant(self.arraydata[index.row()][index.column()])
