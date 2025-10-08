import os
import json
import tempfile
import pytest
from config.config import YAMLConfig


def test_load_yaml_file(tmp_path):
    file_path = tmp_path / "test.yaml"
    content = {
        "foo": "bar",
        "nested": {"a": 1}
    }
    with open(file_path, "w", encoding="utf-8") as f:
        import yaml
        yaml.safe_dump(content, f)

    cfg = YAMLConfig(str(file_path))
    assert cfg._config == content


def test_save_and_reload_yaml(tmp_path):
    file_path = tmp_path / "save.yaml"
    cfg = YAMLConfig(str(file_path))
    cfg._config = {"x": 1, "y": {"z": "v"}}
    cfg._save()

    cfg2 = YAMLConfig(str(file_path))
    assert cfg2._config == {"x": 1, "y": {"z": "v"}}


def test_invalid_yaml_raises(tmp_path):
    file_path = tmp_path / "bad.yaml"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("- just: [unclosed")

    with pytest.raises(Exception):
        YAMLConfig(str(file_path))
