from edat.ui.UIFactory import UIFactory
from edat.ui.SQLTableView import SQLTableView
from edat.utils.ui.TextUtils import TextUtils


class SQLUiFactory(UIFactory):

    def get_table_view_caption(self, controller):
        table_name_label = TextUtils.get_caption_styled_text("Table Name: " + controller.project.data_config.table + " (Database location: " +
            controller.project.data_config.location + " )")
        return table_name_label

    def create_table_view(self, controller):
        return SQLTableView(controller)
