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


from sqlalchemy.orm import Session

from ....core.configuration import get_config
from fastapi.testclient import TestClient

from .... import crud


def test_get_users_me(
    client: TestClient,
    user_token_header
):
    response = client.get(f'{get_config().API_V2_STR}/users/me', headers=user_token_header)

    assert response.status_code == 200
    assert 'username' in response.json()
    assert response.json()['username'] == get_config().USERNAME_TEST_USER


def test_update_users_me(
    db: Session,
    client: TestClient,
    user_token_header
):
    response = client.put(f'{get_config().API_V2_STR}/users/me', headers=user_token_header, json={
        'username': 'toto', 'password': 'toto'}
    )

    assert response.status_code == 200
    assert 'id' in response.json()
    assert 'username' in response.json()
    assert response.json()['username'] == 'toto'

    user_1 = crud.user.get(db, id=response.json()['id'])
    assert user_1.username == response.json()['username']

    authenticated_user_1 = crud.user.authenticate(db, username='toto', password='toto')
    assert authenticated_user_1 is not None
    assert authenticated_user_1.id == response.json()['id']
