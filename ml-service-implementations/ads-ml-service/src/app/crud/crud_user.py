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


from typing import Text, Optional, Union, Dict, Any

from sqlalchemy.orm import Session

from .base import CRUDBase
from ..core.security import get_pwd_hash, verify_pwd
from ..models import User
from ..schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_username(self, db: Session, *, username: Text) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            username=obj_in.username,
            hashed_password=get_pwd_hash(obj_in.password)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[Text, Any]]
    ) -> User:
        update_data = obj_in if isinstance(obj_in, Dict) else obj_in.dict(exclude_unset=True)
        if update_data['password']:
            hashed_password = get_pwd_hash(update_data['password'])
            del update_data['password']
            update_data['hashed_password'] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(
            self, db: Session, *, username: Text, password: Text
    ) -> Optional[User]:
        user = self.get_by_username(db, username=username)
        if not user:
            return None
        if not verify_pwd(password, user.hashed_password):
            return None
        return user


user = CRUDUser(User)
