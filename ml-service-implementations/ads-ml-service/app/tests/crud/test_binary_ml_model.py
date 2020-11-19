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

import sqlalchemy.orm as orm

import app.crud as crud
import app.models as models
import app.schemas as schemas
import app.schemas.mapping as mapping
import app.tests.predictors.common as app_tests_common


def test_create_binary_ml_model(
        db: orm.Session,
        endpoint_in_db: models.Endpoint
) -> typing.NoReturn:
    predictor = app_tests_common.get_classification_predictor()
    binary_create = schemas.BinaryMlModelCreate(
        model_b64=pickle.dumps(predictor),
        input_handling=mapping.ModelInput.DATAFRAME,
        output_handling=mapping.ModelOutput.NUMPY_ARRAY,
        loader=mapping.ModelLoader.JOBLIB
    )
    binary = crud.binary_ml_model.create_with_endpoint(db, obj_in=binary_create, endpoint_id=endpoint_in_db.id)

    assert binary.id == endpoint_in_db.id
    assert isinstance(pickle.loads(binary.model_b64), type(pickle.loads(binary_create.model_b64)))
    assert binary.input_handling == binary_create.input_handling
    assert binary.output_handling == binary_create.output_handling
    assert binary.loader == binary_create.loader


def test_get_binary_ml_model(
        db: orm.Session,
        endpoint_in_db: models.Endpoint
) -> typing.NoReturn:
    predictor = app_tests_common.get_classification_predictor()
    binary_create = schemas.BinaryMlModelCreate(
        model_b64=pickle.dumps(predictor),
        input_handling=mapping.ModelInput.DATAFRAME,
        output_handling=mapping.ModelOutput.NUMPY_ARRAY,
        loader=mapping.ModelLoader.JOBLIB
    )
    binary = crud.binary_ml_model.create_with_endpoint(db, obj_in=binary_create, endpoint_id=endpoint_in_db.id)
    binary_1 = crud.binary_ml_model.get(db, id=binary.id)

    assert binary_1.id == binary.id
    assert binary_1.id == endpoint_in_db.id
    assert isinstance(pickle.loads(binary_1.model_b64), type(pickle.loads(binary_create.model_b64)))
    assert binary_1.input_handling == binary_create.input_handling
    assert binary_1.output_handling == binary_create.output_handling
    assert binary_1.loader == binary_create.loader


def test_get_binary_ml_model_by_endpoint(
        db: orm.Session,
        endpoint_in_db: models.Endpoint
) -> typing.NoReturn:
    predictor = app_tests_common.get_classification_predictor()
    binary_create = schemas.BinaryMlModelCreate(
        model_b64=pickle.dumps(predictor),
        input_handling=mapping.ModelInput.DATAFRAME,
        output_handling=mapping.ModelOutput.NUMPY_ARRAY,
        loader=mapping.ModelLoader.JOBLIB
    )
    binary = crud.binary_ml_model.create_with_endpoint(db, obj_in=binary_create, endpoint_id=endpoint_in_db.id)
    binary_1 = crud.binary_ml_model.get_by_endpoint(db, endpoint_id=endpoint_in_db.id)

    assert binary_1.id == binary.id
    assert binary_1.id == endpoint_in_db.id
    assert isinstance(pickle.loads(binary_1.model_b64), type(pickle.loads(binary_create.model_b64)))
    assert binary_1.input_handling == binary_create.input_handling
    assert binary_1.output_handling == binary_create.output_handling
    assert binary_1.loader == binary_create.loader


def test_delete_binary_ml_model(
        db: orm.Session,
        endpoint_in_db: models.Endpoint
) -> typing.NoReturn:
    predictor = app_tests_common.get_classification_predictor()
    binary_create = schemas.BinaryMlModelCreate(
        model_b64=pickle.dumps(predictor),
        input_handling=mapping.ModelInput.DATAFRAME,
        output_handling=mapping.ModelOutput.NUMPY_ARRAY,
        loader=mapping.ModelLoader.JOBLIB
    )
    binary = crud.binary_ml_model.create_with_endpoint(db, obj_in=binary_create, endpoint_id=endpoint_in_db.id)
    binary_1 = crud.binary_ml_model.delete(db, id=binary.id)
    binary_2 = crud.binary_ml_model.get(db, id=binary.id)

    assert binary_2 is None
    assert binary_1.id == binary.id
    assert binary_1.id == endpoint_in_db.id
    assert isinstance(pickle.loads(binary_1.model_b64), type(pickle.loads(binary_create.model_b64)))
    assert binary_1.input_handling == binary_create.input_handling
    assert binary_1.output_handling == binary_create.output_handling
    assert binary_1.loader == binary_create.loader
