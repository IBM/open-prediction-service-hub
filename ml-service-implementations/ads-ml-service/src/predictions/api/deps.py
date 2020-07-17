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


from typing import Generator

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from ..core.configuration import get_config
from ..core.open_prediction_service import OpenPredictionService
from ..db.session import SessionLocal

# reusable_oauth2: OAuth2PasswordBearer = OAuth2PasswordBearer(
#     tokenUrl=f'{get_config().API_VI_STR}/login/access-token'
# )

reusable_oauth2: OAuth2PasswordBearer = OAuth2PasswordBearer(
    tokenUrl=f'v1/login/access-token'
)


def get_db() -> Generator[Session, None , None]:
    db = None
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# Dependency
def get_ml_service(db: Session = Depends(get_db)) -> OpenPredictionService:
    mls: OpenPredictionService = OpenPredictionService(
        db=db,
        model_cache_size=get_config().MODEL_CACHE_SIZE,
        cache_ttl=get_config().CACHE_TTL
    )
    yield mls


# def get_current_user(
#     db: Session = Depends(get_db), token: Text = Depends(reusable_oauth2)
# ):
#     try:
#         payload = jwt.decode(
#             token, get_config().SECRET_KEY, algorithms=[security.ALGORITHM]
#         )
#         username: str = payload.get('sub')
#         if username is None:
#             raise credentials_exception
#         token_data = TokenData(username=username)
#     except PyJWTError:
#         raise credentials_exception
#     user = get_user(fake_users_db, username=token_data.username)
#     if user is None:
#         raise credentials_exception
#     return user
