#!/usr/bin/env python
# -*- coding: utf-8 -*-
# this module should be Python2-compatible
# see https://docs.python.org/3/distributing/index.html for reference
from setuptools import find_packages, setup

import newstler_site as module

requires = [
    "django==1.11.4",
    "yarl==0.12.0",
    "cached-property==1.3.0",
    "requests==2.18.4",
]


# For future releases for make version by git tag
def next_version(version):
    return version.format_with("{tag}") if version.exact else version.format_with("{tag}.dev{distance}")


setup(
    setup_requires=["setuptools_scm==1.11.1"],
    version="0.0.1",
    name=module.__name__.replace("_", "-"),
    author=module.__author__,
    author_email=module.__team_email__,
    license=module.__package_license__,
    description=module.__package_info__,
    platforms=["all"],
    classifiers=[
        "License :: GNU/GPL",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: HTTP Servers",
        "Topic :: Software Development",
    ],
    long_description=open("README.md").read(),
    packages=find_packages(exclude=("tests*",)),
    include_package_data=True,  # https://setuptools.readthedocs.io/en/latest/setuptools.html#including-data-files
    install_requires=requires,
)
