#!/usr/bin/env python3

from __future__ import annotations

import ast
import json
import os
import shutil
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict
from typing import List

from dynamic_hosting import app
from fastapi.testclient import TestClient
from requests import Response
from tests.models import miniloan_lr, miniloan_rfc, miniloan_rfr

OPENAPI_RESOURCE: Path = Path(__file__).resolve().parents[2].joinpath('resources').joinpath('openapi.json')

TEST_RES_DIR: Path = Path(__file__).resolve().parents[3].joinpath('test').joinpath('resources')
MINILOAN_LR: Path = TEST_RES_DIR.joinpath('miniloan-lr.zip')
MINILOAN_RFC: Path = TEST_RES_DIR.joinpath('miniloan-rfc.zip')
MINILOAN_RFR: Path = TEST_RES_DIR.joinpath('miniloan-rfr.zip')


class TestEmbeddedClient(unittest.TestCase):

    def setUp(self) -> None:
        self.tmp_dir: TemporaryDirectory = TemporaryDirectory()
        os.environ['model_storage'] = str(self.tmp_dir.name)
        self.client: TestClient = TestClient(app)

    def tearDown(self) -> None:
        self.tmp_dir.cleanup()


class TestGetInfo(TestEmbeddedClient):

    @classmethod
    def setUpClass(cls) -> None:
        shutil.copy(src=str(miniloan_rfc()), dst=str(MINILOAN_RFC))

    def setUp(self) -> None:
        super().setUp()
        with MINILOAN_RFC.open(mode='rb') as fd:
            res: Response = self.client.post(
                "/models",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)

    def test_openapi(self):
        res: Response = self.client.get(url='/openapi.json')
        openapi: Dict = res.json()
        with OPENAPI_RESOURCE.open(mode='w') as fd:
            json.dump(obj=openapi, fp=fd)

    def test_get_server_status(self):
        res: Response = self.client.get(url='/status')
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, res.json().get('model_count'))

    def test_get_models(self):
        res: Response = self.client.get(url='/models')
        self.assertEqual(200, res.status_code)

        res_content: Dict = res.json()[0]

        self.assertEqual('miniloan-rfc', res_content['name'])
        self.assertEqual('v0', res_content['version'])
        self.assertEqual('predict_proba', res_content['method_name'])
        self.assertEqual(
            [{'name': 'creditScore', 'order': 0, 'type': 'int64'},
             {'name': 'income', 'order': 1, 'type': 'float32'},
             {'name': 'loanAmount', 'order': 2, 'type': 'float64'},
             {'name': 'monthDuration', 'order': 3, 'type': 'float64'},
             {'name': 'rate', 'order': 4, 'type': 'float64'}],
            res_content['input_schema'])
        self.assertEqual('Loan approval', res_content['metadata']['description'])
        self.assertEqual('ke', res_content['metadata']['author'])
        self.assertIsNotNone(res_content['metadata']['trained_at'])
        self.assertEqual([{'name': 'accuracy', 'value': '0.9843875100080064'}], res_content['metadata']['metrics'])
        self.assertEqual(None, res_content['output_schema'])


class TestAddModel(TestEmbeddedClient):

    def test_add_model(self):
        with MINILOAN_RFC.open(mode='rb') as fd:
            res: Response = self.client.post(
                "/models",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)
        res: Response = self.client.get(url='/status')
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, res.json().get('model_count'))


class TestDeleteModel(TestEmbeddedClient):

    @classmethod
    def setUpClass(cls) -> None:
        shutil.copy(src=str(miniloan_rfc()), dst=str(MINILOAN_RFC))

    def setUp(self) -> None:
        super().setUp()
        with MINILOAN_RFC.open(mode='rb') as fd:
            res: Response = self.client.post(
                "/models",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)

    def test_delete_model(self):
        info_1: Response = self.client.get(url='/status')
        self.assertEqual(200, info_1.status_code)
        self.assertEqual(1, info_1.json().get('model_count'))

        res_delete: Response = self.client.delete(url='/models',
                                                  params={'model_name': 'miniloan-rfc', 'model_version': 'v0'})
        self.assertEqual(200, res_delete.status_code)

        info_2: Response = self.client.get(url='/status')
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

    @classmethod
    def setUpClass(cls) -> None:
        shutil.copy(src=str(miniloan_rfc()), dst=str(MINILOAN_RFC))
        shutil.copy(src=str(miniloan_lr()), dst=str(MINILOAN_LR))
        shutil.copy(src=str(miniloan_rfr()), dst=str(MINILOAN_RFR))

    def setUp(self) -> None:
        super().setUp()

        with MINILOAN_RFC.open(mode='rb') as fd:
            res: Response = self.client.post(
                "/models",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)
        with MINILOAN_RFR.open(mode='rb') as fd:
            res: Response = self.client.post(
                "/models",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)
        with MINILOAN_LR.open(mode='rb') as fd:
            res: Response = self.client.post(
                "/models",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)

    def test_classification(self):
        res: Response = self.client.post(url='/invocations', json={
            "model_name": "miniloan-lr",
            "model_version": "v0",
            "params": TestInvocation.miniloan_input_params})
        self.assertEqual(200, res.status_code)
        self.assertTrue(res.json()['prediction'] in ['true', 'false'])

    def test_regression(self):
        res: Response = self.client.post(url='/invocations', json={
            "model_name": "miniloan-rfr",
            "model_version": "v0",
            "params": TestInvocation.miniloan_input_params
        })

        self.assertEqual(200, res.status_code)
        self.assertTrue(isinstance(ast.literal_eval(res.json()['prediction']), float))

    def test_predict_proba(self):
        res: Response = self.client.post(url='/invocations', json={
            "model_name": "miniloan-rfc",
            "model_version": "v0",
            "params": TestInvocation.miniloan_input_params
        })

        self.assertEqual(200, res.status_code)
        self.assertTrue(res.json()['prediction'] in ['true', 'false'])
        self.assertAlmostEqual(1.0, sum([f['proba'] for f in res.json()['probabilities']]))
