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
import sqlalchemy.orm as saorm

import app.core.configuration as conf
import app.models as models
import app.core.cache as ops_cache


@pytest.mark.parametrize(
    'model_input, output',
    [
        ([{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 10}], [0.5, 10]),
        ([{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': True}], [0.5, True]),
        ([{'name': 'x', 'value': 10}, {'name': 'y', 'value': True}], [10, True]),
        ([{'name': 'x', 'value': 'bad'}, {'name': 'y', 'value': 'good'}], ['bad', 'good']),
    ]
)
def test_value_casting(
        db: saorm.Session,
        client: tstc.TestClient,
        endpoint_with_identity_predictor: models.Endpoint,
        model_input: typ.List[typ.Dict[typ.Text, typ.Any]],
        output
) -> typ.Any:
    response = client.post(
        url=conf.get_config().API_V2_STR + '/predictions',
        json={
            'parameters': model_input,
            'target': [
                {'rel': 'endpoint', 'href': f'ops:///endpoints/{endpoint_with_identity_predictor.id}'}
            ]
        }
    )
    prediction = response.json()['result']['predict']

    assert prediction == output


def test_xgb_prediction(
        db: saorm.Session,
        client: tstc.TestClient,
        endpoint_with_xgb_predictor: models.Endpoint
) -> typ.NoReturn:
    response = client.post(
        url=conf.get_config().API_V2_STR + '/predictions',
        json={
            'parameters': [{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 0.5}],
            'target': [
                {'rel': 'endpoint', 'href': f'ops:///endpoints/{endpoint_with_xgb_predictor.id}'}
            ]
        }
    )
    prediction = response.json()['result']['predict']

    assert response.status_code == 200
    assert isinstance(prediction, list)


def test_prediction(
        db: saorm.Session,
        client: tstc.TestClient,
        endpoint_with_model_and_binary: models.Endpoint
) -> typ.NoReturn:
    ops_cache.cache.clear()
    response = client.post(
        url=conf.get_config().API_V2_STR + '/predictions',
        json={
            'parameters': [{'name': 'x', 'value': 0.5}, {'name': 'y', 'value': 0.5}],
            'target': [
                {'rel': 'endpoint', 'href': f'ops:///endpoints/{endpoint_with_model_and_binary.id}'}
            ]
        }
    )
    prediction = response.json()['result']['predict']

    assert response.status_code == 200
    assert isinstance(prediction, typ.Text)
