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


import io
import threading
import typing

import expiringdict
import joblib
import sqlalchemy.orm as saorm

import app.core.configuration as conf
import app.crud as crud


class BinaryCache(object):
    def __init__(self):
        self.__binary_cache_lock__ = threading.Lock()
        self.__binary_cache__: typing.OrderedDict[int, object] = expiringdict.ExpiringDict(
            max_len=conf.get_config().MODEL_CACHE_SIZE,
            max_age_seconds=conf.get_config().CACHE_TTL
        )

    def get_deserialized_model(self, db: saorm.Session, endpoint_id: int) -> typing.Optional[object]:
        with self.__binary_cache_lock__:
            try:
                m = self.__binary_cache__[endpoint_id]
                return m
            except KeyError:
                archive = crud.binary_ml_model.get_by_endpoint(db, endpoint_id=endpoint_id)
                if not archive:
                    return None
                deserialized = joblib.load(io.BytesIO(archive.model_b64))
                self.__binary_cache__[endpoint_id] = deserialized
                return deserialized
