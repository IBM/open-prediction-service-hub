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


import logging
import typing

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.configuration import get_config

logger = logging.getLogger(__name__)


def get_db_url() -> str:
    if get_config().USE_SQLITE:
        logger.info('Using SQLITE database')
        return f'sqlite:///{get_config().MODEL_STORAGE.joinpath(get_config().DATABASE_NAME)}'
    else:
        logger.info('Using customized database')
        return get_config().DB_URL


def get_db_opts() -> typing.Dict[str, typing.Any]:
    if get_config().USE_SQLITE:
        return {'connect_args': {"check_same_thread": False}}
    else:
        return {} if get_config().DB_ARGS is None else get_config().DB_ARGS


def get_engine():
    url = get_db_url()
    db_options = get_db_opts()
    return create_engine(url, **db_options)


SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=get_engine()
)
