from json import load, dump
from abc import ABC, abstractmethod
import re

class BaseConfig(ABC):
    RE_REFERENCE = re.compile(r'^\$\{([a-zA-Z0-9_.]+)\}$')
    def __init__(self):
        self._config = {}
        
    @abstractmethod
    def load(self, file_path: str):
        """
        Load configuration from a file.
        
        :param file_path: Path to the configuration file.
        """
        pass
    
    @abstractmethod
    def save(self, file_path: str):
        """
        Save configuration to a file.
        
        :param file_path: Path to the configuration file.
        """
        pass
    
    def get(self, key: str):
        """
        Get the value of a configuration key.
        
        :param key: Configuration key.
        :param default: Default value if the key does not exist.
        :return: Configuration value.
        """
        key_tokens = key.split('.')
        config = self._config
        for token in key_tokens:
            if token in config:
                config = config[token]
            else:
                raise KeyError(f"Key '{key}' not found in configuration.")
        if isinstance(config, str):
            # Check for reference
            for match in self.RE_REFERENCE.finditer(config):
                ref_key = match.group(1)
                ref_value = self.get(ref_key)
                config = config.replace(match.group(0), str(ref_value))
        return config
    
    def set(self, key: str, value):
        """
        Set the value of a configuration key.
        
        :param key: Configuration key.
        :param value: Configuration value.
        """
        key_tokens = key.split('.')
        config = self._config
        for token in key_tokens[:-1]:
            if token not in config:
                config[token] = {}
            config = config[token]
        config[key_tokens[-1]] = value
        return self
    
    def remove(self, key: str):
        """
        Remove a configuration key.
        
        :param key: Configuration key.
        """
        key_tokens = key.split('.')
        config = self._config
        for token in key_tokens[:-1]:
            if token in config:
                config = config[token]
            else:
                raise KeyError(f"Key '{key}' not found in configuration.")
        if key_tokens[-1] in config:
            del config[key_tokens[-1]]
        else:
            raise KeyError(f"Key '{key}' not found in configuration.")
        return self

class JSONConfig(BaseConfig):
    def load(self, file_path: str):
        """
        Load configuration from a JSON file.
        
        :param file_path: Path to the JSON configuration file.
        """
        with open(file_path, 'r') as file:
            self._config = load(file)
    
    def save(self, file_path: str):
        """
        Save configuration to a JSON file.
        
        :param file_path: Path to the JSON configuration file.
        """
        with open(file_path, 'w') as file:
            dump(self._config, file, indent=4)
