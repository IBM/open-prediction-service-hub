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

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import sessionmaker

from ..core.configuration import ServerConfiguration, get_config
from ..db import models
from ..core.open_predict_service import PredictionService

DATABASE_NAME: Text = 'EML.db'


# Dependency
def get_ml_service() -> PredictionService:
    engine: Engine = create_engine(
        f'sqlite:///{ServerConfiguration().MODEL_STORAGE.joinpath(DATABASE_NAME)}',
        connect_args={"check_same_thread": False}
    )
    models.Base.metadata.create_all(bind=engine)
    sm_instance: sessionmaker = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine
    )
    db = None
    try:
        db = sm_instance()
        mls: PredictionService = PredictionService(
            db=db,
            model_cache_size=get_config().MODEL_CACHE_SIZE,
            cache_ttl=get_config().CACHE_TTL
        )
        yield mls
    finally:
        db.close()
