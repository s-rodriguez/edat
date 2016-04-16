import logging

from PyQt4.QtCore import QObject, pyqtSignal


class EdatLoggingHandler(logging.Handler):

    def __init__(self):
        logging.Handler.__init__(self)
        self.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        msg = self.format(record)
        XStream.stdout().write(msg)


class XStream(QObject):
    _stdout = None
    messageWritten = pyqtSignal(str)

    @staticmethod
    def stdout():
        if ( not XStream._stdout ):
            XStream._stdout = XStream()
        return XStream._stdout

    def write( self, msg ):
        if ( not self.signalsBlocked() ):
            self.messageWritten.emit(msg)
