from setuptools import setup, find_packages
from os import path


PROJECT_ROOT = path.dirname(path.abspath(__file__))
installation_dependencies = [i.strip() for i in open(path.join(PROJECT_ROOT, 'requirements.txt')).readlines()]


with open(path.join(PROJECT_ROOT, 'README.md'), encoding='utf-8') as fd:
    long_description = fd.read()


setup(
    name='ml-local-provider',
    version='2020.2.24.dev1',
    description='ML service for ADS',
    author='Ke Li',
    author_email='Ke.Li1@ibm.com',
    url='https://github.ibm.com/dba/ads-ml-service',
    # Setting the distribution root. Empty package name stands for the root package
    # The Distutils will take care of converting this platform-neutral representation into whatever is appropriate
    # on your current platform before actually using the pathname.
    package_dir={'': 'src'},
    packages=find_packages('src'),
    install_requires=installation_dependencies,
    long_description=long_description,
    long_description_content_type='text/markdown',
    # To full support Flask, the source file can not be compressed in an .egg
    zip_safe=False
)
