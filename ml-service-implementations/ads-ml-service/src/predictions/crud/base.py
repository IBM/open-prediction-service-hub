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


from typing import TypeVar, Generic, Type, Any, Optional, List, Union, Dict, Text

from fastapi.encoders import jsonable_encoder
from pydantic.main import BaseModel
from sqlalchemy.orm import Session

from ..db.base_class import Base

# ModelType is a type variable that must be subclass of db.Base
ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)

IdType = int


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        Abstract CRUD object with default method to Create, Read, Update and Delete (CRUD).
        """
        self.model = model

    def get(self, db: Session, *, id: IdType) -> Optional[ModelType]:
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
            self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limite(limit).all()

    def count(self, db: Session) -> int:
        return db.query(self.model).count()

    def get_all(self, db: Session) -> List[ModelType]:
        return db.query(self.model).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        data_in = jsonable_encoder(obj_in)
        db_obj = self.model(**data_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: ModelType, obj_in: Union[UpdateSchemaType, Dict[Text, Any]]
    ):
        original = jsonable_encoder(db_obj)
        update_data = obj_in if isinstance(obj_in, Dict) else obj_in.dict(exclude_unset=True)
        for field in original:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: IdType) -> ModelType:
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj
