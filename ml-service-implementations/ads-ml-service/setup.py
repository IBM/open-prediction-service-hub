from pathlib import Path
from typing import Text

from setuptools import setup, find_packages

import re

PROJECT_ROOT = Path(__file__).resolve().parent
with PROJECT_ROOT.joinpath('requirements.txt').open(mode='r', encoding='utf-8') as fd:
    installation_dependencies = [i.strip() for i in fd.readlines()]


def __get_version(init_file: Text) -> Text:
    here: Path = Path(__file__).resolve().parent
    with here.joinpath(init_file).open(mode='r') as fp:
        contents: Text = fp.read()

    for line in contents.splitlines():
        if line.startswith('__version__'):
            result = re.search(pattern=r'([\d.]+).*', string=line)
            if result is not None:
                return result.group(1)
            else:
                raise RuntimeError('Unable to find version string.')


setup(
    version=__get_version('src/predictions/__init__.py'),
    zip_safe=True,
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=installation_dependencies
)
