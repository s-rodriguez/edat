from edat._version import get_versions
__version__ = get_versions()['version']
del get_versions

import sys

from PyQt4.QtGui import QApplication

from edat.controller.ui.MainUIController import MainUiController


def main(cls=None, method=None, resource=None):
    app = QApplication(sys.argv)
    form = MainUiController()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
