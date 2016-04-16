from PyQt4 import QtGui

from af.controller.data.SqliteController import SqliteController


class HierarchyView(QtGui.QDialog):

    def __init__(self, project_controller, attribute):
        super(QtGui.QDialog, self).__init__()

        self.project_controller = project_controller
        self.attribute = attribute
        # TODO:  se crea el SqliteController en vez de usar la factory,
        # ya que el Csvcontroller no tiene implementado el get_distinct_qi_values
        # una vez implementado, usar la factory
        self.db_controller = SqliteController(self.project_controller.project.data_config.location)

        attribute_values = []
        for value in self.db_controller.get_distinct_qi_values(self.project_controller.project.data_config.table, self.attribute.name):
            attribute_values.append(str(value))

        layout = QtGui.QHBoxLayout()
        self.setLayout(layout)

        self.current_level_view = QtGui.QListWidget()
        self.current_level_view.addItems(attribute_values)

        self.next_level_view = QtGui.QListWidget()

        layout.addWidget(self.current_level_view)
        layout.addWidget(self.next_level_view)

        self.setWindowTitle(self.attribute.name + ' Hierarchy')

        self.show()




