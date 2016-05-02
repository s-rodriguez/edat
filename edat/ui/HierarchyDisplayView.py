from PyQt4 import QtGui
from PyQt4.QtWebKit import QWebView

from af.model.reports.HierarchyDisplay import HierarchyDisplay


class HierarchyDisplayView(QtGui.QMainWindow):

    def __init__(self, attribute, parent=None):
        super(QtGui.QMainWindow, self).__init__(parent)

        self.attribute = attribute
        self.hierarchy_display = HierarchyDisplay()

        html_string = self.hierarchy_display.create_display(self.attribute.hierarchy)

        vlayout = QtGui.QVBoxLayout()
        web_view = QWebView()
        web_view.setHtml(html_string)

        vlayout.addWidget(web_view)

        ctr_frame = QtGui.QWidget()
        ctr_frame.setLayout(vlayout)
        self.setCentralWidget(ctr_frame)

        self.resize(400, 250)
        self.setWindowTitle('%s Hierarchy' % self.attribute.name)
        self.show()
