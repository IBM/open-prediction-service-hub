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
import time
import typing
import typing as typ
import re

import pytest
import fastapi.testclient as tstc
import sqlalchemy.orm as orm
import sqlalchemy.orm as saorm

import app.core.configuration as conf
import app.crud as crud
import app.schemas as schemas
import app.tests.predictors.identity.model as app_tests_identity
import app.tests.predictors.scikit_learn.model as app_test_skl
import app.models as models
import app.tests.predictors.pmml_sample.model as app_test_pmml


def test_get_model(
        client: tstc.TestClient,
        model_with_config
) -> typing.NoReturn:
    response = client.get(url=conf.get_config().API_V2_STR + '/models' + f'/{model_with_config.id}')
    model = response.json()

    assert response.status_code == 200
    assert model['id'] == str(model_with_config.id)
    assert dt.datetime.strptime(model['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z') == \
           model_with_config.created_at.astimezone(dt.timezone.utc)
    assert dt.datetime.strptime(model['modified_at'], '%Y-%m-%dT%H:%M:%S.%f%z') == \
           model_with_config.modified_at.astimezone(dt.timezone.utc)
    assert all(
        [
            model[key] == app_test_skl.get_conf()['model'][key] for key in app_test_skl.get_conf()['model'].keys()
        ]
    )


def test_get_models(
        client: tstc.TestClient,
        model_with_config
) -> typing.NoReturn:
    response = client.get(url=conf.get_config().API_V2_STR + '/models')
    rst = response.json()

    assert response.status_code == 200
    assert rst['models'][0]['id'] == str(model_with_config.id)


@pytest.mark.parametrize(
    'http_params',
    [
         ({'offset': -1}),
         ({'limit': 0}),
         ({'limit': 201})
    ]
)
def test_get_endpoints_with_invalid_params(
        client: tstc.TestClient,
        http_params
):
    response = client.get(url=conf.get_config().API_V2_STR + '/models', params=http_params)

    assert response.status_code == 422
    assert response.json()['detail'] == 'Requested offset/limit is not valid'


def test_add_model(
        client: tstc.TestClient,
) -> typing.NoReturn:
    response = client.post(
        url=conf.get_config().API_V2_STR + '/models',
        json=app_test_skl.get_conf()['model']
    )
    model = response.json()

    assert response.status_code == 201
    assert all(
        [model.get(k) == app_test_skl.get_conf()['model'].get(k) for k in app_test_skl.get_conf()['model'].keys()])


def test_update_model_name(
        client: tstc.TestClient,
        model_with_config
) -> typing.NoReturn:
    time.sleep(3)
    response = client.patch(
        url=conf.get_config().API_V2_STR + '/models' + f'/{model_with_config.id}',
        json={
            'name': 'dummy-model'
        }
    )
    model = response.json()

    assert response.status_code == 200
    assert model['name'] == 'dummy-model'
    assert (dt.datetime.strptime(model['modified_at'], '%Y-%m-%dT%H:%M:%S.%f%z') -
            dt.datetime.strptime(model['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')).seconds > 1


def test_update_model_metadata(
        client: tstc.TestClient,
        xgboost_endpoint
) -> typing.NoReturn:
    original_model = client.get(url=conf.get_config().API_V2_STR + '/models' + f'/{xgboost_endpoint.id}').json()
    original_endpoint = client.get(url=conf.get_config().API_V2_STR + '/endpoints' + f'/{xgboost_endpoint.id}').json()

    updated_model = client.patch(
        url=conf.get_config().API_V2_STR + '/models' + f'/{xgboost_endpoint.id}',
        json={
            'metadata': {
                'my-tag': 'predictive-model-1'
            }
        }
    ).json()
    updated_endpoint = client.get(url=conf.get_config().API_V2_STR + '/endpoints' + f'/{xgboost_endpoint.id}').json()

    assert original_model['metadata'] == {'description': 'xgboost model for test'}
    assert original_model['metadata'] == original_endpoint['metadata']
    assert updated_model['metadata'] == {'description': None, 'my-tag': 'predictive-model-1'}


def test_update_model_conf(
        client: tstc.TestClient,
        model_with_config
) -> typing.NoReturn:
    time.sleep(3)
    response = client.patch(
        url=conf.get_config().API_V2_STR + '/models' + f'/{model_with_config.id}',
        json={
            'version': 'dummy'
        }
    )
    model = response.json()

    assert response.status_code == 200
    assert all(
        [
            model.get(k) == app_test_skl.get_conf()['model'].get(k) for k in
            app_test_skl.get_conf()['model'].keys() if k != 'version'
        ]
    )
    assert (dt.datetime.strptime(model['modified_at'], '%Y-%m-%dT%H:%M:%S.%f%z') -
            dt.datetime.strptime(model['created_at'], '%Y-%m-%dT%H:%M:%S.%f%z')).seconds > 1


def test_delete_model(
        db: orm.Session,
        client: tstc.TestClient,
        model_with_config
) -> typing.NoReturn:
    response = client.delete(url=conf.get_config().API_V2_STR + '/models' + f'/{model_with_config.id}')
    response_1 = client.delete(url=conf.get_config().API_V2_STR + '/models' + f'/{model_with_config.id}')
    model = crud.model.get(db, id=model_with_config.id)

    assert response.status_code == 204
    assert response_1.status_code == 404
    assert model is None


def test_add_binary(
        db: saorm.Session,
        client: tstc.TestClient
) -> typ.NoReturn:
    model = crud.model.create(db, obj_in=schemas.ModelCreate())
    crud.model_config.create_with_model(
        db, obj_in=schemas.ModelConfigCreate(configuration=app_test_skl.get_conf()['model']), model_id=model.id
    )
    response = client.post(
        url=conf.get_config().API_V2_STR + '/models' + f'/{model.id}',
        files={'file': pickle.dumps(app_test_skl.get_classification_predictor())},
        data=app_test_skl.get_conf()['binary']
    )
    response_1 = client.get(
        url=conf.get_config().API_V2_STR + '/endpoints' + f'/{model.id}')

    assert response.status_code == 201
    assert response_1.json()['status'] == 'in_service'


def test_add_non_compatible_binary(
        db: saorm.Session,
        client: tstc.TestClient
) -> typ.NoReturn:
    model = crud.model.create(db, obj_in=schemas.ModelCreate())
    crud.model_config.create_with_model(
        db, obj_in=schemas.ModelConfigCreate(configuration=app_test_skl.get_conf()['model']), model_id=model.id
    )
    response = client.post(
        url=conf.get_config().API_V2_STR + '/models' + f'/{model.id}',
        files={'file': 'toto'.encode()},
        data=app_test_skl.get_conf()['binary']
    )
    assert response.status_code == 422


def test_update_binary(
        db: saorm.Session,
        client: tstc.TestClient
) -> typ.NoReturn:
    model = crud.model.create(db, obj_in=schemas.ModelCreate())
    crud.model_config.create_with_model(
        db, obj_in=schemas.ModelConfigCreate(configuration=app_test_skl.get_conf()['model']), model_id=model.id
    )
    response = client.post(
        url=conf.get_config().API_V2_STR + '/models' + f'/{model.id}',
        files={'file': pickle.dumps(app_test_skl.get_classification_predictor())},
        data=app_test_skl.get_conf()['binary']
    )
    response_1 = client.post(
        url=conf.get_config().API_V2_STR + '/models' + f'/{model.id}',
        files={'file': pickle.dumps(app_tests_identity.get_identity_predictor())},
        data=app_test_skl.get_conf()['binary']
    )

    assert response.status_code == 201
    assert response.json()['status'] == 'in_service'
    assert response_1.status_code == 422


def test_not_supported_metadata(
        client: tstc.TestClient,
        xgboost_endpoint: models.Endpoint
) -> typ.NoReturn:
    # When
    resp = client.get(url=f'/models/{xgboost_endpoint.id}/metadata')

    # Assert
    assert resp.status_code == 422
    assert resp.json()['detail'] == 'Format bst is not supported for metadata'


def test_pickle_metadata(
        client: tstc.TestClient
) -> typ.NoReturn:
    # When
    model = client.post(
        url='/upload',
        data={'format': 'pickle'},
        files={'file': ('model.pkl', pickle.dumps(app_test_skl.get_classification_predictor()))}).json()
    model_id = model['id']
    resp = client.get(url=f'/models/{model_id}/metadata')

    # Assert
    assert resp.ok
    assert resp.json()['modelType'] == 'pickle'
    assert resp.json()['pickleProtoVersion'] == '4'


def test_pmml_metadata(
        client: tstc.TestClient
) -> typ.NoReturn:
    # When
    model = client.post(
        url='/upload',
        data={'format': 'pmml'},
        files={'file': ('scorecard.pmml', app_test_pmml.get_pmml_scorecard_file().read_text())}).json()
    model_id = model['id']
    resp = client.get(url=f'/models/{model_id}/metadata')

    # Assert
    assert resp.ok
    assert resp.json()['modelType'] == 'pmml'
    assert resp.json()['modelSubType'] == 'Scorecard'


def test_download_binary(
        client: tstc.TestClient
) -> typ.NoReturn:
    # When
    model_content = app_test_pmml.get_pmml_scorecard_file().read_text()
    model = client.post(
        url='/upload',
        data={'format': 'pmml'},
        files={'file': ('scorecard.pmml', model_content)}).json()
    model_id = model['id']
    resp = client.get(url=f'/models/{model_id}/binary')
    received_filename = re.findall("filename=\"(.+)\"", resp.headers['content-disposition'])[0]

    # Assert
    assert resp.ok
    assert resp.content == str.encode(model_content)
    assert received_filename == 'scorecard.pmml'
