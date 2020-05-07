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


from __future__ import annotations

import ast
import json
import os
import pickle
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict, Text
from typing import List

from dynamic_hosting import app
from fastapi.testclient import TestClient
from requests import Response

from .prepare_models import miniloan_rfc_pickle, miniloan_lr_pickle, miniloan_rfr_pickle, \
    miniloan_rfc_no_class_names_pickle

from dynamic_hosting.localml import VER

OPENAPI_RESOURCE: Path = Path(__file__).resolve().parents[2].joinpath('resources').joinpath('openapi.json')

TEST_RES_DIR: Path = Path(__file__).resolve().parents[3].joinpath('test').joinpath('resources')

shutil.copy(src=str(miniloan_rfc_pickle()), dst=str(TEST_RES_DIR.joinpath('miniloan-rfc.pkl')))
shutil.copy(src=str(miniloan_lr_pickle()), dst=str(TEST_RES_DIR.joinpath('miniloan-lr.pkl')))
shutil.copy(src=str(miniloan_rfr_pickle()), dst=str(TEST_RES_DIR.joinpath('miniloan-rfr.pkl')))

API_VER: Text = f'/v{VER}'


class TestEmbeddedClient(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp_dir: TemporaryDirectory = TemporaryDirectory()
        os.environ['model_storage'] = str(self.tmp_dir.name)
        self.client: TestClient = TestClient(app)

    def tearDown(self) -> None:
        self.tmp_dir.cleanup()


class TestGetInfo(TestEmbeddedClient):

    def setUp(self) -> None:
        super().setUp()
        with miniloan_rfc_pickle().open(mode='rb') as fd:
            res: Response = self.client.post(
                API_VER + "/models",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)

    def test_openapi(self):
        res: Response = self.client.get(url=API_VER + '/openapi.json')
        openapi: Dict = res.json()
        with OPENAPI_RESOURCE.open(mode='w') as fd:
            json.dump(obj=openapi, fp=fd)

    def test_get_server_status(self):
        res: Response = self.client.get(url=API_VER + '/status')
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, res.json().get('model_count'))

    def test_get_models(self):
        res: Response = self.client.get(url=API_VER + '/models')
        self.assertEqual(200, res.status_code)

        res_content: Dict = res.json()[0]

        self.assertEqual('miniloan-rfc', res_content['name'])
        self.assertEqual('v0', res_content['version'])
        self.assertEqual('predict_proba', res_content['method_name'])
        self.assertEqual(
            [{'name': 'creditScore', 'order': 0, 'type': 'int64'},
             {'name': 'income', 'order': 1, 'type': 'float64'},
             {'name': 'loanAmount', 'order': 2, 'type': 'float64'},
             {'name': 'monthDuration', 'order': 3, 'type': 'float64'},
             {'name': 'rate', 'order': 4, 'type': 'float64'}],
            res_content['input_schema'])
        self.assertEqual('Loan approval', res_content['metadata']['description'])
        self.assertEqual('ke', res_content['metadata']['author'])
        self.assertIsNotNone(res_content['metadata']['trained_at'])
        self.assertEqual(float, type(ast.literal_eval(res_content['metadata']['metrics'][0]['value'])))
        self.assertEqual(
            {'attributes': [{'name': 'prediction', 'type': 'str'}, {'name': 'probabilities', 'type': '[Probability]'}]},
            res_content['output_schema'])


class TestAddModel(TestEmbeddedClient):

    def test_add_model(self):
        with miniloan_rfc_pickle().open(mode='rb') as fd:
            contents: bytes = fd.read()

        print(pickle.loads(contents))
        res: Response = self.client.post(
            API_VER + "/models",
            files={'file': contents}
        )
        self.assertEqual(200, res.status_code)
        res: Response = self.client.get(url=API_VER + '/status')
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, res.json().get('model_count'))


class TestDeleteModel(TestEmbeddedClient):

    def setUp(self) -> None:
        super().setUp()
        with miniloan_rfc_pickle().open(mode='rb') as fd:
            res: Response = self.client.post(
                API_VER + "/models",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)

    def test_delete_model_by_name_and_version(self):
        res_delete: Response = self.client.delete(url=API_VER + '/models',
                                                  params={'model_name': 'miniloan-rfc', 'model_version': 'v0'})
        self.assertEqual(200, res_delete.status_code)

        info_2: Response = self.client.get(url=API_VER + '/status')
        self.assertEqual(200, info_2.status_code)
        self.assertEqual(0, info_2.json().get('model_count'))

    def test_delete_model_by_name(self):
        info_1: Response = self.client.get(url=API_VER + '/status')
        self.assertEqual(200, info_1.status_code)
        self.assertEqual(1, info_1.json().get('model_count'))

        res_delete: Response = self.client.delete(url=API_VER + '/models', params={'model_name': 'miniloan-rfc'})
        self.assertEqual(200, res_delete.status_code)

        info_2: Response = self.client.get(url=API_VER + '/status')
        self.assertEqual(200, info_2.status_code)
        self.assertEqual(0, info_2.json().get('model_count'))


class TestInvocation(TestEmbeddedClient):
    miniloan_input_params: List = [
        {
            "name": "creditScore",
            "value": 400
        }, {
            "name": "income",
            "value": 45000
        }, {
            "name": "loanAmount",
            "value": 100000
        }, {
            "name": "monthDuration",
            "value": 24
        }, {
            "name": "rate",
            "value": 2.0
        }
    ]

    def setUp(self) -> None:
        super().setUp()

        with miniloan_rfc_pickle().open(mode='rb') as fd:
            res: Response = self.client.post(
                API_VER + "/models",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)
        with miniloan_rfr_pickle().open(mode='rb') as fd:
            res: Response = self.client.post(
                API_VER + "/models",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)
        with miniloan_lr_pickle().open(mode='rb') as fd:
            res: Response = self.client.post(
                API_VER + "/models",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)
        with miniloan_rfc_no_class_names_pickle().open(mode='rb') as fd:
            res: Response = self.client.post(
                API_VER + "/models",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)

    def test_classification(self):
        res: Response = self.client.post(url=API_VER + '/invocations', json={
            "model_name": "miniloan-lr",
            "model_version": "v0",
            "params": TestInvocation.miniloan_input_params})
        self.assertEqual(200, res.status_code)
        self.assertTrue(res.json()['prediction'] in ['true', 'false'])

    def test_regression(self):
        res: Response = self.client.post(url=API_VER + '/invocations', json={
            "model_name": "miniloan-rfr",
            "model_version": "v0",
            "params": TestInvocation.miniloan_input_params
        })

        self.assertEqual(200, res.status_code)
        self.assertTrue(isinstance(ast.literal_eval(res.json()['prediction']), float))

    def test_predict_proba(self):
        res: Response = self.client.post(url=API_VER + '/invocations', json={
            "model_name": "miniloan-rfc",
            "model_version": "v0",
            "params": TestInvocation.miniloan_input_params
        })

        self.assertEqual(200, res.status_code)
        self.assertTrue(res.json()['prediction'] in ['true', 'false'])
        self.assertAlmostEqual(1.0, sum([f['value'] for f in res.json()['probabilities']]))

    def test_predict_proba_without_class_names(self):
        res: Response = self.client.post(url=API_VER + '/invocations', json={
            "model_name": "miniloan-rfc-no-output-schema",
            "model_version": "v0",
            "params": TestInvocation.miniloan_input_params
        })

        self.assertEqual(200, res.status_code)
        self.assertTrue(res.json()['prediction'] in ["0", "1"])
        self.assertAlmostEqual(1.0, sum([f['value'] for f in res.json()['probabilities']]))
