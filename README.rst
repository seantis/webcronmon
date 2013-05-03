
WebCronMon 
==========

Shows websites monitored on `Webcron.org`_ in kiosk mode.

At `Seantis`_ we use `Webcron.org`_ to monitor our sites. For our customers, as well as for our office monitor screen, we wanted a simple auto-refreshing page that shows the status of our sites at a glance. We therefore wrote this small `Flask`_ application looking like this:

.. image:: https://github.com/seantis/webcronmon/raw/master/screenshots/desktop.png
.. image:: https://github.com/seantis/webcronmon/raw/master/screenshots/mobile.png

The monitor only shows the bare minimum of information to keep things simple:

* list monitors by group
* link the monitors to the actual website
* show the current state (online / offline since)
* show the uptime of the last 30 days

The site will update the list every 60 seconds by default, unless configured otherwise or unless the timer on the upper right is toggled with a mouse-click.

Demo
----

http://monitor.seantis.ch

Requirements
------------

-  Python 2.7

Installation
------------

Create a new folder::

    mkdir webcronmon

Open it::
    
    cd webcronmon

Initialize a virtual environment::

    virtualenv --no-site-packages -p python2.7 .

Install webcronmon::

    pip install webcronmon

Initialize the configuration::

    init-webcronmon

Configuration
-------------

Before you run webcronmon you need to edit the config.ini file created by ``init-webcronmon``. At the least you need to enter your webcron API credentials, but there are other configuration entries you might wish to adjust.

All the configuration options are described in the config.ini that was created for you.

Running
-------

To start webcronmon simply execute ``run-webcronmon`` in the folder in which you have edited your config.ini

Deployment
----------

We recommend to only run one webcronmon instance and offer it through a reverse proxy. Personally we use `Circus`_ by Mozilla with the following circus.ini::

    [watcher:webcronmon]
    gid = webcronmon
    uid = webcronmon
    cmd = /home/webcronmon/app/bin/run-webcronmon
    virtualenv = /home/webcronmon/app
    working_dir = /home/webcronmon/app
    numprocesses = 1
    singleton = True
    copy_env = True

As a reverse proxy we use Nginx as follows::

    server {
        server_name monitor.seantis.ch;

        listen      80;

        location / {
            proxy_pass http://localhost:8081;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_redirect off;
        }
    }

Copyright
---------

`Seantis GmbH`_

License
-------

MIT

History
-------

1.0.1
~~~~~
 - Fixes the app crashing when a monitor reports an offline server

1.0
~~~

 - Initial Release

.. _`Webcron.org`: https://www.webcron.org
.. _`Seantis GmbH`: http://www.seantis.ch
.. _`Seantis`: http://www.seantis.ch
.. _`Flask`: http://flask.pocoo.org
.. _`Circus`: http://circus.readthedocs.org
