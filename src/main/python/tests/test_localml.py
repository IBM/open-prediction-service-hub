#!/usr/bin/env python3

from __future__ import annotations

import os
import unittest
from tempfile import TemporaryDirectory
from typing import Dict, List

from dynamic_hosting import app
from dynamic_hosting.example_model_training import miniloan_rfc, miniloan_rfr, miniloan_lr
from fastapi.testclient import TestClient
from requests import Response


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
        with miniloan_rfc.train().open(mode='rb') as fd:
            res: Response = self.client.post(
                "/archives",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)

    def test_get_server_status(self):
        res: Response = self.client.get(url='/status')
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, res.json().get('model_count'))

    def test_get_models(self):
        res: Response = self.client.get(url='/models')
        self.assertEqual(200, res.status_code)

        res_content: Dict = res.json()[0]
        print(res_content)
        self.assertEqual('miniloan-rfc', res_content['name'])
        self.assertEqual('v0', res_content['version'])
        self.assertEqual('predict_proba', res_content['method_name'])
        self.assertEqual('PREDICT_PROBA', res_content['type'])
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
        with miniloan_rfr.train().open(mode='rb') as fd:
            res: Response = self.client.post(
                "/archives",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)
        res: Response = self.client.get(url='/status')
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, res.json().get('model_count'))


class TestDeleteModel(TestEmbeddedClient):
    def setUp(self) -> None:
        super().setUp()
        with miniloan_rfc.train().open(mode='rb') as fd:
            res: Response = self.client.post(
                "/archives",
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

    def setUp(self) -> None:
        super().setUp()
        with miniloan_rfc.train().open(mode='rb') as fd:
            res: Response = self.client.post(
                "/archives",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)
        with miniloan_rfr.train().open(mode='rb') as fd:
            res: Response = self.client.post(
                "/archives",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)
        with miniloan_lr.train().open(mode='rb') as fd:
            res: Response = self.client.post(
                "/archives",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)

    def test_classification(self):
        res: Response = self.client.post(url='/classification', json={
            "model_name": "miniloan-lr",
            "model_version": "v0",
            "params": TestInvocation.miniloan_input_params})
        self.assertEqual(200, res.status_code)
        self.assertTrue(res.json()['classification_output'] in ['true', 'false'])

    def test_regression(self):
        res: Response = self.client.post(url='/regression', json={
            "model_name": "miniloan-rfr",
            "model_version": "v0",
            "params": TestInvocation.miniloan_input_params
        })
        print(res.json())
        self.assertEqual(200, res.status_code)
        self.assertTrue(isinstance(res.json()['regression_output'], float))

    def test_predict_proba(self):
        res: Response = self.client.post(url='/predict_proba', json={
            "model_name": "miniloan-rfc",
            "model_version": "v0",
            "params": TestInvocation.miniloan_input_params
        })
        print(res.json())
        self.assertEqual(200, res.status_code)
        self.assertTrue(res.json()['predict_output'] in ['true', 'false'])
        self.assertAlmostEqual(1.0, sum([f['proba'] for f in res.json()['probabilities']]))


if __name__ == '__main__':
    unittest.main()
