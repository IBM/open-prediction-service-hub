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
import pickle
from threading import Lock
from typing import Text, Any, Dict, NoReturn, Optional, List, Tuple

from expiringdict import ExpiringDict
from sqlalchemy.orm import Session

from .. import crud
from .. import schemas
from ..core.configuration import get_config
from ..core.model import Model
from ..schemas.model import MLSchema, ModelCreate


class OpenPredictionService:
    # Cache need to be global to all service instances
    MODEL_CACHE: ExpiringDict = None
    # Cache needs to be initiated once per worker
    lock = Lock()

    def __init__(self, db: Session):
        self.db: Session = db
        with OpenPredictionService.lock:
            if OpenPredictionService.MODEL_CACHE is None:
                OpenPredictionService.MODEL_CACHE = ExpiringDict(
                    max_len=get_config().MODEL_CACHE_SIZE,
                    max_age_seconds=get_config().CACHE_TTL
                )

    def add_model(
            self, m: Model
    ) -> None:
        binary_in = schemas.binary_ml_model.BinaryMLModelCreate(model_b64=pickle.dumps(m.model))
        config_in = schemas.model_config.ModelConfigCreate(**m.info.dict())
        model_in = ModelCreate(binary=binary_in, config=config_in, name=m.info.name, version=m.info.version)
        crud.crud_model.model.create(self.db, obj_in=model_in)

    def remove_model(
            self,
            model_name: Text,
            model_version: Optional[Text] = None
    ) -> None:
        if model_version is not None:
            m = crud.model.get_by_name_and_ver(self.db, name=model_name, version=model_version)
            if m is not None:
                crud.model.delete(self.db, id=m.id)
        else:
            # Delete all versions of this model
            models = crud.model.get_all(self.db)
            for m in models:
                if m.name == model_name:
                    crud.model.delete(self.db, id=m.id)

    def get_model(
            self,
            model_name: Text,
            model_version: Text
    ) -> Model:
        logger = logging.getLogger(__name__)
        key: Tuple[Text, Text] = (model_name, model_version)
        m: Model
        try:
            m = OpenPredictionService.MODEL_CACHE[key]
        except KeyError:
            logger.debug(f'model {key} cache miss')
            model = crud.model.get_by_name_and_ver(
                self.db, name=model_name, version=model_version)
            m = Model(model=pickle.loads(model.binary.model_b64), info=MLSchema(**model.config.configuration))
            OpenPredictionService.MODEL_CACHE.__setitem__(key=key, value=m)
        return m

    def get_model_configs(self) -> List[MLSchema]:
        return [config.configuration for config in crud.model_config.get_all(self.db)]

    def count_models(self) -> int:
        return crud.model_config.count(self.db)

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
