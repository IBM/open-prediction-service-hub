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

import app.crud.base as app_crud_base
import app.models as models
import app.schemas as schemas


class CRUDModel(app_crud_base.CRUDBase[models.Endpoint, schemas.EndpointCreate, schemas.EndpointUpdate]):
    def create_with_model(
            self, db: orm.Session, *, obj_in: schemas.EndpointCreate, model_id: app_crud_base.IdType
    ) -> models.Endpoint:
        # noinspection PyArgumentList
        db_obj = self.model(
            **encoders.jsonable_encoder(obj_in),
            deployed_at=dt.datetime.now(tz=dt.timezone.utc),
            id=model_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_with_model_and_binary(
            self,
            db: orm.Session,
            *,
            ec: schemas.EndpointCreate,
            bc: schemas.BinaryMlModelCreate,
            model_id: app_crud_base.IdType,
    ):
        # noinspection PyArgumentList
        endpoint_db_obj = self.model(
            **encoders.jsonable_encoder(ec),
            id=model_id,
            deployed_at=dt.datetime.now(tz=dt.timezone.utc)
        )
        # noinspection PyArgumentList
        binary_db_obj = models.BinaryMlModel(
            **bc.dict(),
            id=model_id
        )
        db.add(endpoint_db_obj)
        db.add(binary_db_obj)
        db.commit()
        db.refresh(endpoint_db_obj)
        return endpoint_db_obj


endpoint = CRUDModel(models.Endpoint)
