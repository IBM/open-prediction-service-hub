from pathlib import Path
from setuptools import setup, find_packages


PROJECT_ROOT = Path(__file__).resolve().parent
with PROJECT_ROOT.joinpath('requirements.txt').open(mode='r', encoding='utf-8') as fd:
    installation_dependencies = [i.strip() for i in fd.readlines()]

setup(
    zip_safe=True,
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=installation_dependencies
)
