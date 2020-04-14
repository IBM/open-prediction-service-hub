#!/usr/bin/env python3

from __future__ import annotations

import os
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from typing import Text

from fastapi.testclient import TestClient

from dynamic_hosting import app

from dynamic_hosting.example_model_training import miniloan_rfc
from requests import Response


class TestEmbeddedClient(unittest.TestCase):
    def setUpC(self) -> None:
        self.tmp_dir: TemporaryDirectory = TemporaryDirectory()
        os.environ['model_storage'] = str(self.tmp_dir.name)
        self.client: TestClient = TestClient(app)

    def tearDown(self) -> None:
        self.tmp_dir.cleanup()


class TestServerConfiguration(TestEmbeddedClient):
    def setUp(self) -> None:
        super().setUpC()
        self.zipfile: Path = miniloan_rfc.train()
        with self.zipfile.open(mode='rb') as fd:
            res: Response = self.client.post(
                "/archives",
                headers={
                    'accept': 'application/json'
                },
                files={'file': fd}
            )
            self.assertEqual(200, res.status_code)

    def tearDown(self) -> None:
        super().tearDown()
        self.zipfile.unlink()

    def test_get_server_status(self):
        res: Response = self.client.get(url='/status')
        self.assertEqual(200, res.status_code)
        self.assertEqual(1, res.json().get('model_count'))
