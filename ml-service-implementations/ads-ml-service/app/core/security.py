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


from datetime import datetime, timedelta
from typing import Union, Text, Any

import jwt
from passlib.context import CryptContext

from ..core.configuration import get_config


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

ALGORITHM = 'HS256'


def create_access_token(
    subject: Union[Text, Any], expires_delta: timedelta = None
) -> Text:
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=get_config().ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {'sub': str(subject), 'exp': expire}
    encoded_jwt = jwt.encode(to_encode, get_config().SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_pwd(plain_password: Text, hashed_password: Text) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_pwd_hash(password: Text) -> Text:
    return pwd_context.hash(password)
