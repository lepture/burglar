#!/usr/bin/env python
# coding: utf-8

import re
from setuptools import setup

try:
    import multiprocessing
except ImportError:
    pass


def fread(filepath):
    with open(filepath, 'r') as f:
        return f.read()


def version():
    content = fread('burglar/__init__.py')
    pattern = r"__version__ = '([0-9\.]*)'"
    m = re.findall(pattern, content)
    return m[0]


install_requires = [
    'requests',
    'lxml',
]


setup(
    name='burglar',
    version=version(),
    url='https://github.com/lepture/burglar',
    author='Hsiaoming Yang',
    author_email='me@lepture.com',
    description='Publish weixin, zhihu daily, zhihu zhuanlan into feeds.',
    long_description=fread('README.rst'),
    license='BSD',
    packages=['burglar'],
    zip_safe=False,
    platforms='any',
    install_requires=install_requires,
    tests_require=['nose'],
    test_suite='nose.collector',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
