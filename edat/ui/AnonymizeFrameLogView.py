import logging

from PyQt4.QtGui import (
    QFrame,
    QPushButton,
    QHBoxLayout,
    QPlainTextEdit,
    QApplication,
)

from edat.utils import strings, EdatLoggingHandler


class AnonymizeFrameLogView(QFrame):

    def __init__(self, button_handle):
        super(QFrame, self).__init__()

        self.main_layout = QHBoxLayout()
        self.button_handle = button_handle

        self.add_anonymization_button()
        self.add_log_panel()

        self.setFrameStyle(QFrame.StyledPanel | QFrame.Plain)
        self.setLayout(self.main_layout)

    def add_anonymization_button(self):
        self.anonymize_button = QPushButton(strings.ANONYMIZE)
        self.anonymize_button.clicked.connect(self.button_handle)
        self.anonymize_button.setMaximumSize(200, 50)
        self.anonymize_button.setStyleSheet('font-size: 18pt; border-width: 2px;')
        self.main_layout.addWidget(self.anonymize_button)

    def add_log_panel(self):
        self.log_panel = QPlainTextEdit()
        self.log_panel.setReadOnly(True)
        self.main_layout.addWidget(self.log_panel, 3)

        self.logging_handler = EdatLoggingHandler.EdatLoggingHandler()

        logging.getLogger().setLevel(logging.INFO)
        logging.getLogger().addHandler(self.logging_handler)

        EdatLoggingHandler.XStream.stdout().messageWritten.connect(self.update_log_panel)

    def update_log_panel(self, msg):
        self.log_panel.appendPlainText(msg)
