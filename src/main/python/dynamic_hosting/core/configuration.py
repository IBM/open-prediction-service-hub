#!/usr/bin/env python3
# Python 3.6+

from __future__ import annotations

import os

import yaml
from pydantic import BaseModel, Field, validator
from pathlib import Path


class ServerConfiguration(BaseModel):
    """
    Embedded machine learning provider configuration
    """
    model_storage: Path = Field(..., description='Directory where the server store ml models')

    @validator('model_storage', always=True)
    def path_check(cls: ServerConfiguration, p: Path) -> Path:
        if not p.exists() or not p.is_dir():
            raise ValueError('{dir} is not a directory'.format(dir=p))
        if not os.access(path=str(p.resolve()), mode=os.R_OK) or not os.access(path=str(p.resolve()), mode=os.W_OK):
            raise PermissionError('R/W permission needed'.format(dir=p))
        return p

    @classmethod
    def from_yaml(cls, conf: Path) -> ServerConfiguration:
        if not conf.exists() or not conf.is_file():
            raise ValueError('{conf} is not a file'.format(conf=conf))
        if not os.access(path=str(conf.resolve()), mode=os.R_OK):
            raise PermissionError('R permission needed'.format(dir=conf))
        with conf.open(mode='r') as fd:
            return ServerConfiguration(**yaml.safe_load(fd))

    @classmethod
    def from_env(cls) -> ServerConfiguration:
        if not os.environ.get('MODEL_STORAGE'):
            raise ValueError('{conf} not exist in env'.format(conf='MODEL_STORAGE'))
        return ServerConfiguration(model_storage=Path(os.environ.get('MODEL_STORAGE')))
