import os

from af.utils import EDAT_PROJECT_EXTENSION, CONFIG_EXTENSION
from edat.exceptions.InfoException import InfoException
from edat.model.Project import Project


class ProjectController:

    def __init__(self):
        self.project = None
        self.unsaved_changes = False

    def create_project(self, name, path_location):

        validation_errors = self._validate_new_project_config(name, path_location)
        if validation_errors is None:
            try:
                self.project = Project(name, path_location)
                self._save_project_data()
                return self.project
            except Exception, e:
                raise InfoException("Couldn't create project file.\n\t{0}".format(e))
        else:
            raise InfoException(validation_errors)

    @staticmethod
    def _validate_new_project_config(name, path_location):
        validation_errors = None
        if os.path.isdir(path_location):
            if os.path.isfile(os.path.join(path_location, name + EDAT_PROJECT_EXTENSION)):
                validation_errors = 'An existent file already has the same name.'
        else:
            validation_errors = 'The location selected is not a directory.'
        return validation_errors

    def _save_project_data(self):
        # Every time we save a project, we override the file with the new content
        project_representation = self.project.project_file_representation(save=True)
        with open(self.project.project_file_location(), 'w+') as project_file:
            project_file.write(project_representation)
        self.unsaved_changes = False

    def save_project(self, name=None, path_location=None):
        # If user chooses 'Save As' option, new name and/or location are to be changed and saved also
        self.project.name = self.project.name if name is None else name
        self.project.location = self.project.path_location if path_location is None else path_location
        self._save_project_data()

    def load_project(self, name, path_location):
        project_file_location = os.path.join(path_location, name + EDAT_PROJECT_EXTENSION)
        if os.path.isdir(path_location) and os.path.isfile(project_file_location):
            self.project = Project(name, path_location)
            self.project.load_project_file(project_file_location)
            return self.project
        else:
            raise InfoException('There is no edat project on the selected location with that name')

    def add_config_data_to_project(self, location, data_type, table):
        self.project.add_config_data(location, data_type, table)
        self.unsaved_changes = True

    def unsaved_changes(self):
        return self.unsaved_changes

    def export_configuration(self, name, location_path):
        data_config_representation = self.project.data_config_representation()

        if data_config_representation is None:
            raise InfoException('No data configuration available for this project.')

        config_location = os.path.join(location_path, name + CONFIG_EXTENSION)
        with open(config_location, 'w+') as config_file:
            config_file.write(data_config_representation)


# TODO: This is just to test this, it should be removed afterwards!
if __name__ == "__main__":
    #pc = ProjectController()
    #pc.create_project('project_test', '/home/srodriguez/repos')
    #pc.load_project('project_test', '/home/srodriguez/repos')
    #pc.add_config_data_to_project('a/directory/location', 'sqlite', 'Cars')
    #pc.save_project()
    #print pc.project.project_file_representation()
    print 'ProjectController Main function -> Delete'
