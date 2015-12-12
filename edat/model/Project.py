

class Project:

    def __init__(self, name, path_location):
        self.name = name
        self.path_location = path_location

    def __str__(self):
        return "Project: {0} ({1})".format(self.name, self.path_location)
