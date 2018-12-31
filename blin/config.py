import json
import logging
import os


class _JsonConfig:
    def __init__(self):
        self._conf = \
            json.loads(open(os.path.join(os.path.abspath(os.path.dirname(__file__)), '../config.json'), 'r').read())

    @property
    def log_level(self):
        return logging.getLevelName(self._conf.get('log_level', 'INFO'))

    def __getattr__(self, item):
        return self._conf[item]


class _EnvConfig:

    @property
    def log_level(self):
        return logging.getLevelName(os.environ.get('LOG_LEVEL', 'INFO'))

    @property
    def checkpoints(self):
        return os.environ.get('CHECKPOINTS', '60,30,10,5,4,3,2,1').split(',')

    def __getattr__(self, item):
        return os.environ[item.upper()]


try:
    Config = _JsonConfig()

except FileNotFoundError:
    Config = _EnvConfig()


