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


import pathlib
import pickle

import pytest
import sqlalchemy.orm as orm

import app.crud as crud
import app.models as models
import app.runtime.cache as app_runtime_cache
import app.schemas as schemas
import app.tests.predictors.identity.model as app_test_identity
import app.tests.predictors.pmml.model as app_test_pmml
import app.tests.predictors.scikit_learn.model as app_test_skl
import app.tests.predictors.xgboost.model as app_test_xgboost
import app.tests.utils.utils as app_test_utils


@pytest.fixture
def endpoint_with_model(
        db: orm.Session
) -> models.Endpoint:
    model = crud.model.create(db, obj_in=schemas.ModelCreate())
    crud.model_config.create_with_model(
        db, obj_in=schemas.ModelConfigCreate(configuration=app_test_skl.get_conf()['model']), model_id=model.id
    )
    endpoint = crud.endpoint.create_with_model(
        db, obj_in=schemas.EndpointCreate(name=app_test_utils.random_string()), model_id=model.id
    )
    return endpoint


@pytest.fixture
def model_with_config(
        db: orm.Session
) -> models.Model:
    model = crud.model.create(db, obj_in=schemas.ModelCreate())
    crud.model_config.create_with_model(
        db, obj_in=schemas.ModelConfigCreate(configuration=app_test_skl.get_conf()['model']), model_id=model.id
    )
    return model


@pytest.fixture
def identity_endpoint(
        db: orm.Session
) -> models.Endpoint:
    config = app_test_identity.get_conf()
    model = crud.model.create(db, obj_in=schemas.ModelCreate())
    crud.model_config.create_with_model(
        db, obj_in=schemas.ModelConfigCreate(configuration=config['model']), model_id=model.id
    )
    endpoint = crud.endpoint.create_with_model(db, obj_in=schemas.EndpointCreate(**config['endpoint']),
                                               model_id=model.id)
    crud.binary_ml_model.create_with_endpoint(db, obj_in=schemas.BinaryMlModelCreate(
        model_b64=pickle.dumps(obj=app_test_identity.get_identity_predictor()),
        **config['binary']
    ), endpoint_id=endpoint.id)
    return endpoint


@pytest.fixture
def skl_endpoint(
        db: orm.Session
) -> models.Endpoint:
    config = app_test_skl.get_conf()
    model = crud.model.create(db, obj_in=schemas.ModelCreate())
    crud.model_config.create_with_model(
        db, obj_in=schemas.ModelConfigCreate(configuration=config['model']), model_id=model.id
    )
    endpoint = crud.endpoint.create_with_model(db, obj_in=schemas.EndpointCreate(**config['endpoint']),
                                               model_id=model.id)
    crud.binary_ml_model.create_with_endpoint(db, obj_in=schemas.BinaryMlModelCreate(
        model_b64=pickle.dumps(app_test_skl.get_classification_predictor()),
        **config['binary']
    ), endpoint_id=endpoint.id)
    return model


@pytest.fixture
def skl_endpoint_with_metadata_for_binary(
        db: orm.Session
) -> models.Endpoint:
    config = app_test_skl.get_conf()
    classification_config_with_additional_info = {
        **config['model'],
        'metadata': {app_runtime_cache.ADDITIONAL_INFO_NAME: {'names': ['x', 'y']}}
    }
    model = crud.model.create(db, obj_in=schemas.ModelCreate())
    crud.model_config.create_with_model(
        db, obj_in=schemas.ModelConfigCreate(configuration=classification_config_with_additional_info),
        model_id=model.id
    )
    endpoint = crud.endpoint.create_with_model(db, obj_in=schemas.EndpointCreate(**config['endpoint']),
                                               model_id=model.id)
    crud.binary_ml_model.create_with_endpoint(db, obj_in=schemas.BinaryMlModelCreate(
        model_b64=pickle.dumps(app_test_skl.get_classification_predictor()),
        **config['binary']
    ), endpoint_id=endpoint.id)
    return model


@pytest.fixture
def pmml_endpoint(
        db: orm.Session,
        tmp_path: pathlib.Path
) -> models.Model:
    config = app_test_pmml.get_conf()
    pmml_path = app_test_pmml.get_pmml_file(tmp_path)
    with pmml_path.open(mode='rb') as fd:
        pmml_file = fd.read()
    model = crud.model.create(db, obj_in=schemas.ModelCreate())
    crud.model_config.create_with_model(
        db, obj_in=schemas.ModelConfigCreate(configuration=config['model']), model_id=model.id
    )
    endpoint = crud.endpoint.create_with_model(db, obj_in=schemas.EndpointCreate(**config['endpoint']),
                                               model_id=model.id)
    crud.binary_ml_model.create_with_endpoint(db, obj_in=schemas.BinaryMlModelCreate(
        model_b64=pmml_file,
        **config['binary']
    ), endpoint_id=endpoint.id)
    return model


@pytest.fixture
def xgboost_endpoint(
        tmp_path,
        db: orm.Session,
) -> models.Endpoint:
    config = app_test_xgboost.get_conf()
    model_path = tmp_path.joinpath('model.bst')
    app_test_xgboost.get_xgboost_classification_predictor().save_model(fname=model_path.__str__())
    model = crud.model.create(db, obj_in=schemas.ModelCreate())
    crud.model_config.create_with_model(
        db, obj_in=schemas.ModelConfigCreate(configuration=config['model']), model_id=model.id
    )
    endpoint = crud.endpoint.create_with_model(db, obj_in=schemas.EndpointCreate(**config['endpoint']),
                                               model_id=model.id)
    with model_path.open(mode='rb') as fd:
        content = fd.read()
    crud.binary_ml_model.create_with_endpoint(db, obj_in=schemas.BinaryMlModelCreate(
        model_b64=content,
        **config['binary']
    ), endpoint_id=endpoint.id)
    return endpoint
