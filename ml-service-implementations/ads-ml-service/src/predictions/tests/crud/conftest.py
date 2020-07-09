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

import pytest
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

from ..utils.utils import random_string
from ...db.base import Base
from ...schemas.user import UserCreate


# In memory sqlite database for testing
@pytest.fixture(scope='module')
def db() -> Generator:
    engine = create_engine('sqlite://', connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    sm_instance = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    db = sm_instance()
    try:
        yield db
    finally:
        db.close()


# Data for user create
@pytest.fixture
def random_user() -> UserCreate:
    username = random_string()
    password = random_string()
    return UserCreate(username=username, password=password)
