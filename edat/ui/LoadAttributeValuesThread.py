from PyQt4.QtCore import (
    QThread,
    pyqtSignal,
)

from af.controller.data.DataFactory import DataFactory


class LoadAttributeValuesThread(QThread):

    load_attribute_values_finished = pyqtSignal(list)

    def __init__(self, project_controller, attribute):
        QThread.__init__(self)
        self.project_controller = project_controller
        self.attribute = attribute

    def __del__(self):
        self.wait()

    def run(self):
        controller = DataFactory.create_controller(self.project_controller.project.data_config.location, self.project_controller.project.data_config.type)
        values = []
        for value in controller.get_distinct_qi_values(self.project_controller.project.data_config.table,
                                                               self.attribute.name):
            values.append(str(value))
        self.load_attribute_values_finished.emit(values)