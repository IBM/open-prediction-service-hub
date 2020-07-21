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


from typing import Generator, Text

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from app.core import security
from pydantic import ValidationError
from sqlalchemy.orm import Session

from ..core.configuration import get_config
from ..core.open_prediction_service import OpenPredictionService
from ..db.session import SessionLocal
from .. import schemas
from .. import crud
from .. import models

reusable_oauth2: OAuth2PasswordBearer = OAuth2PasswordBearer(
    tokenUrl=f'{get_config().API_V2_STR}/login/access-token'
)


def get_db() -> Generator[Session, None, None]:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Dependency
def get_ml_service(db: Session = Depends(get_db)) -> Generator[OpenPredictionService, None, None]:
    yield OpenPredictionService(db=db)


def get_current_user(
    db: Session = Depends(get_db), token: Text = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, get_config().SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        token_data = schemas.token.TokenData(**payload)
    except (PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail='Not valid credentials'
        )
    user = crud.user.get(db, id=token_data.sub)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')
    return user
