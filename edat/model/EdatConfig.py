from datetime import datetime
import os
from af.utils import (
    DATETIME_FORMAT,
    EDAT_PROJECT_EXTENSION,
    get_json_representation,
    load_json_file,
)

class EdatConfig:
    EDAT_CONFIG_FILE = 'edat_config_file'

    def __init__(self, project=None, location=None):
        self.project = project
        self.location = location

    def edat_config_representation(self):
        self.last_saved_time = datetime.now()

        p_representation = {
            'last_saved_timestamp': str(self.last_saved_time),
            'project': self.project,
            'location': self.location,
        }

        return get_json_representation(p_representation)

    def save(self, project=None, location=None):
        self.project = project
        self.location = location
        with open(os.path.join(os.getcwd(), self.EDAT_CONFIG_FILE), 'wb') as temp_file:
            temp_file.write(self.edat_config_representation())

    def load(self):
        edat_config_file_location = os.path.join(os.getcwd(), self.EDAT_CONFIG_FILE)
        if os.path.isfile(edat_config_file_location):
            json_content = load_json_file(edat_config_file_location)
            self.project = json_content['project']
            self.location = json_content['location']

    def exists_config_file(self):
        if (self.location is not None) and (self.project is not None):
            return True
        else:
            return False



