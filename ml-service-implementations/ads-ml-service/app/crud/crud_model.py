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

from sqlalchemy.orm import Session

from .base import CRUDBase
from .crud_binary_ml_model import binary_ml_model
from .crud_model_config import model_config
from ..models import Model
from ..schemas import ModelCreate, ModelUpdate


class CRUDModel(CRUDBase[Model, ModelCreate, ModelUpdate]):
    def create(self, db: Session, *, obj_in: ModelCreate) -> Model:
        db_binary = binary_ml_model.create(db, obj_in=obj_in.binary)
        db_config = model_config.create(db, obj_in=obj_in.config)
        db_obj = Model(
            name=obj_in.name,
            version=obj_in.version,
            binary=db_binary,
            config=db_config
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_name_and_ver(self, db: Session, *, name: Text, version: Text):
        return db.query(Model) \
            .filter(Model.name == name, Model.version == version).first()


model = CRUDModel(Model)
