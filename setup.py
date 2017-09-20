#!/usr/bin/env python3
"""A setuptools to install the script"""

from setuptools import setup

setup(
    # Name of the script as it will appear in /usr/bin.
    name='gpxprocessor',

    # Current version of the script.
    version='0.1.0',

    # Author details.
    author='Konrad Dryja',
    author_email='k.dryja.15@aberdeen.ac.uk',

    # Packages that will be installed.
    packages=['gpxprocessor'],

    # Install all required packages.
    install_requires=['argparse', 'lxml'],

    # Required Python3 or above.
    python_requires='>=3',

    # Repository URL.
    url='https://github.com/devon96/GPXProcessor',  # use the URL to the github repo

    # Main entrypoint to the script.
    entry_points={
        'console_scripts': ['gpxprocessor = gpxprocessor.processor:main']})