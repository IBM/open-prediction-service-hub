#!/usr/bin/env python3

from __future__ import annotations

import ast
import os
import tempfile
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Dict
from typing import List

import yaml
from dynamic_hosting import app
from dynamic_hosting.core.configuration import ServerConfiguration
from fastapi.testclient import TestClient
from requests import Response
from tests.models import miniloan_lr, miniloan_rfc, miniloan_rfr


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
        with miniloan_rfc().open(mode='rb') as fd:
            res: Response = self.client.post(
                "/models",
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
        with miniloan_rfr().open(mode='rb') as fd:
            res: Response = self.client.post(
                "/models",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)
        res: Response = self.client.get(url='/status')
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, res.json().get('model_count'))


class TestDeleteModel(TestEmbeddedClient):
    def setUp(self) -> None:
        super().setUp()
        with miniloan_rfc().open(mode='rb') as fd:
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
        super(TestInvocation, cls).setUpClass()

    def setUp(self) -> None:
        super().setUp()
        with miniloan_rfc().open(mode='rb') as fd:
            res: Response = self.client.post(
                "/models",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)
        with miniloan_rfr().open(mode='rb') as fd:
            res: Response = self.client.post(
                "/models",
                files={'file': fd}
            )
        self.assertEqual(200, res.status_code)
        with miniloan_lr().open(mode='rb') as fd:
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


class TestServerConfiguration(unittest.TestCase):

    def test_conf_file_not_readable(self):
        with tempfile.NamedTemporaryFile(mode='x') as config_file:
            # 'x' mode open for exclusive creation, failing if the file already exists
            tmp_config_file_path: Path = Path(config_file.name)
            tmp_config_file_path.chmod(0o100)
            self.assertRaises(PermissionError, ServerConfiguration.from_yaml, tmp_config_file_path)

    def test_model_storage_not_readable(self):
        with tempfile.TemporaryDirectory() as test_env:
            test_env_path: Path = Path(test_env)
            model_storage: Path = test_env_path.joinpath('test_model_storage')
            model_storage.mkdir(mode=0o300)
            self.assertRaises(PermissionError, ServerConfiguration, model_storage=model_storage)
            model_storage.chmod(mode=0o700)  # help cleanup

    def test_model_storage_not_writable(self):
        with tempfile.TemporaryDirectory() as test_env:
            test_env_path: Path = Path(test_env)
            model_storage: Path = test_env_path.joinpath('test_model_storage')
            model_storage.mkdir(mode=0o500)
            self.assertRaises(PermissionError, ServerConfiguration, model_storage=model_storage)

    def test_conf_file_not_exist(self):
        not_existing_config_file: Path = Path('./not_exist.yaml')
        self.assertRaises(ValueError, ServerConfiguration.from_yaml, not_existing_config_file)

    def test_model_storage_not_exist(self):
        not_existing_model_storage: Path = Path('./not_exist')
        self.assertRaises(ValueError, ServerConfiguration, model_storage=not_existing_model_storage)

    def test_env_not_exist(self):
        if os.environ.get('model_storage'):
            del os.environ['model_storage']
        self.assertRaises(ValueError, ServerConfiguration)

    def test_valid_conf_file(self):
        with tempfile.TemporaryDirectory() as model_storage:
            with tempfile.NamedTemporaryFile(mode='x') as config_file:
                conf: Dict = {'model_storage': model_storage}
                conf_file_path: Path = Path(config_file.name)
                with conf_file_path.open(mode='w') as fd:
                    yaml.dump(conf, fd)
                ServerConfiguration.from_yaml(conf_file_path)

    def test_valid_env(self):
        storage: Path = Path(__file__).resolve().parents[4].joinpath('runtime').joinpath('storage')
        os.environ['model_storage'] = str(storage)
        ServerConfiguration()
