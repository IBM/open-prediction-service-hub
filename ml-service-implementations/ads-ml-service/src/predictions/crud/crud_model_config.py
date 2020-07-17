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


from typing import Text, Optional, List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models.model_config import ModelConfig
from ..schemas.model_config import ModelConfigCreate, ModelConfigUpdate


class CRUDModelConfig(CRUDBase[ModelConfig, ModelConfigCreate, ModelConfigUpdate]):

    def create(self, db: Session, *, obj_in: ModelConfigCreate) -> ModelConfig:
        db_obj = ModelConfig(
            name=obj_in.name,
            version=obj_in.version,
            configuration=obj_in.dict()
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_with_model(self, db: Session, *, obj_in: ModelConfigCreate, model_id: int) -> ModelConfig:
        db_obj = ModelConfig(
            model_id=model_id,
            name=obj_in.name,
            version=obj_in.version,
            configuration=jsonable_encoder(obj_in)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


model_config = CRUDModelConfig(ModelConfig)
