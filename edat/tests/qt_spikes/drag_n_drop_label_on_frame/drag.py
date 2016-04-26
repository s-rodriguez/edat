#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

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
            border-color: white;
        """)

    def mousePressEvent(self, event):
        # write the relative cursor position to mime data
        mimeData = QtCore.QMimeData()
        mimeData.setText(self.text())

        # ghost of label
        pixmap = QtGui.QPixmap.grabWidget(self)
        # below makes the pixmap half transparent
        painter = QtGui.QPainter(pixmap)
        painter.setCompositionMode(painter.CompositionMode_DestinationIn)
        painter.fillRect(pixmap.rect(), QtGui.QColor(0, 0, 0, 127))
        painter.end()

        # make a QDrag
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_()


class Frame(QtGui.QFrame):

    def __init__(self):
        super(Frame, self).__init__()
        self.labels = []

        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout)

        self.setMaximumSize(50, 50)

        self.setAcceptDrops(True)

        self.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Plain)

        p = self.palette()
        p.setColor(self.backgroundRole(), QtCore.Qt.red)
        self.setPalette(p)

    def dragEnterEvent(self, e):
      
        if e.mimeData().hasFormat('text/plain'):
            e.accept()
        else:
            e.ignore() 

    def dropEvent(self, e):
        label = QtGui.QLabel(e.mimeData().text(), self)
        self.layout.addWidget(label)
        self.labels.append(label)
        label.show()
        e.setDropAction(QtCore.Qt.CopyAction)
        

class Example(QtGui.QWidget):
  
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):

        widget_layout = QtGui.QHBoxLayout(self)

        frame1 = QtGui.QFrame()
        frame1.setFrameStyle(QtGui.QFrame.StyledPanel | QtGui.QFrame.Plain)
        layout_1 = QtGui.QVBoxLayout(frame1)

        layout_1.addStretch(1)
        label = MyLabel(self)
        label.setText("label_name")
        layout_1.addWidget(label)
        layout_1.addStretch(1)

        frame = Frame()

        widget_layout.addWidget(frame1, 0)
        layout_1.addStretch(1)
        widget_layout.addWidget(frame, 1)

        self.setWindowTitle('Simple drag & drop')
        self.setGeometry(800, 800, 800, 500)


def main():
  
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()  
  

if __name__ == '__main__':
    main()   
