from edat.ui.UIFactory import UIFactory
from edat.ui.SQLTableView import SQLTableView
from edat.utils.ui.TextUtils import TextUtils


class SQLUiFactory(UIFactory):

    def get_table_view_caption(self, table_name, db_location):
        label = "Table Name: {0} (Database location: {1})".format(table_name, db_location)
        table_name_label = TextUtils.get_caption_styled_text(label)
        return table_name_label

    def create_table_view(self, table_name, db_location):
        return SQLTableView(table_name, db_location)
