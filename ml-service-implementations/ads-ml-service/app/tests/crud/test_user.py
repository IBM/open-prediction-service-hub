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

import sqlalchemy.orm as orm

import app.core.security as security
import app.crud as crud
import app.schemas as schemas
import app.tests.utils.utils as utils


def test_create_user(db: orm.Session, random_user: schemas.UserCreate) -> typing.NoReturn:
    user = crud.user.create(db, obj_in=random_user)

    assert user.username == random_user.username
    assert security.verify_pwd(random_user.password, user.hashed_password)


def test_authenticate_user_good_passwd(db: orm.Session, random_user: schemas.UserCreate) -> typing.NoReturn:
    user = crud.user.create(db, obj_in=random_user)
    authenticated_user = crud.user.authenticate(db, username=user.username, password=random_user.password)

    assert authenticated_user is not None
    assert authenticated_user.id == user.id
    assert authenticated_user.username == random_user.username
    assert authenticated_user.hashed_password == user.hashed_password


def test_authenticate_user_bad_passwd(db: orm.Session, random_user: schemas.UserCreate) -> typing.NoReturn:
    user = crud.user.create(db, obj_in=random_user)
    not_authenticated_user = crud.user.authenticate(db, username=user.username, password='bad-password')

    assert not_authenticated_user is None


def test_authenticate_user_not_existing(db: orm.Session, random_user: schemas.UserCreate) -> typing.NoReturn:
    crud.user.create(db, obj_in=random_user)
    not_authenticated_user = crud.user.authenticate(db, username='not-existing', password='bad-password')

    assert not_authenticated_user is None


def test_get_user(db: orm.Session, random_user: schemas.UserCreate) -> typing.NoReturn:
    user = crud.user.create(db, obj_in=random_user)
    user_1 = crud.user.get(db, id=user.id)

    assert user_1.id == user.id
    assert user_1.username == user.username
    assert user_1.hashed_password == user.hashed_password


def test_get_user_by_username(db: orm.Session, random_user: schemas.UserCreate) -> typing.NoReturn:
    user = crud.user.create(db, obj_in=random_user)
    user_1 = crud.user.get_by_username(db, username=user.username)

    assert user_1.id == user.id
    assert user_1.username == user.username
    assert user_1.hashed_password == user.hashed_password


def test_update_passwd(db: orm.Session, random_user: schemas.UserCreate) -> typing.NoReturn:
    user = crud.user.create(db, obj_in=random_user)
    old_hashed_passwd = user.hashed_password
    new_pwd = utils.random_string()
    user_1 = crud.user.update(db, db_obj=user, obj_in=schemas.UserUpdate(password=new_pwd))
    user_2 = crud.user.authenticate(db, username=user.username, password=random_user.password)
    user_3 = crud.user.authenticate(db, username=user.username, password=new_pwd)

    assert user_1.id == user.id
    assert user_1.hashed_password != old_hashed_passwd
    assert user_2 is None
    assert user_3 is not None


def test_update_username(db: orm.Session, random_user: schemas.UserCreate) -> typing.NoReturn:
    user = crud.user.create(db, obj_in=random_user)
    old_username = user.username
    new_username = utils.random_string()
    user_update = schemas.UserUpdate(username=new_username)
    user_1 = crud.user.update(db, db_obj=user, obj_in=user_update)
    user_2 = crud.user.authenticate(db, username=old_username, password=random_user.password)
    user_3 = crud.user.authenticate(db, username=new_username, password=random_user.password)

    assert user_1.id == user.id
    assert user_1.username != old_username
    assert user_2 is None
    assert user_3 is not None


def test_delete_user(db: orm.Session, random_user: schemas.UserCreate) -> typing.NoReturn:
    user = crud.user.create(db, obj_in=random_user)
    user_1 = crud.user.delete(db, id=user.id)
    user_2 = crud.user.get(db, id=user.id)

    assert user_1.id == user.id
    assert user_1.username == user.username
    assert user_1.hashed_password == user.hashed_password
    assert user_2 is None
