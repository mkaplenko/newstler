# -*- coding: utf-8 -*-
"""
Newstler test case project.
Contains django web site as django_facade, business logic and REST django_facade to Linkedin API.
"""
import os

__author_info__ = [
    ("Michael Kaplenko", "mvkaplenko@gmail.com"),
]
__author__ = ", ".join("{} <{}>".format(*info) for info in __author_info__)
__package_info__ = "News by expirience test case"
__package_license__ = "GNU GPL"
__team_email__ = "mvkaplenko@gmail.com"


def _version():
    """Auto-generated module version"""
    try:
        with open(os.path.join(os.path.abspath(os.path.dirname(__file__)), "version.txt"), "r") as versions_file:
            return versions_file.readline()
    except (OSError, IOError):
        return "local"


__version__ = _version()
__all__ = (
    "__author__",
    "__author_info__",
    "__package_info__",
    "__package_license__",
    "__team_email__",
    "__version__",
)
