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

import logging
from typing import Text, Any, Dict, NoReturn, Optional, List, Tuple

from sqlalchemy.orm import Session
from expiringdict import ExpiringDict

from .core.model import Model, MLSchema
from .db.crud import create_model, delete_model, read_model, read_model_schemas, count_models


class PredictionService:
    # Cache need to be global to all service instances
    MODEL_CACHE: ExpiringDict = None
    MODEL_CONFIGS_CACHE: ExpiringDict = None

    def __init__(self, db: Session, model_cache_size: int, cache_ttl: int):
        self.db: Session = db
        if PredictionService.MODEL_CACHE is None:
            PredictionService.MODEL_CACHE = ExpiringDict(max_len=model_cache_size, max_age_seconds=cache_ttl)
        if PredictionService.MODEL_CONFIGS_CACHE is None:
            PredictionService.MODEL_CONFIGS_CACHE = ExpiringDict(max_len=1, max_age_seconds=cache_ttl)

    def add_model(
            self, m: Model
    ) -> None:
        create_model(self.db, m)

    def remove_model(
            self,
            model_name: Text,
            model_version: Optional[Text] = None
    ) -> None:
        delete_model(self.db, model_name=model_name, model_version=model_version)

    def get_model(
            self,
            model_name: Text,
            model_version: Text
    ) -> Model:
        logger = logging.getLogger(__name__)
        key: Tuple[Text, Text] = (model_name, model_version)
        m: Model
        try:
            m = PredictionService.MODEL_CACHE[key]
        except KeyError:
            logger.debug(f'model {key} cache miss')
            m = read_model(self.db, model_name=model_name, model_version=model_version)
            PredictionService.MODEL_CACHE.__setitem__(key=key, value=m)
        return m

    def get_model_configs(self) -> List[MLSchema]:
        logger = logging.getLogger(__name__)
        configs: List[MLSchema]
        try:
            configs = PredictionService.MODEL_CONFIGS_CACHE['model_configs']
        except KeyError:
            logger.debug('model_configs cache miss')
            configs = read_model_schemas(self.db)
            PredictionService.MODEL_CONFIGS_CACHE.__setitem__(key='model_configs', value=configs)
        return configs

    def count_models(self) -> int:
        return count_models(self.db)

    def invoke(
            self,
            model_name: Text,
            model_version: Text,
            data: Dict
    ) -> Any:
        logger = logging.getLogger(__name__)
        logger.debug('Invoke ml model <{name}> version <{version}>'.format(name=model_name, version=model_version))

        return self.get_model(model_name=model_name, model_version=model_version).invoke(data_input=data)

    def add_archive(
            self,
            archive: bytes
    ) -> NoReturn:
        model: Model = Model.from_pickle(
            pickle_file=archive
        )
        self.add_model(model)
