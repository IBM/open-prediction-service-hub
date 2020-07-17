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


from sqlalchemy.orm import Session

from .base import CRUDBase
from ..models.binary_ml_model import BinaryMLModel
from ..schemas.binary_ml_model import BinaryMLModelCreate, BinaryMLModelUpdate


class CRUDBinaryMLModel(CRUDBase[BinaryMLModel, BinaryMLModelCreate, BinaryMLModelUpdate]):

    def create(self, db: Session, *, obj_in: BinaryMLModelCreate) -> BinaryMLModel:
        db_obj = BinaryMLModel(
           model_b64=obj_in.model_b64
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


binary_ml_model = CRUDBinaryMLModel(BinaryMLModel)
