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


import sqlalchemy as sql
import sqlalchemy.orm as sql_orm

import app.db.base_class as base_class
import app.core.supported_lib as supported_lib


class BinaryMlModel(base_class.Base):
    id = sql.Column('id', sql.Integer, sql.ForeignKey('endpoint.id'),
                    nullable=False, unique=True, index=True, primary_key=True)
    model_b64 = sql.Column('model_b64', sql.LargeBinary, nullable=False)
    library = sql.Column('library', sql.Enum(supported_lib.MlLib), nullable=False)

    endpoint = sql_orm.relationship('Endpoint', back_populates='binary', uselist=False)
