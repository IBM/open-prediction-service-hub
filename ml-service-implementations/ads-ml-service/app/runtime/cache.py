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

import cachetools
import readerwriterlock.rwlock as rwlock
import sqlalchemy.orm as saorm

import app.crud as crud
import app.runtime.wrapper as runtime_wrapper

LOGGER = logging.getLogger(__name__)


class ModelCache(object):
    def __init__(self, max_len: int, max_age_seconds: int):
        self.__cache_lock__ = rwlock.RWLockRead()
        self.__cache__: cachetools.TTLCache[int, runtime_wrapper.ModelInvocationExecutor] = \
            cachetools.TTLCache(maxsize=max_len, ttl=max_age_seconds)

    def get_deserialized_model(
            self, db: saorm.Session, endpoint_id: int
    ) -> typing.Optional[runtime_wrapper.ModelInvocationExecutor]:
        LOGGER.debug('Loading binary for endpoint id: %s', endpoint_id)
        with self.__cache_lock__.gen_rlock():
            if endpoint_id in self.__cache__:
                LOGGER.debug('Model cache hit')
                return self.__cache__.get(endpoint_id)
        LOGGER.debug('Model cache miss')
        archive = crud.binary_ml_model.get_by_endpoint(db, endpoint_id=endpoint_id)
        if not archive:
            LOGGER.error('Binary not exist', exc_info=True)
            return None
        deserialized = runtime_wrapper.ModelInvocationExecutor(
            model=archive.model_b64,
            input_type=archive.input_data_structure,
            output_type=archive.output_data_structure,
            binary_format=archive.format
        )
        with self.__cache_lock__.gen_wlock():
            # already added by other thread
            if endpoint_id in self.__cache__:
                return self.__cache__[endpoint_id]
            self.__cache__[endpoint_id] = deserialized
            return deserialized

    def clear(self):
        with self.__cache_lock__.gen_wlock():
            self.__cache__.clear()


cache = ModelCache(max_len=64, max_age_seconds=60)
