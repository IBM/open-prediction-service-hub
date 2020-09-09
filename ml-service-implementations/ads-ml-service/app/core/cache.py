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
import kfserving
import sqlalchemy.orm as saorm

import app.core.kfserving_impl as kfserving_impl
import app.core.supported_lib as supported_lib
import app.crud as crud
import app.models as models


def _deserialize(db_obj: models.BinaryMlModel) -> kfserving.KFModel:
    model: kfserving.KFModel
    if db_obj.library == supported_lib.MlLib.SKLearn:
        model = kfserving_impl.SKLearnModelImpl(
            predictor_binary=joblib.load(io.BytesIO(db_obj.model_b64))
        )
    elif db_obj.library == supported_lib.MlLib.XGBoost:
        model = kfserving_impl.XGBoostModelImpl(
            predictor_binary=bytearray(db_obj.model_b64)
        )
    else:
        raise RuntimeError(f'ML library not supported: {db_obj.library}')
    model.load()
    return model


class ModelCache(object):
    def __init__(self, max_len: int, max_age_seconds: int):
        self.__cache_lock__ = threading.Lock()
        self.__cache__: typing.OrderedDict[int, kfserving.KFModel] = expiringdict.ExpiringDict(
            max_len=max_len,
            max_age_seconds=max_age_seconds
        )

    def get_deserialized_model(self, db: saorm.Session, endpoint_id: int) -> typing.Optional[kfserving.KFModel]:
        with self.__cache_lock__:
            try:
                m = self.__cache__[endpoint_id]
                return m
            except KeyError:
                archive = crud.binary_ml_model.get_by_endpoint(db, endpoint_id=endpoint_id)
                if not archive:
                    return None
                deserialized = _deserialize(db_obj=archive)
                self.__cache__[endpoint_id] = deserialized
                return deserialized


cache = ModelCache(max_len=64, max_age_seconds=60)
