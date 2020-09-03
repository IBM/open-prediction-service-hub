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


import typing

import fastapi.encoders as encoders
import sqlalchemy.orm as orm

import app.models as models
import app.schemas as schemas
from .base import CRUDBase, IdType


class CRUDModelConfig(CRUDBase[models.ModelConfig, schemas.ModelConfigCreate, schemas.ModelConfigUpdate]):
    def create_with_model(
            self, db: orm.Session, *, obj_in: schemas.ModelConfigCreate, model_id: IdType
    ) -> models.ModelConfig:
        # noinspection PyArgumentList
        db_obj = self.model(
            **encoders.jsonable_encoder(obj_in),
            model_id=model_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_model(self, db: orm.Session, *, model_id: IdType) -> typing.Optional[models.ModelConfig]:
        return db.query(self.model).filter(self.model.model_id == model_id).first()


model_config = CRUDModelConfig(models.ModelConfig)
