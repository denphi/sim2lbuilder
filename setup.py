#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function
from glob import glob
from os.path import join as pjoin


from setupbase import (
    create_cmdclass, install_npm, ensure_targets,
    find_packages, combine_commands, ensure_python,
    get_version, HERE
)

from setuptools import setup


# The name of the project
name = 'sim2lbuilder'

# Ensure a valid python version
ensure_python('>=3.3')

# Get our version
version = get_version(pjoin('sim2lbuilder', '_version.py'))

long_description = ""
with open("README.md", "r") as fh:
    long_description = fh.read()

setup_args = {
    'name'            : name,
    'description'     : 'Simtool builder',
    'long_description_content_type' : 'text/markdown',
    'long_description':long_description,
    'version'         : version,
    'scripts'         : glob(pjoin('scripts', '*')),
    'packages'        : find_packages(),
    'data_files'      : [('assets', [
                        ])],
    'author'          : 'nanoHUB',
    'author_email'    : 'denphi@denphi.com',
    'url'             : 'https://github.com/denphi/sim2lbuilder',
    'license'         : 'BSD',
    'platforms'       : "Linux, Mac OS X, Windows",
    'keywords'        : ['IPython'],
    'classifiers'     : [
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Jupyter',
    ],
    'include_package_data' : True,
    'install_requires' : [
        'ipywidgets>=7.5.0',
        'simtool>=0.3.3',
        'ipython>=7.4.0',
        'traitlets>=4.3.2',
        'ipysheet>=0.4.1',
        'Pillow>=7.2'
    ], 
    'extras_require' : {
        'test': [
        ],
        'examples': [
        ],
        'docs': [
        ],
    },
    'entry_points' : {
    },
}

if __name__ == '__main__':
    setup(**setup_args)
