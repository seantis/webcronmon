import os
import os.path

from flask import Flask
app = Flask(__name__)


def get_config_example():
    this_file = os.path.abspath(__file__)
    config_example = this_file.replace(
        os.path.basename(this_file), 'config.ini.example'
    )
    return open(config_example).read()
