import os
from datetime import datetime

from af.model.DataConfig import DataConfig
from af.utils import (
    DATETIME_FORMAT,
    EDAT_PROJECT_EXTENSION,
    get_json_representation,
    load_json_file,
)
from edat.exceptions.InfoException import InfoException


class Project:

    def __init__(self, name, path_location):
        self.name = name
        self.path_location = path_location
        self.creation_timestamp = datetime.now()
        self.last_saved_time = None
        self.data_config = None
        self.unsaved_changes = False

    def __str__(self):
        return "Project: {0} ({1}) [{2}]".format(
            self.name,
            self.path_location,
            self.creation_timestamp)

    def project_file_location(self):
        return os.path.join(self.path_location, self.name + EDAT_PROJECT_EXTENSION)

    def add_config_data(self, location, data_type, table):
        self.data_config = DataConfig(self, location, data_type, table)

    def load_project_file(self, project_file_location):
        try:
            json_content = load_json_file(project_file_location)
            self.creation_timestamp = datetime.strptime(json_content['creation_timestamp'], DATETIME_FORMAT)
            self.last_saved_time = datetime.strptime(json_content['last_saved_timestamp'], DATETIME_FORMAT)
            if DataConfig.JSON_KEY in json_content.keys():
                self.data_config = DataConfig(self)
                self.data_config.load_config(json_content[DataConfig.JSON_KEY])
        except Exception, e:
            raise InfoException('The project file could not be imported. \n\t{0}'.format(e))

    def data_config_representation(self):
        if self.data_config is not None:
            return self.data_config.config_representation()
        return None

    def project_file_representation(self, save=False):
        if save:
            self.last_saved_time = datetime.now()

        p_representation = {
            'creation_timestamp': str(self.creation_timestamp),
            'last_saved_timestamp': str(self.last_saved_time),
        }

        data_config_representation = self.data_config_representation()
        if data_config_representation is not None:
            p_representation[DataConfig.JSON_KEY] = data_config_representation

        return get_json_representation(p_representation)
