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


import typing

import fastapi.testclient as tstc

import app.core.configuration as conf


def test_get_server_capabilities(
        client: tstc.TestClient
) -> typing.NoReturn:
    response = client.get(f'{conf.get_config().API_V2_STR}/capabilities')
    content = response.json()

    assert response.status_code == 200
    assert content['capabilities']
    assert 'info' in content['capabilities']
    assert 'discover' in content['capabilities']
    assert 'manage' in content['capabilities']
    assert 'run' in content['capabilities']
    assert 'download' in content['capabilities']
    assert 'metadata' in content['capabilities']


def test_get_managed_capabilities(
        client: tstc.TestClient,
        test_upload_size_limit
):
    response = client.get(f'{conf.get_config().API_V2_STR}/capabilities')
    content = response.json()

    assert response.status_code == 200
    assert content['managed_capabilities']
    assert 'supported_input_data_structure' in content['managed_capabilities']
    assert 'supported_output_data_structure' in content['managed_capabilities']
    assert 'supported_binary_format' in content['managed_capabilities']
    assert 'supported_upload_format' in content['managed_capabilities']
    assert 'auto' in content['managed_capabilities']['supported_input_data_structure']
    assert 'auto' in content['managed_capabilities']['supported_input_data_structure']
    assert 'joblib' in content['managed_capabilities']['supported_binary_format']
    assert 'pickle' in content['managed_capabilities']['supported_binary_format']
    assert 'pmml' in content['managed_capabilities']['supported_binary_format']
    assert 'pmml' in content['managed_capabilities']['supported_upload_format']
    assert content['managed_capabilities']['file_size_limit'] == test_upload_size_limit
