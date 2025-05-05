# pylint: disable=line-too-long

"""
Configuration management module.
"""

from json import loads, dump, JSONDecodeError
from abc import ABC, abstractmethod
from datetime import datetime
import re
import os
from typing import Any, Dict

try: # use gamuLogger if available # pragma: no cover
    from gamuLogger import Logger
    Logger.set_module("config")
    def _trace(msg: str) -> None:
        Logger.trace(msg)
except ImportError:
    def _trace(_: str) -> None:
        pass



class BaseConfig(ABC):
    """
    Base class for configuration management.
    This class provides methods to load, save, and manage configuration settings.
    It is designed to be subclassed for specific configuration formats (e.g., JSON, YAML).
    """
    RE_REFERENCE = re.compile(r'^\$\{([a-zA-Z0-9_.]+)\}$')

    def __init__(self):
        self._config : Dict[str, Any] = {}
        self._load()

    @abstractmethod
    def _load(self) -> 'BaseConfig':
        """
        Load configuration
        """

    @abstractmethod
    def _save(self) -> 'BaseConfig':
        """
        Save configuration
        """

    @abstractmethod
    def _reload(self) -> 'BaseConfig':
        """
        Reload configuration
        """

    def get(self, key: str, /, default: Any = None, set_if_not_found: bool = False) -> str | int | float | bool:
        """
        Get the value of a configuration key.
        
        :param key: Configuration key.
        :param default: Default value if the key does not exist.
        :return: Configuration value.
        """
        _trace(f"Getting config value for key: {key}")
        self._reload()
        key_tokens = key.split('.')
        config = self._config
        for token in key_tokens:
            if token in config:
                config = config[token]
            else:
                if default is None:
                    raise KeyError(f"Key '{key}' not found in configuration.")
                if set_if_not_found:
                    self.set(key, default)
                return default
        if isinstance(config, str):
            # Check for reference
            for match in self.RE_REFERENCE.finditer(config):
                ref_key = match.group(1)
                ref_value = self.get(ref_key)
                config = config.replace(match.group(0), str(ref_value))
        elif not isinstance(config, (int, float, bool)):
            raise KeyError(f"The provided key '{key}' is not a valid endpoint for a configuration value.")
        _trace(f"Config value for key '{key}': {config}")
        return config

    def set(self, key: str, value : Any) -> 'BaseConfig':
        """
        Set the value of a configuration key.
        
        :param key: Configuration key.
        :param value: Configuration value.
        """
        _trace(f"Setting config value for key: {key} to {value}")
        self._reload()
        key_tokens = key.split('.')
        config = self._config
        for token in key_tokens[:-1]:
            if token not in config:
                config[token] = {}
            config = config[token]
        try:
            config[key_tokens[-1]] = value
        except TypeError:
            raise TypeError(f"Cannot set value for key '{key}' because key is already a non-dict type.") from None
        self._save()
        return self

    def remove(self, key: str) -> 'BaseConfig':
        """
        Remove a configuration key.
        
        :param key: Configuration key.
        """
        _trace(f"Removing config key: {key}")
        self._reload()
        key_tokens = key.split('.')
        config = self._config
        for token in key_tokens[:-1]:
            if token in config:
                config = config[token]
            else:
                raise KeyError(f"Key '{key}' not found in configuration.")
        if not isinstance(config, (dict, list)):
            raise KeyError(f"Cannot remove key '{key}' because it is not a valid configuration object.")
        if key_tokens[-1] in config:
            del config[key_tokens[-1]]
        else:
            raise KeyError(f"Key '{key}' not found in configuration.")
        return self


class JSONConfig(BaseConfig):
    """
    JSON configuration management class.
    This class provides methods to load, save, and manage configuration settings in JSON format.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._last_modified = None
        super().__init__()

    def _load(self) -> 'JSONConfig':
        """
        Load configuration from a JSON file.
        """
        _trace(f"Loading configuration from {self.file_path}")
        if not os.path.exists(self.file_path):
            self._config = {}
            self._save()
            return self
        with open(self.file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            if content.strip() == "":
                _trace(f"Configuration file {self.file_path} is empty, creating empty config")
                self._config = {}
                self._save()
                return self
            self._config = loads(content)
        return self

    def _reload(self) -> 'JSONConfig':
        """
        Reload configuration from a JSON file if the modification time has changed.
        """
        if not os.path.exists(self.file_path):
            self._config = {}
            self._save()
            return self
        file_modified_time = os.path.getmtime(self.file_path) #when the file was last modified
        config_modified_time = self._last_modified.timestamp() #when the config was last modified (this object)
        if self._last_modified is None or file_modified_time > config_modified_time:
            _trace(f"Reloading configuration from {self.file_path} due to modification time change")
            self._load()
            self._last_modified = datetime.fromtimestamp(file_modified_time)
        else:
            _trace(f"Configuration file {self.file_path} has not changed since last load")
        return self

    def _save(self) -> 'JSONConfig':
        """
        Save configuration to a JSON file.
        """
        _trace(f"Saving configuration to {self.file_path}")
        with open(self.file_path, 'w', encoding="utf-8") as file:
            dump(self._config, file, indent=4)
        self._last_modified = datetime.now()
        return self
