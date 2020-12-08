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
import app.crud.base as app_crud_base
import app.models as models
import app.schemas as schemas


class CRUDUser(app_crud_base.CRUDBase[models.User, schemas.UserCreate, schemas.UserUpdate]):
    def get_by_username(self, db: orm.Session, *, username: typing.Text) -> typing.Optional[models.User]:
        return db.query(self.model).filter(self.model.username == username).first()

    def create(self, db: orm.Session, *, obj_in: schemas.UserCreate) -> models.User:
        # noinspection PyArgumentList
        db_obj = self.model(
            username=obj_in.username,
            hashed_password=security.get_pwd_hash(obj_in.password).encode()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: orm.Session, *, db_obj: models.User,
            obj_in: typing.Union[schemas.UserUpdate, typing.Dict[typing.Text, typing.Any]]
    ) -> models.User:
        update_data = obj_in if isinstance(obj_in, typing.Dict) else obj_in.dict(exclude_unset=True)
        if update_data.get('password'):
            hashed_password = security.get_pwd_hash(update_data['password'])
            del update_data['password']
            update_data['hashed_password'] = hashed_password.encode()
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
            self, db: orm.Session, *, username: typing.Text, password: typing.Text
    ) -> typing.Optional[models.User]:
        user_ = self.get_by_username(db, username=username)
        return user_ \
            if user_ is not None and security.verify_pwd(password, user_.hashed_password) \
            else None  # User not exist / passwd error


user = CRUDUser(models.User)
