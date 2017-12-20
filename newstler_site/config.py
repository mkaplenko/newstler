"""
Defines supported options for all service parameters.
"""
from configparser import ConfigParser
import os

import logging

from django.conf import settings

LOG = logging.getLogger('testlogger')


def define_options() -> ConfigParser:
    options = ConfigParser()
    config_file = os.path.join(settings.BASE_DIR, "config.ini")
    options.read(config_file)
    return options

options = define_options()
