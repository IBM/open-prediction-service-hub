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
import typing

import cachetools
import fastapi
import joblib
import kfserving
import readerwriterlock.rwlock as rwlock
import sqlalchemy.orm as saorm
import starlette.status as status

import app.core.kfserving_impl as kfserving_impl
import app.core.supported_lib as supported_lib
import app.crud as crud
import app.models as models


def _deserialize(db_obj: models.BinaryMlModel) -> kfserving.KFModel:
    model: kfserving.KFModel
    try:
        if db_obj.library == supported_lib.MlLib.SKLearn:
            model = kfserving_impl.SKLearnModelImpl(
                predictor_binary=joblib.load(io.BytesIO(db_obj.model_b64))
            )
        elif db_obj.library == supported_lib.MlLib.XGBoost:
            model = kfserving_impl.XGBoostModelImpl(
                predictor_binary=bytearray(db_obj.model_b64)
            )
        else:
            raise fastapi.HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'ML library not supported: {db_obj.library}')
    except ImportError:
        raise fastapi.HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Can not deserialize model binary')
    model.load()
    return model


class ModelCache(object):
    def __init__(self, max_len: int, max_age_seconds: int):
        self.__cache_lock__ = rwlock.RWLockFair()
        self.__cache__: cachetools.TTLCache[int, kfserving.KFModel] = \
            cachetools.TTLCache(maxsize=max_len, ttl=max_age_seconds)

    def get_deserialized_model(self, db: saorm.Session, endpoint_id: int) -> typing.Optional[kfserving.KFModel]:
        try:
            with self.__cache_lock__.gen_rlock():
                return self.__cache__[endpoint_id]
        except KeyError:
            with self.__cache_lock__.gen_wlock():
                # already added by other thread
                if endpoint_id in self.__cache__:
                    return self.__cache__[endpoint_id]
                archive = crud.binary_ml_model.get_by_endpoint(db, endpoint_id=endpoint_id)
                if not archive:
                    return None
                deserialized = _deserialize(db_obj=archive)
                self.__cache__[endpoint_id] = deserialized
                return deserialized

    def clear(self):
        with self.__cache_lock__.gen_wlock():
            self.__cache__.clear()


cache = ModelCache(max_len=64, max_age_seconds=60)
