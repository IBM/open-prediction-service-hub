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

import functools
import os
import secrets
import typing
from pathlib import Path
from typing import Text

import pydantic
from pydantic import validator, BaseSettings


class ServerConfiguration(BaseSettings):
    """
    ads-ml-service configuration
    """
    API_V2_STR: Text = ''

    SECRET_KEY: Text = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 120
    USERNAME_TEST_USER: Text = 'test-user'
    DEFAULT_USER: Text = 'admin'
    DEFAULT_USER_PWD: Text = 'password'

    ADDITIONAL_INFO_FIELD: Text = 'additional'
    DATABASE_NAME: Text = 'db.sqlite'
    LOGGING: typing.Optional[Path] = '/etc/ads-ml-service/logging/logging.yaml'
    RETRAIN_MODELS: bool = False
    MODEL_CACHE_SIZE: int = 64
    CACHE_TTL: int = 60

    USE_SQLITE: bool = True
    MODEL_STORAGE: typing.Optional[Path] = None
    DB_URL: typing.Optional[pydantic.AnyUrl] = None
    # Additional args for sqlalchemy.create_engine()
    DB_ARGS: typing.Optional[pydantic.Json] = None
    UPLOAD_SIZE_LIMIT: int = 0

    @validator('MODEL_STORAGE')
    def storage_check(
            cls, p: typing.Optional[Path], values: typing.Dict[typing.Text, typing.Any]) -> typing.Optional[Path]:
        if values['USE_SQLITE'] and p is None:
            raise ValueError(f'MODEL_STORAGE is None')
        if not p.exists() or not p.is_dir():
            raise ValueError(f'{p} is not a directory')
        if not os.access(path=str(p.resolve()), mode=os.R_OK) or not os.access(path=str(p.resolve()), mode=os.W_OK):
            raise PermissionError('R/W permission needed')
        return p

    @validator('DB_URL')
    def db_url_check(
            cls,
            p: typing.Optional[pydantic.AnyUrl],
            values: typing.Dict[typing.Text, typing.Any]
    ) -> typing.Optional[pydantic.AnyUrl]:
        if not values['USE_SQLITE'] and p is None:
            raise ValueError(f'DB_URL is None')
        return p


@functools.lru_cache()
def get_config() -> ServerConfiguration:
    return ServerConfiguration()
