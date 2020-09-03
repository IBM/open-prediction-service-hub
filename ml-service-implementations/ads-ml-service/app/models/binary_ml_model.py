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

import sqlalchemy as sa
import sqlalchemy.orm as orm

import app.db.base_class as base_class


class MlLib(typing.Text, enum.Enum):
    SKLearn = 'skl'
    XGBoost = 'xgb'


class BinaryMlModel(base_class.Base):
    model_b64 = sa.Column('model_b64', sa.LargeBinary, nullable=False)
    library = sa.Column('library', sa.Enum(MlLib), nullable=False)

    endpoint_id = sa.Column('endpoint_id', sa.Integer, sa.ForeignKey('endpoint.id'))
    endpoint = orm.relationship('Endpoint', back_populates='binary', uselist=False)
