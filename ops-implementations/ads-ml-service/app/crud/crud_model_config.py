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
import typing

import fastapi.encoders as encoders
import sqlalchemy.orm as orm

import app.crud.base as app_crud_base
import app.models as models
import app.schemas as schemas


class CRUDModelConfig(app_crud_base.CRUDBase[models.ModelConfig, schemas.ModelConfigCreate, schemas.ModelConfigUpdate]):
    def create_with_model(
            self, db: orm.Session, *, obj_in: schemas.ModelConfigCreate, model_id: app_crud_base.IdType
    ) -> models.ModelConfig:
        # noinspection PyArgumentList
        db_obj = self.model(
            id=model_id,
            **encoders.jsonable_encoder(obj_in),
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_model(self, db: orm.Session, *, model_id: app_crud_base.IdType) -> typing.Optional[models.ModelConfig]:
        return self.get(db, id=model_id)

    def update(
            self,
            db: orm.Session,
            *,
            db_obj: models.ModelConfig,
            obj_in: typing.Union[schemas.ModelConfigUpdate, typing.Dict[typing.Text, typing.Any]]
    ) -> models.ModelConfig:
        model = db.query(models.Model).filter(models.Model.id == db_obj.id).first()
        model.modified_at = datetime.datetime.now(tz=datetime.timezone.utc)

        original = encoders.jsonable_encoder(db_obj)
        update_data = obj_in if isinstance(obj_in, typing.Dict) else obj_in.dict(exclude_unset=True)
        for field in original:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        db.add(model)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


model_config = CRUDModelConfig(models.ModelConfig)
