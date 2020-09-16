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


import datetime as dt

import fastapi.encoders as encoders
import sqlalchemy.orm as orm

import app.models as models
import app.schemas as schemas
from .base import CRUDBase, IdType


class CRUDModel(CRUDBase[models.Endpoint, schemas.EndpointCreate, schemas.EndpointUpdate]):

    def create_with_model(
            self, db: orm.Session, *, obj_in: schemas.ModelConfigCreate, model_id: IdType
    ) -> models.Endpoint:
        # noinspection PyArgumentList
        db_obj = self.model(
            **encoders.jsonable_encoder(obj_in),
            deployed_at=dt.datetime.now(tz=dt.timezone.utc),
            model_id=model_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


endpoint = CRUDModel(models.Endpoint)
