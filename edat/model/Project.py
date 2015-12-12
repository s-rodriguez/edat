from datetime import datetime
import json

from edat.exceptions.InfoException import InfoException
from edat.utils import DATETIME_FORMAT

class Project:

    def __init__(self, name, path_location):
        self.name = name
        self.path_location = path_location
        self.creation_timestamp = datetime.now()

    def __str__(self):
        return "Project: {0} ({1}) [{2}]".format(
            self.name,
            self.path_location,
            self.creation_timestamp)

    def load_project_file(self, project_file_location):
        try:
            with open(project_file_location) as project_file:
                json_content = json.loads(project_file.read())
                self.creation_timestamp = datetime.strptime(json_content['creation_timestamp'], DATETIME_FORMAT)
        except Exception, e:
            raise InfoException('The project file could not be imported. \n\t{0}'.format(e))

    def project_file_representation(self):
        p_representation = {}
        p_representation['creation_timestamp'] = str(self.creation_timestamp)

        return json.dumps(p_representation, sort_keys=True, indent=2)
