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

import os
import tempfile
import unittest
from pathlib import Path
from typing import Dict

import yaml
from dynamic_hosting.core.configuration import ServerConfiguration


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
            self.assertRaises(PermissionError, ServerConfiguration, MODEL_STORAGE=model_storage)
            model_storage.chmod(mode=0o700)  # help cleanup

    def test_model_storage_not_writable(self):
        with tempfile.TemporaryDirectory() as test_env:
            test_env_path: Path = Path(test_env)
            model_storage: Path = test_env_path.joinpath('test_model_storage')
            model_storage.mkdir(mode=0o100)
            self.assertRaises(PermissionError, ServerConfiguration, MODEL_STORAGE=model_storage)
            model_storage.chmod(mode=0o700)  # help cleanup

    def test_conf_file_not_exist(self):
        not_existing_config_file: Path = Path('./not_exist.yaml')
        self.assertRaises(ValueError, ServerConfiguration.from_yaml, not_existing_config_file)

    def test_model_storage_not_exist(self):
        not_existing_model_storage: Path = Path('./not_exist')
        self.assertRaises(ValueError, ServerConfiguration, MODEL_STORAGE=not_existing_model_storage)

    def test_env_not_exist(self):
        if os.environ.get('MODEL_STORAGE'):
            del os.environ['MODEL_STORAGE']
        self.assertRaises(ValueError, ServerConfiguration)

    def test_valid_conf_file(self):
        with tempfile.TemporaryDirectory() as model_storage:
            with tempfile.NamedTemporaryFile(mode='x') as config_file:
                conf: Dict = {'MODEL_STORAGE': model_storage}
                conf_file_path: Path = Path(config_file.name)
                with conf_file_path.open(mode='w') as fd:
                    yaml.dump(conf, fd)
                ServerConfiguration.from_yaml(conf_file_path)

    def test_valid_env(self):
        storage: Path = Path(__file__).resolve().parents[4].joinpath('runtime').joinpath('storage')
        os.environ['MODEL_STORAGE'] = str(storage)
        ServerConfiguration()
