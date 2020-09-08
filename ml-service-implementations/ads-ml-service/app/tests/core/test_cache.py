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


import fastapi.testclient as tstc
import sqlalchemy.orm as saorm

import app.core.cache as ops_cache
import app.models as models


def test_cache(
        db: saorm.Session,
        client: tstc.TestClient,
        endpoint_with_model_and_binary: models.Endpoint,
        classification_predictor: object
):
    binary_cache = ops_cache.BinaryCache()
    obj = binary_cache.get_deserialized_model(db, endpoint_with_model_and_binary.id)

    assert isinstance(obj, type(classification_predictor))


def test_cache_binary_not_exist(
        db: saorm.Session,
        client: tstc.TestClient,
        endpoint_with_model_and_binary: models.Endpoint,
        classification_predictor: object
):
    binary_cache = ops_cache.BinaryCache()
    obj = binary_cache.get_deserialized_model(db, endpoint_with_model_and_binary.id + 1)

    assert obj is None
