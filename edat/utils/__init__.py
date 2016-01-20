from PyQt4 import QtGui

def showMessageAlertBox(parent, title, message):
    error_message = QtGui.QMessageBox(parent)
    error_message.setWindowTitle(title)
    error_message.setText(message)
    error_message.exec_()
