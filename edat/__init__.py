import os
import sys

from PyQt4.QtGui import QApplication
from edat.controller.ui.MainUIController import MainUiController

from edat._version import get_versions
__version__ = get_versions()['version']
del get_versions


STATUS = 'debug'


def get_edat_directory():
    return os.path.dirname(os.path.realpath(__file__))


def debug_actions():
    from edat.utils.ui import transform_ui_files_into_py
    transform_ui_files_into_py()


def create_project():
    from edat.utils.tests import create_full_project
    create_full_project()


def main(cls=None, method=None, resource=None):
    # Activate when necessary
    #if STATUS == 'debug':
    #    debug_actions()

    app = QApplication(sys.argv)
    controller = MainUiController()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
