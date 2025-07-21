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
    config_file = os.path.join(temp_dir, 'config.yaml')
    test_data = {
        'name': 'test',
        'value': 123,
        'list': ['item1', 'item2'],
        '_private': 'hidden',
    }

    conf = config.Config(config_file=config_file)
    assert not conf.read()

    conf.name = test_data['name']
    conf.value = test_data['value']
    conf.list = test_data['list']
    conf._private = test_data['_private']
    conf.write()
    assert os.path.exists(config_file)
    with open(config_file, encoding='utf-8') as f:
        saved_data = yaml.safe_load(f)
    assert 'name' in saved_data
    assert '_private' not in saved_data

    conf = config.Config(config_file=config_file)
    assert conf.read()
    assert conf.name == test_data['name']
    assert conf.value == test_data['value']
    assert conf.list == test_data['list']
    assert not hasattr(conf, '_private')

    conf = config.Config.get_config(
        files=[config_file, 'non_existent.yaml'], create=False
    )
    assert conf.name == test_data['name']

    new_config_file = os.path.join(temp_dir, 'new_folder', 'new_config.yaml')
    conf = config.Config.get_config(
        files=[new_config_file], create=True, initial_value='test'
    )
    assert os.path.exists(new_config_file)
    assert conf.initial_value == 'test'
    assert conf.get('non_existent', 'default') == 'default'
    assert str(conf) == repr(conf)
    assert isinstance(str(conf), str)

    assert 'new_key' not in conf
    conf['new_key'] = 'new_value'
    assert conf['new_key'] == 'new_value'


def test_config_query(temp_dir):
    config_file = os.path.join(temp_dir, 'config.yaml')
    test_data = {
        'parent': {
            'child_1': {
                'name': 'Rob',
            },
            'name': 'Parent',
        }
    }
    conf = config.Config(config_file=config_file, create=False, **test_data)
    assert conf.query_get('parent.child_1.name') == 'Rob'
    assert conf.query_get('parent.child_2.name', 'Not Exist') == 'Not Exist'
    conf.query_set('parent.child_1.name', 'Changed')
    assert conf.query_get('parent.child_1.name') == 'Changed'
    with pytest.raises(KeyError):
        conf.query_set('parent.child_2.name', 'Changed')
    conf.query_del('parent.child_1.name')
    assert conf.query_get('parent.child_1.name', 'Deleted') == 'Deleted'
    with pytest.raises(KeyError):
        conf.query_del('parent.child_2.name')


def test_config_del(temp_dir):
    config_file = os.path.join(temp_dir, 'config.yaml')
    test_data = {
        'key_1': 1,
        'key_2': 2,
    }
    conf = config.Config(config_file=config_file, create=False, **test_data)
    del conf['key_1']
    assert 'key_1' not in conf
    with pytest.raises(KeyError):
        del conf['key_1']
