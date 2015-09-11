#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import with_statement
from setuptools import setup

with open("README.md") as f:
    long_description = f.read()

setup(
    name="pyplyr",
    version="0.0.1",
    description="dplyr like method chains for pandas DataFrame.",
    author="airtoxin",
    author_email="airtoxin@icloud.com",
    url="https://github.com/airtoxin/pyplyr",
    py_modules=["pyplyr"],
    include_package_data=True,
    install_requires=[
        "pandas"
    ],
    tests_require=[
        "nose"
    ],
    license="MIT",
    keywords="",
    zip_safe=False,
    classifiers=[]
)
