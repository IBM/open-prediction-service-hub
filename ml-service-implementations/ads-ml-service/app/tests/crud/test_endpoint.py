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
import app.schemas.mapping as mapping
import app.tests.predictors.common as app_tests_common
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
    predictor = app_tests_common.get_classification_predictor()
    binary_in = schemas.BinaryMlModelCreate(
        model_b64=pickle.dumps(predictor),
        input_handling=mapping.ModelInput.DATAFRAME,
        output_handling=mapping.ModelOutput.NUMPY_ARRAY,
        loader=mapping.ModelLoader.JOBLIB
    )
    binary = crud.binary_ml_model.create_with_endpoint(db, obj_in=binary_in, endpoint_id=endpoint_in_db.id)
    crud.endpoint.delete(db, id=endpoint_in_db.id)
    binary_1 = crud.binary_ml_model.get(db, id=binary.id)

    assert binary_1 is None
