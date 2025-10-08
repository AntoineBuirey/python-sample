import os
import tempfile
import pytest
from config.config import INIConfig


def test_load_ini_file(tmp_path):
    file_path = tmp_path / "test.ini"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("[section]\nkey = value\n")

    cfg = INIConfig(str(file_path))
    assert cfg._config["section"]["key"] == "value"


def test_top_level_ini_pairs(tmp_path):
    file_path = tmp_path / "top.ini"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("key1=val1\nkey2=val2\n")

    cfg = INIConfig(str(file_path))
    assert cfg._config["key1"] == "val1"
    assert cfg._config["key2"] == "val2"


def test_save_ini_roundtrip(tmp_path):
    file_path = tmp_path / "out.ini"
    cfg = INIConfig(str(file_path))
    cfg._config = {"section": {"a": "1"}, "global": "v"}
    cfg._save()

    cfg2 = INIConfig(str(file_path))
    assert cfg2._config["section"]["a"] == "1"
    assert cfg2._config["global"] == "v"
