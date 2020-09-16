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

import fastapi
import fastapi.security as fsec
import jwt
import pydantic as pyd
import sqlalchemy.orm as saorm
import starlette.status as status

import app.core.configuration as conf
import app.core.security as security
import app.crud as crud
import app.db.session as session
import app.models as models
import app.schemas as schemas

reusable_oauth2 = fsec.OAuth2PasswordBearer(
    tokenUrl=f'/login/access-token'
)


def get_db() -> typing.Iterable[saorm.Session]:
    db = None
    try:
        db = session.SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
        db: saorm.Session = fastapi.Depends(get_db), token: typing.Text = fastapi.Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, conf.get_config().SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.token.TokenData(**payload)
    except (jwt.PyJWTError, pyd.ValidationError):
        raise fastapi.HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not valid credentials'
        )
    user = crud.user.get(db, id=token_data.sub)
    if user is None:
        raise fastapi.HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user
