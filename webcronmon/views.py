#!/bin/python

from itertools import groupby
from flask import render_template
from dateutil.tz import tzoffset
from dateutil.tz import tzlocal
from datetime import datetime
from dateutil.relativedelta import relativedelta

from webcronmon import api

server_tz = tzoffset('server-timezone', api.utc_offset() * 3600)
local_tz = tzlocal()


class AttributeDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__


def parse_server_time(timestr):
    return datetime.strptime(
        timestr, '%Y-%m-%d %H:%M:%S'
    ).replace(tzinfo=server_tz)


def current_local_time():
    return datetime.now().replace(tzinfo=local_tz)


def human_timedelta(delta):
    # http://code.activestate.com/recipes/
    # 578113-human-readable-format-for-a-given-time-delta/#c3
    attrs = ['years', 'months', 'days', 'hours', 'minutes', 'seconds']
    func = lambda d: [
        '%d %s' % (
            getattr(d, attr), getattr(d, attr) > 1 and attr or attr[:-1]
        ) for attr in attrs if getattr(d, attr)
    ]

    return func(relativedelta(seconds=delta.total_seconds()))


def state_by_monitor():
    """ Return state and optional 'since' timestamp keyed by monitor id.
    The timestamp is onlygiven by the server if the state is 'error'.

    """
    by_id = {}

    for monitor in api.list_monitor_states():
        by_id[monitor.get('id')] = (monitor.get('state'), monitor.get('since'))

    return by_id


def uptime_by_monitor():
    """ Return uptime of the last 30 days by monitor_id. """
    by_id = {}

    for monitor_id, uptime in api.list_monitor_uptimes():
        by_id[monitor_id] = uptime

    return by_id


def active_monitors():
    return [m for m in api.list_monitors() if m.get('status') == '1']


def all_monitors():
    """ Return the monitor data to be displayed on the site, grouped by their
    group defined on webcron.org

    """

    groupkey = lambda m: m.group

    active = sorted(active_monitors(), key=groupkey)

    monitor_states = state_by_monitor()
    monitor_uptimes = uptime_by_monitor()

    def monitor_data(monitor):
        """ Return the data of one monitor as namedtuple (allows for sorting
        using Jinja2)."""

        monitor_id = monitor.get('id')
        state, since = monitor_states[monitor_id]
        uptime = monitor_uptimes[monitor_id]

        if 'http' in monitor.url.text:
            url = monitor.url.text
        else:
            url = monitor.url.get('protocol') + '://' + monitor.url.text

        if state == 'ok':
            status_text = 'Online'
        else:
            status_text = 'Offline for {}'.format(
                ', '.join(human_timedelta(
                    current_local_time() - parse_server_time(since)
                ))
            )

        return dict(
            name=monitor.name,
            state=state,
            uptime=uptime,
            url=url,
            status_text=status_text
        )

    in_groups = {}

    for group, monitors in groupby(active, key=groupkey):
        in_groups[group] = sorted(
            (monitor_data(m) for m in monitors), key=lambda m: m['name']
        )

    return in_groups


def get_clickable_groups(config):
    """ Returns a dictionary of group => link for groups which have an
    associated route. If the group is part of multiple routes the last
    defined route is used.

    """
    clickable = {}

    for route, groups in config.routes:
        if isinstance(groups, basestring):
            continue

        for group in groups:
            clickable[group] = route

    return clickable


def show_monitors(config, shown_groups='*'):

    if shown_groups == '*':
        shown_monitors = all_monitors().items()
    else:
        shown_monitors = (
            (g, m) for g, m in all_monitors().items() if g in shown_groups
        )

    return render_template(
        'index.html',
        monitors=shown_monitors,
        config=config,
        clickable_groups=get_clickable_groups(config)
    )
