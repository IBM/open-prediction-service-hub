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

import sqlalchemy.orm as orm

import app.models as models
import app.schemas as schemas
from .base import CRUDBase, IdType


class CRUDBinaryMLModel(CRUDBase[models.BinaryMlModel, schemas.BinaryMlModelCreate, schemas.BinaryMlModelUpdate]):
    def create_with_endpoint(
            self, db: orm.Session, *, obj_in: schemas.BinaryMlModelCreate, endpoint_id: IdType
    ) -> models.BinaryMlModel:
        # noinspection PyArgumentList
        db_obj = self.model(
            **obj_in.dict(),
            id=endpoint_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_endpoint(self, db: orm.Session, *, endpoint_id: IdType) -> typing.Optional[models.Endpoint]:
        return db.query(self.model).filter(self.model.id == endpoint_id).first()


binary_ml_model = CRUDBinaryMLModel(models.BinaryMlModel)
