import os
import sys

from PyQt4.QtGui import QApplication
from edat.controller.ui.MainUIController import MainUiController
from edat.utils.ui import transform_ui_files_into_py

from edat._version import get_versions
__version__ = get_versions()['version']
del get_versions


STATUS = 'debug'


def get_edat_directory():
    return os.path.dirname(os.path.realpath(__file__))


def main(cls=None, method=None, resource=None):
    app = QApplication(sys.argv)
    form = MainUiController()
    sys.exit(app.exec_())

if __name__ == "__main__":
    if STATUS == 'debug':
        transform_ui_files_into_py()
    main()
