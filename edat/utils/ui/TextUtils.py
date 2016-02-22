from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QFont


class TextUtils:

        def __init__(self):
            pass

        @staticmethod
        def get_header_styled_text(text):
            input_data_label = QtGui.QLabel(text)
            input_data_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            input_data_label.setFont(QFont("Arial", 16))
            input_data_label.setMargin(5)
            return input_data_label

        @staticmethod
        def get_caption_styled_text(text):
            input_data_label = QtGui.QLabel(text)
            input_data_label.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
            input_data_label.setFont(QFont("Arial", 12))
            input_data_label.setMargin(5)
            return input_data_label