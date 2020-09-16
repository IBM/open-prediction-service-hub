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
import secrets
from functools import lru_cache
from pathlib import Path
from typing import Text

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

    DATABASE_NAME: Text = 'EML.db'
    RETRAIN_MODELS: bool = False
    MODEL_CACHE_SIZE: int = 16
    CACHE_TTL: int = 20
    MODEL_STORAGE: Path

    @validator('MODEL_STORAGE')
    def storage_check(cls: ServerConfiguration, p: Path) -> Path:
        if not p.exists() or not p.is_dir():
            raise ValueError(f'{p} is not a directory')
        if not os.access(path=str(p.resolve()), mode=os.R_OK) or not os.access(path=str(p.resolve()), mode=os.W_OK):
            raise PermissionError('R/W permission needed')
        return p


@lru_cache()
def get_config() -> ServerConfiguration:
    return ServerConfiguration()
