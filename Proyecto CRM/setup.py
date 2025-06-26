## File: setup.py
# This file is used to package the CRM console application.
from setuptools import setup, find_packages

setup(
    name="crm_console",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[],
    entry_points={
        "console_scripts": [
            "crm=main:main"
        ]
    },
)
