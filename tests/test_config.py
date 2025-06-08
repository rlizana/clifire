import os
import tempfile

import pytest
import yaml

from clifire import config


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdirname:
        yield tmpdirname


def test_config(temp_dir):
    config_file = os.path.join(temp_dir, "config.yaml")
    test_data = {
        "name": "test",
        "value": 123,
        "list": ["item1", "item2"],
        "_private": "hidden",
    }

    conf = config.Config(config_file=config_file)
    assert not conf.read()

    conf.name = test_data["name"]
    conf.value = test_data["value"]
    conf.list = test_data["list"]
    conf._private = test_data["_private"]
    conf.write()
    assert os.path.exists(config_file)
    with open(config_file, "r", encoding="utf-8") as f:
        saved_data = yaml.safe_load(f)
    assert "name" in saved_data
    assert "_private" not in saved_data

    conf = config.Config(config_file=config_file)
    assert conf.read()
    assert conf.name == test_data["name"]
    assert conf.value == test_data["value"]
    assert conf.list == test_data["list"]
    assert not hasattr(conf, "_private")

    conf = config.Config.get_config(
        files=[config_file, "non_existent.yaml"], create=False
    )
    assert conf.name == test_data["name"]

    new_config_file = os.path.join(temp_dir, "new_folder", "new_config.yaml")
    conf = config.Config.get_config(
        files=[new_config_file], create=True, initial_value="test"
    )
    assert os.path.exists(new_config_file)
    assert conf.initial_value == "test"
    assert conf.get("non_existent", "default") == "default"
    assert str(conf) == repr(conf)
    assert isinstance(str(conf), str)
