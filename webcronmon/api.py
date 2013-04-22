import logging
log = logging.getLogger('webcronmon')

import requests
import functools

from functools import partial
from lxml import objectify

import webcronmon


def get(*args, **kwargs):
    log.info('requesting {}'.format(args[0]))
    return partial(requests.get, auth=requests.auth.HTTPBasicAuth(
        webcronmon.active_config.credentials.username,
        webcronmon.active_config.credentials.password
    ))(*args, **kwargs)


def api_url(function):
    return 'https://api.webcron.org/{}'.format(function)


def objectify_response(result):
    assert result.status_code == 200, """The request failed with the http code
    {}
    """.format(result.status_code)

    return list(
        objectify.fromstring(result.text.encode('utf-8')).iterchildren()
    )


def objectified(fn):

    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        return objectify_response(fn(*args, **kwargs))

    return wrapper


@objectified
def list_monitors():
    return get(api_url('monitor.get'))


@objectified
def list_monitor_states():
    return get(api_url('monitor.state'))


def utc_offset():
    response = objectify_response(get(api_url('time')))
    return int(response[0].get('utc_offset'))


def list_monitor_uptimes():
    uptimes = []

    for monitor in list_monitors():
        monitor_id = monitor.get('id')
        response = objectify_response(get(
            api_url('monitor.uptime') + '/id:{}'.format(monitor_id),
        ))

        uptimes.append((monitor_id, float(response[0].get('percentage'))))

    return uptimes
