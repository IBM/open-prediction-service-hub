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
import sqlalchemy.orm as saorm

import app.core.configuration as app_conf
import app.core.configuration as conf
import app.core.uri as app_uri
import app.tests.predictors.pmml_sample.model as app_test_pmml


def test_add_binary(
        db: saorm.Session,
        client: tstc.TestClient
) -> typ.NoReturn:
    import app.runtime.cache as app_cache
    app_cache.cache.clear()
    pmml_path = app_test_pmml.get_pmml_file()
    with pmml_path.open(mode='r') as fd:
        pmml_model = fd.read()
    model_creation_resp = client.post(
        url=conf.get_config().API_V2_STR + '/upload',
        files={'file': (pmml_path.name, pmml_model)}
    )
    model_json = model_creation_resp.json()
    model_id = model_json['id']
    model_name = model_json['name']

    prediction_resp = client.post(
        url=app_conf.get_config().API_V2_STR + '/predictions',
        json={
            'parameters': [
                {'name': 'creditScore', 'value': 200},
                {'name': 'income', 'value': 20000},
                {'name': 'loanAmount', 'value': 20000},
                {'name': 'monthDuration', 'value': 20},
                {'name': 'rate', 'value': 2.0},
                {'name': 'yearlyReimbursement', 'value': 2000}
            ],
            'target': [
                {'rel': 'endpoint', 'href': app_uri.TEMPLATE.format(
                    resource_type='endpoints', resource_id=model_id)}
            ]
        }
    )
    prediction_json = prediction_resp.json()

    assert model_creation_resp.status_code == 201
    assert prediction_resp.status_code == 200
    assert model_name == 'model'
    assert 'predicted_paymentDefault' in prediction_json['result']
    assert 'probability_0' in prediction_json['result']
    assert 'probability_1' in prediction_json['result']
