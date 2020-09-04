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


import pickle
import typing

import pytest
import sqlalchemy.orm as orm

import app.core.supported_lib as supported_lib
import app.crud as crud
import app.models as models
import app.schemas as schemas
import app.tests.utils.utils as utils


@pytest.fixture()
def binary_create(classification_predictor: object) -> schemas.BinaryMlModelCreate:
    return schemas.BinaryMlModelCreate(
        model_b64=pickle.dumps(classification_predictor),
        library=supported_lib.MlLib.SKLearn
    )


@pytest.fixture
def random_user() -> schemas.UserCreate:
    username = utils.random_string()
    password = utils.random_string()
    return schemas.UserCreate(username=username, password=password)


@pytest.fixture
def model_in_db(
        db: orm.Session, classification_config: typing.Dict[typing.Text, typing.Any]
) -> models.Model:
    return crud.model.create(db, obj_in=schemas.ModelCreate(name=classification_config['name']))


@pytest.fixture
def endpoint_in_db(
        db: orm.Session, model_in_db: models.Model
) -> models.Endpoint:
    return crud.endpoint.create_with_model(
        db, obj_in=schemas.EndpointCreate(name=utils.random_string()), model_id=model_in_db.id
    )
