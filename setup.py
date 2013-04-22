from setuptools import setup, find_packages

config = {
    'name': 'WebCronMon',
    'description': 'Webcron.org Site Monitor',
    'long_description': open('README.md').read(),
    'author': 'Seantis GmbH',
    'url': 'https://pypi.python.org/pypi/webcronmon',
    'author_email': 'info@seantis.ch',
    'version': '1.0',
    'packages': find_packages(),
    'platforms': 'any',
    'license': 'MIT',
    'install_requires': [
        'requests',
        'Flask',
        'lxml',
        'pytz',
        'python_dateutil',
        'Flask_Cache'
    ],
    'entry_points': {
        'console_scripts': [
            'init-webcronmon = webcronmon.scripts:init',
            'run-webcronmon = webcronmon.scripts:run'
        ]
    },
    'classifiers': [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content'
    ],
}

setup(**config)
