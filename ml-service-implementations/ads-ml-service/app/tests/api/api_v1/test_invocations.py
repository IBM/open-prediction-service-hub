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


import ast
import random
import pytest

API_VER = '/v1'


def test_classification(classification_archive, client):
    response = client.post(
        url=API_VER + '/invocations',
        json={
            'model_name': classification_archive.name,
            'model_version': classification_archive.version,
            'params': [
                {'name': 'x', 'value': random.random()},
                {'name': 'y', 'value': random.random()}
            ]
        }
    )

    assert response.status_code == 200
    assert response.json()['prediction'] is not None


def test_classification_with_proba(classification_with_proba_archive, client):
    response = client.post(
        url=API_VER + '/invocations',
        json={
            'model_name': classification_with_proba_archive.name,
            'model_version': classification_with_proba_archive.version,
            'params': [
                {'name': 'x', 'value': random.random()},
                {'name': 'y', 'value': random.random()}
            ]
        }
    )

    assert response.status_code == 200
    assert response.json()['prediction'] is not None
    assert response.json()['probabilities'] is not None
    assert sum([f['value'] for f in response.json()['probabilities']]) == pytest.approx(1.0, 0.01)


def test_regression(regression_archive, client):
    response = client.post(
        url=API_VER + '/invocations',
        json={
            'model_name': regression_archive.name,
            'model_version': regression_archive.version,
            'params': [
                {'name': 'x', 'value': random.random()},
                {'name': 'y', 'value': random.random()}
            ]
        }
    )

    assert response.status_code == 200
    assert response.json()['prediction'] is not None
    assert type(ast.literal_eval(response.json()['prediction'])) == float
