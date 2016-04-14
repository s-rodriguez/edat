from PyQt4.QtWebKit import QWebView

from af.model.reports import create_basic_report
from af.model.reports.TransformationMetrics import TransformationMetrics


class ReportMetricsView(QWebView):

    def __init__(self, project_controller):
        super(QWebView, self).__init__()
        self.project_controller = project_controller
        self.transformation_metrics = TransformationMetrics(self.project_controller.project.data_config)
        self.report_location = create_basic_report(self.transformation_metrics)
        self.set_report_on_view()

    def set_report_on_view(self):
        with open(self.report_location) as f:
            report_html = f.read()
            self.setHtml(report_html)
