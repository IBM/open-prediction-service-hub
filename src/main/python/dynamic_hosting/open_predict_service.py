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
from typing import Text, Any, Dict, NoReturn, Optional, List

from dynamic_hosting.core.model import Model, MLSchema
from dynamic_hosting.db.crud import create_model, delete_model, read_model, read_models, count_models
from sqlalchemy.orm import Session


class PredictionService:

    def __init__(self, db: Session, cache_ttl: int = 10):
        self.db: Session = db

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
        item = read_model(self.db, model_name=model_name, model_version=model_version)
        return Model(model=pickle.loads(item.model_b64), info=MLSchema(**item.configuration))

    def get_model_metadata(self) -> List[MLSchema]:
        return [
            MLSchema(**i.configuration)
            for i in read_models(self.db)
        ]

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
        self.add_model(
            model
        )
