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


import os
import tempfile
from pathlib import Path

import pytest
from app.core.configuration import ServerConfiguration


def test_model_storage_not_readable():
    with tempfile.TemporaryDirectory() as test_env:
        test_env_path: Path = Path(test_env)
        model_storage: Path = test_env_path.joinpath('test_model_storage')
        model_storage.mkdir(mode=0o300)
        with pytest.raises(PermissionError):
            ServerConfiguration(MODEL_STORAGE=model_storage)
        model_storage.chmod(mode=0o700)  # help cleanup


def test_model_storage_not_writable():
    with tempfile.TemporaryDirectory() as test_env:
        test_env_path: Path = Path(test_env)
        model_storage: Path = test_env_path.joinpath('test_model_storage')
        model_storage.mkdir(mode=0o100)
        with pytest.raises(PermissionError):
            ServerConfiguration(MODEL_STORAGE=model_storage)
        model_storage.chmod(mode=0o700)  # help cleanup


def test_model_storage_not_exist():
    not_existing_model_storage: Path = Path('./not_exist')
    with pytest.raises(ValueError):
        ServerConfiguration(MODEL_STORAGE=not_existing_model_storage)


def test_env_not_exist():
    if os.environ.get('MODEL_STORAGE'):
        del os.environ['MODEL_STORAGE']
    with pytest.raises(ValueError):
        ServerConfiguration()


def test_valid_env():
    os.environ['MODEL_STORAGE'] = str('/tmp')
    ServerConfiguration()
