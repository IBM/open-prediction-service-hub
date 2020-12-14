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


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.configuration import get_config

engine = create_engine(
    f'sqlite:///{get_config().MODEL_STORAGE.joinpath(get_config().DATABASE_NAME)}',
    connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
)
