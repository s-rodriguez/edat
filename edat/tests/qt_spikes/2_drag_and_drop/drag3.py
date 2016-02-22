#!/usr/bin/env python
#-*- coding:utf-8 -*-

import sip
sip.setapi('QString', 2)

from PyQt4 import QtCore, QtGui

myMimeType = 'application/MyWindow'

class MyLabel(QtGui.QLabel):
    def __init__(self, parent):
        super(MyLabel, self).__init__(parent)

        self.setStyleSheet("""
            background-color: black;
            color: white;
            font: bold;
            padding: 6px;
            border-width: 2px;
            border-style: solid;
            border-radius: 16px;
            border-color: white;
        """)

    def mousePressEvent(self, event):
        itemData   = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
        dataStream.writeString(self.text())
        dataStream << QtCore.QPoint(event.pos() - self.rect().topLeft())

        mimeData = QtCore.QMimeData()
        mimeData.setData(myMimeType, itemData)
        mimeData.setText(self.text())

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(event.pos() - self.rect().topLeft())

        self.hide()

        if drag.exec_(QtCore.Qt.MoveAction | QtCore.Qt.CopyAction, QtCore.Qt.CopyAction) == QtCore.Qt.MoveAction:
            self.close()

        else:
            self.show()


class MyFrame(QtGui.QFrame):
    def __init__(self, parent=None):
        super(MyFrame, self).__init__(parent)

        self.setStyleSheet("""
            background-color: lightgray;
            border-width: 2px;
            border-style: solid;
            border-color: black;
            margin: 2px;
        """)

        y = 6
        for labelNumber in range(6):
            label = MyLabel(self)
            label.setText("Label #{0}".format(labelNumber))
            label.move(6, y)
            label.show()

            y += label.height() + 2

        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat(myMimeType):
            if event.source() in self.children():
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()

            else:
                event.acceptProposedAction()

        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasFormat(myMimeType):
            mime       = event.mimeData()
            itemData   = mime.data(myMimeType)
            dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.ReadOnly)

            text = QtCore.QByteArray()
            offset = QtCore.QPoint()
            dataStream >> text >> offset

            newLabel = MyLabel(self)
            newLabel.setText(event.mimeData().text())
            newLabel.move(event.pos() - offset)
            newLabel.show()

            if event.source() in self.children():
                event.setDropAction(QtCore.Qt.MoveAction)
                event.accept()

            else:
                event.acceptProposedAction()

        else:
            event.ignore()

class MyWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)

        self.myFrame = MyFrame(self)

        self.setCentralWidget(self.myFrame)

if __name__ == "__main__":
    import sys

    app = QtGui.QApplication(sys.argv)
    app.setApplicationName('MyWindow')

    main = MyWindow()
    main.resize(333, 333)
    main.move(app.desktop().screen().rect().center() - main.rect().center())
    main.show()

    sys.exit(app.exec_())
