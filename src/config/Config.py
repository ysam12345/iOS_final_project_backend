import configparser
import os
import json

class Config:
    def __init__(self):
        self._config = configparser.ConfigParser()
        self._file_root = os.path.dirname(__file__)

    def get_key(self, section, key):

        path = os.path.join(self._file_root, 'key.conf')
        self._config.read(path)
        return json.loads(self._config.get(section, key))

    def get_db(self, section, key):
        path = os.path.join(self._file_root, 'db.conf')
        self._config.read(path)
        return json.loads(self._config.get(section, key))