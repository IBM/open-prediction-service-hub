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


import pytest
import sqlalchemy.orm as orm

import app.crud as crud
import app.models as models
import app.schemas as schemas
import app.tests.predictors.scikit_learn.model as app_test_skl
import app.tests.utils.utils as utils


@pytest.fixture()
def model_create() -> schemas.ModelCreate:
    return schemas.ModelCreate()


@pytest.fixture()
def model_config_create() -> schemas.ModelConfigCreate:
    return schemas.ModelConfigCreate(configuration=app_test_skl.get_conf()['model'])


@pytest.fixture
def random_user() -> schemas.UserCreate:
    username = utils.random_string()
    password = utils.random_string()
    return schemas.UserCreate(username=username, password=password)


@pytest.fixture
def model_in_db(
        db: orm.Session
) -> models.Model:
    return crud.model.create(db, obj_in=schemas.ModelCreate())


@pytest.fixture
def endpoint_in_db(
        db: orm.Session, model_in_db: models.Model
) -> models.Endpoint:
    return crud.endpoint.create_with_model(
        db, obj_in=schemas.EndpointCreate(name=utils.random_string()), model=model_in_db
    )
