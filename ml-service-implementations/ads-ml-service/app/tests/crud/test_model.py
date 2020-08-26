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

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.schemas.binary_ml_model import BinaryMLModelCreate
from app.schemas.model import ModelCreate
from app.schemas.model_config import ModelConfigCreate


def test_create_model(db: Session, classification_predictor, classification_config):
    binary_in = BinaryMLModelCreate(model_b64=pickle.dumps(classification_predictor))
    config_in = ModelConfigCreate(**classification_config)

    model_in = ModelCreate(
        name=classification_config['name'],
        version=classification_config['version'],
        binary=binary_in,
        config=config_in
    )

    model = crud.crud_model.model.create(db, obj_in=model_in)

    assert model is not None
    assert model.name == config_in.name
    assert model.version == config_in.version
    assert jsonable_encoder(model.config.configuration) == jsonable_encoder(config_in)


def test_count_models(db: Session, classification_predictor, classification_config):
    binary_in = BinaryMLModelCreate(model_b64=pickle.dumps(classification_predictor))
    config_in = ModelConfigCreate(**classification_config)

    model_in = ModelCreate(
        name=classification_config['name'],
        version=classification_config['version'],
        binary=binary_in,
        config=config_in
    )

    model = crud.crud_model.model.create(db, obj_in=model_in)

    assert model is not None
    assert crud.model_config.count(db) == 1


def test_get_model(db: Session, classification_predictor, classification_config):
    binary_in = BinaryMLModelCreate(model_b64=pickle.dumps(classification_predictor))
    config_in = ModelConfigCreate(**classification_config)

    model_in = ModelCreate(
        name=classification_config['name'],
        version=classification_config['version'],
        binary=binary_in,
        config=config_in
    )

    model = crud.crud_model.model.create(db, obj_in=model_in)

    model_1 = crud.crud_model.model.get(db, id=model.id)

    assert model_1 is not None
    assert model_1.id == model.id
    assert jsonable_encoder(model_1.config.configuration) == jsonable_encoder(model.config.configuration)


def test_get_model_by_name_and_version(db: Session, classification_predictor, classification_config):
    binary_in = BinaryMLModelCreate(model_b64=pickle.dumps(classification_predictor))
    config_in = ModelConfigCreate(**classification_config)

    model_in = ModelCreate(
        name=classification_config['name'],
        version=classification_config['version'],
        binary=binary_in,
        config=config_in
    )

    model = crud.crud_model.model.create(db, obj_in=model_in)

    model_1 = crud.crud_model.model.get_by_name_and_ver(db, name=classification_config['name'],
                                                        version=classification_config['version'])

    assert model_1 is not None
    assert model_1.id == model.id
    assert jsonable_encoder(model_1.config.configuration) == jsonable_encoder(model.config.configuration)


def test_delete_model(db: Session, classification_predictor, classification_config):
    binary_in = BinaryMLModelCreate(model_b64=pickle.dumps(classification_predictor))
    config_in = ModelConfigCreate(**classification_config)

    model_in = ModelCreate(
        name=classification_config['name'],
        version=classification_config['version'],
        binary=binary_in,
        config=config_in
    )

    model = crud.crud_model.model.create(db, obj_in=model_in)

    model_1 = crud.crud_model.model.delete(db, id=model.id)
    model_2 = crud.crud_model.model.get(db, id=model_1.id)

    assert model_2 is None
    assert model_1.id == model.id
    assert jsonable_encoder(model_1.config.configuration) == jsonable_encoder(model.config.configuration)
