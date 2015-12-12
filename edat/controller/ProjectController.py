from datetime import datetime
import os

from edat.model.Project import Project
from edat.exceptions.InfoException import InfoException
from edat.utils import EDAT_PROJECT_EXTENSION


class ProjectController:

    def __init__(self):
        pass

    def create_project(self, name, path_location):

        validation_errors = self._validate_new_project_config(name, path_location)
        if validation_errors is None:
            try:
                self._create_project_file(name, path_location)
            except Exception, e:
                raise InfoException("Couldn't create project file.\n\t{0}".format(e))

            return Project(name, path_location)
        else:
            raise InfoException(validation_errors)

    @staticmethod
    def _validate_new_project_config(name, path_location):
        validation_errors = None
        if os.path.isdir(path_location):
            if os.path.isfile(os.path.join(path_location, name)):
                validation_errors = 'An existent file already has the same name.'
        else:
            validation_errors = 'The location selected is not a directory.'
        return validation_errors

    def _create_project_file(self, name, path_location):
        with open(os.path.join(path_location, name + EDAT_PROJECT_EXTENSION), 'w+') as project_file:
            project_file.write('creation_timestamp: {}\n'.format(datetime.now()))
