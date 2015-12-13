#!/usr/bin/python
# -*- coding: utf-8 -*-


import sys
from PyQt4 import QtGui


class EdatProjectMainWindow(QtGui.QMainWindow):

    def __init__(self, project_controller):
        super(EdatProjectMainWindow, self).__init__()

        self.project_controller = project_controller

        self.init_ui()

    def init_ui(self):
        self.showMaximized()

        text_edit = QtGui.QTextEdit()
        self.setCentralWidget(text_edit)

        # exit_action = QtGui.QAction(QtGui.QIcon('exit24.png'), 'Exit', self)
        exit_action = QtGui.QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip('Exit application')
        exit_action.triggered.connect(self.close)

        self.statusBar()

        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('&File')
        file_menu.addAction(exit_action)

        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exit_action)

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle(self.project_controller.project.name + ' - ' + self.project_controller.project.path_location)

        self.show()
