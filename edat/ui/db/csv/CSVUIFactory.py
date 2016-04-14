from edat.ui.db.UIFactory import UIFactory
from edat.ui.db.csv.CSVTableView import CSVTableView
from edat.utils.ui.TextUtils import TextUtils

class CSVUIFactory(UIFactory):

    def get_table_view_caption(self, table_name, db_location):
        text = "CSV file: {0}\nFile Location: {1}".format(table_name, db_location)
        table_name_label = TextUtils.get_caption_styled_text(text)
        return table_name_label

    def create_table_view(self, table_name, db_location):
        return CSVTableView(table_name, db_location)
