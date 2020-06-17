from pathlib import Path
from setuptools import setup, find_packages


PROJECT_ROOT = Path(__file__).resolve().parent
with PROJECT_ROOT.joinpath('requirements.txt').open(mode='r', encoding='utf-8') as fd:
    installation_dependencies = [i.strip() for i in fd.readlines()]

with PROJECT_ROOT.joinpath('README.md').open(mode='r', encoding='utf-8') as fd:
    long_description = fd.read()

setup(
    name='OpenPredictionService',
    version='2020.6.10.dev0',
    description='A simple ML model hosting service for rule based systems',
    url='https://github.ibm.com/dba/ads-ml-service',
    packages=find_packages(where='src'),
    install_requires=installation_dependencies,
    long_description=long_description,
    long_description_content_type='text/markdown',
    zip_safe=True
)
