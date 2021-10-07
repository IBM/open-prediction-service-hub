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
import pickle
import typing

import sqlalchemy.orm as orm

import app.crud as crud
import app.models as models
import app.schemas as schemas
import app.schemas.binary_config as mapping
import app.tests.predictors.scikit_learn.model
import app.tests.utils.utils as utils


def test_create_endpoint(db: orm.Session, model_in_db: models.Model) -> typing.NoReturn:
    endpoint_name = utils.random_string()
    endpoint_in = schemas.EndpointCreate(name=endpoint_name)
    endpoint = crud.endpoint.create_with_model(db, obj_in=endpoint_in, model_id=model_in_db.id)

    assert endpoint.name == endpoint_name
    assert endpoint.id == model_in_db.id
    assert (dt.datetime.now(tz=dt.timezone.utc) - endpoint.deployed_at.replace(tzinfo=dt.timezone.utc)).seconds < 1


def test_cascade_delete_with_binary(
        db: orm.Session,
        endpoint_in_db: models.Model,
) -> typing.NoReturn:
    predictor = app.tests.predictors.scikit_learn.model.get_classification_predictor()
    binary_in = schemas.BinaryMlModelCreate(
        model_b64=pickle.dumps(predictor),
        input_data_structure=mapping.ModelInput.DATAFRAME,
        output_data_structure=mapping.ModelOutput.NUMPY_ARRAY,
        format=mapping.ModelWrapper.JOBLIB
    )
    binary = crud.binary_ml_model.create_with_endpoint(db, obj_in=binary_in, endpoint_id=endpoint_in_db.id)
    crud.endpoint.delete(db, id=endpoint_in_db.id)
    binary_1 = crud.binary_ml_model.get(db, id=binary.id)

    assert binary_1 is None


def test_create_endpoint_with_metadata(db: orm.Session, model_in_db: models.Model) -> typing.NoReturn:
    endpoint_name = utils.random_string()
    metadata_in = {
        'tag': 'endpoint'
    }
    endpoint_in = schemas.EndpointCreate(name=endpoint_name, metadata_=metadata_in)
    endpoint = crud.endpoint.create_with_model(db, obj_in=endpoint_in, model_id=model_in_db.id)

    assert endpoint.name == endpoint_name
    assert endpoint.id == model_in_db.id
    assert endpoint.metadata_ == metadata_in


def test_update_endpoint_with_metadata(db: orm.Session, model_in_db: models.Model) -> typing.NoReturn:
    endpoint_name = utils.random_string()
    metadata_in = {
        'tag': 'endpoint'
    }
    metadata_new = {
        'tag': 'new-endpoint'
    }
    endpoint_in = schemas.EndpointCreate(name=endpoint_name, metadata_=metadata_in)
    endpoint = crud.endpoint.create_with_model(db, obj_in=endpoint_in, model_id=model_in_db.id)
    endpoint_update = schemas.EndpointUpdate(metadata_=metadata_new)
    endpoint_updated = crud.endpoint.update(db, db_obj=endpoint, obj_in=endpoint_update)

    assert endpoint_updated.name == endpoint_name
    assert endpoint_updated.id == model_in_db.id
    assert endpoint_updated.metadata_ == metadata_new
