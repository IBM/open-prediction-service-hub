# coding: utf-8

from setuptools import setup, find_packages

NAME = "openapi_server"
VERSION = "2.6.2"
# To install the library, run the following
#
# python setup.py install
#
# prerequisite: setuptools
# http://pypi.python.org/pypi/setuptools

REQUIRES = ["connexion[swagger-ui]"]

setup(
    name=NAME,
    version=VERSION,
    description="Open Prediction Service",
    author_email="",
    url="",
    keywords=["Openapi", "Open Prediction Service"],
    install_requires=REQUIRES,
    packages=find_packages(),
    package_data={'': ['openapi/openapi.yaml']},
    include_package_data=True,
    entry_points={
        'console_scripts': ['openapi_server=openapi.__main__:main']},
    long_description="""\
    The Open Prediction Service API is an effort to provide an Open API that enables unsupported native ML Providers in Decision Designer or Decision Runtime.
    """
)
