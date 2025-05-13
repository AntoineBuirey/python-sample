import pytest
import os
import tomlkit
import tempfile
import time
from datetime import datetime, timedelta
from config.config import TOMLConfig
from time import sleep


@pytest.fixture
def temp_toml_file():
    # Arrange
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".toml") as f:
        f.write("")
    yield f.name
    os.remove(f.name)


def test_load_existing_file(temp_toml_file):
    # Arrange
    initial_data = {"foo": "bar"}
    with open(temp_toml_file, "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps(initial_data))

    # Act
    config = TOMLConfig(temp_toml_file)

    # Assert
    assert config._config == initial_data


def test_load_nonexistent_file(tmp_path):
    # Arrange
    file_path = tmp_path / "nonexistent.toml"

    # Act
    config = TOMLConfig(str(file_path))

    # Assert
    assert config._config == {}
    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        assert tomlkit.loads(f.read()) == {}


def test_save_and_reload(temp_toml_file):
    # Arrange
    config = TOMLConfig(temp_toml_file)
    config._config = {"a": 1, "b": 2}
    config._save()

    # Act
    with open(temp_toml_file, "r", encoding="utf-8") as f:
        data = tomlkit.loads(f.read())

    # Assert
    assert data == {"a": 1, "b": 2}

    # Act
    sleep(0.1)  # Ensure the file modification time changes
    with open(temp_toml_file, "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps({"a": 1, "b": 2, "c": 3}))

    config._reload()

    # Assert
    assert config._config == {"a": 1, "b": 2, "c": 3}


def test_reload_no_change(temp_toml_file):
    # Arrange
    config = TOMLConfig(temp_toml_file)
    config._config = {"foo": "bar"}
    config._save()
    config._last_modified = datetime.now()
    old_last_modified = config._last_modified

    # Act
    config._reload()

    # Assert
    assert config._last_modified == old_last_modified


def test_reload_file_changed(temp_toml_file):
    # Arrange
    config = TOMLConfig(temp_toml_file)
    config._config = {"foo": "bar"}
    config._save()
    time.sleep(0.01)
    with open(temp_toml_file, "w", encoding="utf-8") as f:
        f.write(tomlkit.dumps({"foo": "baz"}))
    os.utime(temp_toml_file, None)
    config._last_modified = datetime.now() - timedelta(seconds=1)

    # Act
    config._reload()

    # Assert
    assert config._config == {"foo": "baz"}


def test_reload_nonexistent_file(tmp_path):
    # Arrange
    file_path = tmp_path / "nonexistent_reload.toml"

    config = TOMLConfig(str(file_path))
    os.remove(file_path)

    # Act
    config._reload()

    # Assert
    assert config._config == {}
    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        assert tomlkit.loads(f.read()) == {}


def test_save_sets_last_modified(temp_toml_file):
    # Arrange
    config = TOMLConfig(temp_toml_file)
    config._config = {"x": 42}

    # Act
    config._save()

    # Assert
    assert isinstance(config._last_modified, datetime)
    with open(temp_toml_file, "r", encoding="utf-8") as f:
        assert tomlkit.loads(f.read()) == {"x": 42}


def test_load_invalid_toml(temp_toml_file):
    # Arrange
    with open(temp_toml_file, "w", encoding="utf-8") as f:
        f.write("invalid_toml = ")

    # Act & Assert
    with pytest.raises(tomlkit.exceptions.TOMLKitError):
        TOMLConfig(temp_toml_file)


@pytest.fixture
def sample_toml_file():
    # Arrange
    content = """
    [section]
    key = "value"
    """
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".toml") as f:
        f.write(content)
    yield f.name
    os.remove(f.name)

def test_load_configuration_from_toml_file(sample_toml_file):
    # Act
    config = TOMLConfig(sample_toml_file)

    # Assert
    assert config._config == {"section": {"key": "value"}}
