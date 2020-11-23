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
import app.schemas.binary_config as app_binary_config


class BinaryMlModel(base_class.Base):
    id = sql.Column('id', sql.Integer, sql.ForeignKey('endpoint.id'),
                    nullable=False, unique=True, index=True, primary_key=True)
    model_b64 = sa.Column('model_b64', sa.LargeBinary, nullable=False)
    input_handling = sa.Column('input_handling', sa.Enum(app_binary_config.ModelInput), nullable=False)
    output_handling = sa.Column('output_handling', sa.Enum(app_binary_config.ModelOutput), nullable=False)
    loader = sa.Column('loader', sa.Enum(app_binary_config.ModelWrapper), nullable=False)

    endpoint = sql_orm.relationship('Endpoint', back_populates='binary', uselist=False)
