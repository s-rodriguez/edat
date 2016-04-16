from PyQt4 import QtSql

from edat.ui.db.AbstractDataTableView import DataTableView

class SQLTableView(DataTableView):

    DATABASE_NAME = "QSQLITE"

    def __init__(self, table_name, db_location):
        super(SQLTableView, self).__init__(table_name, db_location)

    def create_model(self):
        sql_db = QtSql.QSqlDatabase.addDatabase(self.DATABASE_NAME)
        sql_db.setDatabaseName(self.db_location)
        # TODO: logear error
        if sql_db.open():
            model = SqlModel(self.table_name, sql_db)
            return model

class SqlModel(QtSql.QSqlTableModel):
    def __init__(self, table_name, db, parent=None):
        super(SqlModel, self).__init__(parent, db)
        self.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.setTable(table_name)
        self.select()
