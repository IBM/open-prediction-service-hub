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
from typing import NoReturn

from sqlalchemy.orm import Session

from app import crud
from app.schemas.binary_ml_model import BinaryMLModelCreate


def test_create_binary_ml_model(db: Session, classification_predictor, classification_config) -> NoReturn:
    binary_in = BinaryMLModelCreate(model_b64=pickle.dumps(classification_predictor))
    binary_1 = crud.binary_ml_model.create(db, obj_in=binary_in)

    assert type(pickle.loads(binary_1.model_b64)) == type(classification_predictor)


def test_get_binary_ml_model(db: Session, classification_predictor, classification_config) -> NoReturn:
    binary_in = BinaryMLModelCreate(model_b64=pickle.dumps(classification_predictor))
    binary_1 = crud.binary_ml_model.create(db, obj_in=binary_in)
    binary_2 = crud.binary_ml_model.get(db, id=binary_1.id)

    assert type(pickle.loads(binary_2.model_b64)) == type(classification_predictor)


def test_delete_binary_ml_model(db: Session, classification_predictor, classification_config) -> NoReturn:
    binary_in = BinaryMLModelCreate(model_b64=pickle.dumps(classification_predictor))
    binary_1 = crud.binary_ml_model.create(db, obj_in=binary_in)
    binary_2 = crud.binary_ml_model.delete(db, id=binary_1.id)
    binary_3 = crud.binary_ml_model.get(db, id=binary_1.id)

    assert binary_3 is None
    assert binary_2.id == binary_1.id
    assert type(pickle.loads(binary_2.model_b64)) == type(classification_predictor)
