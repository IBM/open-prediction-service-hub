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


from fastapi.testclient import TestClient
from app.core.configuration import get_config
from app.version import __version__


def test_get_server_capabilities(
    client: TestClient
) -> None:
    response = client.get(f'{get_config().API_V2_STR}/capabilities')
    content = response.json()

    assert response.status_code == 200
    assert content['capabilities']
    assert 'info' in content['capabilities']
    assert 'discover' in content['capabilities']
    assert 'manage' in content['capabilities']
    assert 'run' in content['capabilities']
