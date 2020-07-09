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


from typing import NoReturn

from sqlalchemy.orm import Session

from ..utils.utils import random_string
from ... import crud
from ...schemas.user import UserCreate


def test_create_user(db: Session) -> NoReturn:
    username = random_string()
    password = random_string()
    user_in = UserCreate(username=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    assert user.username == username
    assert hasattr(user, 'hashed_password')
