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


import typing as typ

import fastapi.testclient as tstc
import pytest

import app.core.configuration as app_conf
import app.core.uri as app_uri
import app.models as app_models


@pytest.mark.parametrize(
    'model_input, output',
    [
        # Single
        ([{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 0.5}], {'x': 0.5, 'y': 0.5}),
        ([{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 10}], {'x': 0.5, 'y': 10}),
        ([{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': True}], {'x': 0.5, 'y': True}),
        ([{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 'good'}], {'x': 0.5, 'y': 'good'}),
        ([{'name': 'x', 'value': 10}, {'name': 'y', 'value': 10}], {'x': 10, 'y': 10}),
        ([{'name': 'x', 'value': 10}, {'name': 'y', 'value': True}], {'x': 10, 'y': True}),
        ([{'name': 'x', 'value': 10}, {'name': 'y', 'value': 'good'}], {'x': 10, 'y': 'good'}),
        ([{'name': 'x', 'value': True}, {'name': 'y', 'value': True}], {'x': True, 'y': True}),
        ([{'name': 'x', 'value': True}, {'name': 'y', 'value': 'good'}], {'x': True, 'y': 'good'}),
        ([{'name': 'x', 'value': 'bad'}, {'name': 'y', 'value': 'good'}], {'x': 'bad', 'y': 'good'}),
    ]
)
def test_identity_prediction(
        client: tstc.TestClient,
        identity_endpoint: app_models.Endpoint,
        model_input: typ.List[typ.Dict[typ.Text, typ.Any]],
        output
) -> typ.Any:
    import app.runtime.cache as app_cache
    app_cache.cache.clear()
    response = client.post(
        url=app_conf.get_config().API_V2_STR + '/predictions',
        json={
            'parameters': model_input,
            'target': [
                {'rel': 'endpoint', 'href': app_uri.TEMPLATE.format(
                    resource_type='endpoints', resource_id=identity_endpoint.id)}
            ]
        }
    )
    prediction = response.json()['result']

    assert prediction == output


def test_xgboost_prediction(
        client: tstc.TestClient,
        xgboost_endpoint: app_models.Endpoint
) -> typ.NoReturn:
    import app.runtime.cache as app_cache
    app_cache.cache.clear()
    response = client.post(
        url=app_conf.get_config().API_V2_STR + '/predictions',
        json={
            'parameters': [{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 0.5}],
            'target': [
                {'rel': 'endpoint', 'href': app_uri.TEMPLATE.format(
                    resource_type='endpoints', resource_id=xgboost_endpoint.id)}
            ]
        }
    )
    prediction = response.json()['result']['predictions']

    assert response.status_code == 200
    assert isinstance(prediction, typ.List)


def test_skl_prediction(
        client: tstc.TestClient,
        skl_endpoint
) -> typ.NoReturn:
    import app.runtime.cache as app_cache
    app_cache.cache.clear()
    response = client.post(
        url=app_conf.get_config().API_V2_STR + '/predictions',
        json={
            'parameters': [{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 0.5}],
            'target': [
                {'rel': 'endpoint', 'href': app_uri.TEMPLATE.format(
                    resource_type='endpoints', resource_id=skl_endpoint.id)}
            ]
        }
    )
    content = response.json()
    prediction = content['result']['predictions']

    assert response.status_code == 200
    assert isinstance(prediction, typ.Text)


def test_pmml_prediction(
        client: tstc.TestClient,
        pmml_endpoint: app_models.Endpoint
) -> typ.NoReturn:
    import app.runtime.cache as app_cache
    app_cache.cache.clear()
    response = client.post(
        url=app_conf.get_config().API_V2_STR + '/predictions',
        json={
            'parameters': [{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 0.5}],
            'target': [
                {'rel': 'endpoint', 'href': app_uri.TEMPLATE.format(
                    resource_type='endpoints', resource_id=pmml_endpoint.id)}
            ]
        }
    )

    assert response.status_code == 200
    assert response.json()['result']


def test_prediction_with_additional_info(
        client: tstc.TestClient,
        skl_endpoint_with_metadata_for_binary: app_models.Endpoint
) -> typ.NoReturn:
    import app.runtime.cache as app_cache
    app_cache.cache.clear()
    response = client.post(
        url=app_conf.get_config().API_V2_STR + '/predictions',
        json={
            'parameters': [{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 0.5}],
            'target': [
                {'rel': 'endpoint', 'href': app_uri.TEMPLATE.format(
                    resource_type='endpoints', resource_id=skl_endpoint_with_metadata_for_binary.id)}
            ]
        }
    )
    content = response.json()
    additional_info = content['result']

    assert response.status_code == 200
    assert additional_info['names']
    assert additional_info['names'] == ['x', 'y']


def test_prediction_with_additional_info(
        client: tstc.TestClient
) -> typ.NoReturn:
    response = client.post(
        url=app_conf.get_config().API_V2_STR + '/predictions',
        json={
            'parameters': [{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 0.5}],
            'target': [
                {'rel': 'endpoint', 'href': app_uri.TEMPLATE.format(
                    resource_type='endpoints', resource_id='123456')}
            ]
        }
    )

    assert response.status_code == 404
    assert response.json().get('detail') is not None
    assert 'model not found' in response.json().get('detail')
