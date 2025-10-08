import pytest
import os
import json
import tempfile
import time
from datetime import datetime, timedelta
from config.config import JSONConfig
from time import sleep


@pytest.fixture
def temp_json_file():
    # Arrange
    with tempfile.NamedTemporaryFile("w+", delete=False, suffix=".json") as f:
        print("{}", file=f)
    yield f.name
    os.remove(f.name)


@pytest.mark.parametrize(
    "initial_data",
    [
        {"foo": "bar"},
        {},
        {"num": 123, "lst": [1, 2, 3]},
    ],
    ids=["load_existing_file", "load_empty_file", "load_complex_file"]
)
def test_load_existing_file(temp_json_file, initial_data):
    # Arrange

    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump(initial_data, f)

    # Act

    config = JSONConfig(temp_json_file)

    # Assert

    assert config._config == initial_data

def test_load_nonexistent_file(tmp_path):
    # Arrange

    file_path = tmp_path / "nonexistent.json"

    # Act

    config = JSONConfig(str(file_path))

    # Assert

    assert config._config == {}
    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        assert json.load(f) == {}

def test_save_and_reload(temp_json_file):
    # Arrange
    # temp_json_file = "/tmp/tmpgtk3j7su.json"
    
    config = JSONConfig(temp_json_file)
    config._config = {"a": 1, "b": 2}
    config._save()

    # Act
    with open(temp_json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Assert

    assert data == {"a": 1, "b": 2}

    # Act
    sleep(0.1)  # Ensure the file modification time changes
    print(r'{"a": 1, "b": 2, "c": 3}', file=open(temp_json_file, mode="w", encoding="utf-8"))

    print(os.path.getmtime(temp_json_file), config._last_modified.timestamp())

    config._reload()

    # Assert

    assert config._config == {"a": 1, "b": 2, "c": 3}

def test_reload_no_change(temp_json_file):
    # Arrange

    config = JSONConfig(temp_json_file)
    config._config = {"foo": "bar"}
    config._save()
    config._last_modified = datetime.now()
    # Simulate no file change
    old_last_modified = config._last_modified

    # Act

    config._reload()

    # Assert

    assert config._last_modified == old_last_modified

def test_reload_file_changed(temp_json_file):
    # Arrange

    config = JSONConfig(temp_json_file)
    config._config = {"foo": "bar"}
    config._save()
    # Simulate file change by updating mtime
    time.sleep(0.01)
    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump({"foo": "baz"}, f)
    os.utime(temp_json_file, None)
    config._last_modified = datetime.now() - timedelta(seconds=1)

    # Act

    config._reload()

    # Assert

    assert config._config == {"foo": "baz"}

def test_reload_nonexistent_file(tmp_path):
    # Arrange

    file_path = tmp_path / "nonexistent_reload.json"

    config = JSONConfig(str(file_path))
    # Remove file after creation
    os.remove(file_path)

    # Act

    config._reload()

    # Assert

    assert config._config == {}
    assert file_path.exists()
    with open(file_path, "r", encoding="utf-8") as f:
        assert json.load(f) == {}

def test_save_sets_last_modified(temp_json_file):
    # Arrange

    config = JSONConfig(temp_json_file)
    config._config = {"x": 42}

    # Act

    config._save()

    # Assert

    assert isinstance(config._last_modified, datetime)
    with open(temp_json_file, "r", encoding="utf-8") as f:
        assert json.load(f) == {"x": 42}

def test_load_invalid_json(temp_json_file):
    # Arrange

    with open(temp_json_file, "w", encoding="utf-8") as f:
        f.write("{invalid json}")

    # Act & Assert

    with pytest.raises(json.JSONDecodeError):
        JSONConfig(temp_json_file)

def test_load_json_list(temp_json_file):
    # Arrange

    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump([1, 2, 3], f)

    # Act
    with pytest.raises(ValueError):
        JSONConfig(temp_json_file)


def test_json_schema_validation_success(temp_json_file, monkeypatch):
    # Arrange
    schema = {
        "type": "object",
        "properties": {
            "foo": {"type": "string"}
        },
        "required": ["foo"]
    }

    content = {"$schema": "http://example.com/schema", "foo": "bar"}
    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump(content, f)

    class DummyResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return schema

    monkeypatch.setattr("requests.get", lambda url: DummyResponse())

    # Act / Assert - should not raise
    JSONConfig(temp_json_file)


def test_json_schema_fetch_failure(temp_json_file, monkeypatch):
    # Arrange
    content = {"$schema": "http://example.com/schema", "foo": "bar"}
    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump(content, f)

    def raise_exc(url):
        raise Exception("network error")

    monkeypatch.setattr("requests.get", raise_exc)

    # Act / Assert
    with pytest.raises(ValueError) as exc:
        JSONConfig(temp_json_file)
    assert "An error occurred during schema validation" in str(exc.value)


def test_json_schema_validation_failure(temp_json_file, monkeypatch):
    # Arrange: schema requires foo to be integer but file has string
    schema = {
        "type": "object",
        "properties": {
            "foo": {"type": "integer"}
        },
        "required": ["foo"]
    }

    content = {"$schema": "http://example.com/schema", "foo": "not-an-int"}
    with open(temp_json_file, "w", encoding="utf-8") as f:
        json.dump(content, f)

    class DummyResponse:
        def raise_for_status(self):
            return None

        def json(self):
            return schema

    monkeypatch.setattr("requests.get", lambda url: DummyResponse())

    # Act / Assert - validation should fail and raise ValueError
    with pytest.raises(ValueError) as exc:
        JSONConfig(temp_json_file)
    assert "Configuration validation against schema failed" in str(exc.value)


def test_require_validation_without_schema(tmp_path):
    # Arrange
    file_path = tmp_path / "no_schema.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump({"foo": "bar"}, f)

    # Act / Assert
    with pytest.raises(ValueError) as exc:
        JSONConfig(str(file_path), True)
    assert "JSON schema validation is required but no '$schema' key found in configuration" in str(exc.value)


