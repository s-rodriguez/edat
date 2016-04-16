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

        self.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Plain)
        self.setLayout(self.main_layout)

    def set_general_information_panel(self):
        header_label = TextUtils.get_header_styled_text("General Metrics")
        header_label.setAlignment(Qt.AlignLeft)
        header_label.setSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        self.main_layout.addWidget(header_label, 0, Qt.AlignHCenter)

        self.add_qi_eq_classes_differences_table()

    def add_qi_eq_classes_differences_table(self):
        qi_eq_classes_differences = self.transformation_metrics.qi_eq_classes_differences()
        qi_eq_headers = ['Attribute', 'Before', 'After']
        tableview = MetricsTableView(qi_eq_headers, qi_eq_classes_differences, self)
        self.main_layout.addWidget(tableview)

#eq_classes_differences = transformation_metrics.qi_eq_classes_differences()
#transformation_metrics.removed_outlier_rows()
#"eq_classes_amount": transformation_metrics.number_of_qi_eq_classes_generated(),
#"additional_information": transformation_metrics.additional_information,
