import sqlite3

from DataController import DataController


class SqliteController(DataController):

    def __init__(self, data_location):
        DataController.__init__(self, data_location)
        self.controller_type = 'sqlite'

    def execute_query(self, query):
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()

            cursor.execute(query)
            for row in cursor:
                yield row

    def db_available_tables(self):
        """
        From a given sqlite db, it looks for all the tables that exist
        :return: list with all available tables
        """
        query = "SELECT name FROM sqlite_master WHERE type='table';"
        tables = list(self.execute_query(query))
        return tables

    def table_columns_info(self, table_name):
        query = "SELECT * FROM {table}".format(table=table_name)
        with sqlite3.connect(self.data_location) as conn:
            cursor = conn.cursor()

            cursor.execute(query)
            columns_info = list(map(lambda x: x[0], cursor.description))
            return columns_info

    def get_table_data(self, table_name):
        query = "SELECT * FROM {table}".format(table=table_name)
        return list(self.execute_query(query))
