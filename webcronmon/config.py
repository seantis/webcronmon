import os.path
import ConfigParser
import logging.config

from collections import namedtuple

integer_values = (
    'port',
    'auto_refresh',
    'cache_threshold',
    'list_monitors',
    'list_monitor_states',
    'list_monitor_uptimes'
)
boolean_values = ('debug', )


class Config(object):

    def __init__(self, config, section):

        values = dict(_parse_options(k, v) for k, v in config.items(section))

        for key, value in values.items():
            setattr(self, key, value)

        self.as_dictionary = values

    def __iter__(self):
        return self.as_dictionary.values().__iter__()


def _parse_options(key, value):
    if key in integer_values:
        value = int(value)
    elif key in boolean_values:
        value = not (value == '0' or value.lower() == 'false')

    if key.startswith('cache_'):
        key = key.upper()

    return key, value


def _parse_routes(config):
    for route, groups in config.items('routes'):

        assert route.startswith('/'), """
            Route must start with a '/'
        """

        groups = groups.strip().decode('utf-8')

        if groups == '*':
            yield route, groups
        else:
            yield route, [g.strip() for g in groups.split(',')]


def load():
    assert os.path.exists('config.ini'), """
        It seems like config.ini does not exist. Did you run init-webcronmon
        in your current directory?
    """

    logging.config.fileConfig('config.ini')

    config = ConfigParser.SafeConfigParser()
    config.read('config.ini')

    ActiveConfig = namedtuple(
        'ActiveConfig', ['credentials', 'app', 'cache', 'api_cache', 'routes']
    )

    return ActiveConfig(
        Config(config, 'credentials'),
        Config(config, 'app'),
        Config(config, 'cache'),
        Config(config, 'api_cache'),
        list(_parse_routes(config))
    )
