#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name = "s3tools",
    packages = find_packages(),

    entry_points = {
        'console_scripts': [
            's3tools = s3tools.s3tools:main',
            's3slides = s3tools.s3slides:main',
        ],
    }

)
