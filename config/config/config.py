# pylint: disable=line-too-long

"""
Configuration management module.
"""

from json import loads, dumps
from jsonschema import validate, ValidationError
from abc import ABC, abstractmethod
from datetime import datetime
import requests
import re
import os
import tomlkit
from typing import Any, Dict
import configparser
from io import StringIO
import shlex
import yaml

try: # use gamuLogger if available # pragma: no cover
    from gamuLogger import Logger
    Logger.set_module("config")
    def _trace(msg: str) -> None:
        Logger.trace(msg)
except ImportError: # pragma: no cover
    def _trace(msg: str) -> None:
        print(msg)



class BaseConfig:
    """
    Base class for configuration management.
    This class provides methods to manage configuration settings.
    Can be subclassed for specific configuration formats (e.g., JSON, YAML).
    """
    RE_REFERENCE = re.compile(r'\$\{([a-zA-Z0-9_.]+)\}')

    def __init__(self):
        self._config : Dict[str, Any] = {}

    def get(self, key: str, /, default: Any = None, set_if_not_found: bool = False) -> str | int | float | bool:
        """
        Get the value of a configuration key.
        
        :param key: Configuration key.
        :param default: Default value if the key does not exist.
        :return: Configuration value.
        """
        _trace(f"Getting config value for key: {key}")
        key_tokens = key.split('.')
        config = self._config
        for token in key_tokens:
            if token in config:
                config = config[token]
            elif token.isdigit() and 0 <= int(token) < len(config):
                config = config[int(token)]
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
        # elif not isinstance(config, (int, float, bool)):
        #     raise KeyError(f"The provided key '{key}' is not a valid endpoint for a configuration value.")
        _trace(f"Config value for key '{key}': {config}")
        
        if not isinstance(config, (str, int, float, bool)):
            raise KeyError(f"The provided key '{key}' is not a valid endpoint for a configuration value.")
        return config

    def set(self, key: str, value : Any) -> 'BaseConfig':
        """
        Set the value of a configuration key.
        
        :param key: Configuration key.
        :param value: Configuration value.
        """
        _trace(f"Setting config value for key: {key} to {value}")
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
        return self

    def remove(self, key: str) -> 'BaseConfig':
        """
        Remove a configuration key.
        
        :param key: Configuration key.
        """
        _trace(f"Removing config key: {key}")
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

    def __str__(self) -> str:
        """
        String representation of the configuration.
        """
        return str(self._config)

    def __repr__(self) -> str:
        """
        String representation of the configuration.
        """
        return f"{self.__class__.__name__}({self._config})"

    def __items__(self):
        """
        Iterate over the configuration items.

        :return: Iterator over configuration items.
        """
        return self._config.items()

    def __iter__(self):
        """
        Iterate over the configuration keys.

        :return: Iterator over configuration keys.
        """
        return iter(self._config)

    def keys(self):
        """
        Get the configuration keys.

        :return: Configuration keys.
        """
        return self._config.keys()

    def values(self):
        """
        Get the configuration values.

        :return: Configuration values.
        """
        return self._config.values()

    def items(self):
        """
        Get the configuration items.

        :return: Configuration items.
        """
        return self._config.items()

    def __len__(self) -> int:
        """
        Get the number of configuration items.

        :return: Number of configuration items.
        """
        return len(self._config)

    def __getitem__(self, key: str) -> Any:
        """
        Get the value of a configuration key.

        :param key: Configuration key.
        :return: Configuration value.
        """
        return self.get(key)

    def __setitem__(self, key: str, value: Any) -> 'BaseConfig':
        """
        Set the value of a configuration key.

        :param key: Configuration key.
        :param value: Configuration value.
        """
        return self.set(key, value)

    def __delitem__(self, key: str) -> 'BaseConfig':
        """
        Remove a configuration key.

        :param key: Configuration key.
        """
        return self.remove(key)

    def __contains__(self, key: str) -> bool:
        """
        Check if a key exists in the configuration.

        :param key: Configuration key.
        :return: True if the key exists, False otherwise.
        """
        try:
            self.get(key)
            return True
        except KeyError:
            return False

