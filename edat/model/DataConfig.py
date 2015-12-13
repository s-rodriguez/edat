from edat.utils import get_json_representation


class DataConfig:
    JSON_KEY = 'config'

    def __init__(self, project, location=None, data_type=None, table=None):
        self.project = project
        self.location = location
        self.type = data_type
        self.table = table

    def config_representation(self):
        config = {
            'location': self.location,
            'data_type': self.type,
            'table': self.table,
        }
        return get_json_representation(config)

    def load_config(self, config_dict):
        self.location = config_dict['location']
        self.type = config_dict['data_type']
        self.table = config_dict['table']
