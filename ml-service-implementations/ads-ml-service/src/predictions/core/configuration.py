#!/usr/bin/env python3
#
# Copyright 2020 IBM
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.IBM Confidential
#


from __future__ import annotations

import os
from functools import lru_cache
from typing import Optional

import yaml
from pydantic import Field, validator, BaseSettings
from pathlib import Path


class ServerConfiguration(BaseSettings):
    """
    Open Prediction Service configuration
    """
    MODEL_STORAGE: Path = Field(..., description='Directory where OPS store ml models')
    MODEL_CACHE_SIZE: int = Field(16, description='The number of ml models cached in service')
    CACHE_TTL: int = Field(20, description='TTL of cache')

    @validator('MODEL_STORAGE', always=True)
    def storage_check(cls: ServerConfiguration, p: Path) -> Path:
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


@lru_cache()
def get_config(config_file: Optional[Path] = None) -> ServerConfiguration:
    return ServerConfiguration() if config_file is None else ServerConfiguration.from_yaml(config_file)

