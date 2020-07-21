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


from ....core.configuration import get_config
from fastapi.testclient import TestClient


def test_get_access_token(
    client: TestClient
) -> None:
    login = {
        'username': get_config().DEFAULT_USER,
        'password': get_config().DEFAULT_USER_PWD
    }
    response = client.post(f'{get_config().API_V2_STR}/login/access-token', data=login)

    assert response.status_code == 200
    assert 'access_token' in response.json()


def test_use_access_token(
    client: TestClient,
    user_token_header
) -> None:
    response = client.post(f'{get_config().API_V2_STR}/login/test-token', headers=user_token_header)

    assert response.status_code == 200
    assert 'username' in response.json()
    assert response.json()['username'] == get_config().USERNAME_TEST_USER
