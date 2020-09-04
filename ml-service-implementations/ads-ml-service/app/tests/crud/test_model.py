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


import typing

import sqlalchemy.orm as orm

import app.crud as crud
import app.models as models
import app.schemas as schemas
import app.tests.utils.utils as utils


def test_create_model(db: orm.Session, model_create: schemas.ModelCreate) -> typing.NoReturn:
    model = crud.model.create(db, obj_in=model_create)

    assert model.name == model_create.name


def test_get_model(db: orm.Session, model_create: schemas.ModelCreate) -> typing.NoReturn:
    model = crud.model.create(db, obj_in=model_create)
    model_1 = crud.model.get(db, id=model.id)

    assert model_1.id == model.id
    assert model_1.name == model_create.name


def test_get_model_by_name(db: orm.Session, model_create: schemas.ModelCreate) -> typing.NoReturn:
    model = crud.model.create(db, obj_in=model_create)
    model_1 = crud.model.get_by_name(db, model_create.name)

    assert model_1.id == model.id
    assert model_1.name == model_create.name


def test_delete_model(db: orm.Session, model_create: schemas.ModelCreate) -> typing.NoReturn:
    model = crud.model.create(db, obj_in=model_create)
    model_1 = crud.model.delete(db, id=model.id)
    model_2 = crud.model.get(db, id=model_1.id)

    assert model_2 is None
    assert model_1.id == model.id
    assert model_1.name == model_create.name


def test_cascade_delete_with_config(
        db: orm.Session, model_in_db: models.Endpoint, model_config_create: schemas.ModelConfigCreate
) -> typing.NoReturn:
    config = crud.model_config.create_with_model(db, obj_in=model_config_create, model_id=model_in_db.id)
    crud.model.delete(db, id=model_in_db.id)
    config_1 = crud.model_config.get(db, id=config.id)

    assert config_1 is None


def test_cascade_delete_with_endpoint(db: orm.Session, model_in_db: models.Endpoint) -> typing.NoReturn:
    endpoint = crud.endpoint.create_with_model(
        db, obj_in=schemas.EndpointCreate(name=utils.random_string()), model_id=model_in_db.id
    )
    crud.model.delete(db, id=model_in_db.id)
    endpoint_1 = crud.endpoint.get(db, id=endpoint.id)

    assert endpoint_1 is None
