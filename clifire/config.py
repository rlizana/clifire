import os

import yaml

from clifire import out


class Config:
    @classmethod
    def get_config(cls, files: list, create: bool = False, **kwargs):
        def path(*args) -> str:
            exapnd_path = os.path.join(
                *(a.replace("~", os.path.expanduser("~")) for a in args)
            )
            return os.path.abspath(exapnd_path)

        for file in files:
            config_file = path(file)
            out.debug(f"Try read config file {config_file}")
            if os.path.exists(config_file):
                out.debug2("Exists, reading...")
                config = Config(config_file=config_file, **kwargs)
                config.read()
                return config
            out.debug2("Not exist")
        if files:
            file = path(files[0])
            config = Config(config_file=config_file, **kwargs)
            if create:
                config.write()
            return config

    def __init__(self, config_file, **kwargs):
        self._config_file = config_file
        self._config_path = os.path.dirname(config_file)
        self.__dict__.update(kwargs)

    def get(self, key, default=None):
        return getattr(self, key, default)

    def __str__(self) -> str:
        return str(self.__dict__)

    def __repr__(self) -> str:
        return self.__str__()

    def _safe_dict(self, data_dict: dict):
        return {k: v for k, v in data_dict.items() if not k.startswith("_")}

    def read(self):
        if not os.path.exists(self._config_file):
            return False
        with open(self._config_file, "r", encoding="utf-8") as file:
            self.__dict__.update(self._safe_dict(yaml.safe_load(file) or {}))
        return True

    def write(self):
        out.debug(f"Write config file {self._config_file}")
        config_dir = os.path.dirname(self._config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        with open(self._config_file, "w", encoding="utf-8") as file:
            yaml.safe_dump(self._safe_dict(self.__dict__), file)
