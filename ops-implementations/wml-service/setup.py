# coding: utf-8

import sys
from setuptools import setup, find_packages

NAME = "swagger_server"
VERSION = "2.0.1"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion"]

setup(
    name=NAME,
    version=VERSION,
    description="Open Prediction Service",
    author_email="",
    url="",
    keywords=["Swagger", "Open Prediction Service"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['swagger/swagger.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['swagger_server=swagger_server.__main__:main']},
    long_description="""\
    The Open Prediction Service API is an effort to provide an Open API that enables unsupported native ML Providers in Decision Designer or Decision Runtime.
    """
)
