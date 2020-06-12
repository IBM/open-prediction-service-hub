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
    # Setting the distribution root. Empty package name stands for the root package
    # The Distutils will take care of converting this platform-neutral representation into whatever is appropriate
    # on your current platform before actually using the pathname.
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=installation_dependencies,
    long_description=long_description,
    long_description_content_type='text/markdown',
    zip_safe=True
)
