import json
import os

resources_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../schema'))


def load_schema(filepath):
    with open(os.path.join(resources_path, filepath)) as file:
        schema = json.load(file)
        return schema
