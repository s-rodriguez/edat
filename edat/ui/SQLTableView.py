from PyQt4 import QtSql

from edat.ui.DataTableView import DataTableView

class SQLTableView(DataTableView):

    DATABASE_NAME = "QSQLITE"

    def __init__(self, project_data_controller):
        super(SQLTableView, self).__init__(project_data_controller)

    def create_model(self):
        sql_db = QtSql.QSqlDatabase.addDatabase(self.DATABASE_NAME)
        sql_db.setDatabaseName(self.project_data_controller.project.data_config.location)
        # TODO: logear error
        if sql_db.open():
            model = SqlModel(self.project_data_controller.project.data_config.table, sql_db)
            return model

class SqlModel(QtSql.QSqlTableModel):
    def __init__(self, table_name, db, parent=None):
        super(SqlModel, self).__init__(parent, db)
        self.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        self.setTable(table_name)
        self.select()
