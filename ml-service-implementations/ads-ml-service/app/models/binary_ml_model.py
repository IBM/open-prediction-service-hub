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


import enum
import typing

from sqlalchemy import Column, LargeBinary, Integer, ForeignKey, Enum
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class MlLib(typing.Text, enum.Enum):
    SKLearn = 'skl'
    XGBoost = 'xgb'


class BinaryMLModel(Base):
    model_b64 = Column('model_b64', LargeBinary, nullable=False)
    library = Column('library', Enum(MlLib), nullable=False)

    model_id = Column('model_id', Integer, ForeignKey('model.id'))
    model = relationship('Model', back_populates='binary', uselist=False)
