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

import fastapi.encoders as encoders
import sqlalchemy.orm as orm

import app.crud as crud
import app.schemas as schemas


def test_create_model(db: orm.Session, classification_config: typing.Dict[typing.Text, typing.Any]):
    model_in = schemas.ModelCreate(name=classification_config['name'])
    model = crud.model.create(db, obj_in=model_in)

    assert model is not None
    assert model.name == classification_config['name']


def test_count_models(db: orm.Session, classification_config: typing.Dict[typing.Text, typing.Any]):
    model_in = schemas.ModelCreate(name=classification_config['name'])
    model = crud.model.create(db, obj_in=model_in)

    assert model is not None
    assert crud.model.count(db) == 1


def test_get_model(db: orm.Session, classification_config: typing.Dict[typing.Text, typing.Any]):
    model_in = schemas.ModelCreate(name=classification_config['name'])
    model = crud.model.create(db, obj_in=model_in)
    model_1 = crud.model.get(db, id=model.id)

    assert model_1 is not None
    assert model_1.id == model.id
    assert encoders.jsonable_encoder(model_1) == encoders.jsonable_encoder(model)


def test_get_model_by_name(db: orm.Session, classification_config: typing.Dict[typing.Text, typing.Any]):
    model_in = schemas.ModelCreate(name=classification_config['name'])
    model = crud.model.create(db, obj_in=model_in)
    model_1 = crud.model.get_by_name(db, name=classification_config['name'])

    assert model_1 is not None
    assert model_1.id == model.id
    assert encoders.jsonable_encoder(model_1) == encoders.jsonable_encoder(model)


def test_delete_model(db: orm.Session, classification_config: typing.Dict[typing.Text, typing.Any]):
    model_in = schemas.ModelCreate(name=classification_config['name'])
    model = crud.model.create(db, obj_in=model_in)
    model_1 = crud.model.delete(db, id=model.id)
    model_2 = crud.model.get(db, id=model_1.id)

    assert model_2 is None
    assert model_1.id == model.id
    assert encoders.jsonable_encoder(model_1) == encoders.jsonable_encoder(model)
