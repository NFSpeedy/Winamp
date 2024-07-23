import os
from pathlib import Path
import json
from typing import Any


class Singleton:
    _instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instances[cls]

class Config(Singleton):
    def __init__(self):
        self.base_path = Path(os.getcwd())
        self.config_file = self.base_path / 'winamp.json'
        self.load_config()

    def load_config(self):
        """
        Load the config file
        """
        if not self.config_file.exists():
            with open(self.config_file, 'w') as f:
                json.dump({}, f)
        else:
            with open(self.config_file, 'r') as f:
                self.__dict__.update(json.load(f))

    def reload_config(self):
        """
        Clean the exisitng config and reload it from the file
        """
        self.__dict__.clear()
        self.load_config()

    def read_config(self, key: str|int):
        """
        Read a config value
        """
        self.save_config()
        return self.__dict__.get(key)

    def add_config(self, key: str|int, value: Any):
        """
        Add a new config value

        Args:
            key: str: Key of the config
            value: Any: Value of the config
        """
        self.__dict__[key] = value
        self.save_config()

    def remove_config(self, key: str|int):
        """
        Remove a config value

        Args:
            key: str: Key of the config
        """
        del self.__dict__[key]
        self.save_config()

    def save_config(self):
        """
        Save the config to the file
        """
        with open(self.config_file, 'w') as f:
            json.dump(self.__dict__, f)

    def __str__(self):
        return f"WinaAmp Config: {self.config_file.absolute()}"

    def __repr__(self):
        return f"<WinAmp Config: {self.config_file.absolute()}>"

    def __getitem__(self, key: str|int):
        return self.read_config(key)

    def __setitem__(self, key: str|int, value: Any):
        self.add_config(key, value)

    def __delitem__(self, key: str|int):
        self.remove_config(key)

    def __iter__(self):
        raise NotImplementedError("Config object is not iterable")

    def __len__(self):
        return len(self.__dict__)

    def __contains__(self, key: str|int):
        return key in self.__dict__


settings = Config()