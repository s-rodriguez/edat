import json

EDAT_PROJECT_EXTENSION = '.edat'

DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S.%f"


def get_json_representation(data_dict):
    return json.dumps(data_dict, sort_keys=True, indent=2)


def load_json_file(json_file):
    with open(json_file) as f:
        json_content = json.loads(f.read())
        return json_content
