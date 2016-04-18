from PyQt4 import QtGui
from PyQt4.QtCore import Qt

from af.model.reports.TransformationMetrics import TransformationMetrics

from edat.ui.db.MetricsTableView import MetricsTableView
from edat.utils.ui.TextUtils import TextUtils


class ReportMetricsView(QtGui.QFrame):

    def __init__(self, project_controller):
        super(QtGui.QFrame, self).__init__()

        self.project_controller = project_controller
        self.transformation_metrics = TransformationMetrics(self.project_controller.project.data_config)

        self.main_layout = QtGui.QVBoxLayout()

        self.set_general_information_panel()
        self.set_additional_information_panel()

        self.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Plain)
        self.setLayout(self.main_layout)

    def set_general_information_panel(self):
        self.general_information_frame = QtGui.QFrame()
        self.general_information_layout = QtGui.QVBoxLayout()

        self.general_information_layout.addWidget(TextUtils.get_header_styled_text("General Information"))
        self.add_removed_outliers_rows_info()
        self.add_eq_classes_amount_info()
        self.add_qi_eq_classes_differences_table()

        self.general_information_frame.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Plain)
        self.general_information_frame.setLayout(self.general_information_layout)
        self.main_layout.addWidget(self.general_information_frame)

    def add_removed_outliers_rows_info(self):
        title = "Outliers Rows Removed:"
        value = self.transformation_metrics.removed_outlier_rows()
        h_frame = self.create_hbox_frame_title_and_value(title, value)
        self.general_information_layout.addWidget(h_frame, 0, Qt.AlignLeft)

    def add_eq_classes_amount_info(self):
        title = "Amount of Equivalence Classes Generated:"
        value = self.transformation_metrics.number_of_qi_eq_classes_generated()
        h_frame = self.create_hbox_frame_title_and_value(title, value)
        self.general_information_layout.addWidget(h_frame, 0, Qt.AlignLeft)

    def add_qi_eq_classes_differences_table(self):
        qi_eq_classes_differences_str = "QI Equivalence Classes Differences"
        qi_eq_classes_differences_title = TextUtils.get_caption_styled_text(qi_eq_classes_differences_str, italic=True)
        self.general_information_layout.addWidget(qi_eq_classes_differences_title, 0, Qt.AlignLeft)

        table_frame = QtGui.QFrame()
        table_layout = QtGui.QVBoxLayout()

        qi_eq_classes_differences = self.transformation_metrics.qi_eq_classes_differences()
        qi_eq_headers = ['Attribute', 'Before', 'After']
        tableview = MetricsTableView(qi_eq_headers, qi_eq_classes_differences, self)
        table_layout.addWidget(tableview)

        table_frame.setLayout(table_layout)
        self.general_information_layout.addWidget(table_frame)

    def set_additional_information_panel(self):
        self.additional_information_frame = QtGui.QFrame()
        self.additional_information_layout = QtGui.QVBoxLayout()

        self.additional_information_layout.addWidget(TextUtils.get_header_styled_text("Additional Information"))
        self.add_additional_info()

        self.additional_information_frame.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Plain)
        self.additional_information_frame.setLayout(self.additional_information_layout)
        self.main_layout.addWidget(self.additional_information_frame)

    def add_additional_info(self):
        additional_info_frame = QtGui.QFrame()
        additional_info_layout = QtGui.QVBoxLayout()
        additional_info_frame.setLayout(additional_info_layout)

        additional_info_dict = self.transformation_metrics.additional_information
        for key in sorted(additional_info_dict.keys()):
            title = additional_info_dict[key][0]
            value = additional_info_dict[key][1]
            if len(value) < 100:
                h_frame = self.create_hbox_frame_title_and_value(title, value)
                additional_info_layout.addWidget(h_frame, 0, Qt.AlignLeft)
            else:
                h_frame = self.create_hbox_frame_title_and_value(title, "")
                additional_info_layout.addWidget(h_frame, 0, Qt.AlignLeft)

                scroll_area = self.get_scrollable_area_with_value(value)
                additional_info_layout.addWidget(scroll_area)
        
        additional_info_layout.addStretch(1)
        self.additional_information_layout.addWidget(additional_info_frame)

    @staticmethod
    def create_hbox_frame_title_and_value(title, value):
        h_frame = QtGui.QFrame()
        h_box_layout = QtGui.QHBoxLayout()
        h_box_layout.setContentsMargins(0, 0, 0, 0)
        h_box_layout.setSpacing(0)
        
        eq_amount_title = TextUtils.get_caption_styled_text(title, italic=True)
        h_box_layout.addWidget(eq_amount_title)

        eq_amount_value_title = TextUtils.get_caption_styled_text("{0}".format(str(value)), weight=QtGui.QFont.Bold)
        h_box_layout.addWidget(eq_amount_value_title)

        h_frame.setLayout(h_box_layout)

        return h_frame

    @staticmethod
    def get_scrollable_area_with_value(value):
        scroll_widget = QtGui.QWidget()
        scroll_area = QtGui.QScrollArea()
        scroll_area.setMaximumHeight(120)
        scroll_layout = QtGui.QVBoxLayout()
        scroll_widget.setLayout(scroll_layout)

        scroll_layout.addWidget(TextUtils.get_caption_styled_text("{0}".format(str(value))))     

        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameStyle(QtGui.QFrame.NoFrame)
        scroll_area.setFrameShadow(QtGui.QFrame.Plain)
        return scroll_area