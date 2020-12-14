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


from typing import Text, Dict

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from .utils import random_string
from ... import crud
from ...schemas import UserCreate, UserUpdate
from ...core.configuration import get_config


def user_auth_header(
    *, client: TestClient, username: Text, password: Text
) -> Dict[Text, Text]:
    login = {
        'username': username,
        'password': password
    }
    response = client.post(f'{get_config().API_V2_STR}/login/access-token', data=login)
    token = response.json()['access_token']
    header = {'Authorization': f'Bearer {token}'}
    return header


def create_random_user(db: Session):
    username = random_string()
    password = random_string()
    user_in = UserCreate(username=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    return user


def auth_token_from_username(
    *, client: TestClient, username: Text, db: Session
):
    """
    User is created if not exist
    """
    password = random_string()
    user = crud.user.get_by_username(db, username=username)
    if user is None:
        user_create = UserCreate(username=username, password=password)
        crud.user.create(db, obj_in=user_create)
    else:
        user_update = UserUpdate(password=password)
        crud.user.update(db, db_obj=user, obj_in=user_update)
    return user_auth_header(client=client, username=username, password=password)
