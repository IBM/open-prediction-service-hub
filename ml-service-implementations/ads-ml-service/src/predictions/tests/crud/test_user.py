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

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ..utils.utils import random_string
from ... import crud
from ...core.security import verify_pwd
from ...schemas.user import UserCreate, UserUpdate


def test_create_user(db: Session, random_user: UserCreate) -> NoReturn:
    user = crud.user.create(db, obj_in=random_user)
    assert user.username == random_user.username
    assert hasattr(user, 'hashed_password')


def test_authenticate_user(db: Session, random_user: UserCreate) -> NoReturn:
    user = crud.user.create(db, obj_in=random_user)
    authenticated_user = crud.user.authenticate(db, username=random_user.username, password=random_user.password)
    assert authenticated_user is not None
    assert user.username == authenticated_user.username


def test_get_user(db: Session, random_user: UserCreate) -> NoReturn:
    user = crud.user.create(db, obj_in=random_user)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user_2.username == user.username
    assert jsonable_encoder(user_2) == jsonable_encoder(user)


def test_get_user_by_username(db: Session, random_user: UserCreate) -> NoReturn:
    user = crud.user.create(db, obj_in=random_user)
    user_2 = crud.user.get_by_username(db, username=user.username)
    assert user_2
    assert user_2.id == user.id
    assert jsonable_encoder(user_2) == jsonable_encoder(user)


def test_update_user(db: Session, random_user: UserCreate) -> NoReturn:
    user = crud.user.create(db, obj_in=random_user)
    new_pwd = random_string()
    user_update = UserUpdate(password=new_pwd)
    crud.user.update(db, db_obj=user, obj_in=user_update)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user_2.username == user.username
    assert verify_pwd(new_pwd, user_2.hashed_password)


def test_delete_user(db: Session, random_user: UserCreate) -> NoReturn:
    user = crud.user.create(db, obj_in=random_user)
    user_2 = crud.user.delete(db, id=user.id)
    assert user_2.id == user.id
    assert user_2.username == random_user.username
    assert crud.user.get(db, id=user.id) is None
