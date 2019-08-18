# encoding: utf-8

from setuptools import setup, find_packages, Command
import sys
import os
import re
import ast

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md')) as f:
    long_description = f.read()

setup(
    name='galaxest',
    version='0.0.7',
    description="Run test from anywhere to anywhere in the galaxy",
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Fernanda Panca Prima',
    author_email='pancaprima8@gmail.com',
    url='https://github.com/pancaprima/galaxest',
    license='MIT',
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["requests","tweak", "inquirer", "enum"],
    entry_points={
        'console_scripts': [
            'galaxest = galaxest.main:main',
        ]
    },
)
