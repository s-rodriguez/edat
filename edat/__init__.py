import sys

from PyQt4.QtGui import QApplication
from controller.MainUIController import MainUiController


def main(cls=None, method=None, resource=None):
    app = QApplication(sys.argv)
    form = MainUiController()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
