# Author: Marco Cantu Gea
# Clase para obtener las configuraciones de la aplicacion.
# Version 0.0.1

import json
from Storage.LocalStorage import LocalStorage


class Loader:
    _CONFIG_PATH = "config"
    _CONFIG_FILENAME = "config.json"
    _LOCAL_STORAGE = LocalStorage(_CONFIG_PATH)
    _JSON_CONFIG = None

    def __init__(self):
        self.loadConfiguration()

    @classmethod
    def setFileName(cls, fileName):
        if len(fileName) <= 0:
            return ValueError

        cls._CONFIG_FILENAME = fileName

        return cls

    @classmethod
    def loadConfiguration(cls):
        cls._LOCAL_STORAGE.setFileName(cls._CONFIG_FILENAME)

        if not cls._LOCAL_STORAGE.existFile():
            raise NameError("The configuration file was not found")

        json_content = cls._LOCAL_STORAGE.getFileContent()
        cls._JSON_CONFIG = json.loads(json_content)

        return cls

    @classmethod
    def getConfigurations(cls):
        return cls._JSON_CONFIG

    @classmethod
    def getConfig(cls, configName):

        if len(configName) <= 0:
            return None

        try:
            config_found = cls._JSON_CONFIG[configName]
            return config_found
        except TypeError:
            return None
        except ValueError:
            return None

    @staticmethod
    def get_config(configName):
        if len(configName) <= 0:
            return None

        config_loader = Loader()
        return config_loader.getConfig(configName)
