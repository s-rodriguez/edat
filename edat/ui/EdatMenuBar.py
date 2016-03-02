from PyQt4 import QtGui


class EdatMenuBar(QtGui.QMenuBar):

    def __init__(self, project_main_window):
        super(EdatMenuBar, self).__init__()
        self.project_main_window = project_main_window

        self.init_file_menu()

        self.init_help_menu()

    def init_help_menu(self):
        self.help_menu = self.addMenu('&Help')
        user_manual_action = self.help_menu.addAction('User Manual')
        user_manual_action.setShortcut('Ctrl+S')
        user_manual_action.triggered.connect(self.project_main_window.user_manual)

    def init_file_menu(self):
        self.file_menu = self.addMenu('&File')
        
        self.new_project_action = self.file_menu.addAction('New Project')
        self.new_project_action.setShortcut('Ctrl+N')
        self.new_project_action.triggered.connect(self.project_main_window.new_project)

        self.import_project_action = self.file_menu.addAction('Import Project')
        self.import_project_action.setShortcut('Ctrl+T')
        self.import_project_action.triggered.connect(self.project_main_window.import_project)

        self.close_project_action = self.file_menu.addAction('Close Project')
        self.close_project_action.setShortcut('Ctrl+C')
        self.close_project_action.triggered.connect(self.project_main_window.close_project)

        self.file_menu.addSeparator()
        
        self.import_action = self.file_menu.addAction('Import DB')
        self.import_action.setShortcut('Ctrl+I')
        self.import_action.triggered.connect(self.project_main_window.show_import_db_wizard)
        self.import_action.setEnabled(self.project_main_window.is_project_open())
        
        self.save_project_action = self.file_menu.addAction('Save')
        self.save_project_action.setShortcut('Ctrl+S')
        self.save_project_action.setStatusTip('Save Project')
        self.save_project_action.triggered.connect(self.project_main_window.save_project)
        self.save_project_action.setEnabled(self.project_main_window.is_project_open())
        
        self.save_project_as_action = self.file_menu.addAction('Save As')
        self.save_project_as_action.setShortcut('Ctrl+Shift+S')
        self.save_project_as_action.setStatusTip('Save Project As')
        self.save_project_as_action.triggered.connect(self.project_main_window.save_project_as)
        self.save_project_as_action.setEnabled(self.project_main_window.is_project_open())
        
        self.export_configuration_action = self.file_menu.addAction('Export Configuration')
        self.export_configuration_action.setShortcut('Ctrl+E')
        self.export_configuration_action.setStatusTip('Export Configuration')
        self.export_configuration_action.triggered.connect(self.project_main_window.export_configuration)
        self.export_configuration_action.setEnabled(self.project_main_window.is_project_open())

        self.file_menu.addSeparator()

        self.exit_action = QtGui.QAction('Exit', self)
        self.exit_action.setShortcut('Ctrl+Q')
        self.exit_action.setStatusTip('Exit application')
        self.exit_action.triggered.connect(self.project_main_window.close_application)
        
        self.file_menu.addAction(self.exit_action)

    def update_menu(self):
        self.import_action.setEnabled(self.project_main_window.is_project_open())
        self.save_project_action.setEnabled(self.project_main_window.is_project_open())
        self.save_project_as_action.setEnabled(self.project_main_window.is_project_open())
        self.export_configuration_action.setEnabled(self.project_main_window.is_project_open())
        self.close_project_action.setEnabled(self.project_main_window.is_project_open())


