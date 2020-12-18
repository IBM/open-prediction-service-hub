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


from typing import Any
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ... import deps
from .... import crud
from ....core.configuration import get_config
from .... import schemas
from ....core import security
from .... import models

router = APIRouter()


@router.post('/login/access-token', response_model=schemas.Token, include_in_schema=False)
def login_access_token(
        db: Session = Depends(deps.get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    user = crud.user.authenticate(
        db, username=form_data.username, password=form_data.password
    )
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Incorrect username of password'
        )
    access_token_expires = timedelta(minutes=get_config().ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        'access_token': security.create_access_token(
            subject=user.id, expires_delta=access_token_expires
        ),
        'token_type': 'bearer'
    }


@router.post('/login/test-token', response_model=schemas.User, include_in_schema=False)
def test_token(
      current_user: models.User = Depends(deps.get_current_user)
) -> Any:
    return current_user
