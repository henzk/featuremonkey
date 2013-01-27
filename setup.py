#! /usr/bin/env python

import os

DEPS = []
try:
    import importlib
except ImportError:
    DEPS += ['importlib']

try:
    from setuptools import setup
    extra = {
        'install_requires' : DEPS
    }
except ImportError:
    from distutils.core import setup
    extra = {
        'dependencies' : DEPS
    }

def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname)).read()
    except IOError:
        return ''

setup(
    name='featuremonkey',
    version='0.2.0',
    description='FOP for Python',
    long_description=read('README.rst'),
    url='http://github.com/henzk/featuremonkey',
    author='Hendrik Speidel',
    author_email='hendrik@schnapptack.de',
    license="MIT License",
    keywords='fop, features, program composition, program synthesis, monkey-patching',
    packages=['featuremonkey', 'featuremonkey.test', 'featuremonkey.test.mock', 'featuremonkey.test.mock.testpackage1'],
    package_dir={'featuremonkey': 'featuremonkey'},
    package_data={'featuremonkey': []},
    include_package_data=True,
    scripts=['bin/test_featuremonkey'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ],
    **extra
)
