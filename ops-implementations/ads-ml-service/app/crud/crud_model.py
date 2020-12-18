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


import datetime
import typing as typ

import fastapi.encoders as encoders
import sqlalchemy.orm as orm

import app.crud.base as app_crud_base
import app.models as models
import app.schemas as schemas


class CRUDModel(app_crud_base.CRUDBase[models.Model, schemas.ModelCreate, schemas.ModelUpdate]):
    def create(self, db: orm.Session, *, obj_in: schemas.ModelCreate) -> models.Model:
        now = datetime.datetime.now(tz=datetime.timezone.utc)
        # noinspection PyArgumentList
        db_obj = self.model(
            **encoders.jsonable_encoder(obj_in),
            created_at=now,
            modified_at=now
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self,
            db: orm.Session,
            *,
            db_obj: models.Model,
            obj_in: typ.Union[schemas.ModelUpdate, typ.Dict[typ.Text, typ.Any]]
    ) -> models.Model:
        update_data = obj_in if isinstance(obj_in, typ.Dict) else obj_in.dict(exclude_unset=True)
        update_data['modified_at'] = datetime.datetime.now(tz=datetime.timezone.utc)
        return super().update(db, db_obj=db_obj, obj_in=update_data)


model = CRUDModel(models.Model)
