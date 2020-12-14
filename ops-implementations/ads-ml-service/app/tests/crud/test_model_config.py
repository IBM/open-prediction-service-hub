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


import datetime as dt
import time
import typing

import fastapi.encoders as encoders
import sqlalchemy.orm as orm

import app.crud as crud
import app.models as models
import app.schemas as schemas
import app.tests.utils.utils as app_test_utils


def test_create_model_config(
        db: orm.Session, model_config_create: schemas.ModelConfigCreate, model_in_db: models.Model
) -> typing.NoReturn:
    config = crud.model_config.create_with_model(db, obj_in=model_config_create, model_id=model_in_db.id)

    assert config.id == model_in_db.id
    assert encoders.jsonable_encoder(config.configuration) == \
           encoders.jsonable_encoder(model_config_create.configuration)


def test_get_model_config(
        db: orm.Session, model_config_create: schemas.ModelConfigCreate, model_in_db: models.Model
) -> typing.NoReturn:
    config = crud.model_config.create_with_model(db, obj_in=model_config_create, model_id=model_in_db.id)
    config_1 = crud.model_config.get(db, id=config.id)

    assert config_1.id == config.id
    assert config_1.id == model_in_db.id
    assert encoders.jsonable_encoder(config_1.configuration) == \
           encoders.jsonable_encoder(model_config_create.configuration)


def test_get_model_config_by_model(
        db: orm.Session, model_config_create: schemas.ModelConfigCreate, model_in_db: models.Model
) -> typing.NoReturn:
    config = crud.model_config.create_with_model(db, obj_in=model_config_create, model_id=model_in_db.id)
    config_1 = crud.model_config.get_by_model(db, model_id=model_in_db.id)

    assert config_1.id == config.id
    assert config_1.id == model_in_db.id
    assert encoders.jsonable_encoder(config_1.configuration) == \
           encoders.jsonable_encoder(model_config_create.configuration)


def test_get_all_model_configs(
        db: orm.Session, model_config_create: schemas.ModelConfigCreate, model_in_db: models.Model
) -> typing.NoReturn:
    config = crud.model_config.create_with_model(db, obj_in=model_config_create, model_id=model_in_db.id)
    configs = crud.model_config.get_all(db)

    assert configs[0].id == config.id
    assert configs[0].id == model_in_db.id
    assert encoders.jsonable_encoder(configs[0].configuration) == \
           encoders.jsonable_encoder(model_config_create.configuration)


def test_update_model_config(
        db: orm.Session, model_config_create: schemas.ModelConfigCreate, model_in_db: models.Model
) -> typing.NoReturn:
    config = crud.model_config.create_with_model(db, obj_in=model_config_create, model_id=model_in_db.id)
    new_model_name = app_test_utils.random_string()
    model_config_update = model_config_create.copy()
    model_config_update.configuration['name'] = new_model_name
    time.sleep(3)
    config_1 = crud.model_config.update(db, db_obj=config, obj_in=model_config_update)
    model_1 = crud.model.get(db, id=model_in_db.id)

    assert config_1.id == config.id
    assert config_1.configuration['name'] == new_model_name
    assert config_1.model.created_at == model_in_db.created_at
    assert (dt.datetime.now(tz=dt.timezone.utc) - model_1.created_at.replace(tzinfo=dt.timezone.utc)) \
        .total_seconds() > 1
    assert (dt.datetime.now(tz=dt.timezone.utc) - model_1.modified_at.replace(tzinfo=dt.timezone.utc)) \
        .total_seconds() < 1


def test_delete_model_config(
        db: orm.Session, model_config_create: schemas.ModelConfigCreate, model_in_db: models.Model
) -> typing.NoReturn:
    config = crud.model_config.create_with_model(db, obj_in=model_config_create, model_id=model_in_db.id)
    config_1 = crud.model_config.delete(db, id=config.id)
    config_2 = crud.model_config.get(db, id=config.id)

    assert config_2 is None
    assert config_1.id == config.id
    assert config_1.id == model_in_db.id
    assert encoders.jsonable_encoder(config_1.configuration) == \
           encoders.jsonable_encoder(model_config_create.configuration)