class FileConfig(BaseConfig, ABC):
    """
    File configuration management class.

    Must be subclassed for specific file formats (e.g., JSON, TOML) that implement `_to_string` and `_from_string`.
    """
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._last_modified = datetime.now()
        super().__init__()
        self._load()

    def __init_empty(self) -> 'FileConfig':
        self._config = {}
        self._save()
        return self

    def _load(self) -> 'FileConfig':
        """
        Load configuration from a config file.
        the _from_string method must be implemented in subclasses.
        """
        _trace(f"Loading configuration from {self.file_path}")
        if not os.path.exists(self.file_path):
            return self.__init_empty()
        with open(self.file_path, 'r', encoding="utf-8") as file:
            content = file.read()
            if content.strip() == "":
                _trace(f"Configuration file {self.file_path} is empty, creating empty config")
                return self.__init_empty()
            self._from_string(content)
        return self

    def _reload(self) -> 'FileConfig':
        """
        Reload configuration from a JSON file if the modification time has changed.
        """
        if not os.path.exists(self.file_path):
            self._config = {}
            self._save()
            return self
        file_modified_time = os.path.getmtime(self.file_path) #when the file was last modified
        config_modified_time = self._last_modified.timestamp() #when the config was last modified (this object)
        if file_modified_time > config_modified_time:
            _trace(f"Reloading configuration from {self.file_path} due to modification time change")
            self._load()
            self._last_modified = datetime.fromtimestamp(file_modified_time)
        else:
            _trace(f"Configuration file {self.file_path} has not changed since last load")
        return self

    def _save(self) -> 'FileConfig':
        """
        Save configuration to a JSON file.
        """
        _trace(f"Saving configuration to {self.file_path}")
        with open(self.file_path, 'w', encoding="utf-8") as file:
            file.write(self._to_string())
        self._last_modified = datetime.now()
        return self

    def get(self, key: str, /, default: Any = None, set_if_not_found: bool = False) -> str | int | float | bool:
        """
        Get the value of a configuration key.
        
        :param key: Configuration key.
        :param default: Default value if the key does not exist.
        :return: Configuration value.
        """
        self._reload()
        return super().get(key, default, set_if_not_found)

    def set(self, key: str, value: Any) -> 'FileConfig':
        """
        Set the value of a configuration key.
        
        :param key: Configuration key.
        :param value: Configuration value.
        """
        self._reload()
        super().set(key, value)
        self._save()
        return self

    def remove(self, key: str) -> 'FileConfig':
        """
        Remove a configuration key.
        
        :param key: Configuration key.
        """
        self._reload()
        super().remove(key)
        self._save()
        return self

    @abstractmethod
    def _to_string(self) -> str:
        """
        String representation of the configuration.
        """

    @abstractmethod
    def _from_string(self, config_string: str) -> None:
        """
        Create a configuration object from a string.
        
        :param config_string: Configuration string.
        :return: Configuration object.
        """

class JSONConfig(FileConfig):
    """
    JSON configuration management class.
    This class provides methods to load, save, and manage configuration settings in JSON format.
    """

    def __init__(self, file_path: str, require_validation: bool = False):
        super().__init__(file_path)
        self.__validate(require_validation)

    def _to_string(self) -> str:
        """
        String representation of the configuration in JSON format.
        """
        return dumps(self._config, indent=4)

    def _from_string(self, config_string: str) -> None:
        """
        Create a configuration object from a JSON string.
        
        :param config_string: Configuration string.
        :return: Configuration object.
        """
        self._config = loads(config_string)
        if not isinstance(self._config, dict):
            raise ValueError("Invalid JSON format: expected a dictionary.")

    def __validate(self, required: bool):
        """
        Validate the configuration against a JSON schema if provided in the config.
        The url to the schema must be provided in the "$schema" key of the config (https://json-schema.org/)
        """
        if "$schema" in self._config:
            schema_url = self._config["$schema"]
            try:
                response = requests.get(schema_url)
                response.raise_for_status()
                schema = response.json()
                validate(instance=self._config, schema=schema)
            except requests.RequestException as e:
                raise ValueError(f"Failed to fetch JSON schema from {schema_url}: {e}") from None
            except ValidationError as e:
                raise ValueError(f"Configuration validation against schema failed: {e.message}") from None
            except Exception as e:
                raise ValueError(f"An error occurred during schema validation: {e}") from None
            _trace("Configuration validated successfully against schema.")
        else:
            _trace("No JSON schema provided for validation.")
            if required:
                raise ValueError("JSON schema validation is required but no '$schema' key found in configuration.")

