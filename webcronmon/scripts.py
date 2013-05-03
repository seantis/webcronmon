import logging
import os
import os.path

from functools import partial
from flask.ext.cache import Cache


def init():
    """Initializes a directory with the example config.ini."""

    import webcronmon

    working = os.getcwd()
    config_path = os.path.join(working, 'config.ini')

    if os.path.exists(config_path):
        print("config.ini already exists, exiting...")
        return

    with open(os.path.join(working, 'config.ini'), 'w') as config_file:
        config_file.write(webcronmon.get_config_example())

    print ("config.ini was created, please edit before running run-webcronmon")


def run():
    """Runs the flask app using the config.ini found in the working dir."""
    import webcronmon
    import webcronmon.config

    config = webcronmon.active_config = webcronmon.config.load()

    webcronmon.app.debug = config.app.debug
    cache = Cache(config=config.cache.as_dictionary)
    cache.init_app(webcronmon.app)

    import webcronmon.api
    webcronmon.api.list_monitors = cache.cached(
        key_prefix='list_monitors',
        timeout=config.api_cache.list_monitors
    )(webcronmon.api.list_monitors)
    webcronmon.api.list_monitor_states = cache.cached(
        key_prefix='list_monitor_states',
        timeout=config.api_cache.list_monitor_states
    )(webcronmon.api.list_monitor_states)
    webcronmon.api.list_monitor_uptimes = cache.cached(
        key_prefix='list_monitor_uptimes',
        timeout=config.api_cache.list_monitor_uptimes
    )(webcronmon.api.list_monitor_uptimes)

    import webcronmon.views
    for route, shown_groups in config.routes:
        view = partial(
            webcronmon.views.show_monitors,
            config=config,
            shown_groups=shown_groups
        )
        webcronmon.app.add_url_rule(route, route.replace('/', '-'), view)

    # force logging through webcronmon
    webcronmon.app._logger = logging.getLogger('webcronmon')
    webcronmon.app.logger_name = 'webcronmon'

    try:
        webcronmon.app.run(
            host=config.app.host, port=config.app.port, debug=config.app.debug,
        )
    except KeyboardInterrupt:
        pass
