import os
import pytest
from unittest.mock import patch, mock_open
import builtins
import tempfile


# raise a ImportError for "import gamuLogger"
base_import = builtins.__import__
def mock_import(name, globals=None, locals=None, fromlist=(), level=0):
    if name == "gamuLogger":
        raise ImportError("Mocked ImportError for gamuLogger")
    return base_import(name, globals, locals, fromlist, level)
builtins.__import__ = mock_import

from config.config.config import FileConfig

class DummyFileConfig(FileConfig):
    """
    Dummy implementation of FileConfig for testing purposes.
    """
    def _to_string(self) -> str:
        return str(self._config)

    def _from_string(self, config_string: str) -> None:
        self._config = eval(config_string)


class TestFileConfig:
    @pytest.fixture
    def file_config(self):
        with tempfile.NamedTemporaryFile(delete=False, mode="w+") as temp_file:
            temp_file.write('{"key": "value"}')
            temp_file_path = temp_file.name
        config = DummyFileConfig(temp_file_path)
        yield config
        os.remove(temp_file_path)

    def test_get(self, file_config : DummyFileConfig):
        assert file_config.get('key') == 'value'
        assert file_config.get('non_existent_key', default='default_value') == 'default_value'

    def test_set(self, file_config : DummyFileConfig):
        file_config.set('new_key', 'new_value')
        assert file_config.get('new_key') == 'new_value'

    def test_remove(self, file_config : DummyFileConfig):
        file_config.set('key_to_remove', 'value')
        file_config.remove('key_to_remove')
        assert file_config.get('key_to_remove', default='default_value') == 'default_value'

    def test_str(self, file_config : DummyFileConfig):
        assert str(file_config) == "{'key': 'value'}"
        
    def test_repr(self, file_config : DummyFileConfig):
        assert repr(file_config) == f"DummyFileConfig({file_config._config})"