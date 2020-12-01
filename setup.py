#!/usr/bin/env python

from setuptools import setup, find_packages
import io, os

# Package meta-data.
NAME= 'twitterUsernameviaUserID'
DESCRIPTION= "An advanced Twitter scraping tool. No authentication. No API. No limits to fetching usernames from the user id's."
URL= 'https://github.com/rishi-raj-jain/twitterUsernamefromUserID'
EMAIL= 'rishi18304@iiitd.ac.in'
AUTHOR= 'Rishi Raj Jain, Dvanne laine'
REQUIRES_PYTHON= '>=3.6.0'
VERSION= None

# What packages are required for this module to be executed?
REQUIRED = [
    'selenium', 'webdriver_manager', NAME
]

here= os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description= '\n' + f.read()

# Load the package's __version__.py
about= {}
if not VERSION:
    with open(os.path.join(here, NAME, '__version__.py')) as f:
        exec(f.read(), about)
else:
    about['__version__']= VERSION

setup(
    name= NAME,
    version= about['__version__'],
    description= DESCRIPTION,
    long_description= long_description,
    long_description_content_type= "text/markdown",
    author= AUTHOR,
    author_email= EMAIL,
    python_requires= REQUIRES_PYTHON,
    url= URL,
    packages= find_packages(include=[NAME+'*']),
    install_requires= REQUIRED,
    license= 'MIT',
    classifiers= [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)