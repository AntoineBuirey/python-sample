import os
import tempfile
import pytest
from config.config import EnvConfig


def test_load_env_file(tmp_path):
    file_path = tmp_path / ".env"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("# comment\nKEY=VALUE\nOTHER='quoted'\nexport NOQUOTES=123\n")

    cfg = EnvConfig(str(file_path))
    assert cfg._config["KEY"] == "VALUE"
    assert cfg._config["OTHER"] == "quoted"
    assert cfg._config["NOQUOTES"] == "123"


def test_env_save_and_reload(tmp_path):
    file_path = tmp_path / ".env2"
    cfg = EnvConfig(str(file_path))
    cfg._config = {"A": "1", "B": "two"}
    cfg._save()

    cfg2 = EnvConfig(str(file_path))
    assert cfg2._config == {"A": "1", "B": "two"}
