import os

import yaml
from clifire import out


class Config:
    @classmethod
    def get_config(cls, files: list, create: bool = False, **kwargs):
        def path(*args) -> str:
            expand_path = os.path.join(
                *(a.replace('~', os.path.expanduser('~')) for a in args)
            )
            return os.path.abspath(expand_path)

        if not files:
            return None
        for file in files:
            config_file = path(file)
            out.debug(f'Try read config file {config_file}')
            if os.path.exists(config_file):
                out.debug2('Exists, reading...')
                config = Config(config_file=config_file, **kwargs)
                config.read()
                return config
            out.debug2('Not exist')
        file = path(files[0])
        config = Config(config_file=config_file, **kwargs)
        if create:
            config.write()
        return config

    def __init__(self, config_file, **kwargs):
        self._config_file = config_file
        self._config_path = os.path.dirname(config_file)
        self.__dict__.update(kwargs)

    def query_get(self, query, default=None):
        item = self.__dict__
        for key in query.split('.'):
            if key not in item:
                return default
            item = item[key]
        return item

    def query_set(self, query, value):
        item = self.__dict__
        keys = query.split('.')
        while keys:
            key = keys.pop(0)
            if not keys:
                item[key] = value
                return
            if key not in item:
                raise KeyError(f'{query} not exists')
            item = item[key]

    def query_del(self, query):
        item = self.__dict__
        keys = query.split('.')
        while keys:
            key = keys.pop(0)
            if not keys:
                del item[key]
                return
            if key not in item:
                raise KeyError(f'{query} not exists')
            item = item[key]

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __contains__(self, key):
        return key in self.__dict__

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self) -> str:
        return self.__str__()

    def _safe_dict(self, data_dict: dict):
        return {k: v for k, v in data_dict.items() if not k.startswith('_')}

    def read(self):
        if not os.path.exists(self._config_file):
            return False
        with open(self._config_file, encoding='utf-8') as file:
            self.__dict__.update(self._safe_dict(yaml.safe_load(file) or {}))
        return True

    def write(self):
        out.debug(f'Write config file {self._config_file}')
        config_dir = os.path.dirname(self._config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        with open(self._config_file, 'w', encoding='utf-8') as file:
            yaml.safe_dump(self._safe_dict(self.__dict__), file)
