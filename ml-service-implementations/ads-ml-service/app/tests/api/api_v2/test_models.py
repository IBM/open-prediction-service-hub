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

import fastapi.testclient as tstc
import sqlalchemy.orm as orm

import app.core.configuration as conf
import app.crud as crud
import app.models as models


def test_get_model(
        db: orm.Session,
        client: tstc.TestClient,
        classification_config: typing.Dict[typing.Text, typing.Any],
        model_with_config_and_endpoint: models.Model
) -> typing.NoReturn:
    response = client.get(url=conf.get_config().API_V2_STR + '/models' + f'/{model_with_config_and_endpoint.id}')
    model = response.json()

    assert response.status_code == 200
    assert model['id'] == str(model_with_config_and_endpoint.id)
    assert dt.datetime.strptime(
        model['created_at'], '%Y-%m-%dT%H:%M:%S.%f') == model_with_config_and_endpoint.created_at
    assert dt.datetime.strptime(
        model['modified_at'], '%Y-%m-%dT%H:%M:%S.%f') == model_with_config_and_endpoint.modified_at
    assert all(
        [
            model[key] == classification_config[key] for key in classification_config.keys()
        ]
    )


def test_get_models(
        db: orm.Session,
        client: tstc.TestClient,
        classification_config: typing.Dict[typing.Text, typing.Any],
        model_with_config_and_endpoint: models.Model
) -> typing.NoReturn:
    response = client.get(url=conf.get_config().API_V2_STR + '/models')
    rst = response.json()

    assert response.status_code == 200
    assert rst['models'][0]['id'] == str(model_with_config_and_endpoint.id)


def test_add_model(
        db: orm.Session,
        client: tstc.TestClient,
        classification_config: typing.Dict[typing.Text, typing.Any]
) -> typing.NoReturn:
    response = client.post(
        url=conf.get_config().API_V2_STR + '/models',
        json=classification_config
    )
    model = response.json()

    assert response.status_code == 200
    assert all([model.get(k) == classification_config.get(k) for k in classification_config.keys()])


def test_update_model_name(
        db: orm.Session,
        client: tstc.TestClient,
        classification_config: typing.Dict[typing.Text, typing.Any],
        model_with_config_and_endpoint: models.Model
) -> typing.NoReturn:
    time.sleep(2)
    response = client.patch(
        url=conf.get_config().API_V2_STR + '/models' + f'/{model_with_config_and_endpoint.id}',
        json={
            'name': 'dummy-model'
        }
    )
    model = response.json()

    assert response.status_code == 200
    assert model['name'] == 'dummy-model'
    assert (dt.datetime.strptime(model['modified_at'], '%Y-%m-%dT%H:%M:%S.%f') -
            dt.datetime.strptime(model['created_at'], '%Y-%m-%dT%H:%M:%S.%f')).seconds > 1


def test_update_model_conf(
        db: orm.Session,
        client: tstc.TestClient,
        classification_config: typing.Dict[typing.Text, typing.Any],
        model_with_config_and_endpoint: models.Model
) -> typing.NoReturn:
    time.sleep(2)
    response = client.patch(
        url=conf.get_config().API_V2_STR + '/models' + f'/{model_with_config_and_endpoint.id}',
        json={
            'version': 'dummy'
        }
    )
    model = response.json()

    assert response.status_code == 200
    assert all([model.get(k) == classification_config.get(k) for k in classification_config.keys() if k != 'version'])
    assert (dt.datetime.strptime(model['modified_at'], '%Y-%m-%dT%H:%M:%S.%f') -
            dt.datetime.strptime(model['created_at'], '%Y-%m-%dT%H:%M:%S.%f')).seconds > 1


def test_delete_model(
        db: orm.Session,
        client: tstc.TestClient,
        classification_config: typing.Dict[typing.Text, typing.Any],
        model_with_config_and_endpoint: models.Model
) -> typing.NoReturn:
    response = client.delete(url=conf.get_config().API_V2_STR + '/models' + f'/{model_with_config_and_endpoint.id}')
    response_1 = client.delete(url=conf.get_config().API_V2_STR + '/models' + f'/{model_with_config_and_endpoint.id}')
    model = crud.model.get(db, id=model_with_config_and_endpoint.id)

    assert response.status_code == 204
    assert response_1.status_code == 204
    assert model is None
