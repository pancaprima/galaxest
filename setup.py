# encoding: utf-8

from setuptools import setup, find_packages, Command
import sys
import os
import re
import ast

setup(
    name='galaxest',
    version='0.0.2',
    description="Run test from anywhere to anywhere in the galaxy",
    long_description="""No long description yet""",
    classifiers=[
        "Programming Language :: Python :: 2.7",
    ],
    keywords='',
    author='Fernanda Panca Prima',
    author_email='pancaprima8@gmail.com',
    url='',
    license='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=["requests","tweak", "inquirer"],
    entry_points={
        'console_scripts': [
            'galaxest = galaxest.main:main',
        ]
    },
)