class TOMLConfig(FileConfig):
    """
    TOML configuration management class.
    This class provides methods to load, save, and manage configuration settings in TOML format.
    """

    def _to_string(self) -> str:
        """
        String representation of the configuration in TOML format.
        """
        return tomlkit.dumps(self._config)

    def _from_string(self, config_string: str) -> None:
        """
        Create a configuration object from a TOML string.
        
        :param config_string: Configuration string.
        :return: Configuration object.
        """
        self._config = tomlkit.loads(config_string)


class YAMLConfig(FileConfig):
    """
    YAML configuration management class.
    """
    def _to_string(self) -> str:
        """
        String representation of the configuration in YAML format.
        """
        return yaml.safe_dump(self._config, sort_keys=False)

    def _from_string(self, config_string: str) -> None:
        """
        Create a configuration object from a YAML string.
        """
        loaded = yaml.safe_load(config_string)
        # YAML can produce None for empty documents
        self._config = loaded if isinstance(loaded, dict) and loaded is not None else ({} if loaded is None else loaded)


class INIConfig(FileConfig):
    """
    INI configuration management class using configparser.
    Sections become nested dictionaries.
    """
    def _to_string(self) -> str:
        parser = configparser.RawConfigParser()
        # If there are top-level keys (not nested under a section), put them in DEFAULT
        defaults = {}
        for k, v in list(self._config.items()):
            if isinstance(v, dict):
                parser[k] = {str(kk): str(vv) for kk, vv in v.items()}
            else:
                defaults[k] = str(v)
        if defaults:
            parser.defaults().update({str(k): str(v) for k, v in defaults.items()})
        sio = StringIO()
        parser.write(sio)
        return sio.getvalue()

    def _from_string(self, config_string: str) -> None:
        parser = configparser.RawConfigParser()
        try:
            parser.read_string(config_string)
        except configparser.MissingSectionHeaderError:
            # Treat top-level key=value pairs by prepending a DEFAULT section
            parser.read_string("[DEFAULT]\n" + config_string)
        data: Dict[str, Any] = {}
        # defaults (top-level keys)
        defaults = dict(parser.defaults())
        for k, v in defaults.items():
            data[k] = v
        for section in parser.sections():
            items = dict(parser.items(section))
            data[section] = items
        self._config = data


class EnvConfig(FileConfig):
    """
    .env-style configuration (KEY=VALUE per line).
    """
    def _to_string(self) -> str:
        lines = []
        for k, v in self._config.items():
            lines.append(f"{k}={v}")
        return "\n".join(lines) + ("\n" if lines else "")

    def _from_string(self, config_string: str) -> None:
        data: Dict[str, Any] = {}
        for raw_line in config_string.splitlines():
            line = raw_line.strip()
            if not line or line.startswith('#') or line.startswith(';'):
                continue
            # support export VAR=VAL
            if line.startswith('export '):
                line = line[len('export '):]
            if '=' not in line:
                continue
            key, value = line.split('=', 1)
            key = key.strip()
            value = value.strip()
            # remove surrounding quotes if present
            if (value.startswith('"') and value.endswith('"')) or (value.startswith("'") and value.endswith("'")):
                try:
                    # preserve escaped sequences by using shlex
                    value = shlex.split(value)[0]
                except Exception:
                    value = value[1:-1]
            data[key] = value
        self._config = data

class MemoryConfig(BaseConfig):
    """
    In-memory configuration management class.
    This class provides methods to load, save, and manage configuration settings in memory.
    Does not persist to a file.
    """
    def __init__(self, initial: Dict[str, Any]|None = None):
        super().__init__()
        if initial is not None:
            self._config = initial


def get_config(file_path: str) -> FileConfig:
    """
    Get a configuration object based on the file extension.
    
    :param file_path: Path to the configuration file.
    :return: Configuration object.
    """
    if file_path.lower().endswith('.json'):
        return JSONConfig(file_path)
    if file_path.lower().endswith('.toml'):
        return TOMLConfig(file_path)
    if file_path.lower().endswith(('.yaml', '.yml')):
        return YAMLConfig(file_path)
    if file_path.lower().endswith(('.ini', '.cfg')):
        return INIConfig(file_path)
    if file_path.lower().endswith('.env'):
        return EnvConfig(file_path)
    raise ValueError(f"Unsupported configuration file format: {file_path}")
