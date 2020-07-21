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


from typing import Text

from app.schemas import UserUpdate
from fastapi import APIRouter, Depends, Body
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from ... import deps
from .... import crud
from .... import models
from .... import schemas

router = APIRouter()


@router.get('/me', response_model=schemas.User)
def get_user_self(
    *,
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Get current user
    """
    return current_user


@router.put('/me', response_model=schemas.User)
def update_user_self(
    *,
    db: Session = Depends(deps.get_db),
    username: Text = Body(None),
    password: Text = Body(None),
    current_user: models.User = Depends(deps.get_current_user)
):
    """
    Update current user
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdate(**current_user_data)
    if username is not None:
        user_in.username = username
    if password is not None:
        user_in.password = password
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user
