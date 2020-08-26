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


from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas.model_config import ModelConfigCreate


def test_create_model_config(db: Session, classification_config):
    config_in = ModelConfigCreate(**classification_config)
    config = crud.model_config.create(db, obj_in=config_in)

    assert jsonable_encoder(config.configuration) == jsonable_encoder(config_in)


def test_get_schemas(db: Session, classification_config):
    config_in = ModelConfigCreate(**classification_config)
    config = crud.model_config.create(db, obj_in=config_in)
    schemas = crud.model_config.get_all(db)

    assert len(schemas) == 1
    assert schemas[0].id == config.id
    assert jsonable_encoder(schemas[0].configuration) == jsonable_encoder(config_in)


def test_get_model_config(db: Session, classification_config):
    config_in = ModelConfigCreate(**classification_config)
    config = crud.model_config.create(db, obj_in=config_in)
    m_2 = crud.model_config.get(db, id=config.id)

    assert m_2 is not None
    assert jsonable_encoder(m_2.configuration) == jsonable_encoder(config_in)


def test_delete_model_config(db: Session, classification_config):
    config_in = ModelConfigCreate(**classification_config)
    config = crud.model_config.create(db, obj_in=config_in)
    config_2 = crud.model_config.delete(db, id=config.id)

    assert config_2.id == config.id
    assert crud.model_config.get(db, id=config.id) is None
