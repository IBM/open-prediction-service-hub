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
import app.models as models
import app.schemas as schemas


def test_create_model_config(
        db: orm.Session, model_config_create: schemas.ModelConfigCreate, model_in_db: models.Model
) -> typing.NoReturn:
    config = crud.model_config.create_with_model(db, obj_in=model_config_create, model_id=model_in_db.id)

    assert config.model_id == model_in_db.id
    assert encoders.jsonable_encoder(config.configuration) == \
           encoders.jsonable_encoder(model_config_create.configuration)


def test_get_model_config(
        db: orm.Session, model_config_create: schemas.ModelConfigCreate, model_in_db: models.Model
) -> typing.NoReturn:
    config = crud.model_config.create_with_model(db, obj_in=model_config_create, model_id=model_in_db.id)
    config_1 = crud.model_config.get(db, id=config.id)

    assert config_1.id == config.id
    assert config_1.model_id == model_in_db.id
    assert encoders.jsonable_encoder(config_1.configuration) == \
           encoders.jsonable_encoder(model_config_create.configuration)


def test_get_model_config_by_model(
        db: orm.Session, model_config_create: schemas.ModelConfigCreate, model_in_db: models.Model
) -> typing.NoReturn:
    config = crud.model_config.create_with_model(db, obj_in=model_config_create, model_id=model_in_db.id)
    config_1 = crud.model_config.get_by_model(db, model_id=model_in_db.id)

    assert config_1.id == config.id
    assert config_1.model_id == model_in_db.id
    assert encoders.jsonable_encoder(config_1.configuration) == \
           encoders.jsonable_encoder(model_config_create.configuration)


def test_get_all_model_configs(
        db: orm.Session, model_config_create: schemas.ModelConfigCreate, model_in_db: models.Model
) -> typing.NoReturn:
    config = crud.model_config.create_with_model(db, obj_in=model_config_create, model_id=model_in_db.id)
    configs = crud.model_config.get_all(db)

    assert configs[0].id == config.id
    assert configs[0].model_id == model_in_db.id
    assert encoders.jsonable_encoder(configs[0].configuration) == \
           encoders.jsonable_encoder(model_config_create.configuration)


def test_delete_model_config(
        db: orm.Session, model_config_create: schemas.ModelConfigCreate, model_in_db: models.Model
) -> typing.NoReturn:
    config = crud.model_config.create_with_model(db, obj_in=model_config_create, model_id=model_in_db.id)
    config_1 = crud.model_config.delete(db, id=config.id)
    config_2 = crud.model_config.get(db, id=config.id)

    assert config_2 is None
    assert config_1.id == config.id
    assert config_1.model_id == model_in_db.id
    assert encoders.jsonable_encoder(config_1.configuration) == \
           encoders.jsonable_encoder(model_config_create.configuration)
