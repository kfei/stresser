import re
import sys

pkg_file = open("stresser/__init__.py").read()
metadata = dict(re.findall("__([a-z]+)__\s*=\s*'([^']+)'", pkg_file))
description = open('README.md').read()

from setuptools import setup, find_packages

install_requires = []

setup(
    name='stresser',
    description='A large-scale stress testing framework.',
    packages=find_packages(),
    author=metadata['author'],
    author_email=metadata['authoremail'],
    version=metadata['version'],
    url='https://github.com/kfei/stresser',
    license="MIT",
    keywords="stress, test, automation, framework, sikuli",
    long_description=description,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Testing',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
    ],

    install_requires=[
        'setuptools',
        'pika',
        ] + install_requires,

    entry_points={
        'console_scripts': [
            'stress-commander = stresser.commander.cli:main',
            'stress-soldier = stresser.soldier.cli:main'
        ]
    }
)
