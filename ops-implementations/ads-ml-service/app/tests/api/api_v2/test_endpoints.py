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
import typing as typ

import fastapi.testclient as tstc
import sqlalchemy.orm as saorm

import app.core.configuration as conf
import app.crud as crud
import app.models as models


def test_get_endpoint(
        db: saorm.Session,
        client: tstc.TestClient,
        endpoint_with_model: models.Endpoint
) -> typ.NoReturn:
    time.sleep(3)  # To test deployed_at
    response = client.get(
        url=conf.get_config().API_V2_STR + '/endpoints' + f'/{endpoint_with_model.id}')
    endpoint = response.json()

    assert response.status_code == 200
    assert endpoint['id'] == str(endpoint_with_model.id)
    assert endpoint['name'] == endpoint_with_model.name
    assert endpoint['status'] == 'creating'
    assert (dt.datetime.now(tz=dt.timezone.utc) -
            dt.datetime.strptime(endpoint['deployed_at'], '%Y-%m-%dT%H:%M:%S.%f%z')
            .replace(tzinfo=dt.timezone.utc)).seconds > 1


def test_get_endpoint_with_binary(
        db: saorm.Session,
        client: tstc.TestClient,
        skl_endpoint: models.Endpoint
) -> typ.NoReturn:
    response = client.get(url=conf.get_config().API_V2_STR + '/endpoints' + f'/{skl_endpoint.id}')
    endpoint = response.json()

    assert endpoint['status'] == 'in_service'


def test_get_endpoints(
        db: saorm.Session,
        client: tstc.TestClient,
        skl_endpoint: models.Endpoint
) -> typ.NoReturn:
    response = client.get(url=conf.get_config().API_V2_STR + '/endpoints')
    endpoints = response.json()

    assert response.status_code == 200
    assert endpoints['endpoints'][0]['id'] == str(skl_endpoint.id)


def test_patch_endpoint(
        client: tstc.TestClient,
        skl_endpoint: models.Endpoint
) -> typ.NoReturn:
    current_endpoint = client.get(url=f'/endpoints/{skl_endpoint.id}').json()
    patch_endpoint_resp = client.patch(
        url=f'/endpoints/{skl_endpoint.id}',
        json={
            'name': 'new-name',
            'metadata': {'tag': 'updated-metadata'}
        }
    )
    patched_endpoint = patch_endpoint_resp.json()
    updated_endpoint = client.get(url=f'/endpoints/{skl_endpoint.id}').json()

    assert patch_endpoint_resp.status_code == 200
    assert current_endpoint['name'] == 'skl predictor endpoint'
    assert current_endpoint['metadata'] is None
    assert updated_endpoint['name'] == 'new-name'
    assert updated_endpoint['metadata'] == {'description': None, 'tag': 'updated-metadata'}
    assert updated_endpoint['name'] == patched_endpoint['name']
    assert updated_endpoint['metadata'] == patched_endpoint['metadata']


def test_delete_endpoint(
        db: saorm.Session,
        client: tstc.TestClient,
        endpoint_with_model
) -> typ.NoReturn:
    response = client.delete(
        url=conf.get_config().API_V2_STR + '/endpoints' + f'/{endpoint_with_model.id}',
    )
    endpoint = crud.endpoint.get(db, id=endpoint_with_model.id)

    assert response.status_code == 204
    assert endpoint is None
