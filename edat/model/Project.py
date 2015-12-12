from edat.exceptions.InfoException import InfoException

class Project:

    def __init__(self, name, path_location):
        self.name = name
        self.path_location = path_location
        self.creation_timestamp = None

    def __str__(self):
        return "Project: {0} ({1}) [{2}]".format(
            self.name,
            self.path_location,
            self.creation_timestamp)

    def parse_file(self, project_file_location):
        try:
            with open(project_file_location) as project_file:
                content = project_file.readlines()
                self.creation_timestamp = content[0].split('||')[1].strip()
        except Exception, e:
            raise InfoException('The project file could not be imported. \n\t{0}'.format(e))
