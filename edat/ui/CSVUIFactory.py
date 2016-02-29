from edat.ui.UIFactory import UIFactory
from edat.ui.CSVTableView import CSVTableView
from edat.utils.ui.TextUtils import TextUtils

class CSVUIFactory(UIFactory):

    def get_table_view_caption(self, controller):
        table_name_label = TextUtils.get_caption_styled_text("CSV file: " + controller.project.data_config.table + " (Location: " +
            controller.project.data_config.location + ")")
        return table_name_label

    def create_table_view(self, controller):
        return CSVTableView(controller)
